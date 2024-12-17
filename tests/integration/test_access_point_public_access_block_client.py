# pylint: skip-file
import time
from typing import cast
import alibabacloud_oss_v2 as oss
from . import TestIntegration, random_bucket_name, random_lowstr


class TestAccessPointPublicAccessBlock(TestIntegration):

    def test_access_point_public_access_block(self):
        access_point_name_1 = 'ap-test-oss-' + random_lowstr(6)

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

        # create access point
        result = self.client.create_access_point(oss.CreateAccessPointRequest(
            bucket=bucket_name,
            create_access_point_configuration=oss.CreateAccessPointConfiguration(
                access_point_name=access_point_name_1,
                network_origin='internet',
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.access_point_arn)
        self.assertIsNotNone(result.alias)

        try:
            # Waiting for access point creation status to be enabled
            num = 1
            while True:
                get_result = self.client.get_access_point(oss.GetAccessPointRequest(
                    bucket=bucket_name,
                    access_point_name=access_point_name_1,
                ))

                if num > 180:
                    break

                if get_result.status == 'enable':
                    break

                num += 1
                time.sleep(5)

            # put access point public access block
            result = self.client.put_access_point_public_access_block(oss.PutAccessPointPublicAccessBlockRequest(
                bucket=bucket_name,
                access_point_name=access_point_name_1,
                public_access_block_configuration=oss.PublicAccessBlockConfiguration(
                    block_public_access=True,
                ),
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual('OK', result.status)
            self.assertEqual(24, len(result.request_id))
            self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

            # get access point public access block
            result = self.client.get_access_point_public_access_block(oss.GetAccessPointPublicAccessBlockRequest(
                bucket=bucket_name,
                access_point_name=access_point_name_1,
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual('OK', result.status)
            self.assertEqual(24, len(result.request_id))
            self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
            self.assertEqual(True, result.public_access_block_configuration.block_public_access)

            # delete access point public access block
            result = self.client.delete_access_point_public_access_block(oss.DeleteAccessPointPublicAccessBlockRequest(
                bucket=bucket_name,
                access_point_name=access_point_name_1,
            ))
            self.assertEqual(204, result.status_code)
            self.assertEqual(24, len(result.request_id))
            self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        except Exception as e:
            print("Exception: {0}".format(e))
        finally:
            # Delete all access points under the bucket
            num = 1
            while True:
                list_result = self.client.list_access_points(oss.ListAccessPointsRequest(
                    bucket=bucket_name,
                    max_keys=100,
                    continuation_token='',
                ))

                if list_result.access_points is None:
                    print(f"all access point is delete")
                    break

                if num > 180:
                    break

                for ap in list_result.access_points:
                    if ap.access_point_name.startswith('ap-test-oss-'):

                        if ap.status == 'enable':
                            print(f"ap name: {ap.access_point_name}, status: {ap.status}")
                            del_result = self.client.delete_access_point(oss.DeleteAccessPointRequest(
                                bucket=bucket_name,
                                access_point_name=ap.access_point_name,
                            ))
                            self.assertEqual(del_result.status_code, 204)
                            print(f"delete_access_point: {ap.access_point_name}")


                num += 1
                time.sleep(10)

    def test_access_point_public_access_block_v1(self):
        access_point_name_1 = 'ap-test-oss-' + random_lowstr(6)

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

        # create access point
        result = self.signv1_client.create_access_point(oss.CreateAccessPointRequest(
            bucket=bucket_name,
            create_access_point_configuration=oss.CreateAccessPointConfiguration(
                access_point_name=access_point_name_1,
                network_origin='internet',
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.access_point_arn)
        self.assertIsNotNone(result.alias)

        try:
            # Waiting for access point creation status to be enabled
            num = 1
            while True:
                get_result = self.signv1_client.get_access_point(oss.GetAccessPointRequest(
                    bucket=bucket_name,
                    access_point_name=access_point_name_1,
                ))

                if num > 180:
                    break

                if get_result.status == 'enable':
                    break

                num += 1
                time.sleep(5)

            # put access point public access block
            result = self.signv1_client.put_access_point_public_access_block(oss.PutAccessPointPublicAccessBlockRequest(
                bucket=bucket_name,
                access_point_name=access_point_name_1,
                public_access_block_configuration=oss.PublicAccessBlockConfiguration(
                    block_public_access=True,
                ),
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual('OK', result.status)
            self.assertEqual(24, len(result.request_id))
            self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

            # get access point public access block
            result = self.signv1_client.get_access_point_public_access_block(oss.GetAccessPointPublicAccessBlockRequest(
                bucket=bucket_name,
                access_point_name=access_point_name_1,
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual('OK', result.status)
            self.assertEqual(24, len(result.request_id))
            self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
            self.assertEqual(True, result.public_access_block_configuration.block_public_access)

            # delete access point public access block
            result = self.signv1_client.delete_access_point_public_access_block(oss.DeleteAccessPointPublicAccessBlockRequest(
                bucket=bucket_name,
                access_point_name=access_point_name_1,
            ))
            self.assertEqual(204, result.status_code)
            self.assertEqual(24, len(result.request_id))
            self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        except Exception as e:
            print("Exception: {0}".format(e))
        finally:
            # Delete all access points under the bucket
            num = 1
            while True:
                list_result = self.signv1_client.list_access_points(oss.ListAccessPointsRequest(
                    bucket=bucket_name,
                    max_keys=100,
                    continuation_token='',
                ))

                if list_result.access_points is None:
                    print(f"all access point is delete")
                    break

                if num > 180:
                    break

                for ap in list_result.access_points:
                    if ap.access_point_name.startswith('ap-test-oss-'):

                        if ap.status == 'enable':
                            print(f"ap name: {ap.access_point_name}, status: {ap.status}")
                            del_result = self.signv1_client.delete_access_point(oss.DeleteAccessPointRequest(
                                bucket=bucket_name,
                                access_point_name=ap.access_point_name,
                            ))
                            self.assertEqual(del_result.status_code, 204)
                            print(f"delete_access_point: {ap.access_point_name}")

                num += 1
                time.sleep(10)

    def test_access_point_public_access_block_fail(self):
        # create bucket
        bucket_name = random_bucket_name()
        self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))

        # put access point public access block
        try:
            self.invalid_client.put_access_point_public_access_block(oss.PutAccessPointPublicAccessBlockRequest(
                bucket=bucket_name,
                access_point_name='test_access_point_name',
                public_access_block_configuration=oss.PublicAccessBlockConfiguration(
                    block_public_access=True,
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

        # get access point public access block
        try:
            self.invalid_client.get_access_point_public_access_block(oss.GetAccessPointPublicAccessBlockRequest(
                bucket=bucket_name,
                access_point_name='test_access_point_name',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        # delete access point public access block
        try:
            self.invalid_client.delete_access_point_public_access_block(oss.DeleteAccessPointPublicAccessBlockRequest(
                bucket=bucket_name,
                access_point_name='test_access_point_name',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)
