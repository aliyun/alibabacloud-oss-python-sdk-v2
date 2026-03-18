import datetime
from typing import Optional, List, Any, Union
from enum import Enum
from .. import serde


class ObjectWormConfigurationModeType(str, Enum):
    """
    Object-level retention strategy pattern
    """

    GOVERNANCE = 'GOVERNANCE'
    COMPLIANCE = 'COMPLIANCE'


class ObjectWormConfigurationRuleDefaultRetention(serde.Model):
    """
    The container that stores the default retention settings.
    """

    _attribute_map = { 
        'mode': {'tag': 'xml', 'rename': 'Mode', 'type': 'str'},
        'days': {'tag': 'xml', 'rename': 'Days', 'type': 'int'},
        'years': {'tag': 'xml', 'rename': 'Years', 'type': 'int'},
    }

    _xml_map = {
        'name': 'DefaultRetention'
    }

    def __init__(
        self,
        mode: Optional[Union[str, ObjectWormConfigurationModeType]] = None,
        days: Optional[int] = None,
        years: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            mode (str | ObjectWormConfigurationModeType, optional): Object-level retention strategy pattern. Valid values: GOVERNANCE, COMPLIANCE
            days (int, optional): Object-level retention policy days (max 36500)
            years (int, optional): Bucket object level retention policy years (max 100)
        """
        super().__init__(**kwargs)
        self.mode = mode
        self.days = days
        self.years = years


class ObjectWormConfigurationRule(serde.Model):
    """
    The container that stores the object-level retention policy rule.
    """

    _attribute_map = { 
        'default_retention': {'tag': 'xml', 'rename': 'DefaultRetention', 'type': 'ObjectWormConfigurationRuleDefaultRetention,xml'},
    }

    _xml_map = {
        'name': 'Rule'
    }

    _dependency_map = { 
        'DefaultRetention': {'new': lambda: ObjectWormConfigurationRuleDefaultRetention()},
    }

    def __init__(
        self,
        default_retention: Optional[ObjectWormConfigurationRuleDefaultRetention] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            default_retention (ObjectWormConfigurationRuleDefaultRetention, optional): Container with default retention settings
        """
        super().__init__(**kwargs)
        self.default_retention = default_retention


class ObjectWormConfiguration(serde.Model):
    """
    The container that stores the object-level retention policy configuration.
    """

    _attribute_map = { 
        'object_worm_enabled': {'tag': 'xml', 'rename': 'ObjectWormEnabled', 'type': 'str'},
        'rule': {'tag': 'xml', 'rename': 'Rule', 'type': 'ObjectWormConfigurationRule,xml'},
    }

    _xml_map = {
        'name': 'ObjectWormConfiguration'
    }

    _dependency_map = { 
        'Rule': {'new': lambda: ObjectWormConfigurationRule()},
    }

    def __init__(
        self,
        object_worm_enabled: Optional[str] = None,
        rule: Optional[ObjectWormConfigurationRule] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            object_worm_enabled (str, optional): Whether to enable object-level retention policy
            rule (ObjectWormConfigurationRule, optional): Container with object-level retention policy
        """
        super().__init__(**kwargs)
        self.object_worm_enabled = object_worm_enabled
        self.rule = rule


class PutBucketObjectWormConfigurationRequest(serde.RequestModel):
    """
    The request for the PutBucketObjectWormConfiguration operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'object_worm_configuration': {'tag': 'input', 'position': 'body', 'rename': 'ObjectWormConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        object_worm_configuration: Optional[ObjectWormConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            object_worm_configuration (ObjectWormConfiguration, optional): The request body schema.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.object_worm_configuration = object_worm_configuration


class PutBucketObjectWormConfigurationResult(serde.ResultModel):
    """
    The result for the PutBucketObjectWormConfiguration operation.
    """


class GetBucketObjectWormConfigurationRequest(serde.RequestModel):
    """
    The request for the GetBucketObjectWormConfiguration operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
        """
        super().__init__(**kwargs)
        self.bucket = bucket


class GetBucketObjectWormConfigurationResult(serde.ResultModel):
    """
    The result for the GetBucketObjectWormConfiguration operation.
    """

    _attribute_map = { 
        'object_worm_configuration': {'tag': 'output', 'position': 'body', 'rename': 'ObjectWormConfiguration', 'type': 'ObjectWormConfiguration,xml'},
    }

    _dependency_map = { 
        'ObjectWormConfiguration': {'new': lambda: ObjectWormConfiguration()},
    }

    def __init__(
        self,
        object_worm_configuration: Optional[ObjectWormConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            object_worm_configuration (ObjectWormConfiguration, optional): The container that stores object worm config.
        """
        super().__init__(**kwargs)
        self.object_worm_configuration = object_worm_configuration
