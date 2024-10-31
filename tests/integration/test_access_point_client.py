# pylint: skip-file

import time
from typing import cast
import alibabacloud_oss_v2 as oss
from . import TestIntegration, random_bucket_name, random_str, random_lowstr, REGION, USER_ID


class TestAccessPoint(TestIntegration):

    def test_access_point(self):
        access_point_name_1 = 'ap-test-oss-' + random_lowstr(6)
        access_point_name_2 = 'ap-test-oss-'+random_lowstr(6)
        policy = "{\"Version\":\"1\",\"Statement\":[{\"Action\":[\"oss:PutObject\",\"oss:GetObject\"],\"Effect\":\"Deny\",\"Principal\":[\"" + USER_ID + "\"],\"Resource\":[\"acs:oss:" + REGION + ":" + USER_ID + ":accesspoint/" + access_point_name_1 + "\",\"acs:oss:" + REGION + ":" + USER_ID + ":accesspoint/" + access_point_name_1 + "/object/*\"]}]}"


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


        result = self.client.create_access_point(oss.CreateAccessPointRequest(
            bucket=bucket_name,
            create_access_point_configuration=oss.CreateAccessPointConfiguration(
                access_point_name=access_point_name_2,
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
                    print(f"{access_point_name_1} is enable")
                    break

                num += 1
                time.sleep(5)

            num_2 = 1
            while True:
                get_result = self.client.get_access_point(oss.GetAccessPointRequest(
                    bucket=bucket_name,
                    access_point_name=access_point_name_2,
                ))

                if num_2 > 180:
                    break

                if get_result.status == 'enable':
                    print(f"{access_point_name_2} is enable")
                    break

                num_2 += 1
                time.sleep(5)

            # get access point
            result = self.client.get_access_point(oss.GetAccessPointRequest(
                bucket=bucket_name,
                access_point_name=access_point_name_1,
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual(access_point_name_1, result.access_point_name)
            self.assertEqual('internet', result.network_origin)


            # list access point
            result = self.client.list_access_points(oss.ListAccessPointsRequest(
                bucket=bucket_name,
                max_keys=1,
                continuation_token='',
            ))

            self.assertEqual(200, result.status_code)
            self.assertEqual(1, result.max_keys)
            self.assertEqual('internet', result.access_points[0].network_origin)


            result = self.client.list_access_points(oss.ListAccessPointsRequest(
                max_keys=1,
                continuation_token=result.next_continuation_token,
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual(1, result.max_keys)
            self.assertEqual('internet', result.access_points[0].network_origin)



            # create access point policy
            result = self.client.put_access_point_policy(oss.PutAccessPointPolicyRequest(
                bucket=bucket_name,
                access_point_name=access_point_name_1,
                body=policy,
            ))
            self.assertEqual(200, result.status_code)



            # get access point policy
            result = self.client.get_access_point_policy(oss.GetAccessPointPolicyRequest(
                bucket=bucket_name,
                access_point_name=access_point_name_1,
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual(policy, result.body)



            # delete access point policy
            result = self.client.delete_access_point_policy(oss.DeleteAccessPointPolicyRequest(
                bucket=bucket_name,
                access_point_name=access_point_name_1,
            ))
            self.assertEqual(result.status_code, 204)



            # delete access point
            result = self.client.delete_access_point(oss.DeleteAccessPointRequest(
                bucket=bucket_name,
                access_point_name=access_point_name_1,
            ))
            self.assertEqual(result.status_code, 204)



            # delete access point
            result = self.client.delete_access_point(oss.DeleteAccessPointRequest(
                bucket=bucket_name,
                access_point_name=access_point_name_2,
            ))

            self.assertEqual(result.status_code, 204)

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


    def test_access_point_v1(self):
        access_point_name_1 = 'ap-test-oss-' + random_lowstr(6)
        access_point_name_2 = 'ap-test-oss-'+random_lowstr(6)
        policy = "{\"Version\":\"1\",\"Statement\":[{\"Action\":[\"oss:PutObject\",\"oss:GetObject\"],\"Effect\":\"Deny\",\"Principal\":[\"" + USER_ID + "\"],\"Resource\":[\"acs:oss:" + REGION + ":" + USER_ID + ":accesspoint/" + access_point_name_1 + "\",\"acs:oss:" + REGION + ":" + USER_ID + ":accesspoint/" + access_point_name_1 + "/object/*\"]}]}"


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


        result = self.signv1_client.create_access_point(oss.CreateAccessPointRequest(
            bucket=bucket_name,
            create_access_point_configuration=oss.CreateAccessPointConfiguration(
                access_point_name=access_point_name_2,
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
                    print(f"{access_point_name_1} is enable")
                    break

                num += 1
                time.sleep(5)

            num_2 = 1
            while True:
                get_result = self.signv1_client.get_access_point(oss.GetAccessPointRequest(
                    bucket=bucket_name,
                    access_point_name=access_point_name_2,
                ))

                if num_2 > 180:
                    break

                if get_result.status == 'enable':
                    print(f"{access_point_name_2} is enable")
                    break

                num_2 += 1
                time.sleep(5)

            # get access point
            result = self.signv1_client.get_access_point(oss.GetAccessPointRequest(
                bucket=bucket_name,
                access_point_name=access_point_name_1,
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual(access_point_name_1, result.access_point_name)
            self.assertEqual('internet', result.network_origin)


            # list access point
            result = self.signv1_client.list_access_points(oss.ListAccessPointsRequest(
                bucket=bucket_name,
                max_keys=1,
                continuation_token='',
            ))

            self.assertEqual(200, result.status_code)
            self.assertEqual(1, result.max_keys)
            self.assertEqual('internet', result.access_points[0].network_origin)


            result = self.signv1_client.list_access_points(oss.ListAccessPointsRequest(
                max_keys=1,
                continuation_token=result.next_continuation_token,
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual(1, result.max_keys)
            self.assertEqual('internet', result.access_points[0].network_origin)



            # create access point policy
            result = self.signv1_client.put_access_point_policy(oss.PutAccessPointPolicyRequest(
                bucket=bucket_name,
                access_point_name=access_point_name_1,
                body=policy,
            ))
            self.assertEqual(200, result.status_code)



            # get access point policy
            result = self.signv1_client.get_access_point_policy(oss.GetAccessPointPolicyRequest(
                bucket=bucket_name,
                access_point_name=access_point_name_1,
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual(policy, result.body)



            # delete access point policy
            result = self.signv1_client.delete_access_point_policy(oss.DeleteAccessPointPolicyRequest(
                bucket=bucket_name,
                access_point_name=access_point_name_1,
            ))
            self.assertEqual(result.status_code, 204)



            # delete access point
            result = self.signv1_client.delete_access_point(oss.DeleteAccessPointRequest(
                bucket=bucket_name,
                access_point_name=access_point_name_1,
            ))
            self.assertEqual(result.status_code, 204)



            # delete access point
            result = self.signv1_client.delete_access_point(oss.DeleteAccessPointRequest(
                bucket=bucket_name,
                access_point_name=access_point_name_2,
            ))

            self.assertEqual(result.status_code, 204)

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



    def test_access_point_fail(self):
        bucket_name = random_bucket_name()
        access_point_name_1 = 'ap-test-oss-' + random_lowstr(6)
        policy = "{\"Version\":\"1\",\"Statement\":[{\"Action\":[\"oss:PutObject\",\"oss:GetObject\"],\"Effect\":\"Deny\",\"Principal\":[\"" + USER_ID + "\"],\"Resource\":[\"acs:oss:" + REGION + ":" + USER_ID + ":accesspoint/" + access_point_name_1 + "\",\"acs:oss:" + REGION + ":" + USER_ID + ":accesspoint/" + access_point_name_1 + "/object/*\"]}]}"

        try:
            self.invalid_client.create_access_point(oss.CreateAccessPointRequest(
                bucket=bucket_name,
                create_access_point_configuration=oss.CreateAccessPointConfiguration(
                    access_point_name=access_point_name_1,
                    network_origin='internet',
                ),
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(404, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('NoSuchBucket', serr.code)

        try:
            self.invalid_client.get_access_point_policy(oss.GetAccessPointPolicyRequest(
                bucket=bucket_name,
                access_point_name=access_point_name_1,
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(404, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('NoSuchBucket', serr.code)

        try:
            self.invalid_client.list_access_points(oss.ListAccessPointsRequest(
                bucket=bucket_name,
                max_keys=1,
                continuation_token='',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(404, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('NoSuchBucket', serr.code)

        try:
            self.invalid_client.put_access_point_policy(oss.PutAccessPointPolicyRequest(
                bucket=bucket_name,
                access_point_name=access_point_name_1,
                body=policy,
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(404, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('NoSuchBucket', serr.code)

        try:
            self.invalid_client.get_access_point_policy(oss.GetAccessPointPolicyRequest(
                bucket=bucket_name,
                access_point_name=access_point_name_1,
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(404, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('NoSuchBucket', serr.code)

        try:
            self.invalid_client.delete_access_point_policy(oss.DeleteAccessPointPolicyRequest(
                bucket=bucket_name,
                access_point_name=access_point_name_1,
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(404, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('NoSuchBucket', serr.code)


        try:
            self.invalid_client.delete_access_point(oss.DeleteAccessPointRequest(
                bucket=bucket_name,
                access_point_name=access_point_name_1,
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(404, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('NoSuchBucket', serr.code)


