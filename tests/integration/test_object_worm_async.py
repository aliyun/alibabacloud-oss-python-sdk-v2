# pylint: skip-file
from time import sleep
from typing import cast
import unittest
import alibabacloud_oss_v2 as oss
from . import (
    TestIntegration, 
    random_bucket_name,
    random_str,
    REGION,
    ENDPOINT,
    OBJECTNAME_PREFIX,
    ACCESS_ID,
    ACCESS_KEY,
    get_async_client,
)


async def delete_all_objects(self, bucket_name):
    print(f"\n  Cleaning up bucket: {bucket_name}")

    try:
        total_deleted = 0
        key_marker = None
        version_id_marker = None

        while True:
            # List object versions
            request = oss.ListObjectVersionsRequest(
                bucket=bucket_name,
                key_marker=key_marker,
                version_id_marker=version_id_marker
            )
            result = await self.async_client.list_object_versions(request)
            
            if not result.version and not result.delete_marker:
                break

            # Prepare delete request
            delete_objects = []
            # Process object versions if result has version attribute
            if hasattr(result, 'version') and result.version:
                for obj in result.version:
                    delete_objects.append(oss.ObjectIdentifier(
                        key=obj.key,
                        version_id=obj.version_id
                    ))

            # Process delete markers if result has delete_marker attribute
            if hasattr(result, 'delete_marker') and result.delete_marker:
                for obj in result.delete_marker:
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

                del_result = await self.async_client.delete_multiple_objects(oss.DeleteMultipleObjectsRequest(
                    bucket=bucket_name,
                    delete=delete_request,
                ))

                total_deleted += len(delete_objects)
                print(f"    Deleted {len(delete_objects)} objects/versions (Total: {total_deleted})")

            # Update markers for next iteration
            if result.next_key_marker:
                key_marker = result.next_key_marker
                version_id_marker = result.next_version_id_marker
            else:
                break

        if total_deleted > 0:
            print(f"  ✓ Successfully deleted {total_deleted} objects/versions from {bucket_name}")
        else:
            print(f"  ✓ No objects found in {bucket_name}")

        # After deleting all objects, delete the bucket
        try:
            result = await self.async_client.delete_bucket(oss.DeleteBucketRequest(
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


class TestObjectRetentionAsync(TestIntegration, unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        """Set up test fixtures."""
        self.async_client = get_async_client(REGION, ENDPOINT)
        self.invalid_async_client = get_async_client(
            REGION, ENDPOINT,
            oss.credentials.StaticCredentialsProvider('invalid-ak', 'invalid')
        )

    async def asyncTearDown(self):
        """Tear down test fixtures."""
        await self.async_client.close()
        if hasattr(self, 'signv1_async_client'):
            await self.signv1_async_client.close()
        await self.invalid_async_client.close()

    async def test_object_retention_async(self):
        # Create bucket and upload object
        bucket_name = random_bucket_name()
        object_key = 'test-retention-object-async'
        
        result = await self.async_client.put_bucket(oss.PutBucketRequest(
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
        result = await self.async_client.put_bucket_versioning(oss.PutBucketVersioningRequest(
            bucket=bucket_name,
            versioning_configuration=oss.VersioningConfiguration(
                status='Enabled'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        sleep(1)
        
        # Put bucket object worm configuration
        result = await self.async_client.put_bucket_object_worm_configuration(oss.PutBucketObjectWormConfigurationRequest(
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
        
        result = await self.async_client.put_object(oss.PutObjectRequest(
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
        
        result = await self.async_client.put_object_retention(oss.PutObjectRetentionRequest(
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
        result = await self.async_client.get_object_retention(oss.GetObjectRetentionRequest(
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

        await delete_all_objects(self, bucket_name)


    async def test_object_retention_with_bypass_async(self):
        # Create bucket and upload object
        bucket_name = random_bucket_name()
        object_key = 'test-retention-bypass-async'
        
        result = await self.async_client.put_bucket(oss.PutBucketRequest(
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
        result = await self.async_client.put_bucket_versioning(oss.PutBucketVersioningRequest(
            bucket=bucket_name,
            versioning_configuration=oss.VersioningConfiguration(
                status='Enabled'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        sleep(1)
        
        # Put bucket object worm configuration
        result = await self.async_client.put_bucket_object_worm_configuration(oss.PutBucketObjectWormConfigurationRequest(
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
        
        result = await self.async_client.put_object(oss.PutObjectRequest(
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
        
        result = await self.async_client.put_object_retention(oss.PutObjectRetentionRequest(
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

        await delete_all_objects(self, bucket_name)

    async def test_object_retention_fail_async(self):
        # Create bucket and upload object
        bucket_name = random_bucket_name()
        object_key = 'test-retention-fail-async'
        
        await self.async_client.put_bucket(oss.PutBucketRequest(
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
        await self.async_client.put_bucket_object_worm_configuration(oss.PutBucketObjectWormConfigurationRequest(
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
        
        await self.async_client.put_object(oss.PutObjectRequest(
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
            await self.invalid_async_client.put_object_retention(oss.PutObjectRetentionRequest(
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
            await self.invalid_async_client.get_object_retention(oss.GetObjectRetentionRequest(
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

        await delete_all_objects(self, bucket_name)


class TestObjectLegalHoldAsync(TestIntegration, unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        """Set up test fixtures."""
        self.async_client = get_async_client(REGION, ENDPOINT)
        self.invalid_async_client = get_async_client(
            REGION, ENDPOINT,
            oss.credentials.StaticCredentialsProvider('invalid-ak', 'invalid')
        )

    async def asyncTearDown(self):
        """Tear down test fixtures."""
        await self.async_client.close()
        if hasattr(self, 'signv1_async_client'):
            await self.signv1_async_client.close()
        await self.invalid_async_client.close()

    async def test_object_legal_hold_async(self):
        # Create bucket and upload object
        bucket_name = random_bucket_name()
        object_key = 'test-legalhold-object-async'
        
        result = await self.async_client.put_bucket(oss.PutBucketRequest(
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
        result = await self.async_client.put_bucket_versioning(oss.PutBucketVersioningRequest(
            bucket=bucket_name,
            versioning_configuration=oss.VersioningConfiguration(
                status='Enabled'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        sleep(1)

        # Put bucket object worm configuration
        result = await self.async_client.put_bucket_object_worm_configuration(oss.PutBucketObjectWormConfigurationRequest(
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
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        
        result = await self.async_client.put_object(oss.PutObjectRequest(
            bucket=bucket_name,
            key=object_key,
            body=b'test content',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # Put object legal hold ON
        result = await self.async_client.put_object_legal_hold(oss.PutObjectLegalHoldRequest(
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
        result = await self.async_client.get_object_legal_hold(oss.GetObjectLegalHoldRequest(
            bucket=bucket_name,
            key=object_key,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('ON', result.legal_hold.status)

        # Put object legal hold OFF
        result = await self.async_client.put_object_legal_hold(oss.PutObjectLegalHoldRequest(
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
        result = await self.async_client.get_object_legal_hold(oss.GetObjectLegalHoldRequest(
            bucket=bucket_name,
            key=object_key,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('OFF', result.legal_hold.status)

        await delete_all_objects(self, bucket_name)

    async def test_object_legal_hold_fail_async(self):
        # Create bucket and upload object
        bucket_name = random_bucket_name()
        object_key = 'test-legalhold-fail-async'
        
        result = await self.async_client.put_bucket(oss.PutBucketRequest(
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
        result = await self.async_client.put_bucket_versioning(oss.PutBucketVersioningRequest(
            bucket=bucket_name,
            versioning_configuration=oss.VersioningConfiguration(
                status='Enabled'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        
        sleep(1)
        
        # Put bucket object worm configuration
        result = await self.async_client.put_bucket_object_worm_configuration(oss.PutBucketObjectWormConfigurationRequest(
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
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        
        result = await self.async_client.put_object(oss.PutObjectRequest(
            bucket=bucket_name,
            key=object_key,
            body=b'test content',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # Put object legal hold fail
        try:
            await self.invalid_async_client.put_object_legal_hold(oss.PutObjectLegalHoldRequest(
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
            await self.invalid_async_client.get_object_legal_hold(oss.GetObjectLegalHoldRequest(
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

        await delete_all_objects(self, bucket_name)