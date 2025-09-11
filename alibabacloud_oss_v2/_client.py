import copy
import time
import base64
import re
from typing import Any, Optional, Dict, Iterable, List, Union, cast, Tuple, Iterator
from urllib.parse import urlparse, ParseResult, urlencode, quote
from xml.etree import ElementTree as ET
import json
from . import retry
from . import transport
from . import exceptions
from . import utils
from . import defaults
from . import validation
from . import serde
from . import io_utils
from . import endpoints
from .signer import SignerV4, SignerV1
from .credentials import AnonymousCredentialsProvider
from .config import Config
from .types import (
    Retryer,
    CredentialsProvider,
    HttpClient, AsyncHttpClient,
    HttpRequest,
    HttpResponse,
    SigningContext,
    Signer,
    BodyType,
    OperationInput,
    OperationOutput,
    EndpointProvider,
)


class AddressStyle():
    """address style information
    """
    Virtual = 1
    Path = 2
    CName = 3


class _MarkedBody:
    def __init__(
        self,
        body: BodyType,
    ) -> None:
        self._body = body
        self._io_curr: int = 0
        self._is_fileobj = False
        if body is None:
            self._seekable = True
        elif isinstance(body, io_utils.TeeIterator):
            self._seekable = body.seekable()
        elif utils.is_fileobj(body):
            self._seekable = utils.is_seekable(body)
            self._is_fileobj = True
        elif isinstance(body, Iterator):
            self._seekable = False
        elif isinstance(body, (str, bytes, Iterable)):
            self._seekable = True
        else:
            self._seekable = False

    def is_seekable(self) -> bool:
        """'is seekable
        """
        return self._seekable

    def mark(self) -> None:
        """Set the current marked position in the stream.
        """
        if self.is_seekable() is False:
            return

        if self._is_fileobj:
            self._io_curr = self._body.tell()

    def reset(self) -> None:
        """Resets the buffer to the marked position.
        """
        if self.is_seekable() is False:
            return

        if isinstance(self._body, io_utils.TeeIterator):
            self._body.reset()

        if self._is_fileobj:
            self._body.seek(self._io_curr, 0)


class _Options:
    """client level's configuration."""

    def __init__(
        self,
        product: str,
        region: str,
        endpoint: Optional[ParseResult] = None,
        retry_max_attempts: Optional[int] = None,
        retryer: Optional[Retryer] = None,
        signer: Optional[Signer] = None,
        credentials_provider: Optional[CredentialsProvider] = None,
        http_client: Optional[Union[HttpClient, AsyncHttpClient]] = None,
        address_style: Optional[AddressStyle] = None,
        readwrite_timeout: Optional[Union[int, float]] = None,
        response_handlers: Optional[List] = None,
        response_stream: Optional[bool] = None,
        auth_method: Optional[str] = None,
        feature_flags: Optional[int] = None,
        additional_headers: Optional[List[str]] = None,
        operation_timeout: Optional[Union[int, float]] = None,
        endpoint_provider: Optional[EndpointProvider] = None,
    ) -> None:
        self.product = product
        self.region = region
        self.endpoint = endpoint
        self.retry_max_attempts = retry_max_attempts
        self.retryer = retryer
        self.signer = signer
        self.credentials_provider = credentials_provider
        self.http_client = http_client
        self.address_style = address_style
        self.readwrite_timeout = readwrite_timeout
        self.response_handlers = response_handlers or []
        self.response_stream= response_stream
        self.auth_method = auth_method
        self.feature_flags = feature_flags or defaults.FF_DEFAULT
        self.additional_headers = additional_headers
        self.operation_timeout = operation_timeout
        self.endpoint_provider = endpoint_provider

class _InnerOptions:
    """client runtime's information."""
    def __init__(
        self,
        user_agent: str = None,
    ) -> None:
        self.user_agent = user_agent


class _ClientImplMixIn:
    """Client implement"""

    def resolve_config(self, config: Config) ->Tuple[_Options, _InnerOptions]:
        """convert config into client's options"""

        options = _default_options(config)

        _resolve_endpoint(config, options)
        _resolve_retryer(config, options)
        _resolve_signer(config, options)
        _resolve_address_style(config, options)
        _resolve_feature_flags(config, options)
        _resolve_cloud_box(config, options)
        self._resolve_httpclient(config, options) # pylint: disable=no-member

        inner = _InnerOptions()
        #UserAgent
        inner.user_agent = _build_user_agent(config)

        return options, inner

    def resolve_kwargs(self, options: _Options, **kwargs):
        """client's configuration from user by key/value args"""

        if len(kwargs) == 0:
            return

        options.product = kwargs.get("product", options.product)
        options.region = kwargs.get("region", options.region)
        options.endpoint = kwargs.get("endpoint", options.endpoint)
        options.retry_max_attempts = kwargs.get("retry_max_attempts", options.retry_max_attempts)
        options.retryer = kwargs.get("retryer", options.retryer)
        options.signer = kwargs.get("signer", options.signer)
        options.credentials_provider = kwargs.get("credentials_provider", options.credentials_provider)
        options.http_client = kwargs.get("http_client", options.http_client)
        options.address_style = kwargs.get("address_style", options.address_style)
        options.readwrite_timeout = kwargs.get("readwrite_timeout", options.readwrite_timeout)
        options.auth_method = kwargs.get("auth_method", None)
        options.additional_headers = kwargs.get("additional_headers", options.additional_headers)


    def resolve_operation_kwargs(self, options: _Options, **kwargs):
        """operation's configuration from user by key/value args"""

        if len(kwargs) == 0:
            return

        options.retry_max_attempts = kwargs.get("retry_max_attempts", options.retry_max_attempts)
        options.retryer = kwargs.get("retryer", options.retryer)
        options.http_client = kwargs.get("http_client", options.http_client)
        options.readwrite_timeout = kwargs.get("readwrite_timeout", options.readwrite_timeout)
        options.auth_method = kwargs.get("auth_method", options.auth_method)
        options.operation_timeout = kwargs.get("operation_timeout", None)

    def verify_operation(self, op_input: OperationInput, options: _Options) -> None:
        """verify input and options"""

        if not options.endpoint:
            raise exceptions.ParamInvalidError(field="endpoint")

        if (op_input.bucket is not None and
                not validation.is_valid_bucket_name(op_input.bucket)):
            raise exceptions.BucketNameInvalidError(
                name=utils.safety_str(op_input.bucket))

        if (op_input.key is not None and
                not validation.is_valid_object_name(op_input.key)):
            raise exceptions.ObjectNameInvalidError()

    def apply_operation(self, options: _Options, op_input: OperationInput) -> None:
        """apply operation"""
        self._apply_operation_options(options) # pylint: disable=no-member
        self._apply_operation_metadata(op_input, options)


    def build_request_context(self, op_input: OperationInput, options: _Options, inner: _InnerOptions
                              ) -> SigningContext:
        """build request context
        """
        # host & path
        if options.endpoint_provider is not None:
            url = options.endpoint_provider.build_url(op_input)
        else:
            url = _build_url(op_input, options)

        # queries
        if op_input.parameters is not None:
            query = urlencode(op_input.parameters, quote_via=quote)
            if len(query) > 0:
                url = url + "?" + query

        # build http request
        request = HttpRequest(method=op_input.method, url=url)

        # headers
        request.headers.update(op_input.headers or {})

        request.headers.update({'User-Agent': inner.user_agent})

        # body
        body = op_input.body or b''

        # body tracker
        if op_input.op_metadata is not None:
            tracker = op_input.op_metadata.get("opm-request-body-tracker", None)
            if tracker is not None:
                writers = []
                for t in tracker:
                    if hasattr(t, 'write'):
                        writers.append(t)
                if len(writers) > 0:
                    body = io_utils.TeeIterator.from_source(body, writers)

        request.body = body

        # signing context
        context = SigningContext(
            product=options.product,
            region=options.region,
            bucket=op_input.bucket,
            key=op_input.key,
            request=request,
        )

        if utils.safety_str(options.auth_method) == 'query':
            context.auth_method_query = True

        oss_date = request.headers.get('x-oss-date', None)
        if oss_date is not None:
            context.signing_time = serde.deserialize_httptime(oss_date)
        if (expiration_time := op_input.op_metadata.get('expiration_time', None)) is not None:
            context.expiration_time = expiration_time

        context.sub_resource = op_input.op_metadata.get("sub-resource", [])

        return context

    def retry_max_attempts(self, options: _Options) -> int:
        """retry max attempts"""
        if options.retry_max_attempts is not None:
            attempts = int(options.retry_max_attempts)
        elif options.retryer is not None:
            attempts = options.retryer.max_attempts()
        else:
            attempts = defaults.DEFAULT_MAX_ATTEMPTS

        return max(1, attempts)

    def has_feature(self, flag: int) -> bool:
        """has feature"""
        return (self._options.feature_flags & flag) > 0 # pylint: disable=no-member

    def get_retry_attempts(self) -> bool:
        """get retry attempts"""
        return self.retry_max_attempts(self._options) # pylint: disable=no-member

class _SyncClientImpl(_ClientImplMixIn):
    """Sync API Client for common API."""

    def __init__(self, config: Config, **kwargs) -> None:
        options, inner = self.resolve_config(config)
        self.resolve_kwargs(options, **kwargs)

        self._config = config
        self._options = options
        self._inner = inner

    def invoke_operation(self, op_input: OperationInput, **kwargs) -> OperationOutput:
        """Common class interface invoice operation

        Args:
            op_input (OperationInput): _description_

        Raises:
            exceptions.OperationError: _description_

        Returns:
            OperationOutput: _description_
        """

        options = copy.copy(self._options)
        self.resolve_operation_kwargs(options, **kwargs)
        self.apply_operation(options, op_input)

        try:
            self.verify_operation(op_input, options)
            output = self._sent_request(op_input, options)
        except Exception as err:
            raise exceptions.OperationError(
                name=op_input.op_name,
                error=err,
            )

        return output

    def _resolve_httpclient(self, config: Config, options: _Options) -> None:
        """httpclient"""
        if options.http_client:
            return

        kwargs: Dict[str, Any] = {}

        if bool(config.insecure_skip_verify):
            kwargs["insecure_skip_verify"] = True

        if bool(config.enabled_redirect):
            kwargs["enabled_redirect"] = True

        if config.connect_timeout:
            kwargs["connect_timeout"] = config.connect_timeout

        if config.readwrite_timeout:
            kwargs["readwrite_timeout"] = config.readwrite_timeout

        if config.proxy_host:
            kwargs["proxy_host"] = config.proxy_host

        options.http_client = transport.RequestsHttpClient(**kwargs)


    def _apply_operation_options(self, options: _Options) -> None:
        # response handler
        handlers = []

        def service_error_response_handler(response: HttpResponse) -> None:
            """ check service error """
            if response.status_code // 100 == 2:
                return

            if not response.is_stream_consumed:
                _ = response.read()

            if response.headers.get('Content-Type', '') == 'application/json':
                raise _to_service_error_json(response)
            else:
                raise _to_service_error(response)

        # insert service error responsed handler first
        handlers.append(service_error_response_handler)

        handlers.extend(options.response_handlers)

        options.response_handlers = handlers

    def _apply_operation_metadata(self, op_input: OperationInput, options: _Options) -> None:
        handlers = op_input.op_metadata.get('opm-response-handler', None)
        if handlers is not None:
            options.response_handlers.extend(handlers)

        stream = op_input.op_metadata.get('response-stream', None)
        if stream is not None:
            options.response_stream = stream

    def _sent_request(self, op_input: OperationInput, options: _Options) -> OperationOutput:
        context = self.build_request_context(op_input, options, self._inner)
        response = self._sent_http_request(context, options)
        output = OperationOutput(
            status=response.reason,
            status_code=response.status_code,
            headers=response.headers,
            op_input=op_input,
            http_response=response
        )

        # save other info by Metadata filed
        # output.op_metadata
        if context.auth_method_query:
            output.op_metadata['expiration_time'] = context.expiration_time

        # update clock offset

        return output

    def _sent_http_request(self, context: SigningContext, options: _Options) -> HttpResponse:
        request = context.request
        retryer = options.retryer
        max_attempts = self.retry_max_attempts(options)

        # operation timeout
        dealline = None
        if isinstance(options.operation_timeout, (int, float)):
            dealline = time.time() +  options.operation_timeout

        # Mark body
        marked_body = _MarkedBody(request.body)
        marked_body.mark()

        reset_time = context.signing_time is None
        error: Optional[Exception] = None
        response: HttpResponse = None
        for tries in range(max_attempts):
            if tries > 0:
                try:
                    marked_body.reset()
                except:  # pylint: disable=bare-except
                    # if meets reset error, just ignores, and retures last error
                    break

                if reset_time:
                    context.signing_time = None

                dealy = retryer.retry_delay(tries, error)
                time.sleep(dealy)

                # operation timeout
                if dealline is not None and (time.time() > dealline):
                    break

            try:
                error = None
                response = self._sent_http_request_once(context, options)
                break
            except Exception as e:
                error = e

            # operation timeout
            if dealline is not None and (time.time() > dealline):
                break

            if marked_body.is_seekable() is False:
                break

            if not retryer.is_error_retryable(error):
                break

        if error is not None:
            raise error

        return response

    def _sent_http_request_once(self, context: SigningContext, options: _Options) -> HttpResponse:
        # sign request
        if not isinstance(options.credentials_provider, AnonymousCredentialsProvider):
            try:
                cred = options.credentials_provider.get_credentials()
            except Exception as e:
                raise exceptions.CredentialsFetchError(error=e)

            if cred is None or not cred.has_keys():
                raise exceptions.CredentialsEmptyError()

            # update credentials
            context.credentials = cred

            options.signer.sign(context)

        # send
        send_kwargs = {}
        if options.response_stream is not None:
            send_kwargs['stream'] = options.response_stream
        if options.readwrite_timeout is not None:
            send_kwargs['readwrite_timeout'] = options.readwrite_timeout

        response = options.http_client.send(context.request, **send_kwargs)

        # response handler
        for h in options.response_handlers:
            h(response)

        return response

def _default_options(config: Config) -> _Options:
    """convert config to options"""
    return _Options(
        product=defaults.DEFAULT_PRODUCT,
        region=config.region,
        retry_max_attempts=config.retry_max_attempts,
        retryer=cast(Retryer, config.retryer),
        credentials_provider=cast(
            CredentialsProvider, config.credentials_provider),
        http_client=cast(HttpClient, config.http_client),
        additional_headers=config.additional_headers
    )


def _resolve_endpoint(config: Config, options: _Options) -> None:
    """endpoint"""
    disable_ssl = utils.safety_bool(config.disable_ssl)
    endpoint = utils.safety_str(config.endpoint)
    region = utils.safety_str(config.region)
    if len(endpoint) > 0:
        endpoint = endpoints.add_scheme(endpoint, disable_ssl)
    elif validation.is_valid_region(region):
        if bool(config.use_dualstack_endpoint):
            etype = "dualstack"
        elif bool(config.use_internal_endpoint):
            etype = "internal"
        elif bool(config.use_accelerate_endpoint):
            etype = "accelerate"
        else:
            etype = "default"

        endpoint = endpoints.from_region(region, disable_ssl, etype)

    if endpoint == "":
        return

    options.endpoint = urlparse(endpoint)



def _resolve_retryer(_: Config, options: _Options) -> None:
    """retryer"""
    if options.retryer:
        return

    options.retryer = retry.StandardRetryer()


def _resolve_signer(config: Config, options: _Options) -> None:
    """signer"""
    if options.signer:
        return

    if utils.safety_str(config.signature_version) == "v1":
        options.signer = SignerV1()
    else:
        options.signer = SignerV4()


def _resolve_address_style(config: Config, options: _Options) -> None:
    """address_style"""
    if bool(config.use_cname):
        style = AddressStyle.CName
    elif bool(config.use_path_style):
        style = AddressStyle.Path
    else:
        style = AddressStyle.Virtual

    # if the endpoint is ip, set to path-style
    if options.endpoint:
        hostname = options.endpoint.hostname
        if endpoints.is_ip(hostname):
            style = AddressStyle.Path

    options.address_style = style


def _resolve_feature_flags(config: Config, options: _Options) -> None:
    """flags for feature"""
    if utils.safety_bool(config.disable_upload_crc64_check):
        options.feature_flags = options.feature_flags & ~defaults.FF_ENABLE_CRC64_CHECK_UPLOAD

    if utils.safety_bool(config.disable_download_crc64_check):
        options.feature_flags = options.feature_flags & ~defaults.FF_ENABLE_CRC64_CHECK_DOWNLOAD


def _resolve_cloud_box(config: Config, options: _Options) -> None:
    """cloud box"""
    if config.cloud_box_id is not None:
        options.region = str(config.cloud_box_id)
        options.product = defaults.CLOUD_BOX_PRODUCT
        return

    if not config.enable_auto_detect_cloud_box_id:
        return

    host = options.endpoint.hostname
    if not (host.endswith(".oss-cloudbox.aliyuncs.com") or
            host.endswith(".oss-cloudbox-control.aliyuncs.com")):
        return

    keys = host.split(".")
    if len(keys) != 5 or not keys[0].startswith("cb-"):
        return
    options.region = keys[0]
    options.product = defaults.CLOUD_BOX_PRODUCT



def _build_url(op_input: OperationInput, options: _Options) -> str:
    host = ""
    paths = []
    if op_input.bucket is None:
        host = options.endpoint.netloc
    else:
        if options.address_style == AddressStyle.Path:
            host = options.endpoint.netloc
            paths.append(op_input.bucket)
            if op_input.key is None:
                paths.append('')
        elif options.address_style == AddressStyle.CName:
            host = options.endpoint.netloc
        else:
            host = f'{op_input.bucket}.{options.endpoint.netloc}'

    if op_input.key is not None:
        paths.append(quote(op_input.key))

    return f'{options.endpoint.scheme}://{host}/{"/".join(paths)}'


def _to_service_error(response: HttpResponse) -> exceptions.ServiceError:
    timestamp = serde.deserialize_httptime(response.headers.get('Date'))
    content = response.content or b''
    response.close()

    error_fileds = {}
    code = 'BadErrorResponse'
    message = ''
    ec = ''
    request_id = ''
    err_body = b''
    try:
        err_body = content
        if len(err_body) == 0:
            err_body = base64.b64decode(
                response.headers.get('x-oss-err', ''))
        root = ET.fromstring(err_body)
        if root.tag == 'Error':
            for child in root:
                error_fileds[child.tag] = child.text
            message = error_fileds.get('Message', '')
            code = error_fileds.get('Code', '')
            ec = error_fileds.get('EC', '')
            request_id = error_fileds.get('RequestId', '')
        else:
            message = f'Expect root node Error, but get {root.tag}.'
    except ET.ParseError as e:
        errstr = err_body.decode()
        if '<Error>' in errstr and '</Error>' in errstr:
            m = re.search('<Code>(.*)</Code>', errstr)
            if m:
                code = m.group(1)
            m = re.search('<Message>(.*)</Message>', errstr)
            if m:
                message = m.group(1)
        if len(message) == 0:
            message = f'Failed to parse xml from response body due to: {str(e)}. With part response body {err_body[:256]}.'
    except Exception as e:
        message = f'The body of the response was not readable, due to : {str(e)}.'

    return exceptions.ServiceError(
        status_code=response.status_code,
        code=code,
        message=message,
        request_id=request_id or response.headers.get('x-oss-request-id', ''),
        ec=ec or response.headers.get('x-oss-ec', ''),
        timestamp=timestamp,
        request_target=f'{response.request.method} {response.request.url}',
        snapshot=content,
        headers=response.headers,
        error_fileds=error_fileds
    )

def _to_service_error_json(response: HttpResponse) -> exceptions.ServiceError:
    timestamp = serde.deserialize_httptime(response.headers.get('Date'))
    content = response.content or b''
    response.close()

    error_fileds = {}
    code = 'BadErrorResponse'
    message = ''
    ec = ''
    request_id = ''
    err_body = b''
    try:
        err_body = content
        if len(err_body) == 0:
            err_body = base64.b64decode(
                response.headers.get('x-oss-err', ''))
        root = json.loads(err_body)
        errElem = root.get('Error', None)
        if errElem is not None:
            for k, v in errElem.items():
                if isinstance(v, str):
                    error_fileds[k] = v
            message = error_fileds.get('Message', '')
            code = error_fileds.get('Code', '')
            ec = error_fileds.get('EC', '')
            request_id = error_fileds.get('RequestId', '')
        else:
            message = f'Expect root node Error, but get {root.keys()}.'
    except json.JSONDecodeError as e:
        errstr = err_body.decode()
        if '"Error":' in errstr:
            m = re.search('"Code":(.*),', errstr)
            if m:
                code = m.group(1).strip(' "')
            m = re.search('<Message>(.*)</Message>', errstr)
            if m:
                message = m.group(1).strip(' "')
        if len(message) == 0:
            message = f'Failed to parse json from response body due to: {str(e)}. With part response body {err_body[:256]}.'
    except Exception as e:
        message = f'The body of the response was not readable, due to : {str(e)}.'

    return exceptions.ServiceError(
        status_code=response.status_code,
        code=code,
        message=message,
        request_id=request_id or response.headers.get('x-oss-request-id', ''),
        ec=ec or response.headers.get('x-oss-ec', ''),
        timestamp=timestamp,
        request_target=f'{response.request.method} {response.request.url}',
        snapshot=content,
        headers=response.headers,
        error_fileds=error_fileds
    )

def _build_user_agent(config: Config) -> str:
    if config.user_agent:
        return f'{utils.get_default_user_agent()}/{config.user_agent}'

    return utils.get_default_user_agent()
