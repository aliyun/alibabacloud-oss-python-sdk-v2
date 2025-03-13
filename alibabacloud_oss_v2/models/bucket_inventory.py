from typing import Optional, List, Any, Union
from enum import Enum
from .. import serde


class InventoryFormatType(str, Enum):
    """
    The format of the exported inventory list
    """

    CSV = 'CSV'


class InventoryFrequencyType(str, Enum):
    """
    The frequency that inventory lists are exported
    """

    DAILY = 'Daily'
    WEEKLY = 'Weekly'


class InventoryOptionalFieldType(str, Enum):
    """
    InventoryOptionalFieldType The configuration fields that are included in inventory lists.
    """

    SIZE = 'Size'
    LAST_MODIFIED_DATE = 'LastModifiedDate'
    E_TAG = 'ETag'
    STORAGE_CLASS = 'StorageClass'
    IS_MULTIPART_UPLOADED = 'IsMultipartUploaded'
    ENCRYPTION_STATUS = 'EncryptionStatus'
    TRANSITION_TIME = 'TransitionTime'


class SSEKMS(serde.Model):
    """
    The container that stores the customer master key (CMK) used for SSE-KMS encryption.
    """

    _attribute_map = { 
        'key_id': {'tag': 'xml', 'rename': 'KeyId', 'type': 'str'},
    }

    _xml_map = {
        'name': 'SSEKMS'
    }

    def __init__(
        self,
        key_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            key_id (str, optional): The ID of the key that is managed by Key Management Service (KMS).
        """
        super().__init__(**kwargs)
        self.key_id = key_id


class InventorySchedule(serde.Model):
    """
    Contains the frequency that inventory lists are exported
    """

    _attribute_map = { 
        'frequency': {'tag': 'xml', 'rename': 'Frequency', 'type': 'str'},
    }

    _xml_map = {
        'name': 'Schedule'
    }


    def __init__(
        self,
        frequency: Optional[Union[str, InventoryFrequencyType]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            frequency (str | InventoryFrequencyType, optional): The frequency at which the inventory list is exported. Valid values:- Daily: The inventory list is exported on a daily basis. - Weekly: The inventory list is exported on a weekly basis.
        """
        super().__init__(**kwargs)
        self.frequency = frequency


class InventoryFilter(serde.Model):
    """
    The container that stores the prefix used to filter objects. Only objects whose names contain the specified prefix are included in the inventory.
    """

    _attribute_map = { 
        'lower_size_bound': {'tag': 'xml', 'rename': 'LowerSizeBound', 'type': 'int'},
        'upper_size_bound': {'tag': 'xml', 'rename': 'UpperSizeBound', 'type': 'int'},
        'storage_class': {'tag': 'xml', 'rename': 'StorageClass', 'type': 'str'},
        'prefix': {'tag': 'xml', 'rename': 'Prefix', 'type': 'str'},
        'last_modify_begin_time_stamp': {'tag': 'xml', 'rename': 'LastModifyBeginTimeStamp', 'type': 'int'},
        'last_modify_end_time_stamp': {'tag': 'xml', 'rename': 'LastModifyEndTimeStamp', 'type': 'int'},
    }

    _xml_map = {
        'name': 'Filter'
    }


    def __init__(
        self,
        lower_size_bound: Optional[int] = None,
        upper_size_bound: Optional[int] = None,
        storage_class: Optional[str] = None,
        prefix: Optional[str] = None,
        last_modify_begin_time_stamp: Optional[int] = None,
        last_modify_end_time_stamp: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            lower_size_bound (int, optional): The minimum size of the specified object. Unit: B.Valid values: [0 B, 48.8 TB]
            upper_size_bound (int, optional): The maximum size of the specified object. Unit: B.Valid values: (0 B, 48.8 TB]
            storage_class (str, optional): The storage class of the object. You can specify multiple storage classes.Valid values:StandardIAArchiveColdArchiveAll
            prefix (str, optional): The prefix that is specified in the inventory.
            last_modify_begin_time_stamp (int, optional): The beginning of the time range during which the object was last modified. Unit: seconds.Valid values: [1262275200, 253402271999]
            last_modify_end_time_stamp (int, optional): The end of the time range during which the object was last modified. Unit: seconds.Valid values: [1262275200, 253402271999]
        """
        super().__init__(**kwargs)
        self.lower_size_bound = lower_size_bound
        self.upper_size_bound = upper_size_bound
        self.storage_class = storage_class
        self.prefix = prefix
        self.last_modify_begin_time_stamp = last_modify_begin_time_stamp
        self.last_modify_end_time_stamp = last_modify_end_time_stamp


class OptionalFields(serde.Model):
    """
    The container that stores the configuration fields in inventory lists.
    """

    _attribute_map = { 
        'fields': {'tag': 'xml', 'rename': 'Field', 'type': '[str]'},
    }

    _xml_map = {
        'name': 'OptionalFields'
    }


    def __init__(
        self,
        fields: Optional[List[Union[str, InventoryOptionalFieldType]]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            fields (List[Union[str, InventoryOptionalFieldType]], optional): The configuration fields that are included in inventory lists. Available configuration fields:*   Size: the size of the object.*   LastModifiedDate: the time when the object was last modified.*   ETag: the ETag of the object. It is used to identify the content of the object.*   StorageClass: the storage class of the object.*   IsMultipartUploaded: specifies whether the object is uploaded by using multipart upload.*   EncryptionStatus: the encryption status of the object.
        """
        super().__init__(**kwargs)
        self.fields = fields


class InventoryEncryption(serde.Model):
    """
    The container that stores the encryption method of exported inventory lists.
    """

    _attribute_map = { 
        'sse_kms': {'tag': 'xml', 'rename': 'SSE-KMS', 'type': 'SSEKMS'},
        'sse_oss': {'tag': 'xml', 'rename': 'SSE-OSS', 'type': 'str'},
    }

    _xml_map = {
        'name': 'Encryption'
    }

    _dependency_map = { 
        'SSEKMS': {'new': lambda: SSEKMS()},
    }

    def __init__(
        self,
        sse_kms: Optional[SSEKMS] = None,
        sse_oss: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            sse_kms (SSEKMS, optional): The container that stores the customer master key (CMK) used for SSE-KMS encryption.
            sse_oss (str, optional): The container that stores information about the SSE-OSS encryption method.
        """
        super().__init__(**kwargs)
        self.sse_kms = sse_kms
        self.sse_oss = sse_oss

class InventoryOSSBucketDestination(serde.Model):
    """
    The container that stores information about the bucket in which exported inventory lists are stored.
    """

    _attribute_map = {
        'format': {'tag': 'xml', 'rename': 'Format', 'type': 'str'},
        'account_id': {'tag': 'xml', 'rename': 'AccountId', 'type': 'str'},
        'role_arn': {'tag': 'xml', 'rename': 'RoleArn', 'type': 'str'},
        'bucket': {'tag': 'xml', 'rename': 'Bucket', 'type': 'str'},
        'prefix': {'tag': 'xml', 'rename': 'Prefix', 'type': 'str'},
        'encryption': {'tag': 'xml', 'rename': 'Encryption', 'type': 'InventoryEncryption'},
    }

    _xml_map = {
        'name': 'OSSBucketDestination'
    }

    _dependency_map = {
        'InventoryEncryption': {'new': lambda: InventoryEncryption()},
    }

    def __init__(
        self,
        format: Optional[Union[str, InventoryFormatType]] = None,
        account_id: Optional[str] = None,
        role_arn: Optional[str] = None,
        bucket: Optional[str] = None,
        prefix: Optional[str] = None,
        encryption: Optional[InventoryEncryption] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            format (str | InventoryFormatType, optional): The format of exported inventory lists. The exported inventory lists are CSV objects compressed by using GZIP.
            account_id (str, optional): The ID of the account to which permissions are granted by the bucket owner.
            role_arn (str, optional): The Alibaba Cloud Resource Name (ARN) of the role that has the permissions to read all objects from the source bucket and write objects to the destination bucket. Format: `acs:ram::uid:role/rolename`.
            bucket (str, optional): The name of the bucket in which exported inventory lists are stored.
            prefix (str, optional): The prefix of the path in which the exported inventory lists are stored.
            encryption (InventoryEncryption, optional): The container that stores the encryption method of the exported inventory lists.
        """
        super().__init__(**kwargs)
        self.format = format
        self.account_id = account_id
        self.role_arn = role_arn
        self.bucket = bucket
        self.prefix = prefix
        self.encryption = encryption



class InventoryDestination(serde.Model):
    """
    The container that stores information about exported inventory lists.
    """

    _attribute_map = { 
        'oss_bucket_destination': {'tag': 'xml', 'rename': 'OSSBucketDestination', 'type': 'InventoryOSSBucketDestination'},
    }

    _xml_map = {
        'name': 'Destination'
    }

    _dependency_map = { 
        'InventoryOSSBucketDestination': {'new': lambda: InventoryOSSBucketDestination()},
    }

    def __init__(
        self,
        oss_bucket_destination: Optional[InventoryOSSBucketDestination] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            oss_bucket_destination (InventoryOSSBucketDestination, optional): The container that stores information about the bucket in which exported inventory lists are stored.
        """
        super().__init__(**kwargs)
        self.oss_bucket_destination = oss_bucket_destination


class InventoryConfiguration(serde.Model):
    """
    The container that stores the configurations of the inventory.
    """

    _attribute_map = { 
        'included_object_versions': {'tag': 'xml', 'rename': 'IncludedObjectVersions', 'type': 'str'},
        'optional_fields': {'tag': 'xml', 'rename': 'OptionalFields', 'type': 'OptionalFields'},
        'id': {'tag': 'xml', 'rename': 'Id', 'type': 'str'},
        'is_enabled': {'tag': 'xml', 'rename': 'IsEnabled', 'type': 'bool'},
        'destination': {'tag': 'xml', 'rename': 'Destination', 'type': 'InventoryDestination'},
        'schedule': {'tag': 'xml', 'rename': 'Schedule', 'type': 'InventorySchedule'},
        'filter': {'tag': 'xml', 'rename': 'Filter', 'type': 'InventoryFilter'},
    }

    _xml_map = {
        'name': 'InventoryConfiguration'
    }

    _dependency_map = { 
        'OptionalFields': {'new': lambda: OptionalFields()},
        'InventoryDestination': {'new': lambda: InventoryDestination()},
        'InventorySchedule': {'new': lambda: InventorySchedule()},
        'InventoryFilter': {'new': lambda: InventoryFilter()},
    }

    def __init__(
        self,
        included_object_versions: Optional[str] = None,
        optional_fields: Optional[OptionalFields] = None,
        id: Optional[str] = None,
        is_enabled: Optional[bool] = None,
        destination: Optional[InventoryDestination] = None,
        schedule: Optional[InventorySchedule] = None,
        filter: Optional[InventoryFilter] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            included_object_versions (str, optional): Specifies whether to include the version information about the objects in inventory lists. Valid values:*   All: The information about all versions of the objects is exported.*   Current: Only the information about the current versions of the objects is exported.
            optional_fields (OptionalFields, optional): The container that stores the configuration fields in inventory lists.
            id (str, optional): The name of the inventory. The name must be unique in the bucket.
            is_enabled (bool, optional): Specifies whether to enable the bucket inventory feature. Valid values:*   true*   false
            destination (InventoryDestination, optional): The container that stores the exported inventory lists.
            schedule (InventorySchedule, optional): The container that stores information about the frequency at which inventory lists are exported.
            filter (InventoryFilter, optional): The container that stores the prefix used to filter objects. Only objects whose names contain the specified prefix are included in the inventory.
        """
        super().__init__(**kwargs)
        self.included_object_versions = included_object_versions
        self.optional_fields = optional_fields
        self.id = id
        self.is_enabled = is_enabled
        self.destination = destination
        self.schedule = schedule
        self.filter = filter


class ListInventoryConfigurationsResult(serde.Model):
    """
    The container that stores inventory configuration list.
    """

    _attribute_map = { 
        'inventory_configurations': {'tag': 'xml', 'rename': 'InventoryConfiguration', 'type': '[InventoryConfiguration]'},
        'is_truncated': {'tag': 'xml', 'rename': 'IsTruncated', 'type': 'bool'},
        'next_continuation_token': {'tag': 'xml', 'rename': 'NextContinuationToken', 'type': 'str'},
    }

    _xml_map = {
        'name': 'ListInventoryConfigurationsResult'
    }

    _dependency_map = { 
        'InventoryConfiguration': {'new': lambda: InventoryConfiguration()},
    }

    def __init__(
        self,
        inventory_configurations: Optional[List[InventoryConfiguration]] = None,
        is_truncated: Optional[bool] = None,
        next_continuation_token: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            inventory_configurations (List[InventoryConfiguration], optional): The container that stores inventory configurations.
            is_truncated (bool, optional): Specifies whether to list all inventory tasks configured for the bucket.Valid values: true and false- The value of false indicates that all inventory tasks configured for the bucket are listed.- The value of true indicates that not all inventory tasks configured for the bucket are listed. To list the next page of inventory configurations, set the continuation-token parameter in the next request to the value of the NextContinuationToken header in the response to the current request.
            next_continuation_token (str, optional): If the value of IsTruncated in the response is true and value of this header is not null, set the continuation-token parameter in the next request to the value of this header.
        """
        super().__init__(**kwargs)
        self.inventory_configurations = inventory_configurations
        self.is_truncated = is_truncated
        self.next_continuation_token = next_continuation_token





class PutBucketInventoryRequest(serde.RequestModel):
    """
    The request for the PutBucketInventory operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'inventory_id': {'tag': 'input', 'position': 'query', 'rename': 'inventoryId', 'type': 'str', 'required': True},
        'inventory_configuration': {'tag': 'input', 'position': 'body', 'rename': 'InventoryConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        inventory_id: str = None,
        inventory_configuration: Optional[InventoryConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            inventory_id (str, required): The name of the inventory.
            inventory_configuration (InventoryConfiguration, optional): Request body schema.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.inventory_id = inventory_id
        self.inventory_configuration = inventory_configuration


class PutBucketInventoryResult(serde.ResultModel):
    """
    The request for the PutBucketInventory operation.
    """

class GetBucketInventoryRequest(serde.RequestModel):
    """
    The request for the GetBucketInventory operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'inventory_id': {'tag': 'input', 'position': 'query', 'rename': 'inventoryId', 'type': 'str', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        inventory_id: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            inventory_id (str, required): The name of the inventory to be queried.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.inventory_id = inventory_id


class GetBucketInventoryResult(serde.ResultModel):
    """
    The request for the GetBucketInventory operation.
    """

    _attribute_map = { 
        'inventory_configuration': {'tag': 'output', 'position': 'body', 'rename': 'InventoryConfiguration', 'type': 'InventoryConfiguration,xml'},
    }

    _dependency_map = { 
        'InventoryConfiguration': {'new': lambda: InventoryConfiguration()},
    }

    def __init__(
        self,
        inventory_configuration: Optional[InventoryConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            inventory_configuration (InventoryConfiguration, optional): The inventory task configured for a bucket.
        """
        super().__init__(**kwargs)
        self.inventory_configuration = inventory_configuration

class ListBucketInventoryRequest(serde.RequestModel):
    """
    The request for the ListBucketInventory operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'continuation_token': {'tag': 'input', 'position': 'query', 'rename': 'continuation-token', 'type': 'str'},
    }

    def __init__(
        self,
        bucket: str = None,
        continuation_token: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            continuation_token (str, optional): Specify the start position of the list operation. You can obtain this token from the NextContinuationToken field of last ListBucketInventory's result.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.continuation_token = continuation_token


class ListBucketInventoryResult(serde.ResultModel):
    """
    The request for the ListBucketInventory operation.
    """

    _attribute_map = { 
        'list_inventory_configurations_result': {'tag': 'output', 'position': 'body', 'rename': 'ListInventoryConfigurationsResult', 'type': 'ListInventoryConfigurationsResult,xml'},
    }

    _dependency_map = { 
        'ListInventoryConfigurationsResult': {'new': lambda: ListInventoryConfigurationsResult()},
    }

    def __init__(
        self,
        list_inventory_configurations_result: Optional[ListInventoryConfigurationsResult] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            list_inventory_configurations_result (ListInventoryConfigurationsResult, optional): The container that stores inventory configuration list.
        """
        super().__init__(**kwargs)
        self.list_inventory_configurations_result = list_inventory_configurations_result

class DeleteBucketInventoryRequest(serde.RequestModel):
    """
    The request for the DeleteBucketInventory operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'inventory_id': {'tag': 'input', 'position': 'query', 'rename': 'inventoryId', 'type': 'str', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        inventory_id: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            inventory_id (str, required): The name of the inventory that you want to delete.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.inventory_id = inventory_id


class DeleteBucketInventoryResult(serde.ResultModel):
    """
    The request for the DeleteBucketInventory operation.
    """
