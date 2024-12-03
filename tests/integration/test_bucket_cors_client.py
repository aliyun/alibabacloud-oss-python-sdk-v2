# pylint: skip-file

from typing import cast
import alibabacloud_oss_v2 as oss
from . import TestIntegration, random_bucket_name


class TestBucketCors(TestIntegration):

    def test_bucket_cors(self):
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

        # put bucket cors
        result = self.client.put_bucket_cors(oss.PutBucketCorsRequest(
            bucket=bucket_name,
            cors_configuration=oss.CORSConfiguration(
                cors_rules=[oss.CORSRule(
                    allowed_origins=['*'],
                    allowed_methods=['GET', 'HEAD'],
                    allowed_headers=['GET'],
                    expose_headers=['x-oss-test', 'x-oss-test1'],
                    max_age_seconds=33012,
                ), oss.CORSRule(
                    allowed_origins=['http://www.example.com'],
                    allowed_methods=['PUT', 'POST'],
                    allowed_headers=['*'],
                    expose_headers=['x-oss-test2', 'x-oss-test3'],
                    max_age_seconds=33012,
                )],
                response_vary=True,
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket cors
        result = self.client.get_bucket_cors(oss.GetBucketCorsRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('*', result.cors_configuration.cors_rules[0].allowed_origins[0])
        self.assertEqual('GET', result.cors_configuration.cors_rules[0].allowed_methods[0])
        self.assertEqual('HEAD', result.cors_configuration.cors_rules[0].allowed_methods[1])
        self.assertEqual('GET'.lower(), result.cors_configuration.cors_rules[0].allowed_headers[0])
        self.assertEqual('x-oss-test', result.cors_configuration.cors_rules[0].expose_headers[0])
        self.assertEqual('x-oss-test1', result.cors_configuration.cors_rules[0].expose_headers[1])
        self.assertEqual(33012, result.cors_configuration.cors_rules[0].max_age_seconds)
        self.assertEqual('http://www.example.com', result.cors_configuration.cors_rules[1].allowed_origins[0])
        self.assertEqual('PUT', result.cors_configuration.cors_rules[1].allowed_methods[0])
        self.assertEqual('POST', result.cors_configuration.cors_rules[1].allowed_methods[1])
        self.assertEqual('*', result.cors_configuration.cors_rules[1].allowed_headers[0])
        self.assertEqual('x-oss-test2', result.cors_configuration.cors_rules[1].expose_headers[0])
        self.assertEqual('x-oss-test3', result.cors_configuration.cors_rules[1].expose_headers[1])
        self.assertEqual(33012, result.cors_configuration.cors_rules[1].max_age_seconds)
        self.assertEqual(True, result.cors_configuration.response_vary)

        # option object
        result = self.client.option_object(oss.OptionObjectRequest(
            bucket=bucket_name,
            key='example-object-2.jpg',
            origin='http://www.example.com',
            access_control_request_method='PUT',
            access_control_request_headers='x-oss-test2',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('http://www.example.com', result.access_control_allow_origin)
        self.assertEqual('PUT, POST', result.access_control_allow_methods)
        self.assertEqual('x-oss-test2', result.access_control_allow_headers)

        # delete bucket cors
        result = self.client.delete_bucket_cors(oss.DeleteBucketCorsRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

    def test_bucket_cors_v1(self):
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

        # put bucket cors
        result = self.signv1_client.put_bucket_cors(oss.PutBucketCorsRequest(
            bucket=bucket_name,
            cors_configuration=oss.CORSConfiguration(
                cors_rules=[oss.CORSRule(
                    allowed_origins=['*'],
                    allowed_methods=['GET', 'HEAD'],
                    allowed_headers=['GET'],
                    expose_headers=['x-oss-test', 'x-oss-test1'],
                    max_age_seconds=33012,
                ), oss.CORSRule(
                    allowed_origins=['http://www.example.com'],
                    allowed_methods=['PUT', 'POST'],
                    allowed_headers=['*'],
                    expose_headers=['x-oss-test2', 'x-oss-test3'],
                    max_age_seconds=33012,
                )],
                response_vary=True,
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket cors
        result = self.signv1_client.get_bucket_cors(oss.GetBucketCorsRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('*', result.cors_configuration.cors_rules[0].allowed_origins[0])
        self.assertEqual('GET', result.cors_configuration.cors_rules[0].allowed_methods[0])
        self.assertEqual('HEAD', result.cors_configuration.cors_rules[0].allowed_methods[1])
        self.assertEqual('GET'.lower(), result.cors_configuration.cors_rules[0].allowed_headers[0])
        self.assertEqual('x-oss-test', result.cors_configuration.cors_rules[0].expose_headers[0])
        self.assertEqual('x-oss-test1', result.cors_configuration.cors_rules[0].expose_headers[1])
        self.assertEqual(33012, result.cors_configuration.cors_rules[0].max_age_seconds)
        self.assertEqual('http://www.example.com', result.cors_configuration.cors_rules[1].allowed_origins[0])
        self.assertEqual('PUT', result.cors_configuration.cors_rules[1].allowed_methods[0])
        self.assertEqual('POST', result.cors_configuration.cors_rules[1].allowed_methods[1])
        self.assertEqual('*', result.cors_configuration.cors_rules[1].allowed_headers[0])
        self.assertEqual('x-oss-test2', result.cors_configuration.cors_rules[1].expose_headers[0])
        self.assertEqual('x-oss-test3', result.cors_configuration.cors_rules[1].expose_headers[1])
        self.assertEqual(33012, result.cors_configuration.cors_rules[1].max_age_seconds)
        self.assertEqual(True, result.cors_configuration.response_vary)

        # option object
        result = self.signv1_client.option_object(oss.OptionObjectRequest(
            bucket=bucket_name,
            key='example-object-2.jpg',
            origin='http://www.example.com',
            access_control_request_method='PUT',
            access_control_request_headers='x-oss-test2',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('http://www.example.com', result.access_control_allow_origin)
        self.assertEqual('PUT, POST', result.access_control_allow_methods)
        self.assertEqual('x-oss-test2', result.access_control_allow_headers)

        # delete bucket cors
        result = self.signv1_client.delete_bucket_cors(oss.DeleteBucketCorsRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))


    def test_bucket_cors_fail(self):
        # create bucket
        bucket_name = random_bucket_name()
        self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))

        # put bucket cors
        try:
            self.invalid_client.put_bucket_cors(oss.PutBucketCorsRequest(
                bucket=bucket_name,
                cors_configuration=oss.CORSConfiguration(
                    cors_rules=[oss.CORSRule(
                        allowed_origins=['*'],
                        allowed_methods=['GET', 'HEAD'],
                        allowed_headers=['GET'],
                        expose_headers=['x-oss-test', 'x-oss-test1'],
                        max_age_seconds=33012,
                    ), oss.CORSRule(
                        allowed_origins=['http://www.example.com'],
                        allowed_methods=['PUT', 'POST'],
                        allowed_headers=['*'],
                        expose_headers=['x-oss-test2', 'x-oss-test3'],
                        max_age_seconds=33012,
                    )],
                    response_vary=True,
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

        # get bucket cors
        try:
            self.invalid_client.get_bucket_cors(oss.GetBucketCorsRequest(
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

        # delete bucket cors
        try:
            self.invalid_client.delete_bucket_cors(oss.DeleteBucketCorsRequest(
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

        # option object
        try:
            self.invalid_client.option_object(oss.OptionObjectRequest(
                bucket=bucket_name,
                key='example-object-2.jpg',
                origin='http://www.example.com',
                access_control_request_method='PUT',
                access_control_request_headers='x-oss-test2',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('AccessForbidden', serr.code)
