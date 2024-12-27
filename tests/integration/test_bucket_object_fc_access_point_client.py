# pylint: skip-file
import time
from typing import cast
import alibabacloud_oss_v2 as oss
from . import TestIntegration, random_bucket_name, random_lowstr, REGION, USER_ID


class TestBucketObjectFcAccessPoint(TestIntegration):

    def test_access_point_for_object_process(self):
        access_point_name = 'ap-test-oss-' + random_lowstr(6)
        access_point_for_object_process_name = 'ap-test-process-' + random_lowstr(2)

        policy = "{\"Version\":\"1\",\"Statement\":[{\"Action\":[\"oss:PutObject\",\"oss:GetObject\"],\"Effect\":\"Allow\",\"Principal\":[\"" + USER_ID + "\"],\"Resource\":[\"acs:oss:" + REGION + ":" + USER_ID + ":accesspointforobjectprocess/" + access_point_for_object_process_name + "\",\"acs:oss:" + REGION + ":" + USER_ID + ":accesspointforobjectprocess/" + access_point_for_object_process_name + "/object/*\"]}]}"

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
                access_point_name=access_point_name,
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
                    access_point_name=access_point_name,
                ))

                if num > 180:
                    break

                if get_result.status == 'enable':
                    break

                num += 1
                time.sleep(5)

            # create access point for object process
            result = self.client.create_access_point_for_object_process(oss.CreateAccessPointForObjectProcessRequest(
                bucket=bucket_name,
                access_point_for_object_process_name=access_point_for_object_process_name,
                create_access_point_for_object_process_configuration=oss.CreateAccessPointForObjectProcessConfiguration(
                    access_point_name=access_point_name,
                    object_process_configuration=oss.ObjectProcessConfiguration(
                        allowed_features=oss.AllowedFeatures(
                            allowed_features=['GetObject-Range'],
                        ),
                        transformation_configurations=oss.TransformationConfigurations(
                            transformation_configurations=[oss.TransformationConfiguration(
                                actions=oss.AccessPointActions(
                                    actions=['GetObject'],
                                ),
                                content_transformation=oss.ContentTransformation(
                                    function_compute=oss.FunctionCompute(
                                        function_assume_role_arn='acs:ram::111933544165:role/aliyunfcdefaultrole',
                                        function_arn='acs:fc:cn-qingdao:111933544165:services/test-oss-fc.LATEST/functions/fc-01',
                                    ),
                                    additional_features=oss.AdditionalFeatures(
                                        custom_forward_headers=oss.CustomForwardHeaders(
                                            custom_forward_headers=['header1', 'header2'],
                                        ),
                                    ),
                                ),
                            )],
                        ),
                    ),
                ),
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual('OK', result.status)
            self.assertEqual(24, len(result.request_id))
            self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

            # get access point config for object process
            num = 1
            while True:
                get_result = self.client.get_access_point_for_object_process(oss.GetAccessPointForObjectProcessRequest(
                    bucket=bucket_name,
                    access_point_for_object_process_name=access_point_for_object_process_name,
                ))

                if num > 180:
                    break

                if get_result.fc_status == 'enable':
                    break

                num += 1
                time.sleep(5)

            # get access point for object process
            result = self.client.get_access_point_for_object_process(oss.GetAccessPointForObjectProcessRequest(
                bucket=bucket_name,
                access_point_for_object_process_name=access_point_for_object_process_name,
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual('OK', result.status)
            self.assertEqual(24, len(result.request_id))
            self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
            self.assertEqual(access_point_for_object_process_name, result.access_point_name_for_object_process)
            self.assertEqual(access_point_name, result.access_point_name)
            self.assertEqual('enable', result.fc_status)
            self.assertIsNotNone(result.account_id)
            self.assertIsNotNone(result.access_point_for_object_process_arn)
            self.assertEqual(False, result.public_access_block_configuration.block_public_access)
            self.assertIsNotNone(result.creation_date)
            self.assertIsNotNone(result.endpoints.public_endpoint)
            self.assertIsNotNone(result.endpoints.internal_endpoint)


            # list access points for object process
            result = self.client.list_access_points_for_object_process(oss.ListAccessPointsForObjectProcessRequest(
                max_keys=10,
                continuation_token='',
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual('OK', result.status)
            self.assertEqual(24, len(result.request_id))
            self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

            # put access point config for object process
            result = self.client.put_access_point_config_for_object_process(oss.PutAccessPointConfigForObjectProcessRequest(
                bucket=bucket_name,
                access_point_for_object_process_name=access_point_for_object_process_name,
                put_access_point_config_for_object_process_configuration=oss.PutAccessPointConfigForObjectProcessConfiguration(
                    public_access_block_configuration=oss.PublicAccessBlockConfiguration(
                        block_public_access=True,
                    ),
                    object_process_configuration=oss.ObjectProcessConfiguration(
                        allowed_features=oss.AllowedFeatures(
                            allowed_feature=['GetObject-Range'],
                        ),
                        transformation_configurations=oss.TransformationConfigurations(
                            transformation_configuration=[oss.TransformationConfiguration(
                                actions=oss.AccessPointActions(
                                    actions=['GetObject'],
                                ),
                                content_transformation=oss.ContentTransformation(
                                    function_compute=oss.FunctionCompute(
                                        function_assume_role_arn='acs:ram::111933544165:role/aliyunfcdefaultrole',
                                        function_arn='acs:fc:cn-qingdao:111933544165:services/test-oss-fc.LATEST/functions/fc-01',
                                    ),
                                    additional_features=oss.AdditionalFeatures(
                                        custom_forward_headers=oss.CustomForwardHeaders(
                                            custom_forward_headers=['header1', 'header2'],
                                        ),
                                    ),
                                ),
                            )],
                        ),
                    ),
                ),
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual('OK', result.status)
            self.assertEqual(24, len(result.request_id))
            self.assertEqual(24, len(result.headers.get('x-oss-request-id')))


            # get access point config for object process
            result = self.client.get_access_point_config_for_object_process(oss.GetAccessPointConfigForObjectProcessRequest(
                bucket=bucket_name,
                access_point_for_object_process_name=access_point_for_object_process_name,
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual('OK', result.status)
            self.assertEqual(24, len(result.request_id))
            self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

            # put access point policy for object process
            result = self.client.put_access_point_policy_for_object_process(oss.PutAccessPointPolicyForObjectProcessRequest(
                bucket=bucket_name,
                access_point_for_object_process_name=access_point_for_object_process_name,
                body=policy,
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual('OK', result.status)
            self.assertEqual(24, len(result.request_id))
            self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

            # get access point policy for object process
            result = self.client.get_access_point_policy_for_object_process(oss.GetAccessPointPolicyForObjectProcessRequest(
                bucket=bucket_name,
                access_point_for_object_process_name=access_point_for_object_process_name,
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual('OK', result.status)
            self.assertEqual(24, len(result.request_id))
            self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
            self.assertEqual(policy, result.body)

            # delete access point policy for object process
            result = self.client.delete_access_point_policy_for_object_process(oss.DeleteAccessPointPolicyForObjectProcessRequest(
                bucket=bucket_name,
                access_point_for_object_process_name=access_point_for_object_process_name,
            ))
            self.assertEqual(204, result.status_code)
            self.assertEqual(24, len(result.request_id))
            self.assertEqual(24, len(result.headers.get('x-oss-request-id')))


        except Exception as e:
            print("Exception: {0}".format(e))
        finally:
            # Delete all access points for object process under the bucket
            num_apop = 1
            while True:
                list_result = self.client.list_access_points_for_object_process(oss.ListAccessPointsForObjectProcessRequest(
                    max_keys=10,
                    continuation_token='',
                ))

                if list_result.access_points_for_object_process is None or list_result.access_points_for_object_process.access_point_for_object_processs is None:
                    print(f"all access point for object process is delete")
                    break

                if num_apop > 180:
                    break

                for apop in list_result.access_points_for_object_process.access_point_for_object_processs:
                    if apop.status == 'enable':
                        print(f"apop name: {apop.access_point_name_for_object_process}, status: {apop.status}")
                        del_result = self.client.delete_access_point_for_object_process(oss.DeleteAccessPointForObjectProcessRequest(
                            bucket=bucket_name,
                            access_point_for_object_process_name=apop.access_point_name_for_object_process,
                        ))
                        self.assertEqual(del_result.status_code, 204)
                        print(f"delete_access_point_for_object_process: {apop.access_point_name_for_object_process}")

                num_apop += 1
                time.sleep(5)

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
                            print(f"delete access point: {ap.access_point_name}")


                num += 1
                time.sleep(10)


    def test_access_point_for_object_process_v1(self):
        access_point_name = 'ap-test-oss-' + random_lowstr(6)
        access_point_for_object_process_name = 'ap-test-process-' + random_lowstr(2)
        policy = "{\"Version\":\"1\",\"Statement\":[{\"Action\":[\"oss:PutObject\",\"oss:GetObject\"],\"Effect\":\"Allow\",\"Principal\":[\"" + USER_ID + "\"],\"Resource\":[\"acs:oss:" + REGION + ":" + USER_ID + ":accesspointforobjectprocess/" + access_point_for_object_process_name + "\",\"acs:oss:" + REGION + ":" + USER_ID + ":accesspointforobjectprocess/" + access_point_for_object_process_name + "/object/*\"]}]}"

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
                access_point_name=access_point_name,
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
                    access_point_name=access_point_name,
                ))

                if num > 180:
                    break

                if get_result.status == 'enable':
                    break

                num += 1
                time.sleep(5)

            # create access point for object process
            result = self.signv1_client.create_access_point_for_object_process(oss.CreateAccessPointForObjectProcessRequest(
                bucket=bucket_name,
                access_point_for_object_process_name=access_point_for_object_process_name,
                create_access_point_for_object_process_configuration=oss.CreateAccessPointForObjectProcessConfiguration(
                    access_point_name=access_point_name,
                    object_process_configuration=oss.ObjectProcessConfiguration(
                        allowed_features=oss.AllowedFeatures(
                            allowed_features=['GetObject-Range'],
                        ),
                        transformation_configurations=oss.TransformationConfigurations(
                            transformation_configurations=[oss.TransformationConfiguration(
                                actions=oss.AccessPointActions(
                                    actions=['GetObject'],
                                ),
                                content_transformation=oss.ContentTransformation(
                                    function_compute=oss.FunctionCompute(
                                        function_assume_role_arn='acs:ram::111933544165:role/aliyunfcdefaultrole',
                                        function_arn='acs:fc:cn-qingdao:111933544165:services/test-oss-fc.LATEST/functions/fc-01',
                                    ),
                                    additional_features=oss.AdditionalFeatures(
                                        custom_forward_headers=oss.CustomForwardHeaders(
                                            custom_forward_headers=['header1', 'header2'],
                                        ),
                                    ),
                                ),
                            )],
                        ),
                    ),
                ),
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual('OK', result.status)
            self.assertEqual(24, len(result.request_id))
            self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

            # get access point config for object process
            num = 1
            while True:
                get_result = self.signv1_client.get_access_point_for_object_process(oss.GetAccessPointForObjectProcessRequest(
                    bucket=bucket_name,
                    access_point_for_object_process_name=access_point_for_object_process_name,
                ))

                if num > 180:
                    break

                if get_result.fc_status == 'enable':
                    break

                num += 1
                time.sleep(5)

            # get access point for object process
            result = self.signv1_client.get_access_point_for_object_process(oss.GetAccessPointForObjectProcessRequest(
                bucket=bucket_name,
                access_point_for_object_process_name=access_point_for_object_process_name,
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual('OK', result.status)
            self.assertEqual(24, len(result.request_id))
            self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
            self.assertEqual(access_point_for_object_process_name, result.access_point_name_for_object_process)
            self.assertEqual(access_point_name, result.access_point_name)
            self.assertEqual('enable', result.fc_status)
            self.assertIsNotNone(result.account_id)
            self.assertIsNotNone(result.access_point_for_object_process_arn)
            self.assertEqual(False, result.public_access_block_configuration.block_public_access)
            self.assertIsNotNone(result.creation_date)
            self.assertIsNotNone(result.endpoints.public_endpoint)
            self.assertIsNotNone(result.endpoints.internal_endpoint)

            # list access points for object process
            result = self.signv1_client.list_access_points_for_object_process(oss.ListAccessPointsForObjectProcessRequest(
                max_keys=10,
                continuation_token='',
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual('OK', result.status)
            self.assertEqual(24, len(result.request_id))
            self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

            # put access point config for object process
            result = self.signv1_client.put_access_point_config_for_object_process(oss.PutAccessPointConfigForObjectProcessRequest(
                bucket=bucket_name,
                access_point_for_object_process_name=access_point_for_object_process_name,
                put_access_point_config_for_object_process_configuration=oss.PutAccessPointConfigForObjectProcessConfiguration(
                    public_access_block_configuration=oss.PublicAccessBlockConfiguration(
                        block_public_access=True,
                    ),
                    object_process_configuration=oss.ObjectProcessConfiguration(
                        allowed_features=oss.AllowedFeatures(
                            allowed_feature=['GetObject-Range'],
                        ),
                        transformation_configurations=oss.TransformationConfigurations(
                            transformation_configuration=[oss.TransformationConfiguration(
                                actions=oss.AccessPointActions(
                                    actions=['GetObject'],
                                ),
                                content_transformation=oss.ContentTransformation(
                                    function_compute=oss.FunctionCompute(
                                        function_assume_role_arn='acs:ram::111933544165:role/aliyunfcdefaultrole',
                                        function_arn='acs:fc:cn-qingdao:111933544165:services/test-oss-fc.LATEST/functions/fc-01',
                                    ),
                                    additional_features=oss.AdditionalFeatures(
                                        custom_forward_headers=oss.CustomForwardHeaders(
                                            custom_forward_headers=['header1', 'header2'],
                                        ),
                                    ),
                                ),
                            )],
                        ),
                    ),
                ),
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual('OK', result.status)
            self.assertEqual(24, len(result.request_id))
            self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

            # get access point config for object process
            result = self.signv1_client.get_access_point_config_for_object_process(oss.GetAccessPointConfigForObjectProcessRequest(
                bucket=bucket_name,
                access_point_for_object_process_name=access_point_for_object_process_name,
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual('OK', result.status)
            self.assertEqual(24, len(result.request_id))
            self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

            # put access point policy for object process
            result = self.signv1_client.put_access_point_policy_for_object_process(oss.PutAccessPointPolicyForObjectProcessRequest(
                bucket=bucket_name,
                access_point_for_object_process_name=access_point_for_object_process_name,
                body=policy,
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual('OK', result.status)
            self.assertEqual(24, len(result.request_id))
            self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

            # get access point policy for object process
            result = self.signv1_client.get_access_point_policy_for_object_process(oss.GetAccessPointPolicyForObjectProcessRequest(
                bucket=bucket_name,
                access_point_for_object_process_name=access_point_for_object_process_name,
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual('OK', result.status)
            self.assertEqual(24, len(result.request_id))
            self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
            self.assertEqual(policy, result.body)

            # delete access point policy for object process
            result = self.signv1_client.delete_access_point_policy_for_object_process(oss.DeleteAccessPointPolicyForObjectProcessRequest(
                bucket=bucket_name,
                access_point_for_object_process_name=access_point_for_object_process_name,
            ))
            self.assertEqual(204, result.status_code)
            self.assertEqual(24, len(result.request_id))
            self.assertEqual(24, len(result.headers.get('x-oss-request-id')))


        except Exception as e:
            print("Exception: {0}".format(e))
        finally:
            # Delete all access points for object process under the bucket
            num_apop = 1
            while True:
                list_result = self.signv1_client.list_access_points_for_object_process(oss.ListAccessPointsForObjectProcessRequest(
                    max_keys=10,
                    continuation_token='',
                ))

                if list_result.access_points_for_object_process is None or list_result.access_points_for_object_process.access_point_for_object_processs is None:
                    print(f"all access point for object process is delete")
                    break

                if num_apop > 180:
                    break

                for apop in list_result.access_points_for_object_process.access_point_for_object_processs:
                    if apop.status == 'enable':
                        print(f"apop name: {apop.access_point_name_for_object_process}, status: {apop.status}")
                        del_result = self.signv1_client.delete_access_point_for_object_process(oss.DeleteAccessPointForObjectProcessRequest(
                            bucket=bucket_name,
                            access_point_for_object_process_name=apop.access_point_name_for_object_process,
                        ))
                        self.assertEqual(del_result.status_code, 204)
                        print(f"delete_access_point_for_object_process: {apop.access_point_name_for_object_process}")

                num_apop += 1
                time.sleep(5)

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
                            print(f"delete access point: {ap.access_point_name}")

                num += 1
                time.sleep(10)

    def test_access_point_for_object_process_fail(self):
        # create bucket
        bucket_name = random_bucket_name()
        self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))

        # create access point for object process
        try:
            self.invalid_client.create_access_point_for_object_process(oss.CreateAccessPointForObjectProcessRequest(
                bucket=bucket_name,
                access_point_for_object_process_name='test_access_point_for_object_process_name',
                create_access_point_for_object_process_configuration=oss.CreateAccessPointForObjectProcessConfiguration(
                    allow_anonymous_access_for_object_process='test_allow_anonymous_access_for_object_process',
                    access_point_name='test_access_point_name',
                    object_process_configuration=oss.ObjectProcessConfiguration(
                        allowed_features=oss.AllowedFeatures(
                            allowed_feature=['b2aADLXX51', 'pOUxKXIffY'],
                        ),
                        transformation_configurations=oss.TransformationConfigurations(
                            transformation_configuration=[oss.TransformationConfiguration(
                                actions=oss.AccessPointActions(
                                    actions=['F2kfimeKT6', 'RIQZ9CaF3d'],
                                ),
                                content_transformation=oss.ContentTransformation(
                                    function_compute=oss.FunctionCompute(
                                        function_assume_role_arn='test_function_assume_role_arn',
                                        function_arn='test_function_arn',
                                    ),
                                    additional_features=oss.AdditionalFeatures(
                                        custom_forward_headers=oss.CustomForwardHeaders(
                                            custom_forward_headers=['hx2ap1sXUg', 'i6p0Bo3wpj'],
                                        ),
                                    ),
                                ),
                            )],
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

        # get access point config for object process
        try:
            self.invalid_client.get_access_point_config_for_object_process(oss.GetAccessPointConfigForObjectProcessRequest(
                bucket=bucket_name,
                access_point_for_object_process_name='test_access_point_for_object_process_name',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        # list access points for object process
        try:
            self.invalid_client.list_access_points_for_object_process(oss.ListAccessPointsForObjectProcessRequest(
                max_keys=10,
                continuation_token='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)



        # delete access point for object process
        try:
            self.invalid_client.delete_access_point_for_object_process(oss.DeleteAccessPointForObjectProcessRequest(
                bucket=bucket_name,
                access_point_for_object_process_name='test_access_point_for_object_process_name',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        # put access point config for object process
        try:
            self.invalid_client.create_access_point_for_object_process(oss.CreateAccessPointForObjectProcessRequest(
                bucket=bucket_name,
                access_point_for_object_process_name='test_access_point_for_object_process_name',
                create_access_point_for_object_process_configuration=oss.CreateAccessPointForObjectProcessConfiguration(
                    allow_anonymous_access_for_object_process='test_allow_anonymous_access_for_object_process',
                    access_point_name='test_access_point_name',
                    object_process_configuration=oss.ObjectProcessConfiguration(
                        allowed_features=oss.AllowedFeatures(
                            allowed_feature=['b2aADLXX51', 'pOUxKXIffY'],
                        ),
                        transformation_configurations=oss.TransformationConfigurations(
                            transformation_configuration=[oss.TransformationConfiguration(
                                actions=oss.AccessPointActions(
                                    actions=['F2kfimeKT6', 'RIQZ9CaF3d'],
                                ),
                                content_transformation=oss.ContentTransformation(
                                    function_compute=oss.FunctionCompute(
                                        function_assume_role_arn='test_function_assume_role_arn',
                                        function_arn='test_function_arn',
                                    ),
                                    additional_features=oss.AdditionalFeatures(
                                        custom_forward_headers=oss.CustomForwardHeaders(
                                            custom_forward_headers=['hx2ap1sXUg', 'i6p0Bo3wpj'],
                                        ),
                                    ),
                                ),
                            )],
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

        # get access point config for object process
        try:
            self.invalid_client.get_access_point_config_for_object_process(oss.GetAccessPointConfigForObjectProcessRequest(
                bucket=bucket_name,
                access_point_for_object_process_name='test_access_point_for_object_process_name',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        # put access point policy for object process
        try:
            self.invalid_client.put_access_point_policy_for_object_process(oss.PutAccessPointPolicyForObjectProcessRequest(
                bucket=bucket_name,
                access_point_for_object_process_name='test_access_point_for_object_process_name',
                body='xml_data',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        # get access point policy for object process
        try:
            self.invalid_client.get_access_point_policy_for_object_process(oss.GetAccessPointPolicyForObjectProcessRequest(
                bucket=bucket_name,
                access_point_for_object_process_name='test_access_point_for_object_process_name',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        # delete access point policy for object process
        try:
            self.invalid_client.delete_access_point_policy_for_object_process(oss.DeleteAccessPointPolicyForObjectProcessRequest(
                bucket=bucket_name,
                access_point_for_object_process_name='test_access_point_for_object_process_name',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)


        # write get object response
        try:
            self.invalid_client.write_get_object_response(oss.WriteGetObjectResponseRequest(
                request_route='RouteFromFcEvent',
                request_token='TokenFromFcEvent',
                fwd_status='200',
                fwd_header_accept_ranges='bytes',
                fwd_header_cache_control='no-cache',
                fwd_header_content_disposition='attachment',
                fwd_header_content_encoding='gzip',
                fwd_header_content_language='en',
                fwd_header_content_range='bytes 0-9/67589',
                fwd_header_content_type='text/html; charset=utf-8',
                fwd_header_etag='D41D8CD98F00B204E9800998ECF8****',
                fwd_header_expires='Fri, 10 Nov 2023 03:17:58 GMT',
                fwd_header_last_modified='Tue, 10 Oct 2023 03:17:58 GMT',
                body='data',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(404, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('NoSuchBucket', serr.code)