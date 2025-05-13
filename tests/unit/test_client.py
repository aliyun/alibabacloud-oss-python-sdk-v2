# pylint: skip-file
import tempfile
import unittest
from unittest import mock
from typing import cast, Any, List, Iterable
from alibabacloud_oss_v2 import (
    models,
    config, 
    client, 
    credentials, 
    exceptions, 
    signer, 
    defaults,
    retry,
    transport,
    utils,
    io_utils
)
from alibabacloud_oss_v2.types import (
    HttpRequest, 
    HttpResponse, 
    HttpClient, 
    OperationInput, 
    OperationOutput,
    SigningContext
)
from . import MockHttpResponse, MockHttpClient


def _mock_client(request_fn, response_fn, **kwargs):
    cfg = config.load_default()
    cfg.region = 'cn-hangzhou'
    cfg.credentials_provider = credentials.AnonymousCredentialsProvider()
    cfg.http_client = MockHttpClient(
        request_fn=request_fn,
        response_fn=response_fn,
        kwargs=kwargs
    )
    return client.Client(cfg)

def _get_tempfile() -> str:
    return tempfile.gettempprefix()

progress_save_n = 0
def _progress_fn(n, _written, total):
    global progress_save_n
    progress_save_n += n

def _read_body(obj: Any) -> bytes:
    if isinstance(obj, bytes):
        return obj
    elif isinstance(obj, str):
        return obj.encode('utf-8')
    elif utils.is_fileobj(obj):
        return obj.read()
    elif isinstance(obj, Iterable):
        datas = []
        for a in obj:
            if isinstance(a, bytes):
                datas.append(a)
            if isinstance(a, str):
                datas.append(a.encode())
            if isinstance(a, int):
                datas.append(a.to_bytes(1, byteorder="little"))
        return b''.join(datas)
    else:
        raise TypeError(f'not supported type {type(obj)}')


class NonSeekableFile:
    def __init__(self, reader) -> None:
        self._reader =  reader   
    
    def read(self, n: int = -1):
        return self._reader.read(n)
    def readable(self) -> bool:
        return self._reader.readable()

    def seek(self, offset: int, whence: int = 0) -> int:
        return self._reader.seek(offset, whence)

    def seekable(self) -> bool:
        return False
    def tell(self) -> int:
        return self._reader.tell()


class TestSyncClient(unittest.TestCase):
    def test_default_config(self):
        cfg = config.load_default()
        cfg.region = 'cn-hangzhou'
        cfg.credentials_provider = credentials.AnonymousCredentialsProvider()
        clinet = client.Client(cfg)

        #default
        self.assertEqual('oss', clinet._client._options.product)
        self.assertEqual('cn-hangzhou', clinet._client._options.region)
        self.assertEqual('oss-cn-hangzhou.aliyuncs.com', clinet._client._options.endpoint.hostname)
        self.assertEqual('https', clinet._client._options.endpoint.scheme)
        self.assertEqual(None, clinet._client._options.retry_max_attempts)

        self.assertEqual(1, clinet._client._options.address_style)
        self.assertEqual(None, clinet._client._options.readwrite_timeout)
        self.assertEqual([], clinet._client._options.response_handlers)
        self.assertEqual(None, clinet._client._options.auth_method)
        self.assertEqual(defaults.FF_DEFAULT, clinet._client._options.feature_flags)

        self.assertIsInstance(clinet._client._options.retryer, retry.StandardRetryer)
        self.assertEqual(defaults.DEFAULT_MAX_ATTEMPTS, clinet._client._options.retryer.max_attempts())

        self.assertIsInstance(clinet._client._options.signer, signer.SignerV4)
        self.assertIsInstance(clinet._client._options.credentials_provider, credentials.AnonymousCredentialsProvider)
        self.assertIsInstance(clinet._client._options.http_client, transport.RequestsHttpClient)

    def test_config_signature_version(self):
        cfg = config.load_default()
        cfg.region = 'cn-hangzhou'
        cfg.credentials_provider = credentials.AnonymousCredentialsProvider()
        cfg.signature_version = 'v1'

        clinet = client.Client(cfg)
        self.assertIsInstance(clinet._client._options.signer, signer.SignerV1)

        cfg.signature_version = 'any-str'
        clinet = client.Client(cfg)
        self.assertIsInstance(clinet._client._options.signer, signer.SignerV4)

        cfg.signature_version = None
        clinet = client.Client(cfg)
        self.assertIsInstance(clinet._client._options.signer, signer.SignerV4)

    def test_config_endpoint(self):
        cfg = config.load_default()
        cfg.region = 'cn-beijing'
        cfg.credentials_provider = credentials.AnonymousCredentialsProvider()
        clinet = client.Client(cfg)
        self.assertEqual('oss-cn-beijing.aliyuncs.com', clinet._client._options.endpoint.hostname)
        self.assertEqual('https', clinet._client._options.endpoint.scheme)

        cfg = config.Config(
            region='cn-shanghai',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
            use_internal_endpoint=True
        )
        clinet = client.Client(cfg)
        self.assertEqual('oss-cn-shanghai-internal.aliyuncs.com', clinet._client._options.endpoint.hostname)
        self.assertEqual('https', clinet._client._options.endpoint.scheme)

        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
            use_accelerate_endpoint=True
        )
        clinet = client.Client(cfg)
        self.assertEqual('oss-accelerate.aliyuncs.com', clinet._client._options.endpoint.hostname)
        self.assertEqual('https', clinet._client._options.endpoint.scheme)

        cfg = config.Config(
            region='cn-shenzhen',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
            use_dualstack_endpoint=True
        )
        clinet = client.Client(cfg)
        self.assertEqual('cn-shenzhen.oss.aliyuncs.com', clinet._client._options.endpoint.hostname)
        self.assertEqual('https', clinet._client._options.endpoint.scheme)

        cfg = config.Config(
            region='cn-beijing',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
            endpoint='http://oss-cn-shenzhen.aliyuncs.com',
        )
        clinet = client.Client(cfg)
        self.assertEqual('oss-cn-shenzhen.aliyuncs.com', clinet._client._options.endpoint.hostname)
        self.assertEqual('http', clinet._client._options.endpoint.scheme)        

        cfg = config.Config(
            region='cn-shanghai',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
            use_internal_endpoint=True,
            disable_ssl=True
        )
        clinet = client.Client(cfg)
        self.assertEqual('oss-cn-shanghai-internal.aliyuncs.com', clinet._client._options.endpoint.hostname)
        self.assertEqual('http', clinet._client._options.endpoint.scheme)

    def test_config_address_style(self):
        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
        )
        clinet = client.Client(cfg)
        self.assertEqual(1, clinet._client._options.address_style)

        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
            use_cname=True
        )
        clinet = client.Client(cfg)
        self.assertEqual(3, clinet._client._options.address_style)

        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
            use_path_style=True
        )
        clinet = client.Client(cfg)
        self.assertEqual(2, clinet._client._options.address_style)

    def test_config_auth_method(self):
        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
        )
        clinet = client.Client(cfg)
        self.assertEqual(None, clinet._client._options.auth_method)

        clinet = client.Client(cfg, auth_method='query')
        self.assertEqual('query', clinet._client._options.auth_method)

    def test_config_product(self):
        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
        )
        clinet = client.Client(cfg)
        self.assertEqual('oss', clinet._client._options.product)

        clinet = client.Client(cfg, product='oss-cloudbox')
        self.assertEqual('oss-cloudbox', clinet._client._options.product)

    def test_config_retryer(self):
        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
        )
        clinet = client.Client(cfg)
        self.assertIsInstance(clinet._client._options.retryer, retry.StandardRetryer)
        self.assertEqual(defaults.DEFAULT_MAX_ATTEMPTS, clinet._client._options.retryer.max_attempts())
        self.assertEqual(None, clinet._client._options.retry_max_attempts)

        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
            retryer=retry.NopRetryer()
        )
        clinet = client.Client(cfg)
        self.assertIsInstance(clinet._client._options.retryer, retry.NopRetryer)
        self.assertEqual(1, clinet._client._options.retryer.max_attempts())

        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
            retryer=retry.StandardRetryer(max_attempts=5)
        )
        clinet = client.Client(cfg)
        self.assertIsInstance(clinet._client._options.retryer, retry.StandardRetryer)
        self.assertEqual(5, clinet._client._options.retryer.max_attempts())

        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
            retry_max_attempts=4
        )
        clinet = client.Client(cfg)
        self.assertIsInstance(clinet._client._options.retryer, retry.StandardRetryer)
        self.assertEqual(3, clinet._client._options.retryer.max_attempts())
        self.assertEqual(4, clinet._client._options.retry_max_attempts)

    def test_config_httpclient(self):
        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
        )
        clinet = client.Client(cfg)
        self.assertEqual(None, clinet._client._options.readwrite_timeout)
        self.assertIsInstance(clinet._client._options.http_client, transport.RequestsHttpClient)
        httpclient = cast(transport.RequestsHttpClient, clinet._client._options.http_client)
        self.assertEqual(defaults.DEFAULT_CONNECT_TIMEOUT, httpclient._connect_timeout)
        self.assertEqual(defaults.DEFAULT_READWRITE_TIMEOUT, httpclient._read_timeout)
        self.assertEqual(True, httpclient._verify)
        self.assertEqual(False, httpclient._allow_redirects)
        self.assertEqual(None, httpclient._proxies)
        self.assertEqual(defaults.DEFAULT_BLOCK_SIZE, httpclient._block_size)


        #timeout
        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
            connect_timeout=5,
            readwrite_timeout=15
        )
        clinet = client.Client(cfg)
        self.assertEqual(None, clinet._client._options.readwrite_timeout)
        self.assertIsInstance(clinet._client._options.http_client, transport.RequestsHttpClient)
        httpclient = cast(transport.RequestsHttpClient, clinet._client._options.http_client)
        self.assertEqual(5, httpclient._connect_timeout)
        self.assertEqual(15, httpclient._read_timeout)

        # SSL AND redirects
        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
            insecure_skip_verify=True,
            enabled_redirect = True
        )
        clinet = client.Client(cfg)
        self.assertIsInstance(clinet._client._options.http_client, transport.RequestsHttpClient)
        httpclient = cast(transport.RequestsHttpClient, clinet._client._options.http_client)
        self.assertEqual(False, httpclient._verify)
        self.assertEqual(True, httpclient._allow_redirects)

        # proxy host
        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
            proxy_host='http://127.0.0.1:8080'
        )
        clinet = client.Client(cfg)
        self.assertIsInstance(clinet._client._options.http_client, transport.RequestsHttpClient)
        httpclient = cast(transport.RequestsHttpClient, clinet._client._options.http_client)
        self.assertEqual({'http://': 'http://127.0.0.1:8080', 'https://': 'http://127.0.0.1:8080'}, httpclient._proxies)

    def test_config_user_agent(self):
        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
        )
        clinet = client.Client(cfg)
        self.assertEqual(utils.get_default_user_agent(), clinet._client._inner.user_agent)

        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
            user_agent='my-agent'
        )
        clinet = client.Client(cfg)
        self.assertEqual(utils.get_default_user_agent() + '/my-agent', clinet._client._inner.user_agent)

    def test_config_crc64_check(self):
        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
        )
        clinet = client.Client(cfg)
        self.assertGreater(defaults.FF_DEFAULT, 0)
        self.assertEqual(defaults.FF_DEFAULT, clinet._client._options.feature_flags)

        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
            disable_download_crc64_check=True,
            disable_upload_crc64_check=True,
        )
        clinet = client.Client(cfg)
        flags = defaults.FF_CORRECT_CLOCK_SKEW + defaults.FF_AUTO_DETECT_MIME_TYPE
        self.assertEqual(flags, clinet._client._options.feature_flags)

        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
            disable_download_crc64_check=True,
        )
        clinet = client.Client(cfg)
        flags = defaults.FF_CORRECT_CLOCK_SKEW + defaults.FF_AUTO_DETECT_MIME_TYPE + defaults.FF_ENABLE_CRC64_CHECK_UPLOAD
        self.assertEqual(flags, clinet._client._options.feature_flags)

        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
            disable_upload_crc64_check=True,
        )
        clinet = client.Client(cfg)
        flags = defaults.FF_CORRECT_CLOCK_SKEW + defaults.FF_AUTO_DETECT_MIME_TYPE + defaults.FF_ENABLE_CRC64_CHECK_DOWNLOAD
        self.assertEqual(flags, clinet._client._options.feature_flags)                

    def test_config_additional_headers(self):
        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
        )
        clinet = client.Client(cfg)
        self.assertEqual(None, clinet._client._options.additional_headers)

        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
            additional_headers=['content-length']
        )
        clinet = client.Client(cfg)
        self.assertEqual(['content-length'], clinet._client._options.additional_headers)

        clinet = client.Client(cfg, additional_headers=['host'])
        self.assertEqual(['host'], clinet._client._options.additional_headers)

    def test_invoke_operation_config(self):
        self.save_op_input = None
        self.save_options = None
        def do_sent_request(op_input: OperationInput, options: Any) -> OperationOutput:
            self.save_op_input = op_input
            self.save_options = options

        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
        )
        clinet = client.Client(cfg)

        with mock.patch.object(clinet._client, '_sent_request', new= do_sent_request) as _:
            #retry_max_attempts
            op_result = clinet.invoke_operation(OperationInput(
                op_name='InvokeOperation',
                method='GET',
                bucket='bucket',
            ))
            self.assertEqual(None, self.save_options.retry_max_attempts)

            clinet.invoke_operation(
                OperationInput(
                    op_name='InvokeOperation',
                    method='GET',
                    bucket='bucket',
                ),
                retry_max_attempts=10,
            )
            self.assertEqual(10, self.save_options.retry_max_attempts)

            # retryer
            self.assertIsInstance(clinet._client._options.retryer, retry.StandardRetryer)
            clinet.invoke_operation(
                OperationInput(
                    op_name='InvokeOperation',
                    method='GET',
                    bucket='bucket',
                ),
                retryer=retry.NopRetryer(),
            )
            self.assertIsInstance(self.save_options.retryer, retry.NopRetryer)

            # "readwrite_timeout"
            self.assertEqual(None, clinet._client._options.readwrite_timeout)
            clinet.invoke_operation(
                OperationInput(
                    op_name='InvokeOperation',
                    method='GET',
                    bucket='bucket',
                ),
                readwrite_timeout=30,
            )
            self.assertEqual(30, self.save_options.readwrite_timeout)

            # "auth_method"
            self.assertEqual(None, clinet._client._options.auth_method)
            clinet.invoke_operation(
                OperationInput(
                    op_name='InvokeOperation',
                    method='GET',
                    bucket='bucket',
                ),
                auth_method='query',
            )
            self.assertEqual('query', self.save_options.auth_method)

            # "http_client"
            self.assertIsInstance(clinet._client._options.http_client, transport.RequestsHttpClient)
            clinet.invoke_operation(
                OperationInput(
                    op_name='InvokeOperation',
                    method='GET',
                    bucket='bucket',
                ),
                http_client=MockHttpClient(None, None),
            )
            self.assertIsInstance(self.save_options.http_client, MockHttpClient)

            # "operation_timeout"
            self.assertEqual(None, clinet._client._options.operation_timeout)
            clinet.invoke_operation(
                OperationInput(
                    op_name='InvokeOperation',
                    method='GET',
                    bucket='bucket',
                ),
                operation_timeout=40,
            )
            self.assertEqual(40, self.save_options.operation_timeout)


    def test_invoke_operation_user_agent(self):
        self.save_op_context: SigningContext = None
        self.save_options = None
        
        def _sent_http_request_once(context: SigningContext, options: Any) -> HttpResponse:
            self.save_op_context = context
            self.save_options = options
            return MockHttpResponse(
                status_code=200,
                reason='OK',
                headers={'x-oss-request-id': 'id-1234'},
                body=''
            )

        # default user-agent
        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
        )
        clinet = client.Client(cfg)

        with mock.patch.object(clinet._client, '_sent_http_request_once', new= _sent_http_request_once) as _:
            clinet.invoke_operation(
                OperationInput(
                    op_name='InvokeOperation',
                    method='GET',
                    bucket='bucket',
            ))
            self.assertEqual(utils.get_default_user_agent(), self.save_op_context.request.headers['user-agent'])

        # user-define
        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
            user_agent='test-agent'
        )
        clinet = client.Client(cfg)

        with mock.patch.object(clinet._client, '_sent_http_request_once', new= _sent_http_request_once) as _:
            clinet.invoke_operation(
                OperationInput(
                    op_name='InvokeOperation',
                    method='GET',
                    bucket='bucket',
            ))
            self.assertEqual(utils.get_default_user_agent() + '/test-agent', self.save_op_context.request.headers['user-agent'])

    def test_invoke_operation_retry(self):
        self.save_op_context: List[SigningContext] = None
        self.save_options: List[Any] = None

        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
        )
        clinet = client.Client(cfg)

 
        # returns 200, no retry
        self.save_op_context = []
        self.save_options = []
        def _sent_http_request_once(context: SigningContext, options: Any) -> HttpResponse:
            self.save_op_context.append(context) 
            self.save_options.append(options)
            return MockHttpResponse(
                status_code=200,
                reason='OK',
                headers={'x-oss-request-id': 'id-1234'},
                body=''
            )

        with mock.patch.object(clinet._client, '_sent_http_request_once', new= _sent_http_request_once) as _:
            clinet.invoke_operation(
                OperationInput(
                    op_name='InvokeOperation',
                    method='GET',
                    bucket='bucket',
            ))
            self.assertEqual(1, len(self.save_op_context))
            self.assertEqual(1, len(self.save_options))

        # retry error, ex exceptions.ServiceError 500
        self.save_op_context = []
        self.save_options = []
        def _sent_http_request_once(context: SigningContext, options: Any) -> HttpResponse:
            self.save_op_context.append(context) 
            self.save_options.append(options)
            raise exceptions.ServiceError(
                status_code=500,
                code='InternalError',
                request_id='id-1234',
                message='Please contact the server administrator, oss@service.aliyun.com.',
                ec='',
                timestamp='',
                request_target=''
            )

        with mock.patch.object(clinet._client, '_sent_http_request_once', new= _sent_http_request_once) as _:
            try:
                clinet.invoke_operation(
                    OperationInput(
                        op_name='InvokeOperation',
                        method='GET',
                        bucket='bucket',
                ))
                self.fail('should not here')
            except exceptions.OperationError as err:
                self.assertIn("InternalError", str(err))


            self.assertEqual(3, len(self.save_op_context))
            self.assertEqual(3, len(self.save_options))

        # client's retry error, exceptions.RequestError, exceptions.ResponseError
        self.save_op_context = []
        self.save_options = []
        def _sent_http_request_once(context: SigningContext, options: Any) -> HttpResponse:
            self.save_op_context.append(context) 
            self.save_options.append(options)
            raise exceptions.RequestError(error=ValueError('Mock error'))

        with mock.patch.object(clinet._client, '_sent_http_request_once', new= _sent_http_request_once) as _:
            try:
                clinet.invoke_operation(
                    OperationInput(
                        op_name='InvokeOperation',
                        method='GET',
                        bucket='bucket',
                ))
                self.fail('should not here')
            except exceptions.OperationError as err:
                self.assertIn("Mock error", str(err))

            self.assertEqual(3, len(self.save_op_context))
            self.assertEqual(3, len(self.save_options))

        self.save_op_context = []
        self.save_options = []
        def _sent_http_request_once(context: SigningContext, options: Any) -> HttpResponse:
            self.save_op_context.append(context) 
            self.save_options.append(options)
            raise exceptions.ResponseError(error=ValueError('Mock error'))

        with mock.patch.object(clinet._client, '_sent_http_request_once', new= _sent_http_request_once) as _:
            try:
                clinet.invoke_operation(
                    OperationInput(
                        op_name='InvokeOperation',
                        method='GET',
                        bucket='bucket',
                ))
                self.fail('should not here')
            except exceptions.OperationError as err:
                self.assertIn("Mock error", str(err))

            self.assertEqual(3, len(self.save_op_context))
            self.assertEqual(3, len(self.save_options))

        # crc check error, exceptions.InconsistentError
        self.save_op_context = []
        self.save_options = []
        def _sent_http_request_once(context: SigningContext, options: Any) -> HttpResponse:
            self.save_op_context.append(context) 
            self.save_options.append(options)
            raise exceptions.InconsistentError(client_crc='1234', server_crc='456')

        with mock.patch.object(clinet._client, '_sent_http_request_once', new= _sent_http_request_once) as _:
            try:
                clinet.invoke_operation(
                    OperationInput(
                        op_name='InvokeOperation',
                        method='GET',
                        bucket='bucket',
                ))
                self.fail('should not here')
            except exceptions.OperationError as err:
                self.assertIn("crc is inconsistent", str(err))

            self.assertEqual(3, len(self.save_op_context))
            self.assertEqual(3, len(self.save_options))


        # no retry error, exceptions.ServiceError 403
        self.save_op_context = []
        self.save_options = []
        def _sent_http_request_once(context: SigningContext, options: Any) -> HttpResponse:
            self.save_op_context.append(context) 
            self.save_options.append(options)
            raise exceptions.ServiceError(
                status_code=403,
                code='InvalidAccessKeyId',
                request_id='id-1234',
                message='The OSS Access Key Id you provided does not exist in our records.',
                ec='',
                timestamp='',
                request_target=''
            )

        with mock.patch.object(clinet._client, '_sent_http_request_once', new= _sent_http_request_once) as _:
            try:
                clinet.invoke_operation(
                    OperationInput(
                        op_name='InvokeOperation',
                        method='GET',
                        bucket='bucket',
                ))
                self.fail('should not here')
            except exceptions.OperationError as err:
                self.assertIn("InvalidAccessKeyId", str(err))

            self.assertEqual(1, len(self.save_op_context))
            self.assertEqual(1, len(self.save_options))


        # exceptions.CredentialsFetchError
        self.save_op_context = []
        self.save_options = []
        def _sent_http_request_once(context: SigningContext, options: Any) -> HttpResponse:
            self.save_op_context.append(context) 
            self.save_options.append(options)
            raise exceptions.CredentialsFetchError(error=ValueError('Mock Credentials error'))

        with mock.patch.object(clinet._client, '_sent_http_request_once', new= _sent_http_request_once) as _:
            try:
                clinet.invoke_operation(
                    OperationInput(
                        op_name='InvokeOperation',
                        method='GET',
                        bucket='bucket',
                ))
                self.fail('should not here')
            except exceptions.OperationError as err:
                self.assertIn("Mock Credentials error", str(err))

            self.assertEqual(3, len(self.save_op_context))
            self.assertEqual(3, len(self.save_options))


        # retry error and with operation level's retry_max_attempts
        self.save_op_context = []
        self.save_options = []
        def _sent_http_request_once(context: SigningContext, options: Any) -> HttpResponse:
            self.save_op_context.append(context) 
            self.save_options.append(options)
            raise exceptions.ServiceError(
                status_code=500,
                code='InternalError',
                request_id='id-1234',
                message='Please contact the server administrator, oss@service.aliyun.com.',
                ec='',
                timestamp='',
                request_target=''
            )

        with mock.patch.object(clinet._client, '_sent_http_request_once', new= _sent_http_request_once) as _:
            try:
                clinet.invoke_operation(
                    OperationInput(
                        op_name='InvokeOperation',
                        method='GET',
                        bucket='bucket',
                    ),
                    retry_max_attempts=4,
                )
                self.fail('should not here')
            except exceptions.OperationError as err:
                self.assertIn("InternalError", str(err))


            self.assertEqual(4, len(self.save_op_context))
            self.assertEqual(4, len(self.save_options))

    def test_invoke_operation_retryable_body(self):
        self.save_op_context: List[SigningContext] = None
        self.save_options: List[Any] = None
        self.save_data: List[Any] = None

        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
        )
        clinet = client.Client(cfg)

        # str
        self.save_op_context = []
        self.save_options = []
        self.save_data = []
        data = 'hello world'
        def _sent_http_request_once(context: SigningContext, options: Any) -> HttpResponse:
            self.save_op_context.append(context) 
            self.save_options.append(options)
            self.save_data.append(_read_body(context.request.body))
            raise exceptions.ServiceError(
                status_code=500,
                code='InternalError',
                request_id='id-1234',
                message='Please contact the server administrator, oss@service.aliyun.com.',
                ec='',
                timestamp='',
                request_target=''
            )

        with mock.patch.object(clinet._client, '_sent_http_request_once', new= _sent_http_request_once) as _:
            try:
                clinet.invoke_operation(
                    OperationInput(
                        op_name='InvokeOperation',
                        method='GET',
                        bucket='bucket',
                        body=data
                    ),
                )
                self.fail('should not here')
            except exceptions.OperationError as err:
                self.assertIn("InternalError", str(err))

            self.assertEqual(3, len(self.save_op_context))
            self.assertEqual(3, len(self.save_options))
            self.assertEqual(3, len(self.save_data))
            for d in self.save_data:
                self.assertEqual(data.encode(), d)

        # bytes        
        self.save_op_context = []
        self.save_options = []
        self.save_data = []
        data = b'hello world 123'
        def _sent_http_request_once(context: SigningContext, options: Any) -> HttpResponse:
            self.save_op_context.append(context) 
            self.save_options.append(options)
            self.save_data.append(_read_body(context.request.body))
            raise exceptions.ServiceError(
                status_code=500,
                code='InternalError',
                request_id='id-1234',
                message='Please contact the server administrator, oss@service.aliyun.com.',
                ec='',
                timestamp='',
                request_target=''
            )

        with mock.patch.object(clinet._client, '_sent_http_request_once', new= _sent_http_request_once) as _:
            try:
                clinet.invoke_operation(
                    OperationInput(
                        op_name='InvokeOperation',
                        method='GET',
                        bucket='bucket',
                        body=data
                    ),
                )
                self.fail('should not here')
            except exceptions.OperationError as err:
                self.assertIn("InternalError", str(err))

            self.assertEqual(3, len(self.save_op_context))
            self.assertEqual(3, len(self.save_options))
            self.assertEqual(3, len(self.save_data))
            for d in self.save_data:
                self.assertEqual(data, d)

        # bytes list
        self.save_op_context = []
        self.save_options = []
        self.save_data = []
        data = b'hello world'
        data_list = [b'h', b'e',b'l',b'l',b'o',b' ',b'w',b'o',b'r',b'l',b'd']
        def _sent_http_request_once(context: SigningContext, options: Any) -> HttpResponse:
            self.save_op_context.append(context) 
            self.save_options.append(options)
            self.save_data.append(_read_body(context.request.body))
            raise exceptions.ServiceError(
                status_code=500,
                code='InternalError',
                request_id='id-1234',
                message='Please contact the server administrator, oss@service.aliyun.com.',
                ec='',
                timestamp='',
                request_target=''
            )

        with mock.patch.object(clinet._client, '_sent_http_request_once', new= _sent_http_request_once) as _:
            try:
                clinet.invoke_operation(
                    OperationInput(
                        op_name='InvokeOperation',
                        method='GET',
                        bucket='bucket',
                        body=data_list
                    ),
                )
                self.fail('should not here')
            except exceptions.OperationError as err:
                self.assertIn("InternalError", str(err))

            self.assertEqual(3, len(self.save_op_context))
            self.assertEqual(3, len(self.save_options))
            self.assertEqual(3, len(self.save_data))
            for d in self.save_data:
                self.assertEqual(data, d)

        # file        
        self.save_op_context = []
        self.save_options = []
        self.save_data = []
        filepath = "./tests/data/example.jpg"
        with open(filepath, 'rb') as f:
            data = f.read()
        self.assertGreater(len(data), 0)

        def _sent_http_request_once(context: SigningContext, options: Any) -> HttpResponse:
            self.save_op_context.append(context) 
            self.save_options.append(options)
            self.save_data.append(_read_body(context.request.body))
            raise exceptions.ServiceError(
                status_code=500,
                code='InternalError',
                request_id='id-1234',
                message='Please contact the server administrator, oss@service.aliyun.com.',
                ec='',
                timestamp='',
                request_target=''
            )

        with mock.patch.object(clinet._client, '_sent_http_request_once', new= _sent_http_request_once) as _:
            try:
                with open(filepath, 'rb') as f:
                    clinet.invoke_operation(
                        OperationInput(
                            op_name='InvokeOperation',
                            method='GET',
                            bucket='bucket',
                            body=f
                        ),
                    )
                self.fail('should not here')
            except exceptions.OperationError as err:
                self.assertIn("InternalError", str(err))

            self.assertEqual(3, len(self.save_op_context))
            self.assertEqual(3, len(self.save_options))
            self.assertEqual(3, len(self.save_data))
            for d in self.save_data:
                self.assertEqual(data, d)

        # non-seekable file
        self.save_op_context = []
        self.save_options = []
        self.save_data = []        
        def _sent_http_request_once(context: SigningContext, options: Any) -> HttpResponse:
            self.save_op_context.append(context) 
            self.save_options.append(options)
            self.save_data.append(_read_body(context.request.body))
            raise exceptions.ServiceError(
                status_code=500,
                code='InternalError',
                request_id='id-1234',
                message='Please contact the server administrator, oss@service.aliyun.com.',
                ec='',
                timestamp='',
                request_target=''
            )

        with mock.patch.object(clinet._client, '_sent_http_request_once', new= _sent_http_request_once) as _:
            try:
                with open(filepath, 'rb') as f:
                    clinet.invoke_operation(
                        OperationInput(
                            op_name='InvokeOperation',
                            method='GET',
                            bucket='bucket',
                            body=NonSeekableFile(f)
                        ),
                    )
                self.fail('should not here')
            except exceptions.OperationError as err:
                self.assertIn("InternalError", str(err))

            self.assertEqual(1, len(self.save_op_context))
            self.assertEqual(1, len(self.save_options))
            self.assertEqual(1, len(self.save_data))
            for d in self.save_data:
                self.assertEqual(data, d)

        # iter(bytes)
        self.save_op_context = []
        self.save_options = []
        self.save_data = []
        data = b'hello world'
        def _sent_http_request_once(context: SigningContext, options: Any) -> HttpResponse:
            self.save_op_context.append(context) 
            self.save_options.append(options)
            self.save_data.append(_read_body(context.request.body))
            raise exceptions.ServiceError(
                status_code=500,
                code='InternalError',
                request_id='id-1234',
                message='Please contact the server administrator, oss@service.aliyun.com.',
                ec='',
                timestamp='',
                request_target=''
            )

        with mock.patch.object(clinet._client, '_sent_http_request_once', new= _sent_http_request_once) as _:
            try:
                clinet.invoke_operation(
                    OperationInput(
                        op_name='InvokeOperation',
                        method='GET',
                        bucket='bucket',
                        body=iter(data)
                    ),
                )
                self.fail('should not here')
            except exceptions.OperationError as err:
                self.assertIn("InternalError", str(err))

            self.assertEqual(1, len(self.save_op_context))
            self.assertEqual(1, len(self.save_options))
            self.assertEqual(1, len(self.save_data))
            for d in self.save_data:
                self.assertEqual(data, d)


    def test_invoke_operation_retryable_tee_body(self):
        self.save_request: List[HttpRequest] = None
        self.save_data: List[Any] = None

        def _do_sent(request: HttpRequest, **kwargs) -> HttpResponse:
            self.save_request.append(request) 
            self.save_data.append(_read_body(request.body))
            self.assertIsInstance(request.body, io_utils.TeeIterator)
            raise exceptions.ServiceError(
                status_code=500,
                code='InternalError',
                request_id='id-1234',
                message='Please contact the server administrator, oss@service.aliyun.com.',
                ec='',
                timestamp='',
                request_target=''
            )

        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
        )
        clinet = client.Client(cfg)


        # str
        self.save_request = []
        self.save_data = []
        data = 'hello world'

        with mock.patch.object(clinet._client._options.http_client, 'send', new= _do_sent) as _:
            try:
                clinet.put_object(models.PutObjectRequest(
                    bucket='bucket',
                    key='key',
                    body=data
                ))
                self.fail('should not here')
            except exceptions.OperationError as err:
                self.assertIn("InternalError", str(err))

            self.assertEqual(3, len(self.save_request))
            self.assertEqual(3, len(self.save_data))
            for d in self.save_data:
                self.assertEqual(data.encode(), d)

        # bytes
        self.save_request = []
        self.save_data = []
        data = b'hello world 123'

        with mock.patch.object(clinet._client._options.http_client, 'send', new= _do_sent) as _:
            try:
                clinet.put_object(models.PutObjectRequest(
                    bucket='bucket',
                    key='key',
                    body=data
                ))
                self.fail('should not here')
            except exceptions.OperationError as err:
                self.assertIn("InternalError", str(err))

            self.assertEqual(3, len(self.save_request))
            self.assertEqual(3, len(self.save_data))
            for d in self.save_data:
                self.assertEqual(data, d)

        # file-like
        self.save_request = []
        self.save_data = []

        filepath = "./tests/data/example.jpg"
        with open(filepath, 'rb') as f:
            data = f.read()
        self.assertGreater(len(data), 0)

        with mock.patch.object(clinet._client._options.http_client, 'send', new= _do_sent) as _:
            try:
                with open(filepath, 'rb') as f:
                    clinet.put_object(models.PutObjectRequest(
                        bucket='bucket',
                        key='key',
                        body=f
                    ))
                self.fail('should not here')
            except exceptions.OperationError as err:
                self.assertIn("InternalError", str(err))

            self.assertEqual(3, len(self.save_request))
            self.assertEqual(3, len(self.save_data))
            for d in self.save_data:
                self.assertEqual(data, d)

        # bytes list
        self.save_request = []
        self.save_data = []
        data = b'hello world'
        data_list = [b'h', b'e',b'l',b'l',b'o',b' ',b'w',b'o',b'r',b'l',b'd']

        with mock.patch.object(clinet._client._options.http_client, 'send', new= _do_sent) as _:
            try:
                clinet.put_object(models.PutObjectRequest(
                    bucket='bucket',
                    key='key',
                    body=data_list
                ))
                self.fail('should not here')
            except exceptions.OperationError as err:
                self.assertIn("InternalError", str(err))

            self.assertEqual(3, len(self.save_request))
            self.assertEqual(3, len(self.save_data))
            for d in self.save_data:
                self.assertEqual(data, d)

        # bytes iter
        self.save_request = []
        self.save_data = []
        data = b'hello world'
        data_list = [b'h', b'e',b'l',b'l',b'o',b' ',b'w',b'o',b'r',b'l',b'd']

        with mock.patch.object(clinet._client._options.http_client, 'send', new= _do_sent) as _:
            try:
                clinet.put_object(models.PutObjectRequest(
                    bucket='bucket',
                    key='key',
                    body=iter(data_list)
                ))
                self.fail('should not here')
            except exceptions.OperationError as err:
                self.assertIn("InternalError", str(err))

            self.assertEqual(1, len(self.save_request))
            self.assertEqual(1, len(self.save_data))
            for d in self.save_data:
                self.assertEqual(data, d)
    
        # non-seekable file-like
        self.save_request = []
        self.save_data = []

        filepath = "./tests/data/example.jpg"
        with open(filepath, 'rb') as f:
            data = f.read()
        self.assertGreater(len(data), 0)

        with mock.patch.object(clinet._client._options.http_client, 'send', new= _do_sent) as _:
            try:
                with open(filepath, 'rb') as f:
                    clinet.put_object(models.PutObjectRequest(
                        bucket='bucket',
                        key='key',
                        body=NonSeekableFile(f)
                    ))
                self.fail('should not here')
            except exceptions.OperationError as err:
                self.assertIn("InternalError", str(err))

            self.assertEqual(1, len(self.save_request))
            self.assertEqual(1, len(self.save_data))
            for d in self.save_data:
                self.assertEqual(data, d)

    def test_invoke_operation_retryable_with_operation_timeout(self):
        self.save_request: List[HttpRequest] = None
        self.save_data: List[Any] = None

        def _do_sent(request: HttpRequest, **kwargs) -> HttpResponse:
            self.save_request.append(request)
            self.save_data.append(_read_body(request.body))
            self.assertIsInstance(request.body, io_utils.TeeIterator)
            raise exceptions.ServiceError(
                status_code=500,
                code='InternalError',
                request_id='id-1234',
                message='Please contact the server administrator, oss@service.aliyun.com.',
                ec='',
                timestamp='',
                request_target=''
            )

        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
        )
        clinet = client.Client(cfg)


        # str, no operation_timeout
        self.save_request = []
        self.save_data = []
        data = 'hello world'

        with mock.patch.object(clinet._client._options.http_client, 'send', new= _do_sent) as _:
            try:
                clinet.put_object(models.PutObjectRequest(
                    bucket='bucket',
                    key='key',
                    body=data
                ))
                self.fail('should not here')
            except exceptions.OperationError as err:
                self.assertIn("InternalError", str(err))

            self.assertEqual(3, len(self.save_request))
            self.assertEqual(3, len(self.save_data))
            for d in self.save_data:
                self.assertEqual(data.encode(), d)

        # str, with 0 operation_timeout
        self.save_request = []
        self.save_data = []
        data = 'hello world'

        with mock.patch.object(clinet._client._options.http_client, 'send', new= _do_sent) as _:
            try:
                clinet.put_object(models.PutObjectRequest(
                    bucket='bucket',
                    key='key',
                    body=data
                ), operation_timeout=0)
                self.fail('should not here')
            except exceptions.OperationError as err:
                self.assertIn("InternalError", str(err))

            self.assertEqual(1, len(self.save_request))
            self.assertEqual(1, len(self.save_data))
            for d in self.save_data:
                self.assertEqual(data.encode(), d)

        # str, with 10s operation_timeout
        self.save_request = []
        self.save_data = []
        data = 'hello world'

        with mock.patch.object(clinet._client._options.http_client, 'send', new= _do_sent) as _:
            try:
                clinet.put_object(models.PutObjectRequest(
                    bucket='bucket',
                    key='key',
                    body=data
                ), operation_timeout=10)
                self.fail('should not here')
            except exceptions.OperationError as err:
                self.assertIn("InternalError", str(err))

            self.assertEqual(3, len(self.save_request))
            self.assertEqual(3, len(self.save_data))
            for d in self.save_data:
                self.assertEqual(data.encode(), d)

        # str, with 4s operation_timeout 2
        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
            retryer=retry.StandardRetryer(backoff_delayer=retry.FixedDelayBackoff(2.5))
        )
        clinet = client.Client(cfg)
        self.save_request = []
        self.save_data = []
        data = 'hello world'

        with mock.patch.object(clinet._client._options.http_client, 'send', new= _do_sent) as _:
            try:
                clinet.put_object(models.PutObjectRequest(
                    bucket='bucket',
                    key='key',
                    body=data
                ), operation_timeout=4)
                self.fail('should not here')
            except exceptions.OperationError as err:
                self.assertIn("InternalError", str(err))

            self.assertEqual(2, len(self.save_request))
            self.assertEqual(2, len(self.save_data))
            for d in self.save_data:
                self.assertEqual(data.encode(), d)

    def test_invoke_operation_addressing_mode(self):
        """ """
        self.save_op_context: SigningContext = None
        self.save_options = None

        def _sent_http_request_once(context: SigningContext, options: Any) -> HttpResponse:
            self.save_op_context = context
            self.save_options = options
            return MockHttpResponse(
                status_code=200,
                reason='OK',
                headers={'x-oss-request-id': 'id-1234'},
                body=''
            )

        # virtual host
        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
        )
        clinet = client.Client(cfg)
        with mock.patch.object(clinet._client, '_sent_http_request_once', new= _sent_http_request_once) as _:
            # service
            clinet.invoke_operation(
                OperationInput(
                    op_name='InvokeOperation',
                    method='GET',
            ))
            self.assertEqual('https://oss-cn-hangzhou.aliyuncs.com/', self.save_op_context.request.url)

            # bucket
            clinet.invoke_operation(
                OperationInput(
                    op_name='InvokeOperation',
                    method='GET',
                    bucket='bucket',
            ))
            self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/', self.save_op_context.request.url)

            # object
            clinet.invoke_operation(
                OperationInput(
                    op_name='InvokeOperation',
                    method='GET',
                    bucket='bucket',
                    key='+123',
            ))
            self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/%2B123', self.save_op_context.request.url)

        # path style
        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
            use_path_style=True
        )
        clinet = client.Client(cfg)
        with mock.patch.object(clinet._client, '_sent_http_request_once', new= _sent_http_request_once) as _:
            # service
            clinet.invoke_operation(
                OperationInput(
                    op_name='InvokeOperation',
                    method='GET',
            ))
            self.assertEqual('https://oss-cn-hangzhou.aliyuncs.com/', self.save_op_context.request.url)

            # bucket
            clinet.invoke_operation(
                OperationInput(
                    op_name='InvokeOperation',
                    method='GET',
                    bucket='bucket',
            ))
            self.assertEqual('https://oss-cn-hangzhou.aliyuncs.com/bucket/', self.save_op_context.request.url)

            # object
            clinet.invoke_operation(
                OperationInput(
                    op_name='InvokeOperation',
                    method='GET',
                    bucket='bucket',
                    key='+123',
            ))
            self.assertEqual('https://oss-cn-hangzhou.aliyuncs.com/bucket/%2B123', self.save_op_context.request.url)

        # cname
        cfg = config.Config(
            region='cn-hangzhou',
            endpoint='www.cname-example.com',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
            use_cname=True
        )
        clinet = client.Client(cfg)
        with mock.patch.object(clinet._client, '_sent_http_request_once', new= _sent_http_request_once) as _:
            # bucket
            clinet.invoke_operation(
                OperationInput(
                    op_name='InvokeOperation',
                    method='GET',
                    bucket='bucket',
            ))
            self.assertEqual('https://www.cname-example.com/', self.save_op_context.request.url)

            # object
            clinet.invoke_operation(
                OperationInput(
                    op_name='InvokeOperation',
                    method='GET',
                    bucket='bucket',
                    key='+123',
            ))
            self.assertEqual('https://www.cname-example.com/%2B123', self.save_op_context.request.url)

        # ip with port and query
        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
            endpoint='127.0.0.1:8080?123',
        )
        clinet = client.Client(cfg)
        with mock.patch.object(clinet._client, '_sent_http_request_once', new= _sent_http_request_once) as _:
            # service
            clinet.invoke_operation(
                OperationInput(
                    op_name='InvokeOperation',
                    method='GET',
            ))
            self.assertEqual('https://127.0.0.1:8080/', self.save_op_context.request.url)

            # bucket
            clinet.invoke_operation(
                OperationInput(
                    op_name='InvokeOperation',
                    method='GET',
                    bucket='bucket',
            ))
            self.assertEqual('https://127.0.0.1:8080/bucket/', self.save_op_context.request.url)

            # object
            clinet.invoke_operation(
                OperationInput(
                    op_name='InvokeOperation',
                    method='GET',
                    bucket='bucket',
                    key='+123',
            ))
            self.assertEqual('https://127.0.0.1:8080/bucket/%2B123', self.save_op_context.request.url)

        # ip only
        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
            endpoint='127.0.0.1',
        )
        clinet = client.Client(cfg)
        with mock.patch.object(clinet._client, '_sent_http_request_once', new= _sent_http_request_once) as _:
            # bucket
            clinet.invoke_operation(
                OperationInput(
                    op_name='InvokeOperation',
                    method='GET',
                    bucket='bucket',
            ))
            self.assertEqual('https://127.0.0.1/bucket/', self.save_op_context.request.url)

        # endpoint with port, path, query
        cfg = config.Config(
            region='cn-hangzhou',
            endpoint='www.endpoint-example.com:3182/path-test?query-test',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
        )
        clinet = client.Client(cfg)
        with mock.patch.object(clinet._client, '_sent_http_request_once', new= _sent_http_request_once) as _:
            # service
            clinet.invoke_operation(
                OperationInput(
                    op_name='InvokeOperation',
                    method='GET',
            ))
            self.assertEqual('https://www.endpoint-example.com:3182/', self.save_op_context.request.url)

            # bucket
            clinet.invoke_operation(
                OperationInput(
                    op_name='InvokeOperation',
                    method='GET',
                    bucket='bucket',
            ))
            self.assertEqual('https://bucket.www.endpoint-example.com:3182/', self.save_op_context.request.url)

            # object
            clinet.invoke_operation(
                OperationInput(
                    op_name='InvokeOperation',
                    method='GET',
                    bucket='bucket',
                    key='+123',
            ))
            self.assertEqual('https://bucket.www.endpoint-example.com:3182/%2B123', self.save_op_context.request.url)



    def test_invoke_operation_verify(self):
        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
        )
        clinet = client.Client(cfg)        

        for bucket in ["", "12", "ABCD", "#1234"]:
            try:
                clinet.invoke_operation(
                    OperationInput(
                        op_name='InvokeOperation',
                        method='GET',
                        bucket=bucket,
                    ),
                )
                self.fail('should not here')
            except exceptions.OperationError as err:
                self.assertIn("Bucket name is invalid", str(err))

        try:
            clinet.invoke_operation(
                OperationInput(
                    op_name='InvokeOperation',
                    method='GET',
                    bucket='bucket',
                    key='',
                ),
            )
            self.fail('should not here')
        except exceptions.OperationError as err:
            self.assertIn("Object name is invalid", str(err))

        for endpoint in ["", None]:
            try:
                clinet._client._options.endpoint = endpoint
                clinet.invoke_operation(
                    OperationInput(
                        op_name='InvokeOperation',
                        method='GET',
                        bucket='bucket',
                        key='key',
                    ),
                )
                self.fail('should not here')
            except exceptions.OperationError as err:
                self.assertIn("invalid field", str(err))


    def test_resolve_cloud_box(self):
        # default product
        cfg = config.Config()
        c1 = client.Client(cfg)
        self.assertEqual("oss", c1._client._options.product)

        # default region, endpiont
        cfg = config.Config(
            region="test-region",
            endpoint="test-endpoint",
        )
        c2 = client.Client(cfg)
        self.assertEqual("oss", c1._client._options.product)
        self.assertEqual("test-region", c2._client._options.region)
        self.assertIsNotNone(c2._client._options.endpoint)
        self.assertEqual("test-endpoint", c2._client._options.endpoint.hostname)

        # set cloudbox id
        cfg = config.Config(
            region="test-region",
            endpoint="test-endpoint",
            cloud_box_id="test-cloudbox-id",
        )
        c3 = client.Client(cfg)
        self.assertEqual("oss-cloudbox", c3._client._options.product)
        self.assertEqual("test-cloudbox-id", c3._client._options.region)
        self.assertIsNotNone(c3._client._options.endpoint)
        self.assertEqual("test-endpoint", c3._client._options.endpoint.hostname)

        # cb - ** *.{region}.oss - cloudbox - control.aliyuncs.com
        # cb - ** *.{region}.oss - cloudbox.aliyuncs.com

        # auto detect cloudbox id default
        cfg = config.Config(
            region="test-region",
            endpoint="cb-123.test-region.oss-cloudbox-control.aliyuncs.com",
        )
        c4 = client.Client(cfg)
        self.assertEqual("oss", c4._client._options.product)
        self.assertEqual("test-region", c4._client._options.region)
        self.assertIsNotNone(c4._client._options.endpoint)
        self.assertEqual("cb-123.test-region.oss-cloudbox-control.aliyuncs.com", c4._client._options.endpoint.hostname)

        cfg = config.Config(
            region="test-region",
            endpoint="cb-123.test-region.oss-cloudbox.aliyuncs.com",
        )
        c5 = client.Client(cfg)
        self.assertEqual("oss", c5._client._options.product)
        self.assertEqual("test-region", c5._client._options.region)
        self.assertIsNotNone(c5._client._options.endpoint)
        self.assertEqual("cb-123.test-region.oss-cloudbox.aliyuncs.com", c5._client._options.endpoint.hostname)

        # auto detect cloudbox id set false
        cfg = config.Config(
            region="test-region",
            endpoint="cb-123.test-region.oss-cloudbox-control.aliyuncs.com",
            enable_auto_detect_cloud_box_id=False,
        )
        c6 = client.Client(cfg)
        self.assertEqual("oss", c6._client._options.product)
        self.assertEqual("test-region", c6._client._options.region)
        self.assertIsNotNone(c6._client._options.endpoint)
        self.assertEqual("cb-123.test-region.oss-cloudbox-control.aliyuncs.com", c6._client._options.endpoint.hostname)

        cfg = config.Config(
            region="test-region",
            endpoint="cb-123.test-region.oss-cloudbox.aliyuncs.com",
            enable_auto_detect_cloud_box_id=False,
        )
        c7 = client.Client(cfg)
        self.assertEqual("oss", c7._client._options.product)
        self.assertEqual("test-region", c7._client._options.region)
        self.assertIsNotNone(c7._client._options.endpoint)
        self.assertEqual("cb-123.test-region.oss-cloudbox.aliyuncs.com", c7._client._options.endpoint.hostname)

        # auto detect cloudbox id set true
        cfg = config.Config(
            region="test-region",
            endpoint="cb-123.test-region.oss-cloudbox-control.aliyuncs.com",
            enable_auto_detect_cloud_box_id=True,
        )
        c8 = client.Client(cfg)
        self.assertEqual("oss-cloudbox", c8._client._options.product)
        self.assertEqual("cb-123", c8._client._options.region)
        self.assertIsNotNone(c8._client._options.endpoint)
        self.assertEqual("cb-123.test-region.oss-cloudbox-control.aliyuncs.com", c8._client._options.endpoint.hostname)

        cfg = config.Config(
            region="test-region",
            endpoint="cb-123.test-region.oss-cloudbox.aliyuncs.com",
            enable_auto_detect_cloud_box_id=True,
        )
        c9 = client.Client(cfg)
        self.assertEqual("oss-cloudbox", c9._client._options.product)
        self.assertEqual("cb-123", c9._client._options.region)
        self.assertIsNotNone(c9._client._options.endpoint)
        self.assertEqual("cb-123.test-region.oss-cloudbox.aliyuncs.com", c9._client._options.endpoint.hostname)

        cfg = config.Config(
            region="test-region",
            endpoint="cb-123.test-region.oss-cloudbox.aliyuncs.com/test?123",
            enable_auto_detect_cloud_box_id=True,
        )
        c10 = client.Client(cfg)
        self.assertEqual("oss-cloudbox", c10._client._options.product)
        self.assertEqual("cb-123", c10._client._options.region)
        self.assertIsNotNone(c10._client._options.endpoint)
        self.assertEqual("cb-123.test-region.oss-cloudbox.aliyuncs.com", c10._client._options.endpoint.hostname)

        # auto detect cloudbox id set true + non cloud box endpoint
        cfg = config.Config(
            region="test-region",
            endpoint="cb-123.test-region.oss.aliyuncs.com",
            enable_auto_detect_cloud_box_id=True,
        )
        c11 = client.Client(cfg)
        self.assertEqual("oss", c11._client._options.product)
        self.assertEqual("test-region", c11._client._options.region)
        self.assertIsNotNone(c11._client._options.endpoint)
        self.assertEqual("cb-123.test-region.oss.aliyuncs.com", c11._client._options.endpoint.hostname)

        cfg = config.Config(
            region="test-region",
            endpoint="ncb-123.test-region.oss-cloudbox.aliyuncs.com",
            enable_auto_detect_cloud_box_id=True,
        )
        c12 = client.Client(cfg)
        self.assertEqual("oss", c12._client._options.product)
        self.assertEqual("test-region", c12._client._options.region)
        self.assertIsNotNone(c12._client._options.endpoint)
        self.assertEqual("ncb-123.test-region.oss-cloudbox.aliyuncs.com", c12._client._options.endpoint.hostname)

        cfg = config.Config(
            region="test-region",
            endpoint="cb-123.oss-cloudbox.aliyuncs.com",
            enable_auto_detect_cloud_box_id=True,
        )
        c13 = client.Client(cfg)
        self.assertEqual("oss", c13._client._options.product)
        self.assertEqual("test-region", c13._client._options.region)
        self.assertIsNotNone(c13._client._options.endpoint)
        self.assertEqual("cb-123.oss-cloudbox.aliyuncs.com", c13._client._options.endpoint.hostname)

class TestClientBase(unittest.TestCase):
    def setUp(self):
        self.set_requestFunc(None)
        self.set_responseFunc(None)

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        cls.request_dump: HttpRequest = None
        cls.client = _mock_client(cls.requestFunc, cls.responseFunc)
        cls.invoke_request = None
        cls.invoke_response = None

    @classmethod
    def tearDownClass(cls):
        pass

    @classmethod
    def requestFunc(cls, request: HttpRequest):
        cls.request_dump = request
        if cls.invoke_request is not None:
            cls.invoke_request(request)

    @classmethod
    def responseFunc(cls) -> MockHttpResponse:
        if cls.invoke_response is not None:
            return cls.invoke_response()

        return MockHttpResponse(
            status_code=200,
            reason='OK',
            headers={'x-oss-request-id': 'id-1234'},
            body=''
        )

    @classmethod
    def set_requestFunc(cls, fn):
        cls.invoke_request = fn

    @classmethod
    def set_responseFunc(cls, fn):
        cls.invoke_response = fn

    @classmethod
    def response_403_InvalidAccessKeyId(cls) -> MockHttpResponse:
        err_xml = r'''<?xml version="1.0" encoding="UTF-8"?>
            <Error>
                <Code>InvalidAccessKeyId</Code>
                <Message>The OSS Access Key Id you provided does not exist in our records.</Message>
                <RequestId>id-1234</RequestId>
                <HostId>oss-cn-hangzhou.aliyuncs.com</HostId>
                <OSSAccessKeyId>ak</OSSAccessKeyId>
                <EC>0002-00000902</EC>
                <RecommendDoc>https://api.aliyun.com/troubleshoot?q=0002-00000902</RecommendDoc>
            </Error>
        '''
        return MockHttpResponse(
            status_code=403,
            reason='Forbidden',
            headers={
                'Server': 'AliyunOSS',
                'Date': 'Tue, 23 Jul 2024 13:01:06 GMT',
                'Content-Type': 'application/xml',
                'x-oss-ec': '0002-00000902',
                'x-oss-request-id': 'id-1234',
            },
            body=err_xml.encode()
        )

class TestClientExtension(TestClientBase):
    def test_get_object_to_file(self):
        def response_200() -> MockHttpResponse:
            return MockHttpResponse(
                status_code=200,
                reason='OK',
                headers={
                    'Server': 'AliyunOSS',
                    'Date': 'Tue, 03 Sep 2024 06:33:10 GMT',
                    'Content-Length': '11',
                    'Content-MD5': 'XrY7u+Ae7tCTyyK7j1rNww==',
                    'x-oss-request-id': 'id-1234',
                    'x-oss-hash-crc64ecma': '5981764153023615706',
                },
                body=b'hello world'
            )

        self.set_responseFunc(response_200)
        request = models.GetObjectRequest(
            bucket='bucket',
            key='123%456+789#0',
        )
        filepath = _get_tempfile()
        result = self.client.get_object_to_file(request, filepath)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/123%25456%2B789%230', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)
        self.assertEqual('5981764153023615706', result.hash_crc64)

        data = b''
        with open(filepath, 'rb') as f:
            data = f.read()

        self.assertEqual(b'hello world', data)

        #progress
        global progress_save_n
        progress_save_n = 0
        request = models.GetObjectRequest(
            bucket='bucket',
            key='123%456+789#0',
            progress_fn=_progress_fn,
        )
        filepath = _get_tempfile()
        result = self.client.get_object_to_file(request, filepath)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/123%25456%2B789%230', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)
        self.assertEqual('5981764153023615706', result.hash_crc64)
        self.assertEqual(11, progress_save_n)

    def test_get_object_to_file_crc_fail(self):
        def response_200() -> MockHttpResponse:
            return MockHttpResponse(
                status_code=200,
                reason='OK',
                headers={
                    'Server': 'AliyunOSS',
                    'Date': 'Tue, 03 Sep 2024 06:33:10 GMT',
                    'Content-Length': '11',
                    'Content-MD5': 'XrY7u+Ae7tCTyyK7j1rNww==',
                    'x-oss-request-id': 'id-1234',
                    'x-oss-hash-crc64ecma': '5981764153023615707',
                },
                body=b'hello world'
            )

        self.set_responseFunc(response_200)
        request = models.GetObjectRequest(
            bucket='bucket',
            key='123%456+789#0',
        )
        filepath = _get_tempfile()
        try:
            self.client.get_object_to_file(request, filepath)
            self.fail('should not here')
        except exceptions.InconsistentError as err:
            self.assertIn('crc is inconsistent, client 5981764153023615706, server 5981764153023615707', str(err))


class TestClientCRC(unittest.TestCase):

    def test_put_object_crc64_flags(self):  
        self.save_request: List[HttpRequest] = None
        self.save_data: List[Any] = None

        def _do_sent(request: HttpRequest, **kwargs) -> HttpResponse:
            self.save_request.append(request) 
            self.save_data.append(_read_body(request.body))
            return MockHttpResponse(
                status_code=200,
                reason='OK',
                headers={'x-oss-request-id': 'id-1234', 'x-oss-hash-crc64ecma': '123'},
                body=''
            )

        # upload crc check enabled
        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
        )
        clinet = client.Client(cfg)


        self.save_request = []
        self.save_data = []
        data = 'hello world'

        with mock.patch.object(clinet._client._options.http_client, 'send', new= _do_sent) as _:
            try:
                clinet.put_object(models.PutObjectRequest(
                    bucket='bucket',
                    key='key',
                    body=data
                ))
                self.fail('should not here')
            except exceptions.OperationError as err:
                self.assertIn("crc is inconsistent", str(err))

            self.assertEqual(3, len(self.save_request))
            self.assertEqual(3, len(self.save_data))
            for d in self.save_data:
                self.assertEqual(data.encode(), d)


        # upload crc check disenabled
        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
            disable_upload_crc64_check=True
        )
        clinet = client.Client(cfg)

        self.save_request = []
        self.save_data = []
        data = 'hello world'

        with mock.patch.object(clinet._client._options.http_client, 'send', new= _do_sent) as _:
            try:
                result = clinet.put_object(models.PutObjectRequest(
                    bucket='bucket',
                    key='key',
                    body=data
                ))
                self.assertEqual('123', result.hash_crc64)
            except exceptions.OperationError as err:
                self.fail('should not here')

            self.assertEqual(1, len(self.save_request))
            self.assertEqual(1, len(self.save_data))
            for d in self.save_data:
                self.assertEqual(data.encode(), d)

    def test_upload_part_crc64_flags(self):  
        self.save_request: List[HttpRequest] = None
        self.save_data: List[Any] = None

        def _do_sent(request: HttpRequest, **kwargs) -> HttpResponse:
            self.save_request.append(request) 
            self.save_data.append(_read_body(request.body))
            return MockHttpResponse(
                status_code=200,
                reason='OK',
                headers={'x-oss-request-id': 'id-1234', 'x-oss-hash-crc64ecma': '123', 'ETag': "etag"},
                body=''
            )

        # upload crc check enabled
        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
        )
        clinet = client.Client(cfg)

        self.save_request = []
        self.save_data = []
        data = 'hello world'

        with mock.patch.object(clinet._client._options.http_client, 'send', new= _do_sent) as _:
            try:
                clinet.upload_part(models.UploadPartRequest(
                    bucket='bucket',
                    key='key',
                    upload_id='upload-id',
                    part_number=1,
                    body=data
                ))
                self.fail('should not here')
            except exceptions.OperationError as err:
                self.assertIn("crc is inconsistent", str(err))

            self.assertEqual(3, len(self.save_request))
            self.assertEqual(3, len(self.save_data))
            for d in self.save_data:
                self.assertEqual(data.encode(), d)


        # upload crc check disenabled
        cfg = config.Config(
            region='cn-hangzhou',
            credentials_provider=credentials.AnonymousCredentialsProvider(),
            disable_upload_crc64_check=True
        )
        clinet = client.Client(cfg)

        self.save_request = []
        self.save_data = []
        data = 'hello world'

        with mock.patch.object(clinet._client._options.http_client, 'send', new= _do_sent) as _:
            try:
                result = clinet.upload_part(models.UploadPartRequest(
                    bucket='bucket',
                    key='key',
                    upload_id='upload-id',
                    part_number=1,
                    body=data
                ))
                self.assertEqual('123', result.hash_crc64)
            except exceptions.OperationError as err:
                self.fail('should not here')

            self.assertEqual(1, len(self.save_request))
            self.assertEqual(1, len(self.save_data))
            for d in self.save_data:
                self.assertEqual(data.encode(), d)
