# -*- coding: utf-8 -*-
from urllib.parse import ParseResult, quote
from alibabacloud_oss_v2.types import EndpointProvider, BucketNameResolver, OperationInput
from alibabacloud_oss_v2.config import Config


class AgenticProvider(EndpointProvider, BucketNameResolver):
    """Merged EndpointProvider + BucketNameResolver for AgenticBucket/BucketSpace.

    - BucketNameResolver: prefix -> {prefix}-{account_id}-{region}-{suffix}
    - EndpointProvider:
      - with bucket: {fullname}.{endpoint.netloc}/{key}
      - without bucket: {endpoint.netloc}/ (only used by ListAgenticBuckets)
    """

    def __init__(self, endpoint: ParseResult, account_id: str, region: str, suffix: str) -> None:
        self._endpoint = endpoint
        self._account_id = account_id or ""
        self._region = region or ""
        self._suffix = suffix

    def build_bucket_name(self, op_input: OperationInput) -> str:
        if op_input.bucket is None:
            return None
        return f'{op_input.bucket}-{self._account_id}-{self._region}-{self._suffix}'

    def build_url(self, op_input: OperationInput) -> str:
        paths = []
        if op_input.bucket is None:
            host = self._endpoint.netloc
        else:
            host = f'{self.build_bucket_name(op_input)}.{self._endpoint.netloc}'

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
