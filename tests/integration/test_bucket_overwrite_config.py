# pylint: skip-file

from typing import cast
import alibabacloud_oss_v2 as oss
from . import TestIntegration, random_bucket_name


class TestBucketOverwriteConfig(TestIntegration):

    def test_bucket_overwrite_config(self):
        # create bucket
        bucket_name = random_bucket_name()
        result = self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # put bucket overwrite_config
        result = self.client.put_bucket_overwrite_config(oss.PutBucketOverwriteConfigRequest(
            bucket=bucket_name,
            overwrite_configuration=oss.OverwriteConfiguration(
                rules=[
                    oss.OverwriteRule(
                        id='rule1',
                        action='forbid',
                        prefix='a/',
                        suffix='.txt',
                        principals=oss.OverwritePrincipals(
                            principals=['111', '222']
                        )
                    ),
                    oss.OverwriteRule(
                        id='rule2',
                        action='forbid',
                        prefix='b/',
                        suffix='.jpg',
                        principals=oss.OverwritePrincipals(
                            principals=['333']
                        )
                    )
                ],
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket overwrite_config
        result = self.client.get_bucket_overwrite_config(oss.GetBucketOverwriteConfigRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('rule1', result.overwrite_configuration.rules[0].id)
        self.assertEqual('forbid', result.overwrite_configuration.rules[0].action)
        self.assertEqual('a/', result.overwrite_configuration.rules[0].prefix)
        self.assertEqual('.txt', result.overwrite_configuration.rules[0].suffix)
        self.assertEqual('111', result.overwrite_configuration.rules[0].principals.principals[0])
        self.assertEqual('222', result.overwrite_configuration.rules[0].principals.principals[1])
        self.assertEqual('rule2', result.overwrite_configuration.rules[1].id)
        self.assertEqual('forbid', result.overwrite_configuration.rules[1].action)
        self.assertEqual('b/', result.overwrite_configuration.rules[1].prefix)
        self.assertEqual('.jpg', result.overwrite_configuration.rules[1].suffix)
        self.assertEqual('333', result.overwrite_configuration.rules[1].principals.principals[0])

        # delete bucket overwrite_config
        result = self.client.delete_bucket_overwrite_config(oss.DeleteBucketOverwriteConfigRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual('No Content', result.status)


    def test_bucket_overwrite_config_fail(self):
        # create bucket
        bucket_name = random_bucket_name()
        self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
        ))

        # put bucket overwrite_config
        try:
            self.invalid_client.put_bucket_overwrite_config(oss.PutBucketOverwriteConfigRequest(
                bucket=bucket_name,
                overwrite_configuration=oss.OverwriteConfiguration(
                    rules=[
                        oss.OverwriteRule(
                            id='rule1',
                            action='forbid',
                            prefix='a/',
                            suffix='.txt',
                            principals=oss.OverwritePrincipals(
                                principals=['111', '222']
                            )
                        ),
                        oss.OverwriteRule(
                            id='rule2',
                            action='forbid',
                            prefix='b/',
                            suffix='.jpg',
                            principals=oss.OverwritePrincipals(
                                principals=['333']
                            )
                        )
                    ],
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

        # get bucket overwrite_config
        try:
            self.invalid_client.get_bucket_overwrite_config(oss.GetBucketOverwriteConfigRequest(
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

        # delete bucket overwrite_config
        try:
            self.invalid_client.delete_bucket_overwrite_config(oss.DeleteBucketOverwriteConfigRequest(
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

    def test_bucket_overwrite_config_invalid_args(self):

        # create bucket
        bucket_name = 'invalid/123'

        # put bucket overwrite_config
        try:
            self.client.put_bucket_overwrite_config(oss.PutBucketOverwriteConfigRequest(
                bucket=bucket_name,
                overwrite_configuration=oss.OverwriteConfiguration(
                    rules=[
                        oss.OverwriteRule(
                            id='rule1',
                            action='forbid',
                            prefix='a/',
                            suffix='.txt',
                            principals=oss.OverwritePrincipals(
                                principals=['111', '222']
                            )
                        ),
                        oss.OverwriteRule(
                            id='rule2',
                            action='forbid',
                            prefix='b/',
                            suffix='.jpg',
                            principals=oss.OverwritePrincipals(
                                principals=['333']
                            )
                        )
                    ],
                ),
            ))
            self.fail("should not here")
        except Exception as e:
            self.assertIn('Bucket name is invalid, got invalid/123', str(e))

        # get bucket overwrite_config
        try:
            self.client.get_bucket_overwrite_config(oss.GetBucketOverwriteConfigRequest(
                bucket=bucket_name,
            ))
            self.fail("should not here")
        except Exception as e:
            self.assertIn('Bucket name is invalid, got invalid/123', str(e))


        # delete bucket overwrite_config
        try:
            self.client.delete_bucket_overwrite_config(oss.DeleteBucketOverwriteConfigRequest(
                bucket=bucket_name,
            ))
            self.fail("should not here")
        except Exception as e:
            self.assertIn('Bucket name is invalid, got invalid/123', str(e))

        # put bucket overwrite_config
        try:
            self.client.put_bucket_overwrite_config(oss.PutBucketOverwriteConfigRequest(
            ))
            self.fail("should not here")
        except Exception as e:
            self.assertIn('missing required field, bucket', str(e))

        # get bucket overwrite_config
        try:
            self.client.get_bucket_overwrite_config(oss.GetBucketOverwriteConfigRequest(
            ))
            self.fail("should not here")
        except Exception as e:
            self.assertIn('missing required field, bucket', str(e))


        # delete bucket overwrite_config
        try:
            self.client.delete_bucket_overwrite_config(oss.DeleteBucketOverwriteConfigRequest(
            ))
            self.fail("should not here")
        except Exception as e:
            self.assertIn('missing required field, bucket', str(e))
