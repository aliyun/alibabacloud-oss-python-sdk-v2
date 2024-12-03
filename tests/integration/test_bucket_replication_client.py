# pylint: skip-file

from typing import cast
import alibabacloud_oss_v2 as oss
from . import TestIntegration, random_bucket_name, RAM_ROLE_NAME, REGION


class TestBucketReplication(TestIntegration):

    def test_bucket_replication(self):
        # create bucket
        bucket_name = random_bucket_name()
        result = self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # put bucket replication
        result = self.client.put_bucket_replication(oss.PutBucketReplicationRequest(
            bucket=bucket_name,
            replication_configuration=oss.ReplicationConfiguration(
                rules=[oss.ReplicationRule(
                    source_selection_criteria=oss.ReplicationSourceSelectionCriteria(
                        sse_kms_encrypted_objects=oss.SseKmsEncryptedObjects(
                            status=oss.StatusType.ENABLED,
                        ),
                    ),
                    rtc=oss.ReplicationTimeControl(
                        status='disabled',
                    ),
                    destination=oss.ReplicationDestination(
                        bucket=self.bucket_name,
                        location=f'oss-{REGION}',
                        transfer_type=oss.TransferType.OSS_ACC,
                    ),
                    historical_object_replication=oss.HistoricalObjectReplicationType.DISABLED,
                    sync_role=RAM_ROLE_NAME,
                    encryption_configuration=oss.ReplicationEncryptionConfiguration(
                        replica_kms_key_id='c4d49f85-ee30-426b-a5ed-95e9139d****',
                    ),
                    prefix_set=oss.ReplicationPrefixSet(
                        prefixs=['aaa/', 'bbb/'],
                    ),
                    action='ALL',
                )],
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))


        # get bucket replication
        result = self.client.get_bucket_replication(oss.GetBucketReplicationRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(oss.StatusType.ENABLED, result.replication_configuration.rules[0].source_selection_criteria.sse_kms_encrypted_objects.status)
        # self.assertEqual('disabled', result.replication_configuration.rules[0].rtc.status)
        self.assertEqual(self.bucket_name, result.replication_configuration.rules[0].destination.bucket)
        self.assertEqual(f'oss-{REGION}', result.replication_configuration.rules[0].destination.location)
        self.assertEqual(oss.TransferType.OSS_ACC, result.replication_configuration.rules[0].destination.transfer_type)
        self.assertEqual(oss.HistoricalObjectReplicationType.DISABLED, result.replication_configuration.rules[0].historical_object_replication)
        self.assertEqual(RAM_ROLE_NAME, result.replication_configuration.rules[0].sync_role)
        self.assertEqual('c4d49f85-ee30-426b-a5ed-95e9139d****', result.replication_configuration.rules[0].encryption_configuration.replica_kms_key_id)
        self.assertEqual(['aaa/', 'bbb/'], result.replication_configuration.rules[0].prefix_set.prefixs)
        self.assertEqual('ALL', result.replication_configuration.rules[0].action)


        id = result.replication_configuration.rules[0].id
        # put bucket rtc
        result = self.client.put_bucket_rtc(oss.PutBucketRtcRequest(
            bucket=bucket_name,
            rtc_configuration=oss.RtcConfiguration(
                rtc=oss.ReplicationTimeControl(
                    status='disabled',
                ),
                id=id,
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket replication location
        result = self.client.get_bucket_replication_location(oss.GetBucketReplicationLocationRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertIsNotNone(result.replication_location.locations)
        self.assertIsNotNone(result.replication_location.location_transfer_type_constraint.location_transfer_types)


        # get bucket replication progress
        result = self.client.get_bucket_replication_progress(oss.GetBucketReplicationProgressRequest(
            bucket=bucket_name,
            rule_id=id,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(id, result.replication_progress.rules[0].id)
        self.assertEqual('aaa/', result.replication_progress.rules[0].prefix_set.prefixs[0])
        self.assertEqual('bbb/', result.replication_progress.rules[0].prefix_set.prefixs[1])
        self.assertEqual('ALL', result.replication_progress.rules[0].action)
        self.assertEqual(self.bucket_name, result.replication_progress.rules[0].destination.bucket)
        self.assertEqual(f'oss-{REGION}', result.replication_progress.rules[0].destination.location)
        self.assertEqual(oss.TransferType.OSS_ACC, result.replication_progress.rules[0].destination.transfer_type)
        self.assertIsNotNone(result.replication_progress.rules[0].status)
        self.assertEqual(oss.HistoricalObjectReplicationType.DISABLED, result.replication_progress.rules[0].historical_object_replication)

        # delete bucket replication
        result = self.client.delete_bucket_replication(oss.DeleteBucketReplicationRequest(
            bucket=bucket_name,
            replication_rules=oss.ReplicationRules(
                ids=[id],
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

    def test_bucket_replication_v1(self):
        # create bucket
        bucket_name = random_bucket_name()
        result = self.signv1_client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # put bucket replication
        result = self.signv1_client.put_bucket_replication(oss.PutBucketReplicationRequest(
            bucket=bucket_name,
            replication_configuration=oss.ReplicationConfiguration(
                rules=[oss.ReplicationRule(
                    source_selection_criteria=oss.ReplicationSourceSelectionCriteria(
                        sse_kms_encrypted_objects=oss.SseKmsEncryptedObjects(
                            status=oss.StatusType.ENABLED,
                        ),
                    ),
                    rtc=oss.ReplicationTimeControl(
                        status='disabled',
                    ),
                    destination=oss.ReplicationDestination(
                        bucket=self.bucket_name,
                        location=f'oss-{REGION}',
                        transfer_type=oss.TransferType.OSS_ACC,
                    ),
                    historical_object_replication=oss.HistoricalObjectReplicationType.DISABLED,
                    sync_role=RAM_ROLE_NAME,
                    encryption_configuration=oss.ReplicationEncryptionConfiguration(
                        replica_kms_key_id='c4d49f85-ee30-426b-a5ed-95e9139d****',
                    ),
                    prefix_set=oss.ReplicationPrefixSet(
                        prefixs=['aaa/', 'bbb/'],
                    ),
                    action='ALL',
                )],
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))


        # get bucket replication
        result = self.signv1_client.get_bucket_replication(oss.GetBucketReplicationRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(oss.StatusType.ENABLED, result.replication_configuration.rules[0].source_selection_criteria.sse_kms_encrypted_objects.status)
        # self.assertEqual('disabled', result.replication_configuration.rules[0].rtc.status)
        self.assertEqual(self.bucket_name, result.replication_configuration.rules[0].destination.bucket)
        self.assertEqual(f'oss-{REGION}', result.replication_configuration.rules[0].destination.location)
        self.assertEqual(oss.TransferType.OSS_ACC, result.replication_configuration.rules[0].destination.transfer_type)
        self.assertEqual(oss.HistoricalObjectReplicationType.DISABLED, result.replication_configuration.rules[0].historical_object_replication)
        self.assertEqual(RAM_ROLE_NAME, result.replication_configuration.rules[0].sync_role)
        self.assertEqual('c4d49f85-ee30-426b-a5ed-95e9139d****', result.replication_configuration.rules[0].encryption_configuration.replica_kms_key_id)
        self.assertEqual(['aaa/', 'bbb/'], result.replication_configuration.rules[0].prefix_set.prefixs)
        self.assertEqual('ALL', result.replication_configuration.rules[0].action)


        id = result.replication_configuration.rules[0].id
        # put bucket rtc
        result = self.signv1_client.put_bucket_rtc(oss.PutBucketRtcRequest(
            bucket=bucket_name,
            rtc_configuration=oss.RtcConfiguration(
                rtc=oss.ReplicationTimeControl(
                    status='disabled',
                ),
                id=id,
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket replication location
        result = self.signv1_client.get_bucket_replication_location(oss.GetBucketReplicationLocationRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertIsNotNone(result.replication_location.locations)
        self.assertIsNotNone(result.replication_location.location_transfer_type_constraint.location_transfer_types)


        # get bucket replication progress
        result = self.signv1_client.get_bucket_replication_progress(oss.GetBucketReplicationProgressRequest(
            bucket=bucket_name,
            rule_id=id,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(id, result.replication_progress.rules[0].id)
        self.assertEqual('aaa/', result.replication_progress.rules[0].prefix_set.prefixs[0])
        self.assertEqual('bbb/', result.replication_progress.rules[0].prefix_set.prefixs[1])
        self.assertEqual('ALL', result.replication_progress.rules[0].action)
        self.assertEqual(self.bucket_name, result.replication_progress.rules[0].destination.bucket)
        self.assertEqual(f'oss-{REGION}', result.replication_progress.rules[0].destination.location)
        self.assertEqual(oss.TransferType.OSS_ACC, result.replication_progress.rules[0].destination.transfer_type)
        self.assertIsNotNone(result.replication_progress.rules[0].status)
        self.assertEqual(oss.HistoricalObjectReplicationType.DISABLED, result.replication_progress.rules[0].historical_object_replication)

        # delete bucket replication
        result = self.signv1_client.delete_bucket_replication(oss.DeleteBucketReplicationRequest(
            bucket=bucket_name,
            replication_rules=oss.ReplicationRules(
                ids=[id],
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

    def test_bucket_replication_fail(self):
        # create bucket
        bucket_name = random_bucket_name()
        self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))

        # put bucket replication
        try:
            self.invalid_client.put_bucket_replication(oss.PutBucketReplicationRequest(
                bucket=bucket_name,
                replication_configuration=oss.ReplicationConfiguration(
                    rules=[oss.ReplicationRule(
                        source_selection_criteria=oss.ReplicationSourceSelectionCriteria(
                            sse_kms_encrypted_objects=oss.SseKmsEncryptedObjects(
                                status=oss.StatusType.ENABLED,
                            ),
                        ),
                        rtc=oss.ReplicationTimeControl(
                            status='OK',
                        ),
                        destination=oss.ReplicationDestination(
                            bucket=bucket_name,
                            location='oss-cn-hangzhou',
                            transfer_type=oss.TransferType.INTERNAL,
                        ),
                        historical_object_replication=oss.HistoricalObjectReplicationType.DISABLED,
                        sync_role='acs:ram::1283***5:role/AliyunOSSRole',
                        status='OK',
                        encryption_configuration=oss.ReplicationEncryptionConfiguration(
                            replica_kms_key_id='c4d49f85-ee30-426b-a5ed-95e9139d****',
                        ),
                        prefix_set=oss.ReplicationPrefixSet(
                            prefixs=['aaa/', 'bbb/'],
                        ),
                        action='ALL',
                    )],
                ),
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        # put bucket rtc
        try:
            self.invalid_client.put_bucket_rtc(oss.PutBucketRtcRequest(
                bucket=bucket_name,
                rtc_configuration=oss.RtcConfiguration(
                    rtc=oss.ReplicationTimeControl(
                        status='OK',
                    ),
                    id='0022012****',
                ),
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        # get bucket replication
        try:
            self.invalid_client.get_bucket_replication(oss.GetBucketReplicationRequest(
                bucket=bucket_name,
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        # get bucket replication location
        try:
            self.invalid_client.get_bucket_replication_location(oss.GetBucketReplicationLocationRequest(
                bucket=bucket_name,
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        # get bucket replication progress
        try:
            self.invalid_client.get_bucket_replication_progress(oss.GetBucketReplicationProgressRequest(
                bucket=bucket_name,
                rule_id='RlTVnN9',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        # delete bucket replication
        try:
            self.invalid_client.delete_bucket_replication(oss.DeleteBucketReplicationRequest(
                bucket=bucket_name,
                replication_rules=oss.ReplicationRules(
                    ids=['ids1', 'ids2'],
                ),
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)
