import datetime
from typing import Optional, List, Any, Union
from enum import Enum
from .. import serde


class TransferType(str, Enum):
    """
    The link used to transfer data in CRR
    """

    INTERNAL = 'internal'
    OSS_ACC = 'oss_acc'


class StatusType(str, Enum):
    """
    A short description of Status
    """

    ENABLED = 'Enabled'
    DISABLED = 'Disabled'


class HistoricalObjectReplicationType(str, Enum):
    """
    Specify whether to copy historical data.
    """

    ENABLED = 'enabled'
    DISABLED = 'disabled'


class TransferTypes(serde.Model):
    """
    The container that stores the transfer type.
    """

    _attribute_map = { 
        'types': {'tag': 'xml', 'rename': 'Type', 'type': '[str]'},
    }

    _xml_map = {
        'name': 'TransferTypes'
    }

    def __init__(
        self,
        types: Optional[List[str]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            types (List[str], optional): The data transfer type that is used to transfer data in data replication. Valid values:*   internal (default): the default data transfer link used in OSS.*   oss_acc: the link in which data transmission is accelerated. You can set TransferType to oss_acc only when you create CRR rules.
        """
        super().__init__(**kwargs)
        self.types = types


class ReplicationProgressInformation(serde.Model):
    """
    The container that stores the progress of the data replication task. This parameter is returned only when the data replication task is in the doing state.
    """

    _attribute_map = { 
        'historical_object': {'tag': 'xml', 'rename': 'HistoricalObject', 'type': 'str'},
        'new_object': {'tag': 'xml', 'rename': 'NewObject', 'type': 'str'},
    }

    _xml_map = {
        'name': 'Progress'
    }

    def __init__(
        self,
        historical_object: Optional[str] = None,
        new_object: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            historical_object (str, optional): The percentage of the replicated historical data. This parameter is valid only when HistoricalObjectReplication is set to enabled.
            new_object (str, optional): The time used to determine whether data is replicated to the destination bucket. Data that is written to the source bucket before the time is replicated to the destination bucket. The value of this parameter is in the GMT format. Example: Thu, 24 Sep 2015 15:39:18 GMT.
        """
        super().__init__(**kwargs)
        self.historical_object = historical_object
        self.new_object = new_object


class ReplicationPrefixSet(serde.Model):
    """
    The container that stores prefixes. You can specify up to 10 prefixes in each data replication rule.
    """

    _attribute_map = { 
        'prefixs': {'tag': 'xml', 'rename': 'Prefix', 'type': '[str]'},
    }

    _xml_map = {
        'name': 'PrefixSet'
    }

    def __init__(
        self,
        prefixs: Optional[List[str]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            prefixs (List[str], optional): The prefix that is used to specify the object that you want to replicate. Only objects whose names contain the specified prefix are replicated to the destination bucket.*   The value of the Prefix parameter can be up to 1,023 characters in length.*   If you specify the Prefix parameter in a data replication rule, OSS synchronizes new data and historical data based on the value of the Prefix parameter.
        """
        super().__init__(**kwargs)
        self.prefixs = prefixs


class ReplicationRules(serde.Model):
    """
    The container that stores the data replication rule that you want to delete.
    """

    _attribute_map = { 
        'ids': {'tag': 'xml', 'rename': 'ID', 'type': '[str]'},
    }

    _xml_map = {
        'name': 'ReplicationRules'
    }

    def __init__(
        self,
        ids: Optional[List[str]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            ids (List[str], optional): The ID of data replication rules that you want to delete. You can call the GetBucketReplication operation to obtain the ID.
        """
        super().__init__(**kwargs)
        self.ids = ids


class LocationRTCConstraint(serde.Model):
    """
    The container that stores regions in which the RTC can be enabled.
    """

    _attribute_map = { 
        'locations': {'tag': 'xml', 'rename': 'Location', 'type': '[str]'},
    }

    _xml_map = {
        'name': 'LocationRTCConstraint'
    }

    def __init__(
        self,
        locations: Optional[List[str]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            locations (List[str], optional): The regions where RTC is supported.
        """
        super().__init__(**kwargs)
        self.locations = locations


class ReplicationDestination(serde.Model):
    """
    The container that stores the information about the destination bucket.
    """

    _attribute_map = { 
        'bucket': {'tag': 'xml', 'rename': 'Bucket', 'type': 'str'},
        'location': {'tag': 'xml', 'rename': 'Location', 'type': 'str'},
        'transfer_type': {'tag': 'xml', 'rename': 'TransferType', 'type': 'str'},
    }

    _xml_map = {
        'name': 'Destination'
    }

    def __init__(
        self,
        bucket: Optional[str] = None,
        location: Optional[str] = None,
        transfer_type: Optional[Union[str, TransferType]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The destination bucket to which data is replicated.
            location (str, optional): The region in which the destination bucket is located.
            transfer_type (str | TransferType, optional): The link that is used to transfer data during data replication. Valid values:*   internal (default): the default data transfer link used in OSS.*   oss_acc: the transfer acceleration link. You can set TransferType to oss_acc only when you create CRR rules.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.location = location
        self.transfer_type = transfer_type


class ReplicationTimeControl(serde.Model):
    """
    The container that stores information about the Replication Time Control (RTC) status.
    """

    _attribute_map = { 
        'status': {'tag': 'xml', 'rename': 'Status', 'type': 'str'},
    }

    _xml_map = {
        'name': 'RTC'
    }

    def __init__(
        self,
        status: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            status (str, optional): Specifies whether to enable RTC.Valid values:*   disabled            *   enabled
        """
        super().__init__(**kwargs)
        self.status = status


class LocationTransferType(serde.Model):
    """
    The container that stores regions in which the destination bucket can be located with the TransferType information.
    """

    _attribute_map = {
        'location': {'tag': 'xml', 'rename': 'Location', 'type': 'str'},
        'transfer_types': {'tag': 'xml', 'rename': 'TransferTypes', 'type': 'TransferTypes'},
    }

    _xml_map = {
        'name': 'LocationTransferType'
    }

    _dependency_map = {
        'TransferTypes': {'new': lambda: TransferTypes()},
    }

    def __init__(
        self,
        location: Optional[str] = None,
        transfer_types: Optional[TransferTypes] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            location (str, optional): The regions in which the destination bucket can be located.
            transfer_types (TransferTypes, optional): The container that stores the transfer type.
        """
        super().__init__(**kwargs)
        self.location = location
        self.transfer_types = transfer_types

class SseKmsEncryptedObjects(serde.Model):
    """
    The container that is used to filter the source objects that are encrypted by using SSE-KMS. This parameter must be specified if the SourceSelectionCriteria parameter is specified in the data replication rule.
    """

    _attribute_map = { 
        'status': {'tag': 'xml', 'rename': 'Status', 'type': 'str'},
    }

    _xml_map = {
        'name': 'SseKmsEncryptedObjects'
    }

    def __init__(
        self,
        status: Optional[Union[str, StatusType]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            status (str | StatusType, optional): Specifies whether to replicate objects that are encrypted by using SSE-KMS. Valid values:*   Enabled*   Disabled
        """
        super().__init__(**kwargs)
        self.status = status


class ReplicationEncryptionConfiguration(serde.Model):
    """
    
    """

    _attribute_map = { 
        'replica_kms_key_id': {'tag': 'xml', 'rename': 'ReplicaKmsKeyID', 'type': 'str'},
    }

    _xml_map = {
        'name': 'EncryptionConfiguration'
    }

    def __init__(
        self,
        replica_kms_key_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            replica_kms_key_id (str, optional):
        """
        super().__init__(**kwargs)
        self.replica_kms_key_id = replica_kms_key_id


class LocationTransferTypeConstraint(serde.Model):
    """
    The container that stores regions in which the destination bucket can be located with TransferType specified.
    """

    _attribute_map = { 
        'location_transfer_types': {'tag': 'xml', 'rename': 'LocationTransferType', 'type': '[LocationTransferType]'},
    }

    _xml_map = {
        'name': 'LocationTransferTypeConstraint'
    }

    _dependency_map = { 
        'LocationTransferType': {'new': lambda: LocationTransferType()},
    }

    def __init__(
        self,
        location_transfer_types: Optional[List[LocationTransferType]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            location_transfer_types (List[LocationTransferType], optional): The container that stores regions in which the destination bucket can be located with the TransferType information.
        """
        super().__init__(**kwargs)
        self.location_transfer_types = location_transfer_types


class RtcConfiguration(serde.Model):
    """
    The container that stores Replication Time Control (RTC) configurations.
    """

    _attribute_map = { 
        'rtc': {'tag': 'xml', 'rename': 'RTC', 'type': 'RTC'},
        'id': {'tag': 'xml', 'rename': 'ID', 'type': 'str'},
    }

    _xml_map = {
        'name': 'RtcConfiguration'
    }

    _dependency_map = { 
        'RTC': {'new': lambda: ReplicationTimeControl()},
    }

    def __init__(
        self,
        rtc: Optional[ReplicationTimeControl] = None,
        id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            rtc (RTC, optional): The container that stores the status of RTC.
            id (str, optional): The ID of the data replication rule for which you want to configure RTC.
        """
        super().__init__(**kwargs)
        self.rtc = rtc
        self.id = id


class ReplicationProgressRule(serde.Model):
    """
    Information about the progress of the data replication task.
    """

    _attribute_map = {
        'historical_object_replication': {'tag': 'xml', 'rename': 'HistoricalObjectReplication', 'type': 'str'},
        'progress': {'tag': 'xml', 'rename': 'Progress', 'type': 'Progress'},
        'id': {'tag': 'xml', 'rename': 'ID', 'type': 'str'},
        'prefix_set': {'tag': 'xml', 'rename': 'PrefixSet', 'type': 'ReplicationPrefixSet'},
        'action': {'tag': 'xml', 'rename': 'Action', 'type': 'str'},
        'destination': {'tag': 'xml', 'rename': 'Destination', 'type': 'ReplicationDestination'},
        'status': {'tag': 'xml', 'rename': 'Status', 'type': 'str'},
    }

    _xml_map = {
        'name': 'ReplicationProgressRule'
    }

    _dependency_map = {
        'Progress': {'new': lambda: ReplicationProgressInformation()},
        'PrefixSet': {'new': lambda: ReplicationPrefixSet()},
        'Destination': {'new': lambda: ReplicationDestination()},
    }

    def __init__(
        self,
        historical_object_replication: Optional[str] = None,
        progress: Optional[ReplicationProgressInformation] = None,
        id: Optional[str] = None,
        prefix_set: Optional[ReplicationPrefixSet] = None,
        action: Optional[str] = None,
        destination: Optional[ReplicationDestination] = None,
        status: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            historical_object_replication (str, optional): Specifies whether to replicate historical data that exists before data replication is enabled from the source bucket to the destination bucket.*   enabled (default): replicates historical data to the destination bucket.*   disabled: ignores historical data and replicates only data uploaded to the source bucket after data replication is enabled for the source bucket.
            progress (Progress, optional): The container that stores the progress of the data replication task. This parameter is returned only when the data replication task is in the doing state.
            id (str, optional): The ID of the data replication rule.
            prefix_set (ReplicationPrefixSet, optional): The container that stores prefixes. You can specify up to 10 prefixes in each data replication rule.
            action (str, optional): The operations that are synchronized to the destination bucket.*   ALL: PUT, DELETE, and ABORT operations are synchronized to the destination bucket.*   PUT: Write operations are synchronized to the destination bucket, including PutObject, PostObject, AppendObject, CopyObject, PutObjectACL, InitiateMultipartUpload, UploadPart, UploadPartCopy, and CompleteMultipartUpload.
            destination (ReplicationDestination, optional): The container that stores the information about the destination bucket.
            status (str, optional): The status of the data replication task. Valid values:*   starting: OSS creates a data replication task after a data replication rule is configured.*   doing: The replication rule is effective and the replication task is in progress.*   closing: OSS clears a data replication task after the corresponding data replication rule is deleted.
        """
        super().__init__(**kwargs)
        self.historical_object_replication = historical_object_replication
        self.progress = progress
        self.id = id
        self.prefix_set = prefix_set
        self.action = action
        self.destination = destination
        self.status = status


class ReplicationSourceSelectionCriteria(serde.Model):
    """
    The container that specifies other conditions used to filter the source objects that you want to replicate. Filter conditions can be specified only for source objects encrypted by using SSE-KMS.
    """

    _attribute_map = {
        'sse_kms_encrypted_objects': {'tag': 'xml', 'rename': 'SseKmsEncryptedObjects', 'type': 'SseKmsEncryptedObjects'},
    }

    _xml_map = {
        'name': 'SourceSelectionCriteria'
    }

    _dependency_map = {
        'SseKmsEncryptedObjects': {'new': lambda: SseKmsEncryptedObjects()},
    }

    def __init__(
        self,
        sse_kms_encrypted_objects: Optional[SseKmsEncryptedObjects] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            sse_kms_encrypted_objects (SseKmsEncryptedObjects, optional): The container that is used to filter the source objects that are encrypted by using SSE-KMS. This parameter must be specified if the SourceSelectionCriteria parameter is specified in the data replication rule.
        """
        super().__init__(**kwargs)
        self.sse_kms_encrypted_objects = sse_kms_encrypted_objects


class ReplicationRule(serde.Model):
    """
    The data replication rule configuration.
    """

    _attribute_map = {
        'source_selection_criteria': {'tag': 'xml', 'rename': 'SourceSelectionCriteria', 'type': 'ReplicationSourceSelectionCriteria'},
        'rtc': {'tag': 'xml', 'rename': 'RTC', 'type': 'RTC'},
        'destination': {'tag': 'xml', 'rename': 'Destination', 'type': 'ReplicationDestination'},
        'historical_object_replication': {'tag': 'xml', 'rename': 'HistoricalObjectReplication', 'type': 'str'},
        'sync_role': {'tag': 'xml', 'rename': 'SyncRole', 'type': 'str'},
        'status': {'tag': 'xml', 'rename': 'Status', 'type': 'str'},
        'encryption_configuration': {'tag': 'xml', 'rename': 'EncryptionConfiguration', 'type': 'ReplicationEncryptionConfiguration'},
        'id': {'tag': 'xml', 'rename': 'ID', 'type': 'str'},
        'prefix_set': {'tag': 'xml', 'rename': 'PrefixSet', 'type': 'ReplicationPrefixSet'},
        'action': {'tag': 'xml', 'rename': 'Action', 'type': 'str'},
    }

    _xml_map = {
        'name': 'Rule'
    }

    _dependency_map = {
        'SourceSelectionCriteria': {'new': lambda: ReplicationSourceSelectionCriteria()},
        'RTC': {'new': lambda: ReplicationTimeControl()},
        'Destination': {'new': lambda: ReplicationDestination()},
        'EncryptionConfiguration': {'new': lambda: ReplicationEncryptionConfiguration()},
        'PrefixSet': {'new': lambda: ReplicationPrefixSet()},
    }

    def __init__(
        self,
        source_selection_criteria: Optional[ReplicationSourceSelectionCriteria] = None,
        rtc: Optional[ReplicationTimeControl] = None,
        destination: Optional[ReplicationDestination] = None,
        historical_object_replication: Optional[Union[str, HistoricalObjectReplicationType]] = None,
        sync_role: Optional[str] = None,
        status: Optional[str] = None,
        encryption_configuration: Optional[ReplicationEncryptionConfiguration] = None,
        id: Optional[str] = None,
        prefix_set: Optional[ReplicationPrefixSet] = None,
        action: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            source_selection_criteria (ReplicationSourceSelectionCriteria, optional): The container that specifies other conditions used to filter the source objects that you want to replicate. Filter conditions can be specified only for source objects encrypted by using SSE-KMS.
            rtc (RTC, optional): The container that stores the status of the RTC feature.
            destination (ReplicationDestination, optional): The container that stores the information about the destination bucket.
            historical_object_replication (str | HistoricalObjectReplicationType, optional): Specifies whether to replicate historical data that exists before data replication is enabled from the source bucket to the destination bucket. Valid values:*   enabled (default): replicates historical data to the destination bucket.*   disabled: does not replicate historical data to the destination bucket. Only data uploaded to the source bucket after data replication is enabled for the source bucket is replicated.
            sync_role (str, optional): The role that you want to authorize OSS to use to replicate data. If you want to use SSE-KMS to encrypt the objects that are replicated to the destination bucket, you must specify this parameter.
            status (str, optional): The status of the data replication task. Valid values:*   starting: OSS creates a data replication task after a data replication rule is configured.*   doing: The replication rule is effective and the replication task is in progress.*   closing: OSS clears a data replication task after the corresponding data replication rule is deleted.
            encryption_configuration (ReplicationEncryptionConfiguration, optional): The encryption configuration for the objects replicated to the destination bucket. If the Status parameter is set to Enabled, you must specify this parameter.
            id (str, optional): The ID of the rule.
            prefix_set (ReplicationPrefixSet, optional): The container that stores prefixes. You can specify up to 10 prefixes in each data replication rule.
            action (str, optional): The operations that can be synchronized to the destination bucket. If you configure Action in a data replication rule, OSS synchronizes new data and historical data based on the specified value of Action. You can set Action to one or more of the following operation types. Valid values:*   ALL (default): PUT, DELETE, and ABORT operations are synchronized to the destination bucket.*   PUT: Write operations are synchronized to the destination bucket, including PutObject, PostObject, AppendObject, CopyObject, PutObjectACL, InitiateMultipartUpload, UploadPart, UploadPartCopy, and CompleteMultipartUpload.
        """
        super().__init__(**kwargs)
        self.source_selection_criteria = source_selection_criteria
        self.rtc = rtc
        self.destination = destination
        self.historical_object_replication = historical_object_replication
        self.sync_role = sync_role
        self.status = status
        self.encryption_configuration = encryption_configuration
        self.id = id
        self.prefix_set = prefix_set
        self.action = action


class ReplicationConfiguration(serde.Model):
    """
    The container that stores data replication configurations.
    """

    _attribute_map = { 
        'rules': {'tag': 'xml', 'rename': 'Rule', 'type': '[ReplicationRule]'},
    }

    _xml_map = {
        'name': 'ReplicationConfiguration'
    }

    _dependency_map = { 
        'Rule': {'new': lambda: ReplicationRule()},
    }

    def __init__(
        self,
        rules: Optional[List[ReplicationRule]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            rules (List[ReplicationRule], optional): The container that stores the data replication rules.
        """
        super().__init__(**kwargs)
        self.rules = rules


class ReplicationProgress(serde.Model):
    """
    The container that is used to store the progress of data replication tasks.
    """

    _attribute_map = { 
        'rules': {'tag': 'xml', 'rename': 'Rule', 'type': '[ReplicationProgressRule]'},
    }

    _xml_map = {
        'name': 'ReplicationProgress'
    }

    _dependency_map = { 
        'ReplicationProgressRule': {'new': lambda: ReplicationProgressRule()},
    }

    def __init__(
        self,
        rules: Optional[List[ReplicationProgressRule]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            rules (List[ReplicationProgressRule], optional): The container that stores the progress of the data replication task corresponding to each data replication rule.
        """
        super().__init__(**kwargs)
        self.rules = rules


class ReplicationLocation(serde.Model):
    """
    The container that stores the region in which the destination bucket can be located.
    """

    _attribute_map = { 
        'locations': {'tag': 'xml', 'rename': 'Location', 'type': '[str]'},
        'location_transfer_type_constraint': {'tag': 'xml', 'rename': 'LocationTransferTypeConstraint', 'type': 'LocationTransferTypeConstraint'},
        'locationrtc_constraint': {'tag': 'xml', 'rename': 'LocationRTCConstraint', 'type': 'LocationRTCConstraint'},
    }

    _xml_map = {
        'name': 'ReplicationLocation'
    }

    _dependency_map = { 
        'LocationTransferTypeConstraint': {'new': lambda: LocationTransferTypeConstraint()},
        'LocationRTCConstraint': {'new': lambda: LocationRTCConstraint()},
    }

    def __init__(
        self,
        locations: Optional[List[str]] = None,
        location_transfer_type_constraint: Optional[LocationTransferTypeConstraint] = None,
        locationrtc_constraint: Optional[LocationRTCConstraint] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            locations (List[str], optional): The regions in which the destination bucket can be located.
            location_transfer_type_constraint (LocationTransferTypeConstraint, optional): The container that stores regions in which the destination bucket can be located with TransferType specified.
            locationrtc_constraint (LocationRTCConstraint, optional): The container that stores regions in which the RTC can be enabled.
        """
        super().__init__(**kwargs)
        self.locations = locations
        self.location_transfer_type_constraint = location_transfer_type_constraint
        self.locationrtc_constraint = locationrtc_constraint


class PutBucketRtcRequest(serde.RequestModel):
    """
    The request for the PutBucketRtc operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'rtc_configuration': {'tag': 'input', 'position': 'body', 'rename': 'ReplicationRule', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        rtc_configuration: Optional[RtcConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            rtc_configuration (RtcConfiguration, optional): The container of the request body.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.rtc_configuration = rtc_configuration


class PutBucketRtcResult(serde.ResultModel):
    """
    The request for the PutBucketRtc operation.
    """

class PutBucketReplicationRequest(serde.RequestModel):
    """
    The request for the PutBucketReplication operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'replication_configuration': {'tag': 'input', 'position': 'body', 'rename': 'ReplicationConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        replication_configuration: Optional[ReplicationConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            replication_configuration (ReplicationConfiguration, optional): The container of the request body.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.replication_configuration = replication_configuration


class PutBucketReplicationResult(serde.ResultModel):
    """
    The request for the PutBucketReplication operation.
    """

    _attribute_map = { 
        'replication_rule_id': {'tag': 'output', 'position': 'header', 'rename': 'x-oss-replication-rule-id', 'type': 'str'},
    }

    def __init__(
        self,
        replication_rule_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            replication_rule_id (str, optional): <no value>
        """
        super().__init__(**kwargs)
        self.replication_rule_id = replication_rule_id

class GetBucketReplicationRequest(serde.RequestModel):
    """
    The request for the GetBucketReplication operation.
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


class GetBucketReplicationResult(serde.ResultModel):
    """
    The request for the GetBucketReplication operation.
    """

    _attribute_map = { 
        'replication_configuration': {'tag': 'output', 'position': 'body', 'rename': 'ReplicationConfiguration', 'type': 'ReplicationConfiguration,xml'},
    }

    _dependency_map = { 
        'ReplicationConfiguration': {'new': lambda: ReplicationConfiguration()},
    }

    def __init__(
        self,
        replication_configuration: Optional[ReplicationConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            replication_configuration (ReplicationConfiguration, optional): The container that stores data replication configurations.
        """
        super().__init__(**kwargs)
        self.replication_configuration = replication_configuration

class GetBucketReplicationLocationRequest(serde.RequestModel):
    """
    The request for the GetBucketReplicationLocation operation.
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


class GetBucketReplicationLocationResult(serde.ResultModel):
    """
    The request for the GetBucketReplicationLocation operation.
    """

    _attribute_map = { 
        'replication_location': {'tag': 'output', 'position': 'body', 'rename': 'ReplicationLocation', 'type': 'ReplicationLocation,xml'},
    }

    _dependency_map = { 
        'ReplicationLocation': {'new': lambda: ReplicationLocation()},
    }

    def __init__(
        self,
        replication_location: Optional[ReplicationLocation] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            replication_location (ReplicationLocation, optional): The container that stores the region in which the destination bucket can be located.
        """
        super().__init__(**kwargs)
        self.replication_location = replication_location

class GetBucketReplicationProgressRequest(serde.RequestModel):
    """
    The request for the GetBucketReplicationProgress operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'rule_id': {'tag': 'input', 'position': 'query', 'rename': 'rule-id', 'type': 'str', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        rule_id: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucekt.
            rule_id (str, required): The ID of the data replication rule. You can call the GetBucketReplication operation to query the ID.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.rule_id = rule_id


class GetBucketReplicationProgressResult(serde.ResultModel):
    """
    The request for the GetBucketReplicationProgress operation.
    """

    _attribute_map = { 
        'replication_progress': {'tag': 'output', 'position': 'body', 'rename': 'ReplicationProgress', 'type': 'ReplicationProgress,xml'},
    }

    _dependency_map = { 
        'ReplicationProgress': {'new': lambda: ReplicationProgress()},
    }

    def __init__(
        self,
        replication_progress: Optional[ReplicationProgress] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            replication_progress (ReplicationProgress, optional): The container that is used to store the progress of data replication tasks.
        """
        super().__init__(**kwargs)
        self.replication_progress = replication_progress

class DeleteBucketReplicationRequest(serde.RequestModel):
    """
    The request for the DeleteBucketReplication operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'replication_rules': {'tag': 'input', 'position': 'body', 'rename': 'ReplicationRules', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        replication_rules: Optional[ReplicationRules] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            replication_rules (ReplicationRules, optional): The container of the request body.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.replication_rules = replication_rules


class DeleteBucketReplicationResult(serde.ResultModel):
    """
    The request for the DeleteBucketReplication operation.
    """
