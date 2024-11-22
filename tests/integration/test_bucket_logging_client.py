# pylint: skip-file

from typing import cast
import alibabacloud_oss_v2 as oss
from . import TestIntegration, random_bucket_name


class TestBucketLogging(TestIntegration):

    def test_bucket_logging(self):
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

        # put bucket logging
        result = self.client.put_bucket_logging(oss.PutBucketLoggingRequest(
            bucket=bucket_name,
            bucket_logging_status=oss.BucketLoggingStatus(
                logging_enabled=oss.LoggingEnabled(
                    target_bucket=bucket_name,
                    target_prefix='aE>@%ITkxX',
                ),
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket logging
        result = self.client.get_bucket_logging(oss.GetBucketLoggingRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(bucket_name, result.bucket_logging_status.logging_enabled.target_bucket)
        self.assertEqual('aE>@%ITkxX', result.bucket_logging_status.logging_enabled.target_prefix)

        # delete bucket logging
        result = self.client.delete_bucket_logging(oss.DeleteBucketLoggingRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # put user defined log fields config
        result = self.client.put_user_defined_log_fields_config(oss.PutUserDefinedLogFieldsConfigRequest(
            bucket=bucket_name,
            user_defined_log_fields_configuration=oss.UserDefinedLogFieldsConfiguration(
                header_set=oss.LoggingHeaderSet(
                    headers=[';YRUmR^oOZ', '6L1HYCXks#'],
                ),
                param_set=oss.LoggingParamSet(
                    parameters=[';OGrIUYln ', '>SS#m7k?)T'],
                ),
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get user defined log fields config
        result = self.client.get_user_defined_log_fields_config(oss.GetUserDefinedLogFieldsConfigRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(len([';YRUmR^oOZ', '6L1HYCXks#']), result.user_defined_log_fields_configuration.header_set.headers.__len__())
        self.assertEqual(len([';OGrIUYln ', '>SS#m7k?)T']), result.user_defined_log_fields_configuration.param_set.parameters.__len__())

        # delete user defined log fields config
        result = self.client.delete_user_defined_log_fields_config(oss.DeleteUserDefinedLogFieldsConfigRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

    def test_bucket_logging_v1(self):
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

        # put bucket logging
        result = self.signv1_client.put_bucket_logging(oss.PutBucketLoggingRequest(
            bucket=bucket_name,
            bucket_logging_status=oss.BucketLoggingStatus(
                logging_enabled=oss.LoggingEnabled(
                    target_bucket=bucket_name,
                    target_prefix='aE>@%ITkxX',
                ),
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket logging
        result = self.signv1_client.get_bucket_logging(oss.GetBucketLoggingRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(bucket_name, result.bucket_logging_status.logging_enabled.target_bucket)
        self.assertEqual('aE>@%ITkxX', result.bucket_logging_status.logging_enabled.target_prefix)

        # delete bucket logging
        result = self.signv1_client.delete_bucket_logging(oss.DeleteBucketLoggingRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # put user defined log fields config
        result = self.signv1_client.put_user_defined_log_fields_config(oss.PutUserDefinedLogFieldsConfigRequest(
            bucket=bucket_name,
            user_defined_log_fields_configuration=oss.UserDefinedLogFieldsConfiguration(
                header_set=oss.LoggingHeaderSet(
                    headers=[')$k+$;jm+', '5;O$QXOCK2'],
                ),
                param_set=oss.LoggingParamSet(
                    parameters=['IpaR(ad~p', ';uza,9yf71'],
                ),
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get user defined log fields config
        result = self.signv1_client.get_user_defined_log_fields_config(oss.GetUserDefinedLogFieldsConfigRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(len([')$k+$;jm+', '5;O$QXOCK2']), result.user_defined_log_fields_configuration.header_set.headers.__len__())
        self.assertEqual(len(['IpaR(ad~p', ';uza,9yf71']), result.user_defined_log_fields_configuration.param_set.parameters.__len__())

        # delete user defined log fields config
        result = self.signv1_client.delete_user_defined_log_fields_config(oss.DeleteUserDefinedLogFieldsConfigRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))


    def test_bucket_logging_fail(self):
        # create bucket
        bucket_name = random_bucket_name()
        self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))

        # put bucket logging
        try:
            self.invalid_client.put_bucket_logging(oss.PutBucketLoggingRequest(
                bucket=bucket_name,
                bucket_logging_status=oss.BucketLoggingStatus(
                    logging_enabled=oss.LoggingEnabled(
                        target_bucket='q7~sjKc_Lw',
                        target_prefix='aE>@%ITkxX',
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

        # get bucket logging
        try:
            self.invalid_client.get_bucket_logging(oss.GetBucketLoggingRequest(
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

        # delete bucket logging
        try:
            self.invalid_client.delete_bucket_logging(oss.DeleteBucketLoggingRequest(
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

        # put user defined log fields config
        try:
            self.invalid_client.put_user_defined_log_fields_config(oss.PutUserDefinedLogFieldsConfigRequest(
                bucket=bucket_name,
                user_defined_log_fields_configuration=oss.UserDefinedLogFieldsConfiguration(
                    header_set=oss.LoggingHeaderSet(
                        headers=['D@R4G3@Uf;', 'C9xW_T%(hE'],
                    ),
                    param_set=oss.LoggingParamSet(
                        parameters=['Hmb/Lra_~Q', 'FNmTE+w;%e'],
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

        # get user defined log fields config
        try:
            self.invalid_client.get_user_defined_log_fields_config(oss.GetUserDefinedLogFieldsConfigRequest(
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

        # delete user defined log fields config
        try:
            self.invalid_client.delete_user_defined_log_fields_config(oss.DeleteUserDefinedLogFieldsConfigRequest(
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
