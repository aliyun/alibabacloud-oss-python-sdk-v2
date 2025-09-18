
# -*- coding: utf-8 -*-
from urllib.parse import ParseResult, quote
from ..types import EndpointProvider, OperationInput

def from_region(region: str, etype: str) -> str:
    """Generate vectors endpoint from region"""
    if etype == "internal":
        return f"{region}-internal.oss-vectors.aliyuncs.com"
    else:
        return f"{region}.oss-vectors.aliyuncs.com"


class VectorsEndpointProvider(EndpointProvider):
    def __init__(
        self, 
        endpoint: ParseResult,
        account_id: str, 
    ) -> None:
        self._endpoint = endpoint
        self._account_id = account_id or ""

    def build_url(self, op_input: OperationInput) -> str:
        """build the request url"""
        host = ""
        paths = []
        if op_input.bucket is None:
            host = self._endpoint.netloc
        else:
            host = f'{op_input.bucket}-{self._account_id}.{self._endpoint.netloc}'

        if op_input.key is not None:
            paths.append(quote(op_input.key))

        return f'{self._endpoint.scheme}://{host}/{"/".join(paths)}'
