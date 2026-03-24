# pylint: skip-file
from time import sleep
from typing import cast
import alibabacloud_oss_v2 as oss
from . import TestIntegration, random_bucket_name

def delete_all_objects(self, bucket_name):
    print(f"\n  Cleaning up bucket: {bucket_name}")

    try:
        # Use paginator to list all object versions
        paginator = self.client.list_object_versions_paginator()
        request = oss.ListObjectVersionsRequest(bucket=bucket_name)

        total_deleted = 0

        for page in paginator.iter_page(request):
            if not page.version and not page.delete_marker:
                continue

            # Prepare delete request
            delete_objects = []
            # Process object versions if page has version attribute
            if hasattr(page, 'version') and page.version:
                for obj in page.version:
                    delete_objects.append(oss.ObjectIdentifier(
                        key=obj.key,
                        version_id=obj.version_id
                    ))

            # Process delete markers if page has delete_marker attribute
            if hasattr(page, 'delete_marker') and page.delete_marker:
                for obj in page.delete_marker:
                    delete_objects.append(oss.ObjectIdentifier(
                        key=obj.key,
                        version_id=obj.version_id
                    ))

            if delete_objects:
                # Delete multiple objects in batch
                delete_request = oss.Delete(
                    objects=delete_objects,
                    quiet=True  # Don't return details for each deletion
                )

                result = self.client.delete_multiple_objects(oss.DeleteMultipleObjectsRequest(
                    bucket=bucket_name,
                    delete=delete_request,
                ))

                total_deleted += len(delete_objects)
                print(f"    Deleted {len(delete_objects)} objects/versions (Total: {total_deleted})")

        if total_deleted > 0:
            print(f"  ✓ Successfully deleted {total_deleted} objects/versions from {bucket_name}")
        else:
            print(f"  ✓ No objects found in {bucket_name}")

        # After deleting all objects, delete the bucket
        try:
            result = self.client.delete_bucket(oss.DeleteBucketRequest(
                bucket=bucket_name,
            ))
            print(f"  ✓ Successfully deleted bucket: {bucket_name} (request_id: {result.request_id})")
            return True, total_deleted
        except Exception as e:
            print(f"  ✗ Error deleting bucket {bucket_name}: {str(e)}")
            return False, total_deleted

    except Exception as e:
        print(f"  ✗ Error deleting objects from {bucket_name}: {str(e)}")
        return False, 0


class TestObjectRetention(TestIntegration):

    def test_object_retention(self):
        # Create bucket and upload object
        bucket_name = random_bucket_name()
        object_key = 'test-retention-object'
        
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
        
        # Enable versioning
        result = self.client.put_bucket_versioning(oss.PutBucketVersioningRequest(
            bucket=bucket_name,
            versioning_configuration=oss.VersioningConfiguration(
                status='Enabled'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        sleep(1)
        
        # Put bucket object worm configuration
        result = self.client.put_bucket_object_worm_configuration(oss.PutBucketObjectWormConfigurationRequest(
            bucket=bucket_name,
            object_worm_configuration=oss.ObjectWormConfiguration(
                object_worm_enabled='Enabled',
                # rule=oss.ObjectWormConfigurationRule(
                #     default_retention=oss.ObjectWormConfigurationRuleDefaultRetention(
                #         mode=oss.ObjectWormConfigurationModeType.GOVERNANCE,
                #         days=1,
                #     ),
                # ),
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=bucket_name,
            key=object_key,
            body=b'test content',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))

        # Put object retention
        from datetime import datetime, timedelta, timezone
        # Use local time and add 5 seconds, then format to UTC with millisecond precision
        local_time = datetime.now().astimezone() + timedelta(seconds=5)
        utc_time = local_time.astimezone(timezone.utc)
        retain_until_date = utc_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        
        result = self.client.put_object_retention(oss.PutObjectRetentionRequest(
            bucket=bucket_name,
            key=object_key,
            retention=oss.Retention(
                mode=oss.ObjectRetentionModeType.COMPLIANCE,
                retain_until_date=retain_until_date,
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # Get object retention
        result = self.client.get_object_retention(oss.GetObjectRetentionRequest(
            bucket=bucket_name,
            key=object_key,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('COMPLIANCE', result.retention.mode)
        self.assertEqual(retain_until_date, result.retention.retain_until_date)

        sleep(6)

        delete_all_objects(self, bucket_name)

    def test_object_retention_v1(self):
        # Create bucket and upload object
        bucket_name = random_bucket_name()
        object_key = 'test-retention-object-v1'
        
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
        
        # Enable versioning
        result = self.signv1_client.put_bucket_versioning(oss.PutBucketVersioningRequest(
            bucket=bucket_name,
            versioning_configuration=oss.VersioningConfiguration(
                status='Enabled'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        sleep(1)
        
        # Put bucket object worm configuration
        result = self.signv1_client.put_bucket_object_worm_configuration(oss.PutBucketObjectWormConfigurationRequest(
            bucket=bucket_name,
            object_worm_configuration=oss.ObjectWormConfiguration(
                object_worm_enabled='Enabled',
                # rule=oss.ObjectWormConfigurationRule(
                #     default_retention=oss.ObjectWormConfigurationRuleDefaultRetention(
                #         mode=oss.ObjectWormConfigurationModeType.GOVERNANCE,
                #         days=1,
                #     ),
                # ),
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        
        result = self.signv1_client.put_object(oss.PutObjectRequest(
            bucket=bucket_name,
            key=object_key,
            body=b'test content',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))

        # Put object retention
        from datetime import datetime, timedelta, timezone
        # Use local time and add 5 seconds, then format to UTC with millisecond precision
        local_time = datetime.now().astimezone() + timedelta(seconds=5)
        utc_time = local_time.astimezone(timezone.utc)
        retain_until_date = utc_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        
        result = self.signv1_client.put_object_retention(oss.PutObjectRetentionRequest(
            bucket=bucket_name,
            key=object_key,
            retention=oss.Retention(
                mode=oss.ObjectRetentionModeType.GOVERNANCE,
                retain_until_date=retain_until_date,
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # Get object retention
        result = self.signv1_client.get_object_retention(oss.GetObjectRetentionRequest(
            bucket=bucket_name,
            key=object_key,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('GOVERNANCE', result.retention.mode)
        self.assertEqual(retain_until_date, result.retention.retain_until_date)

        sleep(6)

        delete_all_objects(self, bucket_name)

    def test_object_retention_with_bypass(self):
        # Create bucket and upload object
        bucket_name = random_bucket_name()
        object_key = 'test-retention-bypass'
        
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
        
        # Enable versioning
        result = self.client.put_bucket_versioning(oss.PutBucketVersioningRequest(
            bucket=bucket_name,
            versioning_configuration=oss.VersioningConfiguration(
                status='Enabled'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        sleep(1)
        
        # Put bucket object worm configuration
        result = self.client.put_bucket_object_worm_configuration(oss.PutBucketObjectWormConfigurationRequest(
            bucket=bucket_name,
            object_worm_configuration=oss.ObjectWormConfiguration(
                object_worm_enabled='Enabled',
                # rule=oss.ObjectWormConfigurationRule(
                #     default_retention=oss.ObjectWormConfigurationRuleDefaultRetention(
                #         mode=oss.ObjectWormConfigurationModeType.GOVERNANCE,
                #         days=1,
                #     ),
                # ),
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=bucket_name,
            key=object_key,
            body=b'test content',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))

        # Put object retention with bypass governance retention
        from datetime import datetime, timedelta, timezone
        # Use local time and add 5 seconds, then format to UTC with millisecond precision
        local_time = datetime.now().astimezone() + timedelta(seconds=5)
        utc_time = local_time.astimezone(timezone.utc)
        retain_until_date = utc_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        
        result = self.client.put_object_retention(oss.PutObjectRetentionRequest(
            bucket=bucket_name,
            key=object_key,
            bypass_governance_retention=True,
            retention=oss.Retention(
                mode=oss.ObjectRetentionModeType.GOVERNANCE,
                retain_until_date=retain_until_date,
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        sleep(6)

        delete_all_objects(self, bucket_name)

    def test_object_retention_fail(self):
        # Create bucket and upload object
        bucket_name = random_bucket_name()
        object_key = 'test-retention-fail'
        
        self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))
        
        # Enable versioning
        self.client.put_bucket_versioning(oss.PutBucketVersioningRequest(
            bucket=bucket_name,
            versioning_configuration=oss.VersioningConfiguration(
                status='Enabled'
            )
        ))

        sleep(1)
        
        # Put bucket object worm configuration
        self.client.put_bucket_object_worm_configuration(oss.PutBucketObjectWormConfigurationRequest(
            bucket=bucket_name,
            object_worm_configuration=oss.ObjectWormConfiguration(
                object_worm_enabled='Enabled',
                # rule=oss.ObjectWormConfigurationRule(
                #     default_retention=oss.ObjectWormConfigurationRuleDefaultRetention(
                #         mode=oss.ObjectWormConfigurationModeType.GOVERNANCE,
                #         days=1,
                #     ),
                # ),
            ),
        ))
        
        self.client.put_object(oss.PutObjectRequest(
            bucket=bucket_name,
            key=object_key,
            body=b'test content',
        ))

        # Put object retention fail
        from datetime import datetime, timedelta, timezone
        # Use local time and add 5 seconds, then format to UTC with millisecond precision
        local_time = datetime.now().astimezone() + timedelta(seconds=5)
        utc_time = local_time.astimezone(timezone.utc)
        retain_until_date = utc_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        
        try:
            self.invalid_client.put_object_retention(oss.PutObjectRetentionRequest(
                bucket=bucket_name,
                key=object_key,
                retention=oss.Retention(
                    mode=oss.ObjectRetentionModeType.GOVERNANCE,
                    retain_until_date=retain_until_date,
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

        # Get object retention fail
        try:
            self.invalid_client.get_object_retention(oss.GetObjectRetentionRequest(
                bucket=bucket_name,
                key=object_key,
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        sleep(6)

        delete_all_objects(self, bucket_name)


class TestObjectLegalHold(TestIntegration):

    def test_object_legal_hold(self):
        # Create bucket and upload object
        bucket_name = random_bucket_name()
        object_key = 'test-legalhold-object'
        
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
        
        # Enable versioning
        result = self.client.put_bucket_versioning(oss.PutBucketVersioningRequest(
            bucket=bucket_name,
            versioning_configuration=oss.VersioningConfiguration(
                status='Enabled'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        sleep(1)

        # Put bucket object worm configuration
        result = self.client.put_bucket_object_worm_configuration(oss.PutBucketObjectWormConfigurationRequest(
            bucket=bucket_name,
            object_worm_configuration=oss.ObjectWormConfiguration(
                object_worm_enabled='Enabled',
                # rule=oss.ObjectWormConfigurationRule(
                #     default_retention=oss.ObjectWormConfigurationRuleDefaultRetention(
                #         mode=oss.ObjectWormConfigurationModeType.GOVERNANCE,
                #         days=1,
                #     ),
                # ),
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=bucket_name,
            key=object_key,
            body=b'test content',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))

        # Put object legal hold ON
        result = self.client.put_object_legal_hold(oss.PutObjectLegalHoldRequest(
            bucket=bucket_name,
            key=object_key,
            legal_hold=oss.LegalHold(
                status=oss.ObjectLegalHoldStatusType.ON,
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # Get object legal hold
        result = self.client.get_object_legal_hold(oss.GetObjectLegalHoldRequest(
            bucket=bucket_name,
            key=object_key,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('ON', result.legal_hold.status)

        # Put object legal hold OFF
        result = self.client.put_object_legal_hold(oss.PutObjectLegalHoldRequest(
            bucket=bucket_name,
            key=object_key,
            legal_hold=oss.LegalHold(
                status=oss.ObjectLegalHoldStatusType.OFF,
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # Get object legal hold again
        result = self.client.get_object_legal_hold(oss.GetObjectLegalHoldRequest(
            bucket=bucket_name,
            key=object_key,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('OFF', result.legal_hold.status)

        delete_all_objects(self, bucket_name)

    def test_object_legal_hold_v1(self):
        # Create bucket and upload object
        bucket_name = random_bucket_name()
        object_key = 'test-legalhold-object-v1'
        
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
        
        # Enable versioning
        result = self.signv1_client.put_bucket_versioning(oss.PutBucketVersioningRequest(
            bucket=bucket_name,
            versioning_configuration=oss.VersioningConfiguration(
                status='Enabled'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        sleep(1)
        
        # Put bucket object worm configuration
        result = self.signv1_client.put_bucket_object_worm_configuration(oss.PutBucketObjectWormConfigurationRequest(
            bucket=bucket_name,
            object_worm_configuration=oss.ObjectWormConfiguration(
                object_worm_enabled='Enabled',
                # rule=oss.ObjectWormConfigurationRule(
                #     default_retention=oss.ObjectWormConfigurationRuleDefaultRetention(
                #         mode=oss.ObjectWormConfigurationModeType.GOVERNANCE,
                #         days=1,
                #     ),
                # ),
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        
        result = self.signv1_client.put_object(oss.PutObjectRequest(
            bucket=bucket_name,
            key=object_key,
            body=b'test content',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))

        # Put object legal hold ON
        result = self.signv1_client.put_object_legal_hold(oss.PutObjectLegalHoldRequest(
            bucket=bucket_name,
            key=object_key,
            legal_hold=oss.LegalHold(
                status=oss.ObjectLegalHoldStatusType.ON,
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # Get object legal hold
        result = self.signv1_client.get_object_legal_hold(oss.GetObjectLegalHoldRequest(
            bucket=bucket_name,
            key=object_key,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('ON', result.legal_hold.status)

        # Put object legal hold OFF
        result = self.signv1_client.put_object_legal_hold(oss.PutObjectLegalHoldRequest(
            bucket=bucket_name,
            key=object_key,
            legal_hold=oss.LegalHold(
                status=oss.ObjectLegalHoldStatusType.OFF,
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # Get object legal hold again
        result = self.signv1_client.get_object_legal_hold(oss.GetObjectLegalHoldRequest(
            bucket=bucket_name,
            key=object_key,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('OFF', result.legal_hold.status)

        delete_all_objects(self, bucket_name)

    def test_object_legal_hold_fail(self):
        # Create bucket and upload object
        bucket_name = random_bucket_name()
        object_key = 'test-legalhold-fail'
        
        self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))
        
        # Enable versioning
        self.client.put_bucket_versioning(oss.PutBucketVersioningRequest(
            bucket=bucket_name,
            versioning_configuration=oss.VersioningConfiguration(
                status='Enabled'
            )
        ))

        sleep(1)
        
        # Put bucket object worm configuration
        self.client.put_bucket_object_worm_configuration(oss.PutBucketObjectWormConfigurationRequest(
            bucket=bucket_name,
            object_worm_configuration=oss.ObjectWormConfiguration(
                object_worm_enabled='Enabled',
                # rule=oss.ObjectWormConfigurationRule(
                #     default_retention=oss.ObjectWormConfigurationRuleDefaultRetention(
                #         mode=oss.ObjectWormConfigurationModeType.GOVERNANCE,
                #         days=1,
                #     ),
                # ),
            ),
        ))
        
        self.client.put_object(oss.PutObjectRequest(
            bucket=bucket_name,
            key=object_key,
            body=b'test content',
        ))

        # Put object legal hold fail
        try:
            self.invalid_client.put_object_legal_hold(oss.PutObjectLegalHoldRequest(
                bucket=bucket_name,
                key=object_key,
                legal_hold=oss.LegalHold(
                    status=oss.ObjectLegalHoldStatusType.ON,
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

        # Get object legal hold fail
        try:
            self.invalid_client.get_object_legal_hold(oss.GetObjectLegalHoldRequest(
                bucket=bucket_name,
                key=object_key,
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        delete_all_objects(self, bucket_name)


