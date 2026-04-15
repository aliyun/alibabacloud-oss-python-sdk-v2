# -*- coding: utf-8 -*-
"""ARN utilities for OSS."""

from typing import Optional


class ArnResource:
    """Represents an ARN resource.

    Args:
        resource_type: The optional resource type.
        resource: The resource string.
        qualifier: The optional resource qualifier.
    """

    def __init__(
        self,
        resource_type: Optional[str] = None,
        resource: str = "",
        qualifier: Optional[str] = None
    ) -> None:
        self.resource_type = resource_type
        self.resource = resource
        self.qualifier = qualifier

    @classmethod
    def from_string(cls, resource: str) -> 'ArnResource':
        """Creates an ArnResource from a string.

        Args:
            resource: The resource string to parse.

        Returns:
            ArnResource: The parsed ArnResource.
        """
        if not resource:
            return cls(resource="")

        splitter = _find_first_occurrence(resource, [':', '/'])

        if splitter is None:
            return cls(resource=resource)

        resource_type_colon_index = resource.index(splitter)
        resource_type = resource[0:resource_type_colon_index]

        # Find the next occurrence of the same or different splitter after resource_type
        resource_colon_index = resource.find(splitter, resource_type_colon_index + 1)
        if resource_colon_index == -1:
            # No qualifier
            return cls(
                resource_type=resource_type,
                resource=resource[resource_type_colon_index + 1:]
            )
        else:
            # has qualifier
            return cls(
                resource_type=resource_type,
                resource=resource[resource_type_colon_index + 1:resource_colon_index],
                qualifier=resource[resource_colon_index + 1:]
            )
 

class Arn:
    """Represents an ARN.

    Format: acs:{service}:{region}:{accountId}:{resource}

    Args:
        service: The service namespace that identifies the product.
        region: The Region that the resource resides in.
        account_id: The ID of the account that owns the resource.
        resource: The resource string.
    """

    def __init__(
        self,
        service: str = "",
        region: Optional[str] = None,
        account_id: Optional[str] = None,
        resource: str = ""
    ) -> None:
        if not service:
            raise ValueError("service cannot be empty")
        if not resource:
            raise ValueError("resource cannot be empty")
        self.service = service
        self.region = region
        self.account_id = account_id
        self.resource = resource
        self._arn_resource = ArnResource.from_string(self.resource)

    @property
    def arn_resource(self) -> ArnResource:
        """Returns the parsed ArnResource."""
        return self._arn_resource

    def resource_as_string(self) -> str:
        """Returns the resource as string."""
        return self.resource

    @classmethod
    def from_string(cls, arn: str) -> 'Arn':
        """Parses an ARN from a string.

        Args:
            arn: The ARN string to parse.

        Returns:
            Arn: The parsed Arn.

        Raises:
            ValueError: If the ARN is malformed.
        """
        result = cls._parse_arn(arn, throw_on_error=True)
        if result is None:
            raise ValueError("ARN parsing failed")
        return result

    @classmethod
    def try_from_string(cls, arn: str) -> Optional['Arn']:
        """Attempts to parse an ARN from a string.

        Args:
            arn: The ARN string to parse.

        Returns:
            Arn or None: The parsed Arn, or None if parsing failed.
        """
        return cls._parse_arn(arn, throw_on_error=False)

    @classmethod
    def _parse_arn(cls, arn: str, throw_on_error: bool) -> Optional['Arn']:
        """Internal method to parse ARN string."""
        if arn is None:
            return None

        arn_colon_index = arn.find(':')
        if arn_colon_index < 0 or arn[0:arn_colon_index] != 'acs':
            if throw_on_error:
                raise ValueError("Malformed ARN - doesn't start with 'acs:'")
            return None

        service_colon_index = arn.find(':', arn_colon_index + 1)
        if service_colon_index < 0:
            if throw_on_error:
                raise ValueError("Malformed ARN - no service specified")
            return None
        service = arn[arn_colon_index + 1:service_colon_index]

        region_colon_index = arn.find(':', service_colon_index + 1)
        if region_colon_index < 0:
            if throw_on_error:
                raise ValueError("Malformed ARN - no region specified")
            return None
        region = arn[service_colon_index + 1:region_colon_index]

        account_colon_index = arn.find(':', region_colon_index + 1)
        if account_colon_index < 0:
            if throw_on_error:
                raise ValueError("Malformed ARN - no account specified")
            return None
        account_id = arn[region_colon_index + 1:account_colon_index]

        resource = arn[account_colon_index + 1:]
        if not resource:
            if throw_on_error:
                raise ValueError("Malformed ARN - no resource specified")
            return None

        return cls(
            service=service,
            region=region or None,
            account_id=account_id or None,
            resource=resource
        )


def _find_first_occurrence(s: str, chars: list) -> Optional[str]:
    """Finds the first occurrence of any character in chars within s."""
    min_index = -1
    found_char = None
    for c in chars:
        index = s.find(c)
        if index >= 0:
            if min_index < 0 or index < min_index:
                min_index = index
                found_char = c
    return found_char
