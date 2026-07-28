# -*- coding: utf-8 -*-
from urllib.parse import ParseResult, quote
from alibabacloud_oss_v2 import exceptions
from alibabacloud_oss_v2.types import EndpointProvider, BucketNameResolver, OperationInput
from alibabacloud_oss_v2.config import Config
from alibabacloud_oss_v2._client import AddressStyle


class AgenticProvider(EndpointProvider, BucketNameResolver):
    """Merged EndpointProvider + BucketNameResolver for AgenticBucket/BucketSpace.

    - BucketNameResolver: prefix -> {prefix}-{account_id}-{region}-{suffix}
    - EndpointProvider:
      - virtual-hosted (default):
        - with bucket: {fullname}.{endpoint.netloc}/{key}
        - without bucket: {endpoint.netloc}/ (only used by ListAgenticBuckets)
      - path-style (address_style=AddressStyle.Path):
        - with bucket: {endpoint.netloc}/{fullname}/{key}
    """

    def __init__(self, endpoint: ParseResult, account_id: str, region: str, suffix: str,
                 address_style: int = AddressStyle.Virtual) -> None:
        self._endpoint = endpoint
        self._account_id = account_id or ""
        self._region = region or ""
        self._suffix = suffix
        self._address_style = address_style

    def build_bucket_name(self, op_input: OperationInput) -> str:
        if op_input.bucket is None:
            return None
        if not self._account_id:
            raise exceptions.ParamRequiredError(field='AccountId')
        if not self._region:
            raise exceptions.ParamRequiredError(field='Region')
        return f'{op_input.bucket}-{self._account_id}-{self._region}-{self._suffix}'

    def build_url(self, op_input: OperationInput) -> str:
        host = self._endpoint.netloc
        paths = []
        if op_input.bucket is not None:
            if self._address_style == AddressStyle.Path:
                paths.append(self.build_bucket_name(op_input))
                if op_input.key is None:
                    paths.append('')
            else:
                full_name = self.build_bucket_name(op_input)
                if len(full_name) > 63:
                    raise ValueError(
                        f'the host label "{full_name}" exceeds the maximum length of 63 characters')
                host = f'{full_name}.{self._endpoint.netloc}'

        if op_input.key is not None:
            paths.append(quote(op_input.key))

        return f'{self._endpoint.scheme}://{host}/{"/".join(paths)}'


class BucketSpaceHelper:
    """Helper to convert a BucketSpace prefix into a full bucket name.

    Useful when reusing the standard Client for BucketSpace-level Bucket/Object APIs.
    """

    def __init__(self, config: Config) -> None:
        self._account_id = config.account_id or ""
        self._region = config.region or ""

    def to_bucket_name(self, prefix: str) -> str:
        return f"{prefix}-{self._account_id}-{self._region}-bs-apsr"
