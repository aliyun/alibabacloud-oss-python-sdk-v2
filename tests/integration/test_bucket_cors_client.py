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
                    allowed_origins=['Jsd>>S5swN', '~Pb*_W!E@F'],
                    allowed_methods=['GET', 'HEAD'],
                    allowed_headers=['WqFg#jPAj(', 'l~m^57q>,F'],
                    expose_headers=['|K+k~ wJIC', 'B~0-iQ5sbj'],
                    max_age_seconds=33012,
                ), oss.CORSRule(
                    allowed_origins=['r.ABJZsGEd', 'n*TC(El)~:'],
                    allowed_methods=['PUT', 'POST'],
                    allowed_headers=['xrR~F1kUZt', 'bjbVO%XSYe'],
                    expose_headers=['&W%XZmBig6', '+Cp-LuC#vu'],
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
        self.assertEqual(['Jsd>>S5swN', '~Pb*_W!E@F'], result.cors_configuration.cors_rules[0].allowed_origins)
        self.assertEqual(['GET', 'HEAD'], result.cors_configuration.cors_rules[0].allowed_methods)
        self.assertEqual(['WqFg#jPAj('.lower(), 'l~m^57q>,F'.lower()], result.cors_configuration.cors_rules[0].allowed_headers)
        self.assertEqual(['|K+k~ wJIC', 'B~0-iQ5sbj'], result.cors_configuration.cors_rules[0].expose_headers)
        self.assertEqual(33012, result.cors_configuration.cors_rules[0].max_age_seconds)
        self.assertEqual(['r.ABJZsGEd', 'n*TC(El)~:'], result.cors_configuration.cors_rules[1].allowed_origins)
        self.assertEqual(['PUT', 'POST'], result.cors_configuration.cors_rules[1].allowed_methods)
        self.assertEqual(['xrR~F1kUZt'.lower(), 'bjbVO%XSYe'.lower()], result.cors_configuration.cors_rules[1].allowed_headers)
        self.assertEqual(['&W%XZmBig6', '+Cp-LuC#vu'], result.cors_configuration.cors_rules[1].expose_headers)
        self.assertEqual(33012, result.cors_configuration.cors_rules[1].max_age_seconds)
        self.assertEqual(True, result.cors_configuration.response_vary)

        # option object
        result = self.client.option_object(oss.OptionObjectRequest(
            bucket=bucket_name,
            key='example-object-2.jpg',
            origin='Jsd>>S5swN',
            access_control_request_method='HEAD',
            access_control_request_headers='WqFg#jPAj(',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('Jsd>>S5swN', result.access_control_allow_origin)
        self.assertEqual('GET, HEAD', result.access_control_allow_methods)
        self.assertEqual('WqFg#jPAj(', result.access_control_allow_headers)

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
                    allowed_origins=['3Lt@.6iq)8', '_mDCcVl1iG'],
                    allowed_methods=['DELETE', 'HEAD'],
                    allowed_headers=['j5VP*Yfjq_', '#rgmVDBfTW'],
                    expose_headers=['zK4d3,tLfa', '&d!RA4)xR~'],
                    max_age_seconds=33012,
                ), oss.CORSRule(
                    allowed_origins=['v8 GT-+V<I', ')q(A8&^FZQ'],
                    allowed_methods=['PUT', 'POST'],
                    allowed_headers=['QT^EA+kio?', 'ew_CTE+WbL'],
                    expose_headers=['p^?ub~R+$F', 'I$%-O?d$ZK'],
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
        self.assertEqual(['3Lt@.6iq)8', '_mDCcVl1iG'], result.cors_configuration.cors_rules[0].allowed_origins)
        self.assertEqual(['DELETE', 'HEAD'], result.cors_configuration.cors_rules[0].allowed_methods)
        self.assertEqual(['j5VP*Yfjq_'.lower(), '#rgmVDBfTW'.lower()], result.cors_configuration.cors_rules[0].allowed_headers)
        self.assertEqual(['zK4d3,tLfa', '&d!RA4)xR~'], result.cors_configuration.cors_rules[0].expose_headers)
        self.assertEqual(33012, result.cors_configuration.cors_rules[0].max_age_seconds)
        self.assertEqual(['v8 GT-+V<I', ')q(A8&^FZQ'], result.cors_configuration.cors_rules[1].allowed_origins)
        self.assertEqual(['PUT', 'POST'], result.cors_configuration.cors_rules[1].allowed_methods)
        self.assertEqual(['QT^EA+kio?'.lower(), 'ew_CTE+WbL'.lower()], result.cors_configuration.cors_rules[1].allowed_headers)
        self.assertEqual(['p^?ub~R+$F', 'I$%-O?d$ZK'], result.cors_configuration.cors_rules[1].expose_headers)
        self.assertEqual(33012, result.cors_configuration.cors_rules[1].max_age_seconds)
        self.assertEqual(True, result.cors_configuration.response_vary)

        # option object
        result = self.signv1_client.option_object(oss.OptionObjectRequest(
            bucket=bucket_name,
            key='example-object-2.jpg',
            origin=')q(A8&^FZQ',
            access_control_request_method='POST',
            access_control_request_headers='ew_CTE+WbL',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(')q(A8&^FZQ', result.access_control_allow_origin)
        self.assertEqual('PUT, POST', result.access_control_allow_methods)
        self.assertEqual('ew_CTE+WbL', result.access_control_allow_headers)

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
                        allowed_origins=['r^Mnk;-Yr;', 'XG*n*xDV+!'],
                        allowed_methods=['Xn/GB?U6L%', '(WFP_f9+fo'],
                        allowed_headers=['Tz6xsrF3zP', 'X6:X0Ttr7S'],
                        expose_headers=['V3ibsYcRMf', ':gVra;04af'],
                        max_age_seconds=33012,
                    ), oss.CORSRule(
                        allowed_origins=['rFrp:<Ls7b', 'BEy~pTdJ|*'],
                        allowed_methods=['7W!|8!~bNM', 'I-X;d2_;m%'],
                        allowed_headers=['+Dec^Ae#Dx', '<f)-E6ODSC'],
                        expose_headers=['yrk/NR9)^>', '*M$_n|#Zet'],
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
                origin='D3>GnzF+j ',
                access_control_request_method='GET',
                access_control_request_headers='jpOfuv/7BO',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('AccessForbidden', serr.code)
