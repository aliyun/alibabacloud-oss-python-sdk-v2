
# -*- coding: utf-8 -*-
from urllib.parse import ParseResult
from ..types import EndpointProvider, OperationInput
from .._client import AddressStyle


def from_region(region: str, etype: str) -> str:
    """Generate tables endpoint from region"""
    if etype == "internal":
        return f"{region}-internal.oss-tables.aliyuncs.com"
    else:
        return f"{region}.oss-tables.aliyuncs.com"


class TablesEndpointProvider(EndpointProvider):
    """Endpoint provider for OSS Tables API.

    Supports both VirtualHosted and Path address styles.
    For VirtualHosted style, the bucket ARN is parsed to construct
    a virtual-hosted style endpoint.
    """

    def __init__(
        self,
        endpoint: ParseResult,
        address_style: AddressStyle = AddressStyle.Virtual,
    ) -> None:
        """Initialize the endpoint provider.

        Args:
            endpoint: The parsed endpoint URL.
            address_style: The address style to use (Virtual or Path).
        """
        self._endpoint = endpoint
        self._address_style = address_style

    def build_url(self, op_input: OperationInput) -> str:
        """Build the request URL based on address style.

        For VirtualHosted style with bucket ARN like:
        acs:oss-tables:region:account-id:bucket/bucket-name

        The host is constructed as: bucket-name-account-id.endpoint

        For Path or CName style, the host remains unchanged.

        Args:
            op_input: The operation input containing bucket and key.

        Returns:
            The constructed URL string.

        Raises:
            ValueError: If the bucket ARN format is invalid.
        """
        paths = []
        host = self._endpoint.netloc

        if op_input.bucket is not None:
            if self._address_style == AddressStyle.Virtual:
                # Parse bucket ARN
                # acs:oss-tables:region:account-id:bucket/bucket-name
                bucket_arn = op_input.bucket

                # Split by ':' to get parts
                vh_vals = bucket_arn.split(':')
                if len(vh_vals) != 5:
                    raise ValueError("input.bucket is not bucket arn")

                # Split the last part by '/' to get bucket type and bucket name
                vh_vals2 = vh_vals[4].split('/')
                if len(vh_vals2) != 2:
                    raise ValueError("input.bucket is not bucket arn")

                # vh_vals[3] is account-id, vh_vals2[1] is bucket-name
                # Construct: bucket-name-account-id.host
                host = f"{vh_vals2[1]}-{vh_vals[3]}.{host}"
            # For Path or CName style, the host remains unchanged

        if op_input.key is not None:
            paths.append(op_input.key)

        return f'{self._endpoint.scheme}://{host}/{"/".join(paths)}'
