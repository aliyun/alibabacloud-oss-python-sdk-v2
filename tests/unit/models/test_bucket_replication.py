# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_replication as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse

class TestPutBucketReplication(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutBucketReplicationRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.replication_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutBucketReplicationRequest(
            bucket='bucketexampletest',
            replication_configuration=model.ReplicationConfiguration(
                rules=[model.ReplicationRule(
                    source_selection_criteria=model.ReplicationSourceSelectionCriteria(
                        sse_kms_encrypted_objects=model.SseKmsEncryptedObjects(
                            status=model.StatusType.ENABLED,
                        ),
                    ),
                    rtc=model.ReplicationTimeControl(
                        status='OK',
                    ),
                    destination=model.ReplicationDestination(
                        bucket='bucketexampletest',
                        location='oss-cn-hangzhou',
                        transfer_type=model.TransferType.OSS_ACC,
                    ),
                    historical_object_replication=model.HistoricalObjectReplicationType.DISABLED,
                    sync_role='%3j-$,Ovxm',
                    status='OK',
                    encryption_configuration=model.ReplicationEncryptionConfiguration(
                        replica_kms_key_id='R/(x~ud&gP',
                    ),
                    id='0022012****',
                    prefix_set=model.ReplicationPrefixSet(
                        prefixs=['weL15FfhdL', 'WT@ih5G8K@'],
                    ),
                    action='62,)fFPgQ&',
                ), model.ReplicationRule(
                    source_selection_criteria=model.ReplicationSourceSelectionCriteria(
                        sse_kms_encrypted_objects=model.SseKmsEncryptedObjects(
                            status=model.StatusType.DISABLED,
                        ),
                    ),
                    rtc=model.ReplicationTimeControl(
                        status='OK',
                    ),
                    destination=model.ReplicationDestination(
                        bucket='bucketexampletest',
                        location='oss-cn-hangzhou',
                        transfer_type=model.TransferType.INTERNAL,
                    ),
                    historical_object_replication=model.HistoricalObjectReplicationType.DISABLED,
                    sync_role='%3j-$,Ovxm',
                    status='OK',
                    encryption_configuration=model.ReplicationEncryptionConfiguration(
                        replica_kms_key_id='R/(x~ud&gP',
                    ),
                    id='0022012****',
                    prefix_set=model.ReplicationPrefixSet(
                        prefixs=['&zL>issa6g', 'U$K\9+W96'],
                    ),
                    action='62,)fFPgQ&',
                )],
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual(model.StatusType.ENABLED, request.replication_configuration.rules[0].source_selection_criteria.sse_kms_encrypted_objects.status)
        self.assertEqual('OK', request.replication_configuration.rules[0].rtc.status)
        self.assertEqual('bucketexampletest', request.replication_configuration.rules[0].destination.bucket)
        self.assertEqual('oss-cn-hangzhou', request.replication_configuration.rules[0].destination.location)
        self.assertEqual(model.TransferType.OSS_ACC, request.replication_configuration.rules[0].destination.transfer_type)
        self.assertEqual(model.HistoricalObjectReplicationType.DISABLED, request.replication_configuration.rules[0].historical_object_replication)
        self.assertEqual('%3j-$,Ovxm', request.replication_configuration.rules[0].sync_role)
        self.assertEqual('OK', request.replication_configuration.rules[0].status)
        self.assertEqual('R/(x~ud&gP', request.replication_configuration.rules[0].encryption_configuration.replica_kms_key_id)
        self.assertEqual('0022012****', request.replication_configuration.rules[0].id)
        self.assertEqual(['weL15FfhdL', 'WT@ih5G8K@'], request.replication_configuration.rules[0].prefix_set.prefixs)
        self.assertEqual('62,)fFPgQ&', request.replication_configuration.rules[0].action)
        self.assertEqual(model.StatusType.DISABLED, request.replication_configuration.rules[1].source_selection_criteria.sse_kms_encrypted_objects.status)
        self.assertEqual('OK', request.replication_configuration.rules[1].rtc.status)
        self.assertEqual('bucketexampletest', request.replication_configuration.rules[1].destination.bucket)
        self.assertEqual('oss-cn-hangzhou', request.replication_configuration.rules[1].destination.location)
        self.assertEqual(model.TransferType.INTERNAL, request.replication_configuration.rules[1].destination.transfer_type)
        self.assertEqual(model.HistoricalObjectReplicationType.DISABLED, request.replication_configuration.rules[1].historical_object_replication)
        self.assertEqual('%3j-$,Ovxm', request.replication_configuration.rules[1].sync_role)
        self.assertEqual('OK', request.replication_configuration.rules[1].status)
        self.assertEqual('R/(x~ud&gP', request.replication_configuration.rules[1].encryption_configuration.replica_kms_key_id)
        self.assertEqual('0022012****', request.replication_configuration.rules[1].id)
        self.assertEqual(['&zL>issa6g', 'U$K\9+W96'], request.replication_configuration.rules[1].prefix_set.prefixs)
        self.assertEqual('62,)fFPgQ&', request.replication_configuration.rules[1].action)

        request = model.PutBucketReplicationRequest(
            bucket='bucketexampletest',
            replication_configuration=model.ReplicationConfiguration(
                rules=[model.ReplicationRule(
                    source_selection_criteria=model.ReplicationSourceSelectionCriteria(
                        sse_kms_encrypted_objects=model.SseKmsEncryptedObjects(
                            status='Disabled',
                        ),
                    ),
                    rtc=model.ReplicationTimeControl(
                        status='OK',
                    ),
                    destination=model.ReplicationDestination(
                        bucket='bucketexampletest',
                        location='oss-cn-hangzhou',
                        transfer_type='internal',
                    ),
                    historical_object_replication='disabled',
                    sync_role='%3j-$,Ovxm',
                    status='OK',
                    encryption_configuration=model.ReplicationEncryptionConfiguration(
                        replica_kms_key_id='R/(x~ud&gP',
                    ),
                    id='0022012****',
                    prefix_set=model.ReplicationPrefixSet(
                        prefixs=['^NH1I)-4+t', 'bX1n~Q#);-'],
                    ),
                    action='62,)fFPgQ&',
                ), model.ReplicationRule(
                    source_selection_criteria=model.ReplicationSourceSelectionCriteria(
                        sse_kms_encrypted_objects=model.SseKmsEncryptedObjects(
                            status='Disabled',
                        ),
                    ),
                    rtc=model.ReplicationTimeControl(
                        status='OK',
                    ),
                    destination=model.ReplicationDestination(
                        bucket='bucketexampletest',
                        location='oss-cn-hangzhou',
                        transfer_type='internal',
                    ),
                    historical_object_replication='enabled',
                    sync_role='%3j-$,Ovxm',
                    status='OK',
                    encryption_configuration=model.ReplicationEncryptionConfiguration(
                        replica_kms_key_id='R/(x~ud&gP',
                    ),
                    id='0022012****',
                    prefix_set=model.ReplicationPrefixSet(
                        prefixs=['pA>>@Fpz;p', '/tK9%N|#JO'],
                    ),
                    action='62,)fFPgQ&',
                )],
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('Disabled', request.replication_configuration.rules[0].source_selection_criteria.sse_kms_encrypted_objects.status)
        self.assertEqual('OK', request.replication_configuration.rules[0].rtc.status)
        self.assertEqual('bucketexampletest', request.replication_configuration.rules[0].destination.bucket)
        self.assertEqual('oss-cn-hangzhou', request.replication_configuration.rules[0].destination.location)
        self.assertEqual('internal', request.replication_configuration.rules[0].destination.transfer_type)
        self.assertEqual('disabled', request.replication_configuration.rules[0].historical_object_replication)
        self.assertEqual('%3j-$,Ovxm', request.replication_configuration.rules[0].sync_role)
        self.assertEqual('OK', request.replication_configuration.rules[0].status)
        self.assertEqual('R/(x~ud&gP', request.replication_configuration.rules[0].encryption_configuration.replica_kms_key_id)
        self.assertEqual('0022012****', request.replication_configuration.rules[0].id)
        self.assertEqual(['^NH1I)-4+t', 'bX1n~Q#);-'], request.replication_configuration.rules[0].prefix_set.prefixs)
        self.assertEqual('62,)fFPgQ&', request.replication_configuration.rules[0].action)
        self.assertEqual('Disabled', request.replication_configuration.rules[1].source_selection_criteria.sse_kms_encrypted_objects.status)
        self.assertEqual('OK', request.replication_configuration.rules[1].rtc.status)
        self.assertEqual('bucketexampletest', request.replication_configuration.rules[1].destination.bucket)
        self.assertEqual('oss-cn-hangzhou', request.replication_configuration.rules[1].destination.location)
        self.assertEqual('internal', request.replication_configuration.rules[1].destination.transfer_type)
        self.assertEqual('enabled', request.replication_configuration.rules[1].historical_object_replication)
        self.assertEqual('%3j-$,Ovxm', request.replication_configuration.rules[1].sync_role)
        self.assertEqual('OK', request.replication_configuration.rules[1].status)
        self.assertEqual('R/(x~ud&gP', request.replication_configuration.rules[1].encryption_configuration.replica_kms_key_id)
        self.assertEqual('0022012****', request.replication_configuration.rules[1].id)
        self.assertEqual(['pA>>@Fpz;p', '/tK9%N|#JO'], request.replication_configuration.rules[1].prefix_set.prefixs)
        self.assertEqual('62,)fFPgQ&', request.replication_configuration.rules[1].action)


    def test_serialize_request(self):
        request = model.PutBucketReplicationRequest(
            bucket='bucketexampletest',
            replication_configuration=model.ReplicationConfiguration(
                rules=[model.ReplicationRule(
                    source_selection_criteria=model.ReplicationSourceSelectionCriteria(
                        sse_kms_encrypted_objects=model.SseKmsEncryptedObjects(
                            status=model.StatusType.DISABLED,
                        ),
                    ),
                    rtc=model.ReplicationTimeControl(
                        status='OK',
                    ),
                    destination=model.ReplicationDestination(
                        bucket='bucketexampletest',
                        location='oss-cn-hangzhou',
                        transfer_type=model.TransferType.INTERNAL,
                    ),
                    historical_object_replication=model.HistoricalObjectReplicationType.DISABLED,
                    sync_role='%3j-$,Ovxm',
                    status='OK',
                    encryption_configuration=model.ReplicationEncryptionConfiguration(
                        replica_kms_key_id='R/(x~ud&gP',
                    ),
                    id='0022012****',
                    prefix_set=model.ReplicationPrefixSet(
                        prefixs=['8YzxhLj^<s', '+7~9MS~m~J'],
                    ),
                    action='62,)fFPgQ&',
                ), model.ReplicationRule(
                    source_selection_criteria=model.ReplicationSourceSelectionCriteria(
                        sse_kms_encrypted_objects=model.SseKmsEncryptedObjects(
                            status=model.StatusType.DISABLED,
                        ),
                    ),
                    rtc=model.ReplicationTimeControl(
                        status='OK',
                    ),
                    destination=model.ReplicationDestination(
                        bucket='bucketexampletest',
                        location='oss-cn-hangzhou',
                        transfer_type=model.TransferType.INTERNAL,
                    ),
                    historical_object_replication=model.HistoricalObjectReplicationType.DISABLED,
                    sync_role='%3j-$,Ovxm',
                    status='OK',
                    encryption_configuration=model.ReplicationEncryptionConfiguration(
                        replica_kms_key_id='R/(x~ud&gP',
                    ),
                    id='0022012****',
                    prefix_set=model.ReplicationPrefixSet(
                        prefixs=['~n!_P#nK)u', '$Nff<F:t0/'],
                    ),
                    action='62,)fFPgQ&',
                )],
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutBucketReplication',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutBucketReplication', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.PutBucketReplicationResult()
        self.assertIsNone(result.replication_rule_id)
        self.assertIsInstance(result, serde.Model)

        result = model.PutBucketReplicationResult(
            replication_rule_id='Cr:ikaa.:i',
        )
        self.assertEqual('Cr:ikaa.:i', result.replication_rule_id)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutBucketReplicationResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                    'x-oss-version-id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('x-oss-version-id'))


class TestPutBucketRtc(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutBucketRtcRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.rtc_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutBucketRtcRequest(
            bucket='bucketexampletest',
            rtc_configuration=model.RtcConfiguration(
                rtc=model.ReplicationTimeControl(
                    status='enabled',
                ),
                id='0022012****',
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('enabled', request.rtc_configuration.rtc.status)
        self.assertEqual('0022012****', request.rtc_configuration.id)

    def test_serialize_request(self):
        request = model.PutBucketRtcRequest(
            bucket='bucketexampletest',
            rtc_configuration=model.RtcConfiguration(
                rtc=model.ReplicationTimeControl(
                    status='enabled',
                ),
                id='0022012****',
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutBucketRtc',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutBucketRtc', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.PutBucketRtcResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutBucketRtcResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                    'x-oss-version-id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('x-oss-version-id'))


class TestGetBucketReplication(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketReplicationRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetBucketReplicationRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.GetBucketReplicationRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketReplication',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetBucketReplication', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetBucketReplicationResult()
        self.assertIsNone(result.replication_configuration)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketReplicationResult(
            replication_configuration=model.ReplicationConfiguration(
                rules=[model.ReplicationRule(
                    source_selection_criteria=model.ReplicationSourceSelectionCriteria(
                        sse_kms_encrypted_objects=model.SseKmsEncryptedObjects(
                            status=model.StatusType.DISABLED,
                        ),
                    ),
                    rtc=model.ReplicationTimeControl(
                        status='enabled',
                    ),
                    destination=model.ReplicationDestination(
                        bucket='bucketexampletest',
                        location='oss-cn-hangzhou',
                        transfer_type=model.TransferType.OSS_ACC,
                    ),
                    historical_object_replication=model.HistoricalObjectReplicationType.ENABLED,
                    sync_role='P5Fu.R2)t-',
                    status='enabled',
                    encryption_configuration=model.ReplicationEncryptionConfiguration(
                        replica_kms_key_id='rYj%X5Yukp',
                    ),
                    id='0022012****',
                    prefix_set=model.ReplicationPrefixSet(
                        prefixs=['DzftH$VLp', 'c7jKu ^ 4ie * '],
                    ),
                    action='x?&>J%#0Cy',
                ), model.ReplicationRule(
                    source_selection_criteria=model.ReplicationSourceSelectionCriteria(
                        sse_kms_encrypted_objects=model.SseKmsEncryptedObjects(
                            status=model.StatusType.ENABLED,
                        ),
                    ),
                    rtc=model.ReplicationTimeControl(
                        status='enabled',
                    ),
                    destination=model.ReplicationDestination(
                        bucket='bucketexampletest',
                        location='oss-cn-hangzhou',
                        transfer_type=model.TransferType.INTERNAL,
                    ),
                    historical_object_replication=model.HistoricalObjectReplicationType.ENABLED,
                    sync_role='P5Fu.R2)t-',
                    status='enabled',
                    encryption_configuration=model.ReplicationEncryptionConfiguration(
                        replica_kms_key_id='rYj%X5Yukp',
                    ),
                    id='0022012****',
                    prefix_set=model.ReplicationPrefixSet(
                        prefixs=['pU^k<dYEYF', 'ZXc)cu%g8D'],
                    ),
                    action='x?&>J%#0Cy',
                )],
            ),
        )
        self.assertEqual(model.StatusType.DISABLED, result.replication_configuration.rules[0].source_selection_criteria.sse_kms_encrypted_objects.status)
        self.assertEqual('enabled', result.replication_configuration.rules[0].rtc.status)
        self.assertEqual('bucketexampletest', result.replication_configuration.rules[0].destination.bucket)
        self.assertEqual('oss-cn-hangzhou', result.replication_configuration.rules[0].destination.location)
        self.assertEqual(model.TransferType.OSS_ACC, result.replication_configuration.rules[0].destination.transfer_type)
        self.assertEqual(model.HistoricalObjectReplicationType.ENABLED, result.replication_configuration.rules[0].historical_object_replication)
        self.assertEqual('P5Fu.R2)t-', result.replication_configuration.rules[0].sync_role)
        self.assertEqual('enabled', result.replication_configuration.rules[0].status)
        self.assertEqual('rYj%X5Yukp', result.replication_configuration.rules[0].encryption_configuration.replica_kms_key_id)
        self.assertEqual('0022012****', result.replication_configuration.rules[0].id)
        self.assertEqual(['DzftH$VLp', 'c7jKu ^ 4ie * '], result.replication_configuration.rules[0].prefix_set.prefixs)
        self.assertEqual('x?&>J%#0Cy', result.replication_configuration.rules[0].action)
        self.assertEqual(model.StatusType.ENABLED, result.replication_configuration.rules[1].source_selection_criteria.sse_kms_encrypted_objects.status)
        self.assertEqual('enabled', result.replication_configuration.rules[1].rtc.status)
        self.assertEqual('bucketexampletest', result.replication_configuration.rules[1].destination.bucket)
        self.assertEqual('oss-cn-hangzhou', result.replication_configuration.rules[1].destination.location)
        self.assertEqual(model.TransferType.INTERNAL, result.replication_configuration.rules[1].destination.transfer_type)
        self.assertEqual(model.HistoricalObjectReplicationType.ENABLED, result.replication_configuration.rules[1].historical_object_replication)
        self.assertEqual('P5Fu.R2)t-', result.replication_configuration.rules[1].sync_role)
        self.assertEqual('enabled', result.replication_configuration.rules[1].status)
        self.assertEqual('rYj%X5Yukp', result.replication_configuration.rules[1].encryption_configuration.replica_kms_key_id)
        self.assertEqual('0022012****', result.replication_configuration.rules[1].id)
        self.assertEqual(['pU^k<dYEYF', 'ZXc)cu%g8D'], result.replication_configuration.rules[1].prefix_set.prefixs)
        self.assertEqual('x?&>J%#0Cy', result.replication_configuration.rules[1].action)

        result = model.GetBucketReplicationResult(
            replication_configuration=model.ReplicationConfiguration(
                rules=[model.ReplicationRule(
                    source_selection_criteria=model.ReplicationSourceSelectionCriteria(
                        sse_kms_encrypted_objects=model.SseKmsEncryptedObjects(
                            status='Enabled',
                        ),
                    ),
                    rtc=model.ReplicationTimeControl(
                        status='enabled',
                    ),
                    destination=model.ReplicationDestination(
                        bucket='bucketexampletest',
                        location='oss-cn-hangzhou',
                        transfer_type='internal',
                    ),
                    historical_object_replication='enabled',
                    sync_role='P5Fu.R2)t-',
                    status='enabled',
                    encryption_configuration=model.ReplicationEncryptionConfiguration(
                        replica_kms_key_id='rYj%X5Yukp',
                    ),
                    id='0022012****',
                    prefix_set=model.ReplicationPrefixSet(
                        prefixs=['59#VccCeHl', 'FjCyq,s7#c'],
                    ),
                    action='x?&>J%#0Cy',
                ), model.ReplicationRule(
                    source_selection_criteria=model.ReplicationSourceSelectionCriteria(
                        sse_kms_encrypted_objects=model.SseKmsEncryptedObjects(
                            status='Disabled',
                        ),
                    ),
                    rtc=model.ReplicationTimeControl(
                        status='enabled',
                    ),
                    destination=model.ReplicationDestination(
                        bucket='bucketexampletest',
                        location='oss-cn-hangzhou',
                        transfer_type='internal',
                    ),
                    historical_object_replication='disabled',
                    sync_role='P5Fu.R2)t-',
                    status='enabled',
                    encryption_configuration=model.ReplicationEncryptionConfiguration(
                        replica_kms_key_id='rYj%X5Yukp',
                    ),
                    id='0022012****',
                    prefix_set=model.ReplicationPrefixSet(
                        prefixs=['3+jTPG*o6X', 'mp(N>Z>mJ'],
                    ),
                    action='x?&>J%#0Cy',
                )],
            ),
        )
        self.assertEqual('Enabled', result.replication_configuration.rules[0].source_selection_criteria.sse_kms_encrypted_objects.status)
        self.assertEqual('enabled', result.replication_configuration.rules[0].rtc.status)
        self.assertEqual('bucketexampletest', result.replication_configuration.rules[0].destination.bucket)
        self.assertEqual('oss-cn-hangzhou', result.replication_configuration.rules[0].destination.location)
        self.assertEqual('internal', result.replication_configuration.rules[0].destination.transfer_type)
        self.assertEqual('enabled', result.replication_configuration.rules[0].historical_object_replication)
        self.assertEqual('P5Fu.R2)t-', result.replication_configuration.rules[0].sync_role)
        self.assertEqual('enabled', result.replication_configuration.rules[0].status)
        self.assertEqual('rYj%X5Yukp', result.replication_configuration.rules[0].encryption_configuration.replica_kms_key_id)
        self.assertEqual('0022012****', result.replication_configuration.rules[0].id)
        self.assertEqual(['59#VccCeHl', 'FjCyq,s7#c'], result.replication_configuration.rules[0].prefix_set.prefixs)
        self.assertEqual('x?&>J%#0Cy', result.replication_configuration.rules[0].action)
        self.assertEqual('Disabled', result.replication_configuration.rules[1].source_selection_criteria.sse_kms_encrypted_objects.status)
        self.assertEqual('enabled', result.replication_configuration.rules[1].rtc.status)
        self.assertEqual('bucketexampletest', result.replication_configuration.rules[1].destination.bucket)
        self.assertEqual('oss-cn-hangzhou', result.replication_configuration.rules[1].destination.location)
        self.assertEqual('internal', result.replication_configuration.rules[1].destination.transfer_type)
        self.assertEqual('disabled', result.replication_configuration.rules[1].historical_object_replication)
        self.assertEqual('P5Fu.R2)t-', result.replication_configuration.rules[1].sync_role)
        self.assertEqual('enabled', result.replication_configuration.rules[1].status)
        self.assertEqual('rYj%X5Yukp', result.replication_configuration.rules[1].encryption_configuration.replica_kms_key_id)
        self.assertEqual('0022012****', result.replication_configuration.rules[1].id)
        self.assertEqual(['3+jTPG*o6X', 'mp(N>Z>mJ'], result.replication_configuration.rules[1].prefix_set.prefixs)
        self.assertEqual('x?&>J%#0Cy', result.replication_configuration.rules[1].action)


    def test_deserialize_result(self):
        xml_data = r'''
        <ReplicationConfiguration>
        </ReplicationConfiguration>'''

        result = model.GetBucketReplicationResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <ReplicationConfiguration>
          <Rule>
            <ID>test_replication_1</ID>
            <PrefixSet>
              <Prefix>source1</Prefix>
              <Prefix>video</Prefix>
            </PrefixSet>
            <Action>PUT</Action>
            <Destination>
              <Bucket>destbucket</Bucket>
              <Location>oss-cn-beijing</Location>
              <TransferType>oss_acc</TransferType>
            </Destination>
            <Status>doing</Status>
            <HistoricalObjectReplication>enabled</HistoricalObjectReplication>
            <SyncRole>aliyunramrole</SyncRole>
            <RTC>
              <Status>enabled</Status>
            </RTC>
          </Rule>
        </ReplicationConfiguration>
        '''

        result = model.GetBucketReplicationResult()
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=xml_data,
            )
        )
        deserializer = [serde.deserialize_output_xmlbody]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertEqual('test_replication_1', result.replication_configuration.rules[0].id)
        self.assertEqual('source1', result.replication_configuration.rules[0].prefix_set.prefixs[0])
        self.assertEqual('video', result.replication_configuration.rules[0].prefix_set.prefixs[1])
        self.assertEqual('PUT', result.replication_configuration.rules[0].action)
        self.assertEqual('destbucket', result.replication_configuration.rules[0].destination.bucket)
        self.assertEqual('oss-cn-beijing', result.replication_configuration.rules[0].destination.location)
        self.assertEqual('oss_acc', result.replication_configuration.rules[0].destination.transfer_type)
        self.assertEqual('doing', result.replication_configuration.rules[0].status)
        self.assertEqual('enabled', result.replication_configuration.rules[0].historical_object_replication)
        self.assertEqual('aliyunramrole', result.replication_configuration.rules[0].sync_role)
        self.assertEqual('enabled', result.replication_configuration.rules[0].rtc.status)


class TestGetBucketReplicationLocation(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketReplicationLocationRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetBucketReplicationLocationRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.GetBucketReplicationLocationRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketReplicationLocation',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetBucketReplicationLocation', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetBucketReplicationLocationResult()
        self.assertIsNone(result.replication_location)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketReplicationLocationResult(
            replication_location=model.ReplicationLocation(
                locations=['Qwn,?>K84y', 'qBVX@$5&Ph'],
                location_transfer_type_constraint=model.LocationTransferTypeConstraint(
                    location_transfer_types=[model.LocationTransferType(
                        location='oss-cn-hangzhou',
                        transfer_types=model.TransferTypes(
                            types=['bTKdoSYN~K', '4io$O jdsP'],
                        ),
                    ), model.LocationTransferType(
                        location='oss-cn-hangzhou',
                        transfer_types=model.TransferTypes(
                            types=['TDfE+g<ooP', 'IHiyU1<zl_'],
                        ),
                    )],
                ),
                locationrtc_constraint=model.LocationRTCConstraint(
                    locations=['?G6Ps7V<^r', '.%@<F!Y<<K'],
                ),
            ),
        )
        self.assertEqual(['Qwn,?>K84y', 'qBVX@$5&Ph'], result.replication_location.locations)
        self.assertEqual('oss-cn-hangzhou', result.replication_location.location_transfer_type_constraint.location_transfer_types[0].location)
        self.assertEqual(['bTKdoSYN~K', '4io$O jdsP'], result.replication_location.location_transfer_type_constraint.location_transfer_types[0].transfer_types.types)
        self.assertEqual('oss-cn-hangzhou', result.replication_location.location_transfer_type_constraint.location_transfer_types[1].location)
        self.assertEqual(['TDfE+g<ooP', 'IHiyU1<zl_'], result.replication_location.location_transfer_type_constraint.location_transfer_types[1].transfer_types.types)
        self.assertEqual(['?G6Ps7V<^r', '.%@<F!Y<<K'], result.replication_location.locationrtc_constraint.locations)

    def test_deserialize_result(self):
        xml_data = r'''
        <ReplicationLocation>
        </ReplicationLocation>'''

        result = model.GetBucketReplicationLocationResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <ReplicationLocation>
          <Location>oss-cn-beijing</Location>
          <Location>oss-cn-qingdao</Location>
          <Location>oss-cn-shenzhen</Location>
          <Location>oss-cn-hongkong</Location>
          <Location>oss-us-west-1</Location>
          <LocationTransferTypeConstraint>
            <LocationTransferType>
              <Location>oss-cn-hongkong</Location>
                <TransferTypes>
                  <Type>oss_acc</Type>
                </TransferTypes>
              </LocationTransferType>
              <LocationTransferType>
                <Location>oss-us-west-1</Location>
                <TransferTypes>
                  <Type>oss_acc</Type>
                </TransferTypes>
              </LocationTransferType>
            </LocationTransferTypeConstraint>
          </ReplicationLocation>
        '''

        result = model.GetBucketReplicationLocationResult()
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=xml_data,
            )
        )
        deserializer = [serde.deserialize_output_xmlbody]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertEqual('oss-cn-beijing', result.replication_location.locations[0])
        self.assertEqual('oss-cn-qingdao', result.replication_location.locations[1])
        self.assertEqual('oss-cn-shenzhen', result.replication_location.locations[2])
        self.assertEqual('oss-cn-hongkong', result.replication_location.locations[3])
        self.assertEqual('oss-us-west-1', result.replication_location.locations[4])
        self.assertEqual('oss-cn-hongkong', result.replication_location.location_transfer_type_constraint.location_transfer_types[0].location)
        self.assertEqual('oss_acc', result.replication_location.location_transfer_type_constraint.location_transfer_types[0].transfer_types.types[0])
        self.assertEqual('oss-us-west-1', result.replication_location.location_transfer_type_constraint.location_transfer_types[1].location)
        self.assertEqual('oss_acc', result.replication_location.location_transfer_type_constraint.location_transfer_types[1].transfer_types.types[0])


class TestGetBucketReplicationProgress(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketReplicationProgressRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.rule_id)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetBucketReplicationProgressRequest(
            bucket='bucketexampletest',
            rule_id='nr \T3>y~$',
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('nr \T3>y~$', request.rule_id)

    def test_serialize_request(self):
        request = model.GetBucketReplicationProgressRequest(
            bucket='bucketexampletest',
            rule_id='nr \T3>y~$',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketReplicationProgress',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetBucketReplicationProgress', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)
        self.assertEqual('nr \T3>y~$', op_input.parameters.get('rule-id'))

    def test_constructor_result(self):
        result = model.GetBucketReplicationProgressResult()
        self.assertIsNone(result.replication_progress)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketReplicationProgressResult(
            replication_progress=model.ReplicationProgress(
                rules=[model.ReplicationProgressRule(
                    historical_object_replication='xv8*Iov4u.',
                    progress=model.ReplicationProgressInformation(
                        historical_object='3W(95Odk-h',
                        new_object=')vx^D+VMrN',
                    ),
                    id='0022012****',
                    prefix_set=model.ReplicationPrefixSet(
                        prefixs=['K^o+BYWL 5', 'LR#tep~d~H'],
                    ),
                    action='wfU!f&GW0>',
                    destination=model.ReplicationDestination(
                        bucket='bucketexampletest',
                        location='oss-cn-hangzhou',
                        transfer_type=model.TransferType.OSS_ACC,
                    ),
                    status='enabled',
                ), model.ReplicationProgressRule(
                    historical_object_replication='xv8*Iov4u.',
                    progress=model.ReplicationProgressInformation(
                        historical_object='3W(95Odk-h',
                        new_object=')vx^D+VMrN',
                    ),
                    id='0022012****',
                    prefix_set=model.ReplicationPrefixSet(
                        prefixs=['K9K_je9BD$', 'FCm+#VRLM('],
                    ),
                    action='wfU!f&GW0>',
                    destination=model.ReplicationDestination(
                        bucket='bucketexampletest',
                        location='oss-cn-hangzhou',
                        transfer_type=model.TransferType.INTERNAL,
                    ),
                    status='enabled',
                )],
            ),
        )
        self.assertEqual('xv8*Iov4u.', result.replication_progress.rules[0].historical_object_replication)
        self.assertEqual('3W(95Odk-h', result.replication_progress.rules[0].progress.historical_object)
        self.assertEqual(')vx^D+VMrN', result.replication_progress.rules[0].progress.new_object)
        self.assertEqual('0022012****', result.replication_progress.rules[0].id)
        self.assertEqual(['K^o+BYWL 5', 'LR#tep~d~H'], result.replication_progress.rules[0].prefix_set.prefixs)
        self.assertEqual('wfU!f&GW0>', result.replication_progress.rules[0].action)
        self.assertEqual('bucketexampletest', result.replication_progress.rules[0].destination.bucket)
        self.assertEqual('oss-cn-hangzhou', result.replication_progress.rules[0].destination.location)
        self.assertEqual(model.TransferType.OSS_ACC, result.replication_progress.rules[0].destination.transfer_type)
        self.assertEqual('enabled', result.replication_progress.rules[0].status)
        self.assertEqual('xv8*Iov4u.', result.replication_progress.rules[1].historical_object_replication)
        self.assertEqual('3W(95Odk-h', result.replication_progress.rules[1].progress.historical_object)
        self.assertEqual(')vx^D+VMrN', result.replication_progress.rules[1].progress.new_object)
        self.assertEqual('0022012****', result.replication_progress.rules[1].id)
        self.assertEqual(['K9K_je9BD$', 'FCm+#VRLM('], result.replication_progress.rules[1].prefix_set.prefixs)
        self.assertEqual('wfU!f&GW0>', result.replication_progress.rules[1].action)
        self.assertEqual('bucketexampletest', result.replication_progress.rules[1].destination.bucket)
        self.assertEqual('oss-cn-hangzhou', result.replication_progress.rules[1].destination.location)
        self.assertEqual(model.TransferType.INTERNAL, result.replication_progress.rules[1].destination.transfer_type)
        self.assertEqual('enabled', result.replication_progress.rules[1].status)

        result = model.GetBucketReplicationProgressResult(
            replication_progress=model.ReplicationProgress(
                rules=[model.ReplicationProgressRule(
                    historical_object_replication='xv8*Iov4u.',
                    progress=model.ReplicationProgressInformation(
                        historical_object='3W(95Odk-h',
                        new_object=')vx^D+VMrN',
                    ),
                    id='0022012****',
                    prefix_set=model.ReplicationPrefixSet(
                        prefixs=['.G\G-Mp.>#', '\6S%1ZqiUr'],
                    ),
                    action='wfU!f&GW0>',
                    destination=model.ReplicationDestination(
                        bucket='bucketexampletest',
                        location='oss-cn-hangzhou',
                        transfer_type='internal',
                    ),
                    status='enabled',
                ), model.ReplicationProgressRule(
                    historical_object_replication='xv8*Iov4u.',
                    progress=model.ReplicationProgressInformation(
                        historical_object='3W(95Odk-h',
                        new_object=')vx^D+VMrN',
                    ),
                    id='0022012****',
                    prefix_set=model.ReplicationPrefixSet(
                        prefixs=['c0b:^u9<5z', 'G1redk-B3D'],
                    ),
                    action='wfU!f&GW0>',
                    destination=model.ReplicationDestination(
                        bucket='bucketexampletest',
                        location='oss-cn-hangzhou',
                        transfer_type='oss_acc',
                    ),
                    status='enabled',
                )],
            ),
        )
        self.assertEqual('xv8*Iov4u.', result.replication_progress.rules[0].historical_object_replication)
        self.assertEqual('3W(95Odk-h', result.replication_progress.rules[0].progress.historical_object)
        self.assertEqual(')vx^D+VMrN', result.replication_progress.rules[0].progress.new_object)
        self.assertEqual('0022012****', result.replication_progress.rules[0].id)
        self.assertEqual(['.G\G-Mp.>#', '\6S%1ZqiUr'], result.replication_progress.rules[0].prefix_set.prefixs)
        self.assertEqual('wfU!f&GW0>', result.replication_progress.rules[0].action)
        self.assertEqual('bucketexampletest', result.replication_progress.rules[0].destination.bucket)
        self.assertEqual('oss-cn-hangzhou', result.replication_progress.rules[0].destination.location)
        self.assertEqual('internal', result.replication_progress.rules[0].destination.transfer_type)
        self.assertEqual('enabled', result.replication_progress.rules[0].status)
        self.assertEqual('xv8*Iov4u.', result.replication_progress.rules[1].historical_object_replication)
        self.assertEqual('3W(95Odk-h', result.replication_progress.rules[1].progress.historical_object)
        self.assertEqual(')vx^D+VMrN', result.replication_progress.rules[1].progress.new_object)
        self.assertEqual('0022012****', result.replication_progress.rules[1].id)
        self.assertEqual(['c0b:^u9<5z', 'G1redk-B3D'], result.replication_progress.rules[1].prefix_set.prefixs)
        self.assertEqual('wfU!f&GW0>', result.replication_progress.rules[1].action)
        self.assertEqual('bucketexampletest', result.replication_progress.rules[1].destination.bucket)
        self.assertEqual('oss-cn-hangzhou', result.replication_progress.rules[1].destination.location)
        self.assertEqual('oss_acc', result.replication_progress.rules[1].destination.transfer_type)
        self.assertEqual('enabled', result.replication_progress.rules[1].status)

    def test_deserialize_result(self):
        xml_data = r'''
        <ReplicationProgress>
        </ReplicationProgress>'''

        result = model.GetBucketReplicationProgressResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <ReplicationProgress>
         <Rule>
           <ID>test_replication_1</ID>
           <PrefixSet>
            <Prefix>source_image</Prefix>
            <Prefix>video</Prefix>
           </PrefixSet>
           <Action>PUT</Action>
           <Destination>
            <Bucket>target-bucket</Bucket>
            <Location>oss-cn-beijing</Location>
            <TransferType>oss_acc</TransferType>
           </Destination>
           <Status>doing</Status>
           <HistoricalObjectReplication>enabled</HistoricalObjectReplication>
           <Progress>
            <HistoricalObject>0.85</HistoricalObject>
            <NewObject>2015-09-24T15:28:14.000Z</NewObject>
           </Progress>
         </Rule>
        </ReplicationProgress>
        '''

        result = model.GetBucketReplicationProgressResult()
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=xml_data,
            )
        )
        deserializer = [serde.deserialize_output_xmlbody]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertEqual('test_replication_1', result.replication_progress.rules[0].id)
        self.assertEqual('source_image', result.replication_progress.rules[0].prefix_set.prefixs[0])
        self.assertEqual('video', result.replication_progress.rules[0].prefix_set.prefixs[1])
        self.assertEqual('PUT', result.replication_progress.rules[0].action)
        self.assertEqual('target-bucket', result.replication_progress.rules[0].destination.bucket)
        self.assertEqual('oss-cn-beijing', result.replication_progress.rules[0].destination.location)
        self.assertEqual('oss_acc', result.replication_progress.rules[0].destination.transfer_type)
        self.assertEqual('doing', result.replication_progress.rules[0].status)
        self.assertEqual('enabled', result.replication_progress.rules[0].historical_object_replication)
        self.assertEqual('0.85', result.replication_progress.rules[0].progress.historical_object)
        self.assertEqual('2015-09-24T15:28:14.000Z', result.replication_progress.rules[0].progress.new_object)


class TestDeleteBucketReplication(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DeleteBucketReplicationRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.replication_rules)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DeleteBucketReplicationRequest(
            bucket='bucketexampletest',
            replication_rules=model.ReplicationRules(
                ids=['n>/;roWyOc', 'y-)kDJC8KU'],
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual(['n>/;roWyOc', 'y-)kDJC8KU'], request.replication_rules.ids)

    def test_serialize_request(self):
        request = model.DeleteBucketReplicationRequest(
            bucket='bucketexampletest',
            replication_rules=model.ReplicationRules(
                ids=['3c?:ex\~bl', 'l>LhMAXK2N'],
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteBucketReplication',
            method='DELETE',
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteBucketReplication', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.DeleteBucketReplicationResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.DeleteBucketReplicationResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                    'x-oss-version-id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('x-oss-version-id'))

