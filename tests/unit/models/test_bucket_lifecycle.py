# pylint: skip-file
import datetime
import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_lifecycle as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse


class TestPutBucketLifecycle(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutBucketLifecycleRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.allow_same_action_overlap)
        self.assertIsNone(request.lifecycle_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutBucketLifecycleRequest(
            bucket='bucketexampletest',
            allow_same_action_overlap='true',
            lifecycle_configuration=model.LifecycleConfiguration(
                rules=[model.LifecycleRule(
                    tags=[model.Tag(
                        key='key1',
                        value='value1',
                    ), model.Tag(
                        key='key12',
                        value='value12',
                    )],
                    noncurrent_version_expiration=model.NoncurrentVersionExpiration(
                        noncurrent_days=80479,
                    ),
                    filter=model.LifecycleRuleFilter(
                        object_size_greater_than=48877,
                        object_size_less_than=84934,
                        filter_not=[model.LifecycleRuleNot(
                            prefix='aaa',
                            tag=model.Tag(
                                key='key3',
                                value='value3',
                            ),
                        ), model.LifecycleRuleNot(
                            prefix='bbb',
                            tag=model.Tag(
                                key='key4',
                                value='value4',
                            ),
                        )],
                    ),
                    id='0022012****',
                    expiration=model.LifecycleRuleExpiration(
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                        days=37348,
                        expired_object_delete_marker=False,
                    ),
                    transitions=[model.LifecycleRuleTransition(
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                        days=37348,
                        storage_class=model.StorageClassType.COLDARCHIVE,
                        is_access_time=False,
                        return_to_std_when_visit=False,
                        allow_small_file=True,
                    ), model.LifecycleRuleTransition(
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                        days=37348,
                        storage_class=model.StorageClassType.DEEPCOLDARCHIVE,
                        is_access_time=False,
                        return_to_std_when_visit=True,
                        allow_small_file=True,
                    )],
                    noncurrent_version_transitions=[model.NoncurrentVersionTransition(
                        is_access_time=False,
                        return_to_std_when_visit=True,
                        allow_small_file=True,
                        noncurrent_days=80479,
                        storage_class=model.StorageClassType.DEEPCOLDARCHIVE,
                    ), model.NoncurrentVersionTransition(
                        is_access_time=True,
                        return_to_std_when_visit=True,
                        allow_small_file=True,
                        noncurrent_days=80479,
                        storage_class=model.StorageClassType.DEEPCOLDARCHIVE,
                    )],
                    atime_base=97611,
                    prefix='aaa',
                    status='OK',
                    abort_multipart_upload=model.LifecycleRuleAbortMultipartUpload(
                        days=37348,
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                    ),
                ), model.LifecycleRule(
                    tags=[model.Tag(
                        key='key5',
                        value='value5',
                    ), model.Tag(
                        key='key6',
                        value='value6',
                    )],
                    noncurrent_version_expiration=model.NoncurrentVersionExpiration(
                        noncurrent_days=80479,
                    ),
                    filter=model.LifecycleRuleFilter(
                        object_size_greater_than=48877,
                        object_size_less_than=84934,
                        filter_not=[model.LifecycleRuleNot(
                            prefix='aaa',
                            tag=model.Tag(
                                key='key7',
                                value='value7',
                            ),
                        )],
                    ),
                    id='0022012****',
                    expiration=model.LifecycleRuleExpiration(
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                        days=37348,
                        expired_object_delete_marker=False,
                    ),
                    transitions=[model.LifecycleRuleTransition(
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                        days=37348,
                        storage_class=model.StorageClassType.ARCHIVE,
                        is_access_time=True,
                        return_to_std_when_visit=True,
                        allow_small_file=True,
                    ), model.LifecycleRuleTransition(
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                        days=37348,
                        storage_class=model.StorageClassType.COLDARCHIVE,
                        is_access_time=True,
                        return_to_std_when_visit=True,
                        allow_small_file=True,
                    )],
                    noncurrent_version_transitions=[model.NoncurrentVersionTransition(
                        is_access_time=True,
                        return_to_std_when_visit=True,
                        allow_small_file=True,
                        noncurrent_days=80479,
                        storage_class=model.StorageClassType.COLDARCHIVE,
                    ), model.NoncurrentVersionTransition(
                        is_access_time=True,
                        return_to_std_when_visit=True,
                        allow_small_file=True,
                        noncurrent_days=80479,
                        storage_class=model.StorageClassType.ARCHIVE,
                    )],
                    atime_base=97611,
                    prefix='aaa',
                    status='OK',
                    abort_multipart_upload=model.LifecycleRuleAbortMultipartUpload(
                        days=37348,
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                    ),
                )],
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('true', request.allow_same_action_overlap)
        self.assertEqual('key1', request.lifecycle_configuration.rules[0].tags[0].key)
        self.assertEqual('value1', request.lifecycle_configuration.rules[0].tags[0].value)
        self.assertEqual('key12', request.lifecycle_configuration.rules[0].tags[1].key)
        self.assertEqual('value12', request.lifecycle_configuration.rules[0].tags[1].value)
        self.assertEqual(80479, request.lifecycle_configuration.rules[0].noncurrent_version_expiration.noncurrent_days)
        self.assertEqual(48877, request.lifecycle_configuration.rules[0].filter.object_size_greater_than)
        self.assertEqual(84934, request.lifecycle_configuration.rules[0].filter.object_size_less_than)
        self.assertEqual('aaa', request.lifecycle_configuration.rules[0].filter.filter_not[0].prefix)
        self.assertEqual('key3', request.lifecycle_configuration.rules[0].filter.filter_not[0].tag.key)
        self.assertEqual('value3', request.lifecycle_configuration.rules[0].filter.filter_not[0].tag.value)
        self.assertEqual('bbb', request.lifecycle_configuration.rules[0].filter.filter_not[1].prefix)
        self.assertEqual('key4', request.lifecycle_configuration.rules[0].filter.filter_not[1].tag.key)
        self.assertEqual('value4', request.lifecycle_configuration.rules[0].filter.filter_not[1].tag.value)
        self.assertEqual('0022012****', request.lifecycle_configuration.rules[0].id)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657), request.lifecycle_configuration.rules[0].expiration.created_before_date)
        self.assertEqual('2023-12-17T00:20:57.000Z', request.lifecycle_configuration.rules[0].expiration.created_before_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual(37348, request.lifecycle_configuration.rules[0].expiration.days)
        self.assertEqual(False, request.lifecycle_configuration.rules[0].expiration.expired_object_delete_marker)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657), request.lifecycle_configuration.rules[0].transitions[0].created_before_date)
        self.assertEqual('2023-12-17T00:20:57.000Z', request.lifecycle_configuration.rules[0].transitions[0].created_before_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual(37348, request.lifecycle_configuration.rules[0].transitions[0].days)
        self.assertEqual('ColdArchive', request.lifecycle_configuration.rules[0].transitions[0].storage_class)
        self.assertEqual(False, request.lifecycle_configuration.rules[0].transitions[0].is_access_time)
        self.assertEqual(False, request.lifecycle_configuration.rules[0].transitions[0].return_to_std_when_visit)
        self.assertEqual(True, request.lifecycle_configuration.rules[0].transitions[0].allow_small_file)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657), request.lifecycle_configuration.rules[0].transitions[1].created_before_date)
        self.assertEqual('2023-12-17T00:20:57.000Z', request.lifecycle_configuration.rules[0].transitions[1].created_before_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual(37348, request.lifecycle_configuration.rules[0].transitions[1].days)
        self.assertEqual('DeepColdArchive', request.lifecycle_configuration.rules[0].transitions[1].storage_class)
        self.assertEqual(False, request.lifecycle_configuration.rules[0].transitions[1].is_access_time)
        self.assertEqual(True, request.lifecycle_configuration.rules[0].transitions[1].return_to_std_when_visit)
        self.assertEqual(True, request.lifecycle_configuration.rules[0].transitions[1].allow_small_file)
        self.assertEqual(False, request.lifecycle_configuration.rules[0].noncurrent_version_transitions[0].is_access_time)
        self.assertEqual(True, request.lifecycle_configuration.rules[0].noncurrent_version_transitions[0].return_to_std_when_visit)
        self.assertEqual(True, request.lifecycle_configuration.rules[0].noncurrent_version_transitions[0].allow_small_file)
        self.assertEqual(80479, request.lifecycle_configuration.rules[0].noncurrent_version_transitions[0].noncurrent_days)
        self.assertEqual('DeepColdArchive', request.lifecycle_configuration.rules[0].noncurrent_version_transitions[0].storage_class)
        self.assertEqual(True, request.lifecycle_configuration.rules[0].noncurrent_version_transitions[1].is_access_time)
        self.assertEqual(True, request.lifecycle_configuration.rules[0].noncurrent_version_transitions[1].return_to_std_when_visit)
        self.assertEqual(True, request.lifecycle_configuration.rules[0].noncurrent_version_transitions[1].allow_small_file)
        self.assertEqual(80479, request.lifecycle_configuration.rules[0].noncurrent_version_transitions[1].noncurrent_days)
        self.assertEqual('DeepColdArchive', request.lifecycle_configuration.rules[0].noncurrent_version_transitions[1].storage_class)
        self.assertEqual(97611, request.lifecycle_configuration.rules[0].atime_base)
        self.assertEqual('aaa', request.lifecycle_configuration.rules[0].prefix)
        self.assertEqual('OK', request.lifecycle_configuration.rules[0].status)
        self.assertEqual(37348, request.lifecycle_configuration.rules[0].abort_multipart_upload.days)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657), request.lifecycle_configuration.rules[0].abort_multipart_upload.created_before_date)
        self.assertEqual('2023-12-17T00:20:57.000Z', request.lifecycle_configuration.rules[0].abort_multipart_upload.created_before_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('key5', request.lifecycle_configuration.rules[1].tags[0].key)
        self.assertEqual('value5', request.lifecycle_configuration.rules[1].tags[0].value)
        self.assertEqual('key6', request.lifecycle_configuration.rules[1].tags[1].key)
        self.assertEqual('value6', request.lifecycle_configuration.rules[1].tags[1].value)
        self.assertEqual(80479, request.lifecycle_configuration.rules[1].noncurrent_version_expiration.noncurrent_days)
        self.assertEqual(48877, request.lifecycle_configuration.rules[1].filter.object_size_greater_than)
        self.assertEqual(84934, request.lifecycle_configuration.rules[1].filter.object_size_less_than)
        self.assertEqual('aaa', request.lifecycle_configuration.rules[1].filter.filter_not[0].prefix)
        self.assertEqual('key7', request.lifecycle_configuration.rules[1].filter.filter_not[0].tag.key)
        self.assertEqual('value7', request.lifecycle_configuration.rules[1].filter.filter_not[0].tag.value)
        self.assertEqual('0022012****', request.lifecycle_configuration.rules[1].id)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657), request.lifecycle_configuration.rules[1].expiration.created_before_date)
        self.assertEqual('2023-12-17T00:20:57.000Z', request.lifecycle_configuration.rules[1].expiration.created_before_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual(37348, request.lifecycle_configuration.rules[1].expiration.days)
        self.assertEqual(False, request.lifecycle_configuration.rules[1].expiration.expired_object_delete_marker)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657), request.lifecycle_configuration.rules[1].transitions[0].created_before_date)
        self.assertEqual('2023-12-17T00:20:57.000Z', request.lifecycle_configuration.rules[1].transitions[0].created_before_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual(37348, request.lifecycle_configuration.rules[1].transitions[0].days)
        self.assertEqual('Archive', request.lifecycle_configuration.rules[1].transitions[0].storage_class)
        self.assertEqual(True, request.lifecycle_configuration.rules[1].transitions[0].is_access_time)
        self.assertEqual(True, request.lifecycle_configuration.rules[1].transitions[0].return_to_std_when_visit)
        self.assertEqual(True, request.lifecycle_configuration.rules[1].transitions[0].allow_small_file)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657), request.lifecycle_configuration.rules[1].transitions[1].created_before_date)
        self.assertEqual('2023-12-17T00:20:57.000Z', request.lifecycle_configuration.rules[1].transitions[1].created_before_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual(37348, request.lifecycle_configuration.rules[1].transitions[1].days)
        self.assertEqual('ColdArchive', request.lifecycle_configuration.rules[1].transitions[1].storage_class)
        self.assertEqual(True, request.lifecycle_configuration.rules[1].transitions[1].is_access_time)
        self.assertEqual(True, request.lifecycle_configuration.rules[1].transitions[1].return_to_std_when_visit)
        self.assertEqual(True, request.lifecycle_configuration.rules[1].transitions[1].allow_small_file)
        self.assertEqual(True, request.lifecycle_configuration.rules[1].noncurrent_version_transitions[0].is_access_time)
        self.assertEqual(True, request.lifecycle_configuration.rules[1].noncurrent_version_transitions[0].return_to_std_when_visit)
        self.assertEqual(True, request.lifecycle_configuration.rules[1].noncurrent_version_transitions[0].allow_small_file)
        self.assertEqual(80479, request.lifecycle_configuration.rules[1].noncurrent_version_transitions[0].noncurrent_days)
        self.assertEqual('ColdArchive', request.lifecycle_configuration.rules[1].noncurrent_version_transitions[0].storage_class)
        self.assertEqual(True, request.lifecycle_configuration.rules[1].noncurrent_version_transitions[1].is_access_time)
        self.assertEqual(True, request.lifecycle_configuration.rules[1].noncurrent_version_transitions[1].return_to_std_when_visit)
        self.assertEqual(True, request.lifecycle_configuration.rules[1].noncurrent_version_transitions[1].allow_small_file)
        self.assertEqual(80479, request.lifecycle_configuration.rules[1].noncurrent_version_transitions[1].noncurrent_days)
        self.assertEqual('Archive', request.lifecycle_configuration.rules[1].noncurrent_version_transitions[1].storage_class)
        self.assertEqual(97611, request.lifecycle_configuration.rules[1].atime_base)
        self.assertEqual('aaa', request.lifecycle_configuration.rules[1].prefix)
        self.assertEqual('OK', request.lifecycle_configuration.rules[1].status)
        self.assertEqual(37348, request.lifecycle_configuration.rules[1].abort_multipart_upload.days)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657), request.lifecycle_configuration.rules[1].abort_multipart_upload.created_before_date)
        self.assertEqual('2023-12-17T00:20:57.000Z', request.lifecycle_configuration.rules[1].abort_multipart_upload.created_before_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))


        request = model.PutBucketLifecycleRequest(
            bucket='bucketexampletest',
            allow_same_action_overlap='false',
            lifecycle_configuration=model.LifecycleConfiguration(
                rules=[model.LifecycleRule(
                    transitions=[model.LifecycleRuleTransition(
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                        days=37348,
                        storage_class='Standard',
                        is_access_time=True,
                        return_to_std_when_visit=True,
                        allow_small_file=True,
                    ), model.LifecycleRuleTransition(
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                        days=37348,
                        storage_class='DeepColdArchive',
                        is_access_time=True,
                        return_to_std_when_visit=True,
                        allow_small_file=True,
                    )],
                    noncurrent_version_transitions=[model.NoncurrentVersionTransition(
                        is_access_time=True,
                        return_to_std_when_visit=True,
                        allow_small_file=True,
                        noncurrent_days=80479,
                        storage_class='DeepColdArchive',
                    ), model.NoncurrentVersionTransition(
                        is_access_time=True,
                        return_to_std_when_visit=True,
                        allow_small_file=True,
                        noncurrent_days=80479,
                        storage_class='Archive',
                    )],
                ), model.LifecycleRule(
                    transitions=[model.LifecycleRuleTransition(
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                        days=37348,
                        storage_class='ColdArchive',
                        is_access_time=True,
                        return_to_std_when_visit=True,
                        allow_small_file=True,
                    ), model.LifecycleRuleTransition(
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                        days=37348,
                        storage_class='IA',
                        is_access_time=True,
                        return_to_std_when_visit=True,
                        allow_small_file=True,
                    )],
                    noncurrent_version_transitions=[model.NoncurrentVersionTransition(
                        is_access_time=True,
                        return_to_std_when_visit=True,
                        allow_small_file=True,
                        noncurrent_days=80479,
                        storage_class='IA',
                    ), model.NoncurrentVersionTransition(
                        is_access_time=True,
                        return_to_std_when_visit=True,
                        allow_small_file=True,
                        noncurrent_days=80479,
                        storage_class='ColdArchive',
                    )],
                )],
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('false', request.allow_same_action_overlap)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657), request.lifecycle_configuration.rules[0].transitions[0].created_before_date)
        self.assertEqual('2023-12-17T00:20:57.000Z', request.lifecycle_configuration.rules[0].transitions[0].created_before_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual(37348, request.lifecycle_configuration.rules[0].transitions[0].days)
        self.assertEqual('Standard', request.lifecycle_configuration.rules[0].transitions[0].storage_class)
        self.assertEqual(True, request.lifecycle_configuration.rules[0].transitions[0].is_access_time)
        self.assertEqual(True, request.lifecycle_configuration.rules[0].transitions[0].return_to_std_when_visit)
        self.assertEqual(True, request.lifecycle_configuration.rules[0].transitions[0].allow_small_file)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657), request.lifecycle_configuration.rules[0].transitions[1].created_before_date)
        self.assertEqual('2023-12-17T00:20:57.000Z', request.lifecycle_configuration.rules[0].transitions[1].created_before_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual(37348, request.lifecycle_configuration.rules[0].transitions[1].days)
        self.assertEqual('DeepColdArchive', request.lifecycle_configuration.rules[0].transitions[1].storage_class)
        self.assertEqual(True, request.lifecycle_configuration.rules[0].transitions[1].is_access_time)
        self.assertEqual(True, request.lifecycle_configuration.rules[0].transitions[1].return_to_std_when_visit)
        self.assertEqual(True, request.lifecycle_configuration.rules[0].transitions[1].allow_small_file)
        self.assertEqual(True, request.lifecycle_configuration.rules[0].noncurrent_version_transitions[0].is_access_time)
        self.assertEqual(True, request.lifecycle_configuration.rules[0].noncurrent_version_transitions[0].return_to_std_when_visit)
        self.assertEqual(True, request.lifecycle_configuration.rules[0].noncurrent_version_transitions[0].allow_small_file)
        self.assertEqual(80479, request.lifecycle_configuration.rules[0].noncurrent_version_transitions[0].noncurrent_days)
        self.assertEqual('DeepColdArchive', request.lifecycle_configuration.rules[0].noncurrent_version_transitions[0].storage_class)
        self.assertEqual(True, request.lifecycle_configuration.rules[0].noncurrent_version_transitions[1].is_access_time)
        self.assertEqual(True, request.lifecycle_configuration.rules[0].noncurrent_version_transitions[1].return_to_std_when_visit)
        self.assertEqual(True, request.lifecycle_configuration.rules[0].noncurrent_version_transitions[1].allow_small_file)
        self.assertEqual(80479, request.lifecycle_configuration.rules[0].noncurrent_version_transitions[1].noncurrent_days)
        self.assertEqual('Archive', request.lifecycle_configuration.rules[0].noncurrent_version_transitions[1].storage_class)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657), request.lifecycle_configuration.rules[1].transitions[0].created_before_date)
        self.assertEqual('2023-12-17T00:20:57.000Z', request.lifecycle_configuration.rules[1].transitions[0].created_before_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual(37348, request.lifecycle_configuration.rules[1].transitions[0].days)
        self.assertEqual('ColdArchive', request.lifecycle_configuration.rules[1].transitions[0].storage_class)
        self.assertEqual(True, request.lifecycle_configuration.rules[1].transitions[0].is_access_time)
        self.assertEqual(True, request.lifecycle_configuration.rules[1].transitions[0].return_to_std_when_visit)
        self.assertEqual(True, request.lifecycle_configuration.rules[1].transitions[0].allow_small_file)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657), request.lifecycle_configuration.rules[1].transitions[1].created_before_date)
        self.assertEqual('2023-12-17T00:20:57.000Z', request.lifecycle_configuration.rules[1].transitions[1].created_before_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual(37348, request.lifecycle_configuration.rules[1].transitions[1].days)
        self.assertEqual('IA', request.lifecycle_configuration.rules[1].transitions[1].storage_class)
        self.assertEqual(True, request.lifecycle_configuration.rules[1].transitions[1].is_access_time)
        self.assertEqual(True, request.lifecycle_configuration.rules[1].transitions[1].return_to_std_when_visit)
        self.assertEqual(True, request.lifecycle_configuration.rules[1].transitions[1].allow_small_file)
        self.assertEqual(True, request.lifecycle_configuration.rules[1].noncurrent_version_transitions[0].is_access_time)
        self.assertEqual(True, request.lifecycle_configuration.rules[1].noncurrent_version_transitions[0].return_to_std_when_visit)
        self.assertEqual(True, request.lifecycle_configuration.rules[1].noncurrent_version_transitions[0].allow_small_file)
        self.assertEqual(80479, request.lifecycle_configuration.rules[1].noncurrent_version_transitions[0].noncurrent_days)
        self.assertEqual('IA', request.lifecycle_configuration.rules[1].noncurrent_version_transitions[0].storage_class)
        self.assertEqual(True, request.lifecycle_configuration.rules[1].noncurrent_version_transitions[1].is_access_time)
        self.assertEqual(True, request.lifecycle_configuration.rules[1].noncurrent_version_transitions[1].return_to_std_when_visit)
        self.assertEqual(True, request.lifecycle_configuration.rules[1].noncurrent_version_transitions[1].allow_small_file)
        self.assertEqual(80479, request.lifecycle_configuration.rules[1].noncurrent_version_transitions[1].noncurrent_days)
        self.assertEqual('ColdArchive', request.lifecycle_configuration.rules[1].noncurrent_version_transitions[1].storage_class)


    def test_serialize_request(self):
        request = model.PutBucketLifecycleRequest(
            bucket='bucketexampletest',
            allow_same_action_overlap='false',
            lifecycle_configuration=model.LifecycleConfiguration(
                rules=[model.LifecycleRule(
                    id='0022012****',
                    expiration=model.LifecycleRuleExpiration(
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                        days=37348,
                        expired_object_delete_marker=False,
                    ),
                    transitions=[model.LifecycleRuleTransition(
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                        days=37348,
                        storage_class='Standard',
                        is_access_time=True,
                        return_to_std_when_visit=True,
                        allow_small_file=True,
                    )],
                    noncurrent_version_transitions=[model.NoncurrentVersionTransition(
                        is_access_time=True,
                        return_to_std_when_visit=True,
                        allow_small_file=True,
                        noncurrent_days=80479,
                        storage_class='DeepColdArchive',
                    )],
                )],
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutBucketLifecycle',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutBucketLifecycle', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.PutBucketLifecycleResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutBucketLifecycleResult()
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


class TestGetBucketLifecycle(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketLifecycleRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetBucketLifecycleRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.GetBucketLifecycleRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketLifecycle',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetBucketLifecycle', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetBucketLifecycleResult()
        self.assertIsNone(result.lifecycle_configuration)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketLifecycleResult(
            lifecycle_configuration=model.LifecycleConfiguration(
                rules=[model.LifecycleRule(
                    tags=[model.Tag(
                        key='key1',
                        value='value1',
                    ), model.Tag(
                        key='key2',
                        value='value2',
                    )],
                    noncurrent_version_expiration=model.NoncurrentVersionExpiration(
                        noncurrent_days=55959,
                    ),
                    filter=model.LifecycleRuleFilter(
                        object_size_greater_than=16967,
                        object_size_less_than=68626,
                        filter_not=[model.LifecycleRuleNot(
                            prefix='aaa',
                            tag=model.Tag(
                                key='key3',
                                value='value3',
                            ),
                        ), model.LifecycleRuleNot(
                            prefix='bbb',
                            tag=model.Tag(
                                key='key4',
                                value='value4',
                            ),
                        )],
                    ),
                    id='0022012****',
                    expiration=model.LifecycleRuleExpiration(
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                        days=12590,
                        expired_object_delete_marker=True,
                    ),
                    transitions=[model.LifecycleRuleTransition(
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                        days=12590,
                        storage_class=model.StorageClassType.IA,
                        is_access_time=False,
                        return_to_std_when_visit=True,
                        allow_small_file=False,
                    ), model.LifecycleRuleTransition(
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                        days=12590,
                        storage_class=model.StorageClassType.IA,
                        is_access_time=True,
                        return_to_std_when_visit=True,
                        allow_small_file=False,
                    )],
                    noncurrent_version_transitions=[model.NoncurrentVersionTransition(
                        is_access_time=True,
                        return_to_std_when_visit=True,
                        allow_small_file=True,
                        noncurrent_days=55959,
                        storage_class=model.StorageClassType.STANDARD,
                    ), model.NoncurrentVersionTransition(
                        is_access_time=True,
                        return_to_std_when_visit=True,
                        allow_small_file=True,
                        noncurrent_days=55959,
                        storage_class=model.StorageClassType.COLDARCHIVE,
                    )],
                    atime_base=69470,
                    prefix='aaa',
                    status='OK',
                    abort_multipart_upload=model.LifecycleRuleAbortMultipartUpload(
                        days=12590,
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                    ),
                ), model.LifecycleRule(
                    tags=[model.Tag(
                        key='key5',
                        value='value5',
                    ), model.Tag(
                        key='key6',
                        value='value6',
                    )],
                    noncurrent_version_expiration=model.NoncurrentVersionExpiration(
                        noncurrent_days=55959,
                    ),
                    filter=model.LifecycleRuleFilter(
                        object_size_greater_than=16967,
                        object_size_less_than=68626,
                        filter_not=[model.LifecycleRuleNot(
                            prefix='aaa',
                            tag=model.Tag(
                                key='key7',
                                value='value7',
                            ),
                        )],
                    ),
                    id='0022012****',
                    expiration=model.LifecycleRuleExpiration(
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                        days=12590,
                        expired_object_delete_marker=True,
                    ),
                    transitions=[model.LifecycleRuleTransition(
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                        days=12590,
                        storage_class=model.StorageClassType.IA,
                        is_access_time=True,
                        return_to_std_when_visit=True,
                        allow_small_file=True,
                    ), model.LifecycleRuleTransition(
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                        days=12590,
                        storage_class=model.StorageClassType.STANDARD,
                        is_access_time=True,
                        return_to_std_when_visit=True,
                        allow_small_file=True,
                    )],
                    noncurrent_version_transitions=[model.NoncurrentVersionTransition(
                        is_access_time=True,
                        return_to_std_when_visit=True,
                        allow_small_file=True,
                        noncurrent_days=55959,
                        storage_class=model.StorageClassType.STANDARD,
                    ), model.NoncurrentVersionTransition(
                        is_access_time=True,
                        return_to_std_when_visit=True,
                        allow_small_file=True,
                        noncurrent_days=55959,
                        storage_class=model.StorageClassType.ARCHIVE,
                    )],
                    atime_base=69470,
                    prefix='aaa',
                    status='OK',
                    abort_multipart_upload=model.LifecycleRuleAbortMultipartUpload(
                        days=12590,
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                    ),
                )],
            ),
        )
        self.assertEqual('key1', result.lifecycle_configuration.rules[0].tags[0].key)
        self.assertEqual('value1', result.lifecycle_configuration.rules[0].tags[0].value)
        self.assertEqual('key2', result.lifecycle_configuration.rules[0].tags[1].key)
        self.assertEqual('value2', result.lifecycle_configuration.rules[0].tags[1].value)
        self.assertEqual(55959, result.lifecycle_configuration.rules[0].noncurrent_version_expiration.noncurrent_days)
        self.assertEqual(16967, result.lifecycle_configuration.rules[0].filter.object_size_greater_than)
        self.assertEqual(68626, result.lifecycle_configuration.rules[0].filter.object_size_less_than)
        self.assertEqual('aaa', result.lifecycle_configuration.rules[0].filter.filter_not[0].prefix)
        self.assertEqual('key3', result.lifecycle_configuration.rules[0].filter.filter_not[0].tag.key)
        self.assertEqual('value3', result.lifecycle_configuration.rules[0].filter.filter_not[0].tag.value)
        self.assertEqual('bbb', result.lifecycle_configuration.rules[0].filter.filter_not[1].prefix)
        self.assertEqual('key4', result.lifecycle_configuration.rules[0].filter.filter_not[1].tag.key)
        self.assertEqual('value4', result.lifecycle_configuration.rules[0].filter.filter_not[1].tag.value)
        self.assertEqual('0022012****', result.lifecycle_configuration.rules[0].id)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657), result.lifecycle_configuration.rules[0].expiration.created_before_date)
        self.assertEqual('2023-12-17T00:20:57.000Z', result.lifecycle_configuration.rules[0].expiration.created_before_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual(12590, result.lifecycle_configuration.rules[0].expiration.days)
        self.assertEqual(True, result.lifecycle_configuration.rules[0].expiration.expired_object_delete_marker)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657), result.lifecycle_configuration.rules[0].transitions[0].created_before_date)
        self.assertEqual('2023-12-17T00:20:57.000Z', result.lifecycle_configuration.rules[0].transitions[0].created_before_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual(12590, result.lifecycle_configuration.rules[0].transitions[0].days)
        self.assertEqual('IA', result.lifecycle_configuration.rules[0].transitions[0].storage_class)
        self.assertEqual(False, result.lifecycle_configuration.rules[0].transitions[0].is_access_time)
        self.assertEqual(True, result.lifecycle_configuration.rules[0].transitions[0].return_to_std_when_visit)
        self.assertEqual(False, result.lifecycle_configuration.rules[0].transitions[0].allow_small_file)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657), result.lifecycle_configuration.rules[0].transitions[1].created_before_date)
        self.assertEqual('2023-12-17T00:20:57.000Z', result.lifecycle_configuration.rules[0].transitions[1].created_before_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual(12590, result.lifecycle_configuration.rules[0].transitions[1].days)
        self.assertEqual('IA', result.lifecycle_configuration.rules[0].transitions[1].storage_class)
        self.assertEqual(True, result.lifecycle_configuration.rules[0].transitions[1].is_access_time)
        self.assertEqual(True, result.lifecycle_configuration.rules[0].transitions[1].return_to_std_when_visit)
        self.assertEqual(False, result.lifecycle_configuration.rules[0].transitions[1].allow_small_file)
        self.assertEqual(True, result.lifecycle_configuration.rules[0].noncurrent_version_transitions[0].is_access_time)
        self.assertEqual(True, result.lifecycle_configuration.rules[0].noncurrent_version_transitions[0].return_to_std_when_visit)
        self.assertEqual(True, result.lifecycle_configuration.rules[0].noncurrent_version_transitions[0].allow_small_file)
        self.assertEqual(55959, result.lifecycle_configuration.rules[0].noncurrent_version_transitions[0].noncurrent_days)
        self.assertEqual('Standard', result.lifecycle_configuration.rules[0].noncurrent_version_transitions[0].storage_class)
        self.assertEqual(True, result.lifecycle_configuration.rules[0].noncurrent_version_transitions[1].is_access_time)
        self.assertEqual(True, result.lifecycle_configuration.rules[0].noncurrent_version_transitions[1].return_to_std_when_visit)
        self.assertEqual(True, result.lifecycle_configuration.rules[0].noncurrent_version_transitions[1].allow_small_file)
        self.assertEqual(55959, result.lifecycle_configuration.rules[0].noncurrent_version_transitions[1].noncurrent_days)
        self.assertEqual('ColdArchive', result.lifecycle_configuration.rules[0].noncurrent_version_transitions[1].storage_class)
        self.assertEqual(69470, result.lifecycle_configuration.rules[0].atime_base)
        self.assertEqual('aaa', result.lifecycle_configuration.rules[0].prefix)
        self.assertEqual('OK', result.lifecycle_configuration.rules[0].status)
        self.assertEqual(12590, result.lifecycle_configuration.rules[0].abort_multipart_upload.days)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657), result.lifecycle_configuration.rules[0].abort_multipart_upload.created_before_date)
        self.assertEqual('2023-12-17T00:20:57.000Z', result.lifecycle_configuration.rules[0].abort_multipart_upload.created_before_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('key5', result.lifecycle_configuration.rules[1].tags[0].key)
        self.assertEqual('value5', result.lifecycle_configuration.rules[1].tags[0].value)
        self.assertEqual('key6', result.lifecycle_configuration.rules[1].tags[1].key)
        self.assertEqual('value6', result.lifecycle_configuration.rules[1].tags[1].value)
        self.assertEqual(55959, result.lifecycle_configuration.rules[1].noncurrent_version_expiration.noncurrent_days)
        self.assertEqual(16967, result.lifecycle_configuration.rules[1].filter.object_size_greater_than)
        self.assertEqual(68626, result.lifecycle_configuration.rules[1].filter.object_size_less_than)
        self.assertEqual('aaa', result.lifecycle_configuration.rules[1].filter.filter_not[0].prefix)
        self.assertEqual('key7', result.lifecycle_configuration.rules[1].filter.filter_not[0].tag.key)
        self.assertEqual('value7', result.lifecycle_configuration.rules[1].filter.filter_not[0].tag.value)
        self.assertEqual('0022012****', result.lifecycle_configuration.rules[1].id)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657), result.lifecycle_configuration.rules[1].expiration.created_before_date)
        self.assertEqual('2023-12-17T00:20:57.000Z', result.lifecycle_configuration.rules[1].expiration.created_before_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual(12590, result.lifecycle_configuration.rules[1].expiration.days)
        self.assertEqual(True, result.lifecycle_configuration.rules[1].expiration.expired_object_delete_marker)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657), result.lifecycle_configuration.rules[1].transitions[0].created_before_date)
        self.assertEqual('2023-12-17T00:20:57.000Z', result.lifecycle_configuration.rules[1].transitions[0].created_before_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual(12590, result.lifecycle_configuration.rules[1].transitions[0].days)
        self.assertEqual('IA', result.lifecycle_configuration.rules[1].transitions[0].storage_class)
        self.assertEqual(True, result.lifecycle_configuration.rules[1].transitions[0].is_access_time)
        self.assertEqual(True, result.lifecycle_configuration.rules[1].transitions[0].return_to_std_when_visit)
        self.assertEqual(True, result.lifecycle_configuration.rules[1].transitions[0].allow_small_file)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657), result.lifecycle_configuration.rules[1].transitions[1].created_before_date)
        self.assertEqual('2023-12-17T00:20:57.000Z', result.lifecycle_configuration.rules[1].transitions[1].created_before_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual(12590, result.lifecycle_configuration.rules[1].transitions[1].days)
        self.assertEqual('Standard', result.lifecycle_configuration.rules[1].transitions[1].storage_class)
        self.assertEqual(True, result.lifecycle_configuration.rules[1].transitions[1].is_access_time)
        self.assertEqual(True, result.lifecycle_configuration.rules[1].transitions[1].return_to_std_when_visit)
        self.assertEqual(True, result.lifecycle_configuration.rules[1].transitions[1].allow_small_file)
        self.assertEqual(True, result.lifecycle_configuration.rules[1].noncurrent_version_transitions[0].is_access_time)
        self.assertEqual(True, result.lifecycle_configuration.rules[1].noncurrent_version_transitions[0].return_to_std_when_visit)
        self.assertEqual(True, result.lifecycle_configuration.rules[1].noncurrent_version_transitions[0].allow_small_file)
        self.assertEqual(55959, result.lifecycle_configuration.rules[1].noncurrent_version_transitions[0].noncurrent_days)
        self.assertEqual('Standard', result.lifecycle_configuration.rules[1].noncurrent_version_transitions[0].storage_class)
        self.assertEqual(True, result.lifecycle_configuration.rules[1].noncurrent_version_transitions[1].is_access_time)
        self.assertEqual(True, result.lifecycle_configuration.rules[1].noncurrent_version_transitions[1].return_to_std_when_visit)
        self.assertEqual(True, result.lifecycle_configuration.rules[1].noncurrent_version_transitions[1].allow_small_file)
        self.assertEqual(55959, result.lifecycle_configuration.rules[1].noncurrent_version_transitions[1].noncurrent_days)
        self.assertEqual('Archive', result.lifecycle_configuration.rules[1].noncurrent_version_transitions[1].storage_class)
        self.assertEqual(69470, result.lifecycle_configuration.rules[1].atime_base)
        self.assertEqual('aaa', result.lifecycle_configuration.rules[1].prefix)
        self.assertEqual('OK', result.lifecycle_configuration.rules[1].status)
        self.assertEqual(12590, result.lifecycle_configuration.rules[1].abort_multipart_upload.days)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657), result.lifecycle_configuration.rules[1].abort_multipart_upload.created_before_date)
        self.assertEqual('2023-12-17T00:20:57.000Z', result.lifecycle_configuration.rules[1].abort_multipart_upload.created_before_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))


        result = model.GetBucketLifecycleResult(
            lifecycle_configuration=model.LifecycleConfiguration(
                rules=[model.LifecycleRule(
                    tags=[model.Tag(
                        key='key1',
                        value='value1',
                    )],
                    noncurrent_version_expiration=model.NoncurrentVersionExpiration(
                        noncurrent_days=55959,
                    ),
                    filter=model.LifecycleRuleFilter(
                        object_size_greater_than=16967,
                        object_size_less_than=68626,
                        filter_not=[model.LifecycleRuleNot(
                            prefix='aaa',
                        )],
                    ),
                    id='0022012****',
                    expiration=model.LifecycleRuleExpiration(
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                        days=12590,
                        expired_object_delete_marker=True,
                    ),
                    transitions=[model.LifecycleRuleTransition(
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                        days=12590,
                        storage_class='Archive',
                        is_access_time=True,
                        return_to_std_when_visit=True,
                        allow_small_file=True,
                    )],
                    noncurrent_version_transitions=[model.NoncurrentVersionTransition(
                        is_access_time=True,
                        return_to_std_when_visit=True,
                        allow_small_file=True,
                        noncurrent_days=55959,
                        storage_class='Archive',
                    )],
                    atime_base=69470,
                    prefix='aaa',
                    status='OK',
                    abort_multipart_upload=model.LifecycleRuleAbortMultipartUpload(
                        days=12590,
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                    ),
                )],
            ),
        )
        self.assertEqual('key1', result.lifecycle_configuration.rules[0].tags[0].key)
        self.assertEqual('value1', result.lifecycle_configuration.rules[0].tags[0].value)
        self.assertEqual(55959, result.lifecycle_configuration.rules[0].noncurrent_version_expiration.noncurrent_days)
        self.assertEqual(16967, result.lifecycle_configuration.rules[0].filter.object_size_greater_than)
        self.assertEqual(68626, result.lifecycle_configuration.rules[0].filter.object_size_less_than)
        self.assertEqual('aaa', result.lifecycle_configuration.rules[0].filter.filter_not[0].prefix)
        self.assertEqual('0022012****', result.lifecycle_configuration.rules[0].id)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657), result.lifecycle_configuration.rules[0].expiration.created_before_date)
        self.assertEqual('2023-12-17T00:20:57.000Z', result.lifecycle_configuration.rules[0].expiration.created_before_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual(12590, result.lifecycle_configuration.rules[0].expiration.days)
        self.assertEqual(True, result.lifecycle_configuration.rules[0].expiration.expired_object_delete_marker)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657), result.lifecycle_configuration.rules[0].transitions[0].created_before_date)
        self.assertEqual('2023-12-17T00:20:57.000Z', result.lifecycle_configuration.rules[0].transitions[0].created_before_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual(12590, result.lifecycle_configuration.rules[0].transitions[0].days)
        self.assertEqual('Archive', result.lifecycle_configuration.rules[0].transitions[0].storage_class)
        self.assertEqual(True, result.lifecycle_configuration.rules[0].transitions[0].is_access_time)
        self.assertEqual(True, result.lifecycle_configuration.rules[0].transitions[0].return_to_std_when_visit)
        self.assertEqual(True, result.lifecycle_configuration.rules[0].transitions[0].allow_small_file)
        self.assertEqual(True, result.lifecycle_configuration.rules[0].noncurrent_version_transitions[0].is_access_time)
        self.assertEqual(True, result.lifecycle_configuration.rules[0].noncurrent_version_transitions[0].return_to_std_when_visit)
        self.assertEqual(True, result.lifecycle_configuration.rules[0].noncurrent_version_transitions[0].allow_small_file)
        self.assertEqual(55959, result.lifecycle_configuration.rules[0].noncurrent_version_transitions[0].noncurrent_days)
        self.assertEqual('Archive', result.lifecycle_configuration.rules[0].noncurrent_version_transitions[0].storage_class)
        self.assertEqual(69470, result.lifecycle_configuration.rules[0].atime_base)
        self.assertEqual('aaa', result.lifecycle_configuration.rules[0].prefix)
        self.assertEqual('OK', result.lifecycle_configuration.rules[0].status)
        self.assertEqual(12590, result.lifecycle_configuration.rules[0].abort_multipart_upload.days)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657), result.lifecycle_configuration.rules[0].abort_multipart_upload.created_before_date)
        self.assertEqual('2023-12-17T00:20:57.000Z', result.lifecycle_configuration.rules[0].abort_multipart_upload.created_before_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))

    def test_deserialize_result(self):
        xml_data = r'''
         <LifecycleConfiguration>
         </LifecycleConfiguration>'''

        result = model.GetBucketLifecycleResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
         <LifecycleConfiguration>
             <Rule>
                 <ID>delete after one day</ID>
                 <Prefix>logs1/</Prefix>
                 <Status>Enabled</Status>
                 <Expiration>
                     <CreatedBeforeDate>2020-06-22T11:42:32.000Z</CreatedBeforeDate>
                     <Days>1</Days>
                     <ExpiredObjectDeleteMarker>true</ExpiredObjectDeleteMarker>
                 </Expiration>
                 <AbortMultipartUpload>
                     <Days>30</Days>
                 </AbortMultipartUpload>
             </Rule>
             <Rule>
                 <ID>atime transition1</ID>
                 <Prefix>logs1/</Prefix>
                 <Status>Enabled</Status>
                 <Transition>
                     <Days>30</Days>
                     <StorageClass>IA</StorageClass>
                     <IsAccessTime>true</IsAccessTime>
                     <ReturnToStdWhenVisit>false</ReturnToStdWhenVisit>
                 </Transition>
                 <Transition>
                     <Days>33</Days>
                     <StorageClass>Archive</StorageClass>
                     <IsAccessTime>false</IsAccessTime>
                     <ReturnToStdWhenVisit>true</ReturnToStdWhenVisit>
                 </Transition>
                 <AtimeBase>1631698332</AtimeBase>
             </Rule>
             <Rule>
                 <ID>atime transition2</ID>
                 <Prefix>logs2/</Prefix>
                 <Status>Enabled</Status>
                 <NoncurrentVersionTransition>
                     <NoncurrentDays>10</NoncurrentDays>
                     <StorageClass>IA</StorageClass>
                     <IsAccessTime>true</IsAccessTime>
                     <ReturnToStdWhenVisit>false</ReturnToStdWhenVisit>
                 </NoncurrentVersionTransition>
                <NoncurrentVersionTransition>
                     <NoncurrentDays>103</NoncurrentDays>
                     <StorageClass>DeepColdArchive</StorageClass>
                     <IsAccessTime>false</IsAccessTime>
                     <ReturnToStdWhenVisit>true</ReturnToStdWhenVisit>
                 </NoncurrentVersionTransition>
                 <AtimeBase>1631698332</AtimeBase>
             </Rule>
             <Rule>
                 <ID>RuleID</ID>
                 <Prefix>Prefix</Prefix>
                 <Status>Enabled</Status>
                 <Filter>
                     <ObjectSizeGreaterThan>500</ObjectSizeGreaterThan>
                     <ObjectSizeLessThan>64000</ObjectSizeLessThan>
                     <Not>
                         <Prefix>abc/not1/</Prefix>
                         <Tag>
                             <Key>notkey1</Key>
                             <Value>notvalue1</Value>
                         </Tag>
                     </Not>
                     <Not>
                         <Prefix>abc/not2/</Prefix>
                         <Tag>
                             <Key>notkey2</Key>
                             <Value>notvalue2</Value>
                         </Tag>
                     </Not>
                 </Filter>
             </Rule>
         </LifecycleConfiguration>
         '''

        result = model.GetBucketLifecycleResult()
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
        self.assertEqual('delete after one day', result.lifecycle_configuration.rules[0].id)
        self.assertEqual('logs1/', result.lifecycle_configuration.rules[0].prefix)
        self.assertEqual('Enabled', result.lifecycle_configuration.rules[0].status)
        self.assertEqual('2020-06-22T11:42:32.000Z', result.lifecycle_configuration.rules[0].expiration.created_before_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual(1, result.lifecycle_configuration.rules[0].expiration.days)
        self.assertEqual(True, result.lifecycle_configuration.rules[0].expiration.expired_object_delete_marker)
        self.assertEqual(30, result.lifecycle_configuration.rules[0].abort_multipart_upload.days)
        self.assertEqual('atime transition1', result.lifecycle_configuration.rules[1].id)
        self.assertEqual('logs1/', result.lifecycle_configuration.rules[1].prefix)
        self.assertEqual('Enabled', result.lifecycle_configuration.rules[1].status)
        self.assertEqual(30, result.lifecycle_configuration.rules[1].transitions[0].days)
        self.assertEqual('IA', result.lifecycle_configuration.rules[1].transitions[0].storage_class)
        self.assertEqual(True, result.lifecycle_configuration.rules[1].transitions[0].is_access_time)
        self.assertEqual(False, result.lifecycle_configuration.rules[1].transitions[0].return_to_std_when_visit)
        self.assertEqual(33, result.lifecycle_configuration.rules[1].transitions[1].days)
        self.assertEqual('Archive', result.lifecycle_configuration.rules[1].transitions[1].storage_class)
        self.assertEqual(False, result.lifecycle_configuration.rules[1].transitions[1].is_access_time)
        self.assertEqual(True, result.lifecycle_configuration.rules[1].transitions[1].return_to_std_when_visit)
        self.assertEqual(1631698332, result.lifecycle_configuration.rules[1].atime_base)
        self.assertEqual('atime transition2', result.lifecycle_configuration.rules[2].id)
        self.assertEqual('logs2/', result.lifecycle_configuration.rules[2].prefix)
        self.assertEqual('Enabled', result.lifecycle_configuration.rules[2].status)
        self.assertEqual(10, result.lifecycle_configuration.rules[2].noncurrent_version_transitions[0].noncurrent_days)
        self.assertEqual('IA', result.lifecycle_configuration.rules[2].noncurrent_version_transitions[0].storage_class)
        self.assertEqual(True, result.lifecycle_configuration.rules[2].noncurrent_version_transitions[0].is_access_time)
        self.assertEqual(False, result.lifecycle_configuration.rules[2].noncurrent_version_transitions[0].return_to_std_when_visit)
        self.assertEqual(103, result.lifecycle_configuration.rules[2].noncurrent_version_transitions[1].noncurrent_days)
        self.assertEqual('DeepColdArchive', result.lifecycle_configuration.rules[2].noncurrent_version_transitions[1].storage_class)
        self.assertEqual(False, result.lifecycle_configuration.rules[2].noncurrent_version_transitions[1].is_access_time)
        self.assertEqual(True, result.lifecycle_configuration.rules[2].noncurrent_version_transitions[1].return_to_std_when_visit)
        self.assertEqual(1631698332, result.lifecycle_configuration.rules[2].atime_base)
        self.assertEqual('RuleID', result.lifecycle_configuration.rules[3].id)
        self.assertEqual('Prefix', result.lifecycle_configuration.rules[3].prefix)
        self.assertEqual('Enabled', result.lifecycle_configuration.rules[3].status)
        self.assertEqual(500, result.lifecycle_configuration.rules[3].filter.object_size_greater_than)
        self.assertEqual(64000, result.lifecycle_configuration.rules[3].filter.object_size_less_than)
        self.assertEqual('abc/not1/', result.lifecycle_configuration.rules[3].filter.filter_not[0].prefix)
        self.assertEqual('notkey1', result.lifecycle_configuration.rules[3].filter.filter_not[0].tag.key)
        self.assertEqual('notvalue1', result.lifecycle_configuration.rules[3].filter.filter_not[0].tag.value)
        self.assertEqual('abc/not2/', result.lifecycle_configuration.rules[3].filter.filter_not[1].prefix)
        self.assertEqual('notkey2', result.lifecycle_configuration.rules[3].filter.filter_not[1].tag.key)
        self.assertEqual('notvalue2', result.lifecycle_configuration.rules[3].filter.filter_not[1].tag.value)


class TestDeleteBucketLifecycle(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DeleteBucketLifecycleRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DeleteBucketLifecycleRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)


    def test_serialize_request(self):
        request = model.DeleteBucketLifecycleRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteBucketLifecycle',
            method='DELETE',
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteBucketLifecycle', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.DeleteBucketLifecycleResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.DeleteBucketLifecycleResult()
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