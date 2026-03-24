# pylint: skip-file
import time
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


class TestBucketObjectWormConfigurationAsync(TestIntegration, unittest.IsolatedAsyncioTestCase):
    
    async def asyncSetUp(self):
        self.async_client = get_async_client(REGION, ENDPOINT)
        self.invalid_async_client = get_async_client(
            REGION, ENDPOINT,
            oss.credentials.StaticCredentialsProvider('invalid-ak', 'invalid')
        )

    async def asyncTearDown(self):
        await self.async_client.close()
        if hasattr(self, 'signv1_async_client'):
            await self.signv1_async_client.close()
        await self.invalid_async_client.close()

    async def test_bucket_object_worm_configuration(self):
        # create bucket
        bucket_name = random_bucket_name()
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

        # enable versioning
        result = await self.async_client.put_bucket_versioning(oss.PutBucketVersioningRequest(
            bucket=bucket_name,
            versioning_configuration=oss.VersioningConfiguration(
                status='Enabled'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        time.sleep(1)

        # put bucket object worm configuration with GOVERNANCE mode and 1 day
        result = await self.async_client.put_bucket_object_worm_configuration(oss.PutBucketObjectWormConfigurationRequest(
            bucket=bucket_name,
            object_worm_configuration=oss.ObjectWormConfiguration(
                object_worm_enabled='Enabled',
                rule=oss.ObjectWormConfigurationRule(
                    default_retention=oss.ObjectWormConfigurationRuleDefaultRetention(
                        mode=oss.ObjectWormConfigurationModeType.GOVERNANCE,
                        days=1,
                    ),
                ),
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        time.sleep(1)

        # get bucket object worm configuration
        result = await self.async_client.get_bucket_object_worm_configuration(oss.GetBucketObjectWormConfigurationRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('Enabled', result.object_worm_configuration.object_worm_enabled)
        self.assertEqual(oss.ObjectWormConfigurationModeType.GOVERNANCE, result.object_worm_configuration.rule.default_retention.mode)
        self.assertEqual(1, result.object_worm_configuration.rule.default_retention.days)


    async def test_bucket_object_worm_configuration_fail(self):
        # create bucket
        bucket_name = random_bucket_name()
        await self.async_client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))

        # enable versioning
        await self.async_client.put_bucket_versioning(oss.PutBucketVersioningRequest(
            bucket=bucket_name,
            versioning_configuration=oss.VersioningConfiguration(
                status='Enabled'
            )
        ))

        time.sleep(1)

        # put bucket object worm configuration
        try:
            await self.invalid_async_client.put_bucket_object_worm_configuration(oss.PutBucketObjectWormConfigurationRequest(
                bucket=bucket_name,
                object_worm_configuration=oss.ObjectWormConfiguration(
                    object_worm_enabled='Enabled',
                    rule=oss.ObjectWormConfigurationRule(
                        default_retention=oss.ObjectWormConfigurationRuleDefaultRetention(
                            mode=oss.ObjectWormConfigurationModeType.GOVERNANCE,
                            days=1,
                        ),
                    ),
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

        # get bucket object worm configuration
        try:
            await self.invalid_async_client.get_bucket_object_worm_configuration(oss.GetBucketObjectWormConfigurationRequest(
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
