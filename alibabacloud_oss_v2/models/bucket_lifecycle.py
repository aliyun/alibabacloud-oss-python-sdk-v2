import datetime
from typing import Optional, List, Any, Union
from .. import serde
from .enums import StorageClassType
from .structs import Tag


class LifecycleRuleTransition(serde.Model):
    """
    The conversion of the storage class of objects that match the lifecycle rule when the objects expire. The storage class of the objects can be converted to IA, Archive, and ColdArchive. The storage class of Standard objects in a Standard bucket can be converted to IA, Archive, or Cold Archive. The period of time from when the objects expire to when the storage class of the objects is converted to Archive must be longer than the period of time from when the objects expire to when the storage class of the objects is converted to IA. For example, if the validity period is set to 30 for objects whose storage class is converted to IA after the validity period, the validity period must be set to a value greater than 30 for objects whose storage class is converted to Archive.  Either Days or CreatedBeforeDate is required.
    """

    _attribute_map = { 
        'created_before_date': {'tag': 'xml', 'rename': 'CreatedBeforeDate', 'type': 'datetime,ios8601date'},
        'days': {'tag': 'xml', 'rename': 'Days', 'type': 'int'},
        'storage_class': {'tag': 'xml', 'rename': 'StorageClass', 'type': 'str'},
        'is_access_time': {'tag': 'xml', 'rename': 'IsAccessTime', 'type': 'bool'},
        'return_to_std_when_visit': {'tag': 'xml', 'rename': 'ReturnToStdWhenVisit', 'type': 'bool'},
        'allow_small_file': {'tag': 'xml', 'rename': 'AllowSmallFile', 'type': 'bool'},
    }

    _xml_map = {
        'name': 'Transition'
    }

    def __init__(
        self,
        created_before_date: Optional[datetime.datetime] = None,
        days: Optional[int] = None,
        storage_class: Optional[Union[str, StorageClassType]] = None,
        is_access_time: Optional[bool] = None,
        return_to_std_when_visit: Optional[bool] = None,
        allow_small_file: Optional[bool] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            created_before_date (datetime.datetime, optional): The date based on which the lifecycle rule takes effect. OSS performs the specified operation on data whose last modified date is earlier than this date. Specify the time in the ISO 8601 standard. The time must be at 00:00:00 in UTC.
            days (int, optional): The number of days from when the objects were last modified to when the lifecycle rule takes effect.
            storage_class (str | StorageClassType, optional): The storage class to which objects are converted. Valid values:*   IA*   Archive*   ColdArchive  You can convert the storage class of objects in an IA bucket to only Archive or Cold Archive.
            is_access_time (bool, optional): Specifies whether the lifecycle rule applies to objects based on their last access time. Valid values:*   true: The rule applies to objects based on their last access time.*   false: The rule applies to objects based on their last modified time.
            return_to_std_when_visit (bool, optional): Specifies whether to convert the storage class of non-Standard objects back to Standard after the objects are accessed. This parameter takes effect only when the IsAccessTime parameter is set to true. Valid values:*   true: converts the storage class of the objects to Standard.*   false: does not convert the storage class of the objects to Standard.
            allow_small_file (bool, optional): Specifies whether to convert the storage class of objects whose sizes are less than 64 KB to IA, Archive, or Cold Archive based on their last access time. Valid values:*   true: converts the storage class of objects that are smaller than 64 KB to IA, Archive, or Cold Archive. Objects that are smaller than 64 KB are charged as 64 KB. Objects that are greater than or equal to 64 KB are charged based on their actual sizes. If you set this parameter to true, the storage fees may increase.*   false: does not convert the storage class of an object that is smaller than 64 KB.
        """
        super().__init__(**kwargs)
        self.created_before_date = created_before_date
        self.days = days
        self.storage_class = storage_class
        self.is_access_time = is_access_time
        self.return_to_std_when_visit = return_to_std_when_visit
        self.allow_small_file = allow_small_file



class NoncurrentVersionExpiration(serde.Model):
    """
    The delete operation that you want OSS to perform on the previous versions of the objects that match the lifecycle rule when the previous versions expire.
    """

    _attribute_map = { 
        'noncurrent_days': {'tag': 'xml', 'rename': 'NoncurrentDays', 'type': 'int'},
    }

    _xml_map = {
        'name': 'NoncurrentVersionExpiration'
    }

    def __init__(
        self,
        noncurrent_days: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            noncurrent_days (int, optional): The number of days from when the objects became previous versions to when the lifecycle rule takes effect.
        """
        super().__init__(**kwargs)
        self.noncurrent_days = noncurrent_days


class LifecycleRuleAbortMultipartUpload(serde.Model):
    """
    The delete operation that you want OSS to perform on the parts that are uploaded in incomplete multipart upload tasks when the parts expire.
    """

    _attribute_map = { 
        'days': {'tag': 'xml', 'rename': 'Days', 'type': 'int'},
        'created_before_date': {'tag': 'xml', 'rename': 'CreatedBeforeDate', 'type': 'datetime.datetime'},
    }

    _xml_map = {
        'name': 'AbortMultipartUpload'
    }

    def __init__(
        self,
        days: Optional[int] = None,
        created_before_date: Optional[datetime.datetime] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            days (int, optional): The number of days from when the objects were last modified to when the lifecycle rule takes effect.
            created_before_date (datetime.datetime, optional): The date based on which the lifecycle rule takes effect. OSS performs the specified operation on data whose last modified date is earlier than this date. Specify the time in the ISO 8601 standard. The time must be at 00:00:00 in UTC.
        """
        super().__init__(**kwargs)
        self.days = days
        self.created_before_date = created_before_date


class LifecycleRuleExpiration(serde.Model):
    """
    The delete operation to perform on objects based on the lifecycle rule. For an object in a versioning-enabled bucket, the delete operation specified by this parameter is performed only on the current version of the object.The period of time from when the objects expire to when the objects are deleted must be longer than the period of time from when the objects expire to when the storage class of the objects is converted to IA or Archive.
    """

    _attribute_map = { 
        'created_before_date': {'tag': 'xml', 'rename': 'CreatedBeforeDate', 'type': 'datetime.datetime'},
        'days': {'tag': 'xml', 'rename': 'Days', 'type': 'int'},
        'expired_object_delete_marker': {'tag': 'xml', 'rename': 'ExpiredObjectDeleteMarker', 'type': 'bool'},
    }

    _xml_map = {
        'name': 'Expiration'
    }

    def __init__(
        self,
        created_before_date: Optional[datetime.datetime] = None,
        days: Optional[int] = None,
        expired_object_delete_marker: Optional[bool] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            created_before_date (datetime.datetime, optional): The date based on which the lifecycle rule takes effect. OSS performs the specified operation on data whose last modified date is earlier than this date. The value of this parameter is in the yyyy-MM-ddT00:00:00.000Z format.Specify the time in the ISO 8601 standard. The time must be at 00:00:00 in UTC.
            days (int, optional): The number of days from when the objects were last modified to when the lifecycle rule takes effect.
            expired_object_delete_marker (bool, optional): Specifies whether to automatically remove expired delete markers.*   true: Expired delete markers are automatically removed. If you set this parameter to true, you cannot specify the Days or CreatedBeforeDate parameter.*   false: Expired delete markers are not automatically removed. If you set this parameter to false, you must specify the Days or CreatedBeforeDate parameter.
        """
        super().__init__(**kwargs)
        self.created_before_date = created_before_date
        self.days = days
        self.expired_object_delete_marker = expired_object_delete_marker


class NoncurrentVersionTransition(serde.Model):
    """
    The conversion of the storage class of previous versions of the objects that match the lifecycle rule when the previous versions expire. The storage class of the previous versions can be converted to IA or Archive. The period of time from when the previous versions expire to when the storage class of the previous versions is converted to Archive must be longer than the period of time from when the previous versions expire to when the storage class of the previous versions is converted to IA.
    """

    _attribute_map = { 
        'is_access_time': {'tag': 'xml', 'rename': 'IsAccessTime', 'type': 'bool'},
        'return_to_std_when_visit': {'tag': 'xml', 'rename': 'ReturnToStdWhenVisit', 'type': 'bool'},
        'allow_small_file': {'tag': 'xml', 'rename': 'AllowSmallFile', 'type': 'bool'},
        'noncurrent_days': {'tag': 'xml', 'rename': 'NoncurrentDays', 'type': 'int'},
        'storage_class': {'tag': 'xml', 'rename': 'StorageClass', 'type': 'str'},
    }

    _xml_map = {
        'name': 'NoncurrentVersionTransition'
    }

    def __init__(
        self,
        is_access_time: Optional[bool] = None,
        return_to_std_when_visit: Optional[bool] = None,
        allow_small_file: Optional[bool] = None,
        noncurrent_days: Optional[int] = None,
        storage_class: Optional[Union[str, StorageClassType]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            is_access_time (bool, optional): Specifies whether the lifecycle rule applies to objects based on their last access time. Valid values:*   true: The rule applies to objects based on their last access time.*   false: The rule applies to objects based on their last modified time.
            return_to_std_when_visit (bool, optional): Specifies whether to convert the storage class of non-Standard objects back to Standard after the objects are accessed. This parameter takes effect only when the IsAccessTime parameter is set to true. Valid values:*   true: converts the storage class of the objects to Standard.*   false: does not convert the storage class of the objects to Standard.
            allow_small_file (bool, optional): Specifies whether to convert the storage class of objects whose sizes are less than 64 KB to IA, Archive, or Cold Archive based on their last access time. Valid values:*   true: converts the storage class of objects that are smaller than 64 KB to IA, Archive, or Cold Archive. Objects that are smaller than 64 KB are charged as 64 KB. Objects that are greater than or equal to 64 KB are charged based on their actual sizes. If you set this parameter to true, the storage fees may increase.*   false: does not convert the storage class of an object that is smaller than 64 KB.
            noncurrent_days (int, optional): The number of days from when the objects became previous versions to when the lifecycle rule takes effect.
            storage_class (str | StorageClassType, optional): The storage class to which objects are converted. Valid values:*   IA*   Archive*   ColdArchive  You can convert the storage class of objects in an IA bucket to only Archive or Cold Archive.
        """
        super().__init__(**kwargs)
        self.is_access_time = is_access_time
        self.return_to_std_when_visit = return_to_std_when_visit
        self.allow_small_file = allow_small_file
        self.noncurrent_days = noncurrent_days
        self.storage_class = storage_class

class LifecycleRuleNot(serde.Model):
    """
    The condition that is matched by objects to which the lifecycle rule does not apply.
    """

    _attribute_map = {
        'prefix': {'tag': 'xml', 'rename': 'Prefix', 'type': 'str'},
        'tag': {'tag': 'xml', 'rename': 'Tag', 'type': 'Tag'},
    }

    _xml_map = {
        'name': 'Not'
    }

    _dependency_map = {
        'Tag': {'new': lambda: Tag()},
    }

    def __init__(
        self,
        prefix: Optional[str] = None,
        tag: Optional[Tag] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            prefix (str, optional): The prefix in the names of the objects to which the lifecycle rule does not apply.
            tag (Tag, optional): The tag of the objects to which the lifecycle rule does not apply.
        """
        super().__init__(**kwargs)
        self.prefix = prefix
        self.tag = tag


class LifecycleRuleFilter(serde.Model):
    """
    The container that stores the Not parameter that is used to filter objects.
    """

    _attribute_map = {
        'object_size_greater_than': {'tag': 'xml', 'rename': 'ObjectSizeGreaterThan', 'type': 'int'},
        'object_size_less_than': {'tag': 'xml', 'rename': 'ObjectSizeLessThan', 'type': 'int'},
        'nots': {'tag': 'xml', 'rename': 'Not', 'type': '[LifecycleRuleNot]'},
    }

    _xml_map = {
        'name': 'Filter'
    }

    _dependency_map = {
        'Not': {'new': lambda: LifecycleRuleNot()},
    }

    @property
    def filter_not(self) -> Optional[List[LifecycleRuleNot]]:
        return self.nots

    def __init__(
        self,
        object_size_greater_than: Optional[int] = None,
        object_size_less_than: Optional[int] = None,
        filter_not: Optional[List[LifecycleRuleNot]] = None,
        nots: Optional[List[LifecycleRuleNot]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            object_size_greater_than (int, optional): This lifecycle rule only applies to files larger than this size.
            object_size_less_than (int, optional): This lifecycle rule only applies to files smaller than this size.
            filter_not (List[LifecycleRuleNot], optional): The condition that is matched by objects to which the lifecycle rule does not apply.
            nots (List[LifecycleRuleNot], optional): The condition that is matched by objects to which the lifecycle rule does not apply.
                The nots parameter has the same functionality as the filter_not parameter. it is the standardized name for filter_not.
                If both exist simultaneously, the value of nots will take precedence.
        """
        super().__init__(**kwargs)
        self.object_size_greater_than = object_size_greater_than
        self.object_size_less_than = object_size_less_than
        self.nots = nots if nots is not None else filter_not


class LifecycleRule(serde.Model):
    """
    The container that stores lifecycle rules.*   A lifecycle rule cannot be configured to convert the storage class of objects in an Archive bucket.*   The period of time from when the objects expire to when the objects are deleted must be longer than the period of time from when the objects expire to when the storage class of the objects is converted to IA or Archive.
    """

    _attribute_map = { 
        'tags': {'tag': 'xml', 'rename': 'Tag', 'type': '[Tag]'},
        'noncurrent_version_expiration': {'tag': 'xml', 'rename': 'NoncurrentVersionExpiration', 'type': 'NoncurrentVersionExpiration'},
        'filter': {'tag': 'xml', 'rename': 'Filter', 'type': 'LifecycleRuleFilter'},
        'id': {'tag': 'xml', 'rename': 'ID', 'type': 'str'},
        'expiration': {'tag': 'xml', 'rename': 'Expiration', 'type': 'LifecycleRuleExpiration'},
        'transitions': {'tag': 'xml', 'rename': 'Transition', 'type': '[LifecycleRuleTransition]'},
        'noncurrent_version_transitions': {'tag': 'xml', 'rename': 'NoncurrentVersionTransition', 'type': '[NoncurrentVersionTransition]'},
        'atime_base': {'tag': 'xml', 'rename': 'AtimeBase', 'type': 'int'},
        'prefix': {'tag': 'xml', 'rename': 'Prefix', 'type': 'str'},
        'status': {'tag': 'xml', 'rename': 'Status', 'type': 'str'},
        'abort_multipart_upload': {'tag': 'xml', 'rename': 'AbortMultipartUpload', 'type': 'LifecycleRuleAbortMultipartUpload'},
    }

    _xml_map = {
        'name': 'Rule'
    }

    _dependency_map = { 
        'Tag': {'new': lambda: Tag()},
        'NoncurrentVersionExpiration': {'new': lambda: NoncurrentVersionExpiration()},
        'Filter': {'new': lambda: LifecycleRuleFilter()},
        'Expiration': {'new': lambda: LifecycleRuleExpiration()},
        'Transition': {'new': lambda: LifecycleRuleTransition()},
        'NoncurrentVersionTransition': {'new': lambda: NoncurrentVersionTransition()},
        'AbortMultipartUpload': {'new': lambda: LifecycleRuleAbortMultipartUpload()},
    }

    def __init__(
        self,
        tags: Optional[List[Tag]] = None,
        noncurrent_version_expiration: Optional[NoncurrentVersionExpiration] = None,
        filter: Optional[LifecycleRuleFilter] = None,
        id: Optional[str] = None,
        expiration: Optional[LifecycleRuleExpiration] = None,
        transitions: Optional[List[LifecycleRuleTransition]] = None,
        noncurrent_version_transitions: Optional[List[NoncurrentVersionTransition]] = None,
        atime_base: Optional[int] = None,
        prefix: Optional[str] = None,
        status: Optional[str] = None,
        abort_multipart_upload: Optional[LifecycleRuleAbortMultipartUpload] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            tags (List[Tag], optional): The tag of the objects to which the lifecycle rule applies. You can specify multiple tags.
            noncurrent_version_expiration (NoncurrentVersionExpiration, optional): The delete operation that you want OSS to perform on the previous versions of the objects that match the lifecycle rule when the previous versions expire.
            filter (LifecycleRuleFilter, optional): The container that stores the Not parameter that is used to filter objects.
            id (str, optional): The ID of the lifecycle rule. The ID can contain up to 255 characters. If you do not specify the ID, OSS automatically generates a unique ID for the lifecycle rule.
            expiration (LifecycleRuleExpiration, optional): The delete operation to perform on objects based on the lifecycle rule. For an object in a versioning-enabled bucket, the delete operation specified by this parameter is performed only on the current version of the object.The period of time from when the objects expire to when the objects are deleted must be longer than the period of time from when the objects expire to when the storage class of the objects is converted to IA or Archive.
            transitions (List[LifecycleRuleTransition], optional): The conversion of the storage class of objects that match the lifecycle rule when the objects expire. The storage class of the objects can be converted to IA, Archive, and ColdArchive. The storage class of Standard objects in a Standard bucket can be converted to IA, Archive, or Cold Archive. The period of time from when the objects expire to when the storage class of the objects is converted to Archive must be longer than the period of time from when the objects expire to when the storage class of the objects is converted to IA. For example, if the validity period is set to 30 for objects whose storage class is converted to IA after the validity period, the validity period must be set to a value greater than 30 for objects whose storage class is converted to Archive.  Either Days or CreatedBeforeDate is required.
            noncurrent_version_transitions (List[NoncurrentVersionTransition], optional): The conversion of the storage class of previous versions of the objects that match the lifecycle rule when the previous versions expire. The storage class of the previous versions can be converted to IA or Archive. The period of time from when the previous versions expire to when the storage class of the previous versions is converted to Archive must be longer than the period of time from when the previous versions expire to when the storage class of the previous versions is converted to IA.
            atime_base (int, optional): Timestamp for when access tracking was enabled.
            prefix (str, optional): The prefix in the names of the objects to which the rule applies. The prefixes specified by different rules cannot overlap.*   If Prefix is specified, this rule applies only to objects whose names contain the specified prefix in the bucket.*   If Prefix is not specified, this rule applies to all objects in the bucket.
            status (str, optional): Specifies whether to enable the rule. Valid values:*   Enabled: enables the rule. OSS periodically executes the rule.*   Disabled: does not enable the rule. OSS ignores the rule.
            abort_multipart_upload (LifecycleRuleAbortMultipartUpload, optional): The delete operation that you want OSS to perform on the parts that are uploaded in incomplete multipart upload tasks when the parts expire.
        """
        super().__init__(**kwargs)
        self.tags = tags
        self.noncurrent_version_expiration = noncurrent_version_expiration
        self.filter = filter
        self.id = id
        self.expiration = expiration
        self.transitions = transitions
        self.noncurrent_version_transitions = noncurrent_version_transitions
        self.atime_base = atime_base
        self.prefix = prefix
        self.status = status
        self.abort_multipart_upload = abort_multipart_upload


class LifecycleConfiguration(serde.Model):
    """
    The container that stores the lifecycle rules configured for the bucket.
    """

    _attribute_map = { 
        'rules': {'tag': 'xml', 'rename': 'Rule', 'type': '[LifecycleRule]'},
    }

    _xml_map = {
        'name': 'LifecycleConfiguration'
    }

    _dependency_map = { 
        'LifecycleRule': {'new': lambda: LifecycleRule()},
    }

    def __init__(
        self,
        rules: Optional[List[LifecycleRule]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            rules (List[LifecycleRule], optional): The container that stores the lifecycle rules.
        """
        super().__init__(**kwargs)
        self.rules = rules


class PutBucketLifecycleRequest(serde.RequestModel):
    """
    The request for the PutBucketLifecycle operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'allow_same_action_overlap': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-allow-same-action-overlap', 'type': 'str'},
        'lifecycle_configuration': {'tag': 'input', 'position': 'body', 'rename': 'LifecycleConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        allow_same_action_overlap: Optional[str] = None,
        lifecycle_configuration: Optional[LifecycleConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            allow_same_action_overlap (str, optional): Specifies whether to allow overlapped prefixes. Valid values:true: Overlapped prefixes are allowed.false: Overlapped prefixes are not allowed.
            lifecycle_configuration (LifecycleConfiguration, optional): The container of the request body.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.allow_same_action_overlap = allow_same_action_overlap
        self.lifecycle_configuration = lifecycle_configuration


class PutBucketLifecycleResult(serde.ResultModel):
    """
    The request for the PutBucketLifecycle operation.
    """

class GetBucketLifecycleRequest(serde.RequestModel):
    """
    The request for the GetBucketLifecycle operation.
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


class GetBucketLifecycleResult(serde.ResultModel):
    """
    The request for the GetBucketLifecycle operation.
    """

    _attribute_map = { 
        'lifecycle_configuration': {'tag': 'output', 'position': 'body', 'rename': 'LifecycleConfiguration', 'type': 'LifecycleConfiguration,xml'},
    }

    _dependency_map = { 
        'LifecycleConfiguration': {'new': lambda: LifecycleConfiguration()},
    }

    def __init__(
        self,
        lifecycle_configuration: Optional[LifecycleConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            lifecycle_configuration (LifecycleConfiguration, optional): The container that stores the lifecycle rules configured for the bucket.
        """
        super().__init__(**kwargs)
        self.lifecycle_configuration = lifecycle_configuration

class DeleteBucketLifecycleRequest(serde.RequestModel):
    """
    The request for the DeleteBucketLifecycle operation.
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


class DeleteBucketLifecycleResult(serde.ResultModel):
    """
    The request for the DeleteBucketLifecycle operation.
    """
