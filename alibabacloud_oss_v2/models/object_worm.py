"""Models for object retention and legal hold APIs"""

from typing import Optional, Any, Union
from enum import Enum
from .. import serde


class ObjectRetentionModeType(str, Enum):
    """The retention mode of the object-level WORM configuration."""
    GOVERNANCE = 'GOVERNANCE'
    COMPLIANCE = 'COMPLIANCE'


class ObjectLegalHoldStatusType(str, Enum):
    """The status of the object legal hold."""
    ON = 'ON'
    OFF = 'OFF'


class Retention(serde.Model):
    """The container for object retention configuration."""

    _attribute_map = {
        'mode': {'tag': 'xml', 'rename': 'Mode', 'type': 'str'},
        'retain_until_date': {'tag': 'xml', 'rename': 'RetainUntilDate', 'type': 'str'},
    }

    _xml_map = {
        'name': 'Retention'
    }

    def __init__(
        self,
        mode: Optional[Union[str, ObjectRetentionModeType]] = None,
        retain_until_date: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            mode (str | ObjectRetentionModeType, optional): The retention mode. Valid values: GOVERNANCE, COMPLIANCE.
            retain_until_date (str, optional): The date until which the object is retained. ISO 8601 format (e.g., '2025-11-10T16:00:00.000Z').
        """
        super().__init__(**kwargs)
        self.mode = mode
        self.retain_until_date = retain_until_date


class LegalHold(serde.Model):
    """The container for object legal hold configuration."""

    _attribute_map = {
        'status': {'tag': 'xml', 'rename': 'Status', 'type': 'str'},
    }

    _xml_map = {
        'name': 'LegalHold'
    }

    def __init__(
        self,
        status: Optional[Union[str, ObjectLegalHoldStatusType]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            status (str | ObjectLegalHoldStatusType, optional): The legal hold status. Valid values: ON, OFF.
        """
        super().__init__(**kwargs)
        self.status = status


class PutObjectRetentionRequest(serde.RequestModel):
    """The request for the PutObjectRetention operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'key': {'tag': 'input', 'position': 'path', 'rename': 'key', 'type': 'str', 'required': True},
        'version_id': {'tag': 'input', 'position': 'query', 'rename': 'versionId', 'type': 'str'},
        'bypass_governance_retention': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-bypass-governance-retention', 'type': 'bool'},
        'retention': {'tag': 'input', 'position': 'body', 'rename': 'Retention', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        version_id: Optional[str] = None,
        bypass_governance_retention: Optional[Union[str, bool]] = None,
        retention: Optional[Retention] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            version_id (str, optional): The version ID of the object.
            bypass_governance_retention (Union[str, bool], optional): Bypass the governance retention mode.
            retention (ObjectRetentionConfiguration, optional): The object retention configuration.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.version_id = version_id
        self.bypass_governance_retention = bypass_governance_retention
        self.retention = retention


class PutObjectRetentionResult(serde.ResultModel):
    """The result for the PutObjectRetention operation."""


class GetObjectRetentionRequest(serde.RequestModel):
    """The request for the GetObjectRetention operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'key': {'tag': 'input', 'position': 'path', 'rename': 'key', 'type': 'str', 'required': True},
        'version_id': {'tag': 'input', 'position': 'query', 'rename': 'versionId', 'type': 'str'},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        version_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            version_id (str, optional): The version ID of the object.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.version_id = version_id


class GetObjectRetentionResult(serde.ResultModel):
    """The result for the GetObjectRetention operation."""

    _attribute_map = {
        'retention': {'tag': 'output', 'position': 'body', 'rename': 'Retention', 'type': 'Retention,xml'},
    }

    _dependency_map = {
        'Retention': {'new': lambda: Retention()},
    }

    def __init__(
        self,
        retention: Optional[Retention] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            retention (Retention, optional): The object retention configuration.
        """
        super().__init__(**kwargs)
        self.retention = retention


class PutObjectLegalHoldRequest(serde.RequestModel):
    """The request for the PutObjectLegalHold operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'key': {'tag': 'input', 'position': 'path', 'rename': 'key', 'type': 'str', 'required': True},
        'version_id': {'tag': 'input', 'position': 'query', 'rename': 'versionId', 'type': 'str'},
        'legal_hold': {'tag': 'input', 'position': 'body', 'rename': 'LegalHold', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        version_id: Optional[str] = None,
        legal_hold: Optional[LegalHold] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            version_id (str, optional): The version ID of the object.
            legal_hold (LegalHold, optional): The object legal hold configuration.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.version_id = version_id
        self.legal_hold = legal_hold


class PutObjectLegalHoldResult(serde.ResultModel):
    """The result for the PutObjectLegalHold operation."""


class GetObjectLegalHoldRequest(serde.RequestModel):
    """The request for the GetObjectLegalHold operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'key': {'tag': 'input', 'position': 'path', 'rename': 'key', 'type': 'str', 'required': True},
        'version_id': {'tag': 'input', 'position': 'query', 'rename': 'versionId', 'type': 'str'},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        version_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            version_id (str, optional): The version ID of the object.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.version_id = version_id


class GetObjectLegalHoldResult(serde.ResultModel):
    """The result for the GetObjectLegalHold operation."""

    _attribute_map = {
        'legal_hold': {'tag': 'output', 'position': 'body', 'rename': 'LegalHold', 'type': 'LegalHold,xml'},
    }

    _dependency_map = {
        'LegalHold': {'new': lambda: LegalHold()},
    }

    def __init__(
        self,
        legal_hold: Optional[LegalHold] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            legal_hold (LegalHold, optional): The object legal hold configuration.
        """
        super().__init__(**kwargs)
        self.legal_hold = legal_hold
