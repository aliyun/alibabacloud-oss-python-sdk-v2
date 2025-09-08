from typing import Optional, Union, List
from .types import CredentialsProvider, HttpClient, Retryer
from . import defaults

class Config(object):
    """Configuration for client."""
    def __init__(
        self,
        region: str = None,
        endpoint: Optional[str] = None,
        signature_version: Optional[str] = None,
        credentials_provider: Optional[CredentialsProvider] = None,
        retry_max_attempts: Optional[int] = None,
        retryer: Optional[Retryer] = None,
        http_client: Optional[HttpClient] = None,
        connect_timeout: Optional[Union[int, float]] = None,
        readwrite_timeout: Optional[Union[int, float]] = None,
        use_dualstack_endpoint: Optional[bool] = None,
        use_accelerate_endpoint: Optional[bool] = None,
        use_internal_endpoint: Optional[bool] = None,
        disable_ssl: Optional[bool] = None,
        insecure_skip_verify: Optional[bool] = None,
        enabled_redirect: Optional[bool] = None,
        use_cname: Optional[bool] = None,
        use_path_style: Optional[bool] = None,
        proxy_host: Optional[Union[str, dict]] = None,
        disable_upload_crc64_check: Optional[bool] = None,
        disable_download_crc64_check: Optional[bool] = None,
        additional_headers: Optional[List[str]] = None,
        user_agent: Optional[str] = None,
        cloud_box_id: Optional[str] = None,
        enable_auto_detect_cloud_box_id: Optional[bool] = None,
        account_id: Optional[str] = None
    ) -> None:
        """
        Args:
            region (str, required): The region in which the bucket is located.
            endpoint (str, optional): The domain names that other services can use to access OSS.
            credentials_provider (CredentialsProvider, optional): The credentials provider to use when signing requests.
            connect_timeout (int|float, optional): The time in seconds till a timeout exception is thrown
                when attempting to make a connection. The default is 10 seconds.
            readwrite_timeout (int|float, optional): The time in seconds till a timeout exception is thrown
                when attempting to read from a connection. The default is 20 seconds.
            retry_max_attempts (int, optional): Specifies the maximum number attempts an API client will call
                an operation that fails with a retryable error.
            retryer (Retryer, optional): Guides how HTTP requests should be retried in case of recoverable failures.
            http_client (HttpClient, optional): The HTTP client to invoke API calls with.
            use_cname (bool, optional): If the endpoint is s CName, set this flag to true
            use_path_style (bool, optional): Allows you to enable the client to use path-style addressing, 
                i.e., https://oss-cn-hangzhou.aliyuncs.com/bucket/key.
            signature_version (str, optional): The signature version when signing requests. Valid values v4, v1
            disable_ssl (bool, optional): Forces the endpoint to be resolved as HTTP.
            insecure_skip_verify (bool, optional): Skip server certificate verification.
            enabled_redirect (bool, optional): Enable http redirect or not. Default is disable
            use_dualstack_endpoint (bool, optional): Dual-stack endpoints are provided in some regions.
                This allows an IPv4 client and an IPv6 client to access a bucket by using the same endpoint.
                Set this to True to use a dual-stack endpoint for the requests.
            use_accelerate_endpoint (bool, optional): OSS provides the transfer acceleration feature to accelerate date transfers
                of data uploads and downloads across countries and regions.
                Set this to True to use a accelerate endpoint for the requests.
            use_internal_endpoint (bool, optional): You can use an internal endpoint to communicate between Alibaba Cloud services located 
                within the same region over the internal network. You are not charged for the traffic generated over the internal network.
                Set this to True to use a internal endpoint for the requests.
            proxy_host: (Union[str, dict], optional): The proxy setting.
                If proxy_host is str type, i.e. 'http://10.10.1.10:3128', both HTTP and HTTPS are supported.
                Or give a proxy for a specific scheme by dict type, i.e. {'http': 'http://10.10.1.10:3128/'}.
            disable_upload_crc64_check: (bool, optional): Check data integrity of uploads via the crc64 by default.
                This feature takes effect for put_object, append_object, upload_part, uploader.upload_from and uploader.upload_file
                Set this to `true` to disable this feature.
            disable_download_crc64_check: (bool, optional): Check data integrity of uploads via the crc64 by default.
                This feature only takes effect for downloader.download_file, get_object_to_file.
                Set this to `true` to disable this feature.
            additional_headers: (List[str], optional): Additional signable headers.
            user_agent: (str, optional): The optional user specific identifier appended to the User-Agent header.
            cloud_box_id: (str, optional): The cloud box id.
            enable_auto_detect_cloud_box_id: (bool, optional): The cloud box id is automatically extracted from endpoint.
            account_id: (str, optional): The account id, must be required in vectors options.
        """
        self.region = region
        self.endpoint = endpoint
        self.signature_version = signature_version
        self.credentials_provider = credentials_provider
        self.retry_max_attempts = retry_max_attempts
        self.retryer = retryer
        self.http_client = http_client
        self.connect_timeout = connect_timeout
        self.readwrite_timeout = readwrite_timeout
        self.use_dualstack_endpoint = use_dualstack_endpoint
        self.use_accelerate_endpoint = use_accelerate_endpoint
        self.use_internal_endpoint = use_internal_endpoint
        self.disable_ssl = disable_ssl
        self.insecure_skip_verify = insecure_skip_verify
        self.enabled_redirect = enabled_redirect
        self.use_cname = use_cname
        self.use_path_style = use_path_style
        self.proxy_host = proxy_host
        self.disable_upload_crc64_check = disable_upload_crc64_check
        self.disable_download_crc64_check = disable_download_crc64_check
        self.additional_headers = additional_headers
        self.user_agent = user_agent
        self.cloud_box_id = cloud_box_id
        self.enable_auto_detect_cloud_box_id = enable_auto_detect_cloud_box_id
        self.account_id = account_id

def load_default() -> Config:
    """Using the SDK's default configuration"""
    return Config(
        signature_version=defaults.DEFAULT_SIGNATURE_VERSION,
        connect_timeout=defaults.DEFAULT_CONNECT_TIMEOUT,
        readwrite_timeout=defaults.DEFAULT_READWRITE_TIMEOUT,
    )
