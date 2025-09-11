import copy
import time
import asyncio
import time
import base64
import re
import inspect
from typing import Any, Optional, Dict, AsyncIterator, AsyncIterable
from urllib.parse import urlencode, quote
from xml.etree import ElementTree as ET
from .. import exceptions
from .. import serde
from .. import utils
from .. import serde
from ..credentials import AnonymousCredentialsProvider
from ..config import Config
from .._client import (
    _ClientImplMixIn,
    _Options,
    _InnerOptions,
    _build_url
)
from ..types import (
    AsyncHttpResponse,
    SigningContext,
    OperationInput,
    OperationOutput,
    HttpRequest,
    BodyType
)
from .transport import AioHttpClient
from . import aio_utils

class _AsyncMarkedBody:
    def __init__(
        self,
        body: BodyType,
    ) -> None:
        self._body = body
        self._io_curr: int = 0
        self._is_fileobj = False
        if body is None:
            self._seekable = True
        elif isinstance(body, aio_utils.TeeAsyncIterator):
            self._seekable = body.seekable()
        elif utils.is_fileobj(body):
            self._seekable = utils.is_seekable(body)
            self._is_fileobj = True
        elif isinstance(body, AsyncIterator):
            self._seekable = False
        elif isinstance(body, (str, bytes, AsyncIterable)):
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

        if isinstance(self._body, aio_utils.TeeAsyncIterator):
            self._body.reset()

        if self._is_fileobj:
            self._body.seek(self._io_curr, 0)

class _AsyncClientImpl(_ClientImplMixIn):
    """ASync API Client for common API."""

    def __init__(self, config: Config, **kwargs) -> None:
        options, inner = self.resolve_config(config)
        self.resolve_kwargs(options, **kwargs)

        self._config = config
        self._options = options
        self._inner = inner

    async def close(self):
        """_summary_
        """
        if self._options.http_client is not None:
            await self._options.http_client.close()

    async def invoke_operation(self, op_input: OperationInput, **kwargs) -> OperationOutput:
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
            output = await self._sent_request(op_input, options)
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

        options.http_client = AioHttpClient(**kwargs)


    def _apply_operation_options(self, options: _Options) -> None:
        # response handler
        handlers = []

        async def service_error_response_handler(response: AsyncHttpResponse) -> None:
            """ check service error """
            if response.status_code // 100 == 2:
                return

            if not response.is_stream_consumed:
                await response.read()

            raise await _to_service_error(response)

        # insert service error responsed handler first
        handlers.append(service_error_response_handler)

        handlers.extend(options.response_handlers)

        options.response_handlers = handlers

    def _apply_operation_metadata(self, op_input: OperationInput, options: _Options) -> None:
        handlers = op_input.op_metadata.get('opm-response-handler', None)
        if handlers is not None:
            options.response_handlers.extend(handlers)


    def _build_request_context(self, op_input: OperationInput, options: _Options, inner: _InnerOptions
                              ) -> SigningContext:
        """build request context
        """
        # host & path
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
                    body = aio_utils.TeeAsyncIterator.from_source(body, writers)

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

    async def _sent_request(self, op_input: OperationInput, options: _Options) -> OperationOutput:

        context = self._build_request_context(op_input, options, self._inner)
        response = await self._sent_http_request(context, options)

        output = OperationOutput(
            status=response.reason,
            status_code=response.status_code,
            headers=response.headers,
            op_input=op_input,
            http_response=response
        )

        # save other info by Metadata filed
        # output.op_metadata

        # update clock offset

        return output

    async def _sent_http_request(self, context: SigningContext, options: _Options) -> AsyncHttpResponse:
        request = context.request
        retryer = options.retryer
        max_attempts = self.retry_max_attempts(options)

        # operation timeout
        dealline = None
        if isinstance(options.operation_timeout, (int, float)):
            dealline = time.time() +  options.operation_timeout

        # Mark body
        marked_body = _AsyncMarkedBody(request.body)
        marked_body.mark()

        reset_time = context.signing_time is None
        error: Optional[Exception] = None
        response: AsyncHttpResponse = None
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
                await asyncio.sleep(dealy)

                # operation timeout
                if dealline is not None and (time.time() > dealline):
                    break                

            try:
                error = None
                response = await self._sent_http_request_once(context, options)
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

    async def _sent_http_request_once(self, context: SigningContext, options: _Options) -> AsyncHttpResponse:
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
        #if options.response_stream is not None:
        #    send_kwargs['stream'] = options.response_stream

        response = await options.http_client.send(context.request, **send_kwargs)

        # response handler
        for h in options.response_handlers:
            if inspect.iscoroutinefunction(h):
                await h(response)
            else:
                h(response)

        return response


async def _to_service_error(response: AsyncHttpResponse) -> exceptions.ServiceError:
    timestamp = serde.deserialize_httptime(response.headers.get('Date'))
    content = response.content or b''
    await response.close()

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
