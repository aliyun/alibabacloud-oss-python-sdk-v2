# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_website as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse

class TestPutBucketWebsite(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutBucketWebsiteRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.website_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutBucketWebsiteRequest(
            bucket='bucketexampletest',
            website_configuration=model.WebsiteConfiguration(
                index_document=model.IndexDocument(
                    suffix='9AMhr6F099',
                    support_sub_dir=True,
                    type=90502,
                ),
                error_document=model.ErrorDocument(
                    key='example-object-2.jpg',
                    http_status=18838,
                ),
                routing_rules=model.RoutingRules(
                    routing_rules=[model.RoutingRule(
                        rule_number=6052,
                        condition=model.RoutingRuleCondition(
                            key_suffix_equals='IGpnK#g1;O',
                            http_error_code_returned_equals=27934,
                            include_headers=[model.RoutingRuleIncludeHeader(
                                key='example-object-2.jpg',
                                equals='dN$i?qw+pU',
                            ), model.RoutingRuleIncludeHeader(
                                key='example-object-2.jpg',
                                equals='dN$i?qw+pU',
                            )],
                            key_prefix_equals='>xJsVadsc&',
                        ),
                        redirect=model.RoutingRuleRedirect(
                            mirror_url='@Dz7_/@WBD',
                            replace_key_with='e++B 3?b:H',
                            enable_replace_prefix=True,
                            pass_query_string=True,
                            mirror_headers=model.MirrorHeaders(
                                pass_all=False,
                                passs=['Tvr:fU0bWD', '&2%aj;|WN@'],
                                removes=[';C953edJ+Y', '5+u9ynIfdi'],
                                sets=[model.MirrorHeadersSet(
                                    key='example-object-2.jpg',
                                    value='~5,%9@a*9H',
                                ), model.MirrorHeadersSet(
                                    key='example-object-2.jpg',
                                    value='~5,%9@a*9H',
                                )],
                            ),
                            http_redirect_code=2970,
                            mirror_sni=False,
                            protocol='H9.\LhRAs-',
                            replace_key_prefix_with='J-SMDz/4oU',
                            redirect_type='imyLg7kr82',
                            mirror_pass_query_string=False,
                            host_name='Hqhix,~8ez',
                            mirror_follow_redirect=True,
                            mirror_check_md5=False,
                            mirror_pass_original_slashes=False,
                        ),
                    ), model.RoutingRule(
                        rule_number=6052,
                        condition=model.RoutingRuleCondition(
                            key_suffix_equals='IGpnK#g1;O',
                            http_error_code_returned_equals=27934,
                            include_headers=[model.RoutingRuleIncludeHeader(
                                key='example-object-2.jpg',
                                equals='dN$i?qw+pU',
                            ), model.RoutingRuleIncludeHeader(
                                key='example-object-2.jpg',
                                equals='dN$i?qw+pU',
                            )],
                            key_prefix_equals='>xJsVadsc&',
                        ),
                        redirect=model.RoutingRuleRedirect(
                            mirror_url='@Dz7_/@WBD',
                            replace_key_with='e++B 3?b:H',
                            enable_replace_prefix=True,
                            pass_query_string=True,
                            mirror_headers=model.MirrorHeaders(
                                pass_all=False,
                                passs=['9 tYid6?qI', 'Gvubue>ZqT'],
                                removes=['EVf\/BGq2u', '%co 5Q3)yH'],
                                sets=[model.MirrorHeadersSet(
                                    key='example-object-2.jpg',
                                    value='~5,%9@a*9H',
                                ), model.MirrorHeadersSet(
                                    key='example-object-2.jpg',
                                    value='~5,%9@a*9H',
                                )],
                            ),
                            http_redirect_code=2970,
                            mirror_sni=True,
                            protocol='H9.\LhRAs-',
                            replace_key_prefix_with='J-SMDz/4oU',
                            redirect_type='imyLg7kr82',
                            mirror_pass_query_string=False,
                            host_name='Hqhix,~8ez',
                            mirror_follow_redirect=True,
                            mirror_check_md5=False,
                            mirror_pass_original_slashes=True,
                        ),
                    )],
                ),
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('9AMhr6F099', request.website_configuration.index_document.suffix)
        self.assertEqual(True, request.website_configuration.index_document.support_sub_dir)
        self.assertEqual(90502, request.website_configuration.index_document.type)
        self.assertEqual('example-object-2.jpg', request.website_configuration.error_document.key)
        self.assertEqual(18838, request.website_configuration.error_document.http_status)
        self.assertEqual(6052, request.website_configuration.routing_rules.routing_rules[0].rule_number)
        self.assertEqual('IGpnK#g1;O', request.website_configuration.routing_rules.routing_rules[0].condition.key_suffix_equals)
        self.assertEqual(27934, request.website_configuration.routing_rules.routing_rules[0].condition.http_error_code_returned_equals)
        self.assertEqual('example-object-2.jpg', request.website_configuration.routing_rules.routing_rules[0].condition.include_headers[0].key)
        self.assertEqual('dN$i?qw+pU', request.website_configuration.routing_rules.routing_rules[0].condition.include_headers[0].equals)
        self.assertEqual('example-object-2.jpg', request.website_configuration.routing_rules.routing_rules[0].condition.include_headers[1].key)
        self.assertEqual('dN$i?qw+pU', request.website_configuration.routing_rules.routing_rules[0].condition.include_headers[1].equals)
        self.assertEqual('>xJsVadsc&', request.website_configuration.routing_rules.routing_rules[0].condition.key_prefix_equals)
        self.assertEqual('@Dz7_/@WBD', request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_url)
        self.assertEqual('e++B 3?b:H', request.website_configuration.routing_rules.routing_rules[0].redirect.replace_key_with)
        self.assertEqual(True, request.website_configuration.routing_rules.routing_rules[0].redirect.enable_replace_prefix)
        self.assertEqual(True, request.website_configuration.routing_rules.routing_rules[0].redirect.pass_query_string)
        self.assertEqual(False, request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.pass_all)
        self.assertEqual('Tvr:fU0bWD', request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.passs[0])
        self.assertEqual('&2%aj;|WN@', request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.passs[1])
        self.assertEqual(';C953edJ+Y', request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.removes[0])
        self.assertEqual('5+u9ynIfdi', request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.removes[1])
        self.assertEqual('example-object-2.jpg', request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[0].key)
        self.assertEqual('~5,%9@a*9H', request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[0].value)
        self.assertEqual('example-object-2.jpg', request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[1].key)
        self.assertEqual('~5,%9@a*9H', request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[1].value)
        self.assertEqual(2970, request.website_configuration.routing_rules.routing_rules[0].redirect.http_redirect_code)
        self.assertEqual(False, request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_sni)
        self.assertEqual('H9.\LhRAs-', request.website_configuration.routing_rules.routing_rules[0].redirect.protocol)
        self.assertEqual('J-SMDz/4oU', request.website_configuration.routing_rules.routing_rules[0].redirect.replace_key_prefix_with)
        self.assertEqual('imyLg7kr82', request.website_configuration.routing_rules.routing_rules[0].redirect.redirect_type)
        self.assertEqual(False, request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_pass_query_string)
        self.assertEqual('Hqhix,~8ez', request.website_configuration.routing_rules.routing_rules[0].redirect.host_name)
        self.assertEqual(True, request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_follow_redirect)
        self.assertEqual(False, request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_check_md5)
        self.assertEqual(False, request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_pass_original_slashes)
        self.assertEqual(6052, request.website_configuration.routing_rules.routing_rules[1].rule_number)
        self.assertEqual('IGpnK#g1;O', request.website_configuration.routing_rules.routing_rules[1].condition.key_suffix_equals)
        self.assertEqual(27934, request.website_configuration.routing_rules.routing_rules[1].condition.http_error_code_returned_equals)
        self.assertEqual('example-object-2.jpg', request.website_configuration.routing_rules.routing_rules[1].condition.include_headers[0].key)
        self.assertEqual('dN$i?qw+pU', request.website_configuration.routing_rules.routing_rules[1].condition.include_headers[0].equals)
        self.assertEqual('example-object-2.jpg', request.website_configuration.routing_rules.routing_rules[1].condition.include_headers[1].key)
        self.assertEqual('dN$i?qw+pU', request.website_configuration.routing_rules.routing_rules[1].condition.include_headers[1].equals)
        self.assertEqual('>xJsVadsc&', request.website_configuration.routing_rules.routing_rules[1].condition.key_prefix_equals)
        self.assertEqual('@Dz7_/@WBD', request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_url)
        self.assertEqual('e++B 3?b:H', request.website_configuration.routing_rules.routing_rules[1].redirect.replace_key_with)
        self.assertEqual(True, request.website_configuration.routing_rules.routing_rules[1].redirect.enable_replace_prefix)
        self.assertEqual(True, request.website_configuration.routing_rules.routing_rules[1].redirect.pass_query_string)
        self.assertEqual(False, request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.pass_all)
        self.assertEqual('9 tYid6?qI', request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.passs[0])
        self.assertEqual('Gvubue>ZqT', request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.passs[1])
        self.assertEqual('EVf\/BGq2u', request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.removes[0])
        self.assertEqual('%co 5Q3)yH', request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.removes[1])
        self.assertEqual('example-object-2.jpg', request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.sets[0].key)
        self.assertEqual('~5,%9@a*9H', request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.sets[0].value)
        self.assertEqual('example-object-2.jpg', request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.sets[1].key)
        self.assertEqual('~5,%9@a*9H', request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.sets[1].value)
        self.assertEqual(2970, request.website_configuration.routing_rules.routing_rules[1].redirect.http_redirect_code)
        self.assertEqual(True, request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_sni)
        self.assertEqual('H9.\LhRAs-', request.website_configuration.routing_rules.routing_rules[1].redirect.protocol)
        self.assertEqual('J-SMDz/4oU', request.website_configuration.routing_rules.routing_rules[1].redirect.replace_key_prefix_with)
        self.assertEqual('imyLg7kr82', request.website_configuration.routing_rules.routing_rules[1].redirect.redirect_type)
        self.assertEqual(False, request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_pass_query_string)
        self.assertEqual('Hqhix,~8ez', request.website_configuration.routing_rules.routing_rules[1].redirect.host_name)
        self.assertEqual(True, request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_follow_redirect)
        self.assertEqual(False, request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_check_md5)
        self.assertEqual(True, request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_pass_original_slashes)

    def test_serialize_request(self):
        request = model.PutBucketWebsiteRequest(
            bucket='bucketexampletest',
            website_configuration=model.WebsiteConfiguration(
                index_document=model.IndexDocument(
                    suffix='9AMhr6F099',
                    support_sub_dir=True,
                    type=90502,
                ),
                error_document=model.ErrorDocument(
                    key='example-object-2.jpg',
                    http_status=18838,
                ),
                routing_rules=model.RoutingRules(
                    routing_rules=[model.RoutingRule(
                        rule_number=6052,
                        condition=model.RoutingRuleCondition(
                            key_suffix_equals='IGpnK#g1;O',
                            http_error_code_returned_equals=27934,
                            include_headers=[model.RoutingRuleIncludeHeader(
                                key='example-object-2.jpg',
                                equals='dN$i?qw+pU',
                            ), model.RoutingRuleIncludeHeader(
                                key='example-object-2.jpg',
                                equals='dN$i?qw+pU',
                            )],
                            key_prefix_equals='>xJsVadsc&',
                        ),
                        redirect=model.RoutingRuleRedirect(
                            mirror_url='@Dz7_/@WBD',
                            replace_key_with='e++B 3?b:H',
                            enable_replace_prefix=True,
                            pass_query_string=True,
                            mirror_headers=model.MirrorHeaders(
                                pass_all=True,
                                passs=['sfT%mG!8zC', '-~#460+04+'],
                                removes=['x&$mNU+xL|', 'OHT)V3Q5:R'],
                                sets=[model.MirrorHeadersSet(
                                    key='example-object-2.jpg',
                                    value='~5,%9@a*9H',
                                ), model.MirrorHeadersSet(
                                    key='example-object-2.jpg',
                                    value='~5,%9@a*9H',
                                )],
                            ),
                            http_redirect_code=2970,
                            mirror_sni=True,
                            protocol='H9.\LhRAs-',
                            replace_key_prefix_with='J-SMDz/4oU',
                            redirect_type='imyLg7kr82',
                            mirror_pass_query_string=False,
                            host_name='Hqhix,~8ez',
                            mirror_follow_redirect=True,
                            mirror_check_md5=True,
                            mirror_pass_original_slashes=True,
                        ),
                    ), model.RoutingRule(
                        rule_number=6052,
                        condition=model.RoutingRuleCondition(
                            key_suffix_equals='IGpnK#g1;O',
                            http_error_code_returned_equals=27934,
                            include_headers=[model.RoutingRuleIncludeHeader(
                                key='example-object-2.jpg',
                                equals='dN$i?qw+pU',
                            ), model.RoutingRuleIncludeHeader(
                                key='example-object-2.jpg',
                                equals='dN$i?qw+pU',
                            )],
                            key_prefix_equals='>xJsVadsc&',
                        ),
                        redirect=model.RoutingRuleRedirect(
                            mirror_url='@Dz7_/@WBD',
                            replace_key_with='e++B 3?b:H',
                            enable_replace_prefix=True,
                            pass_query_string=True,
                            mirror_headers=model.MirrorHeaders(
                                pass_all=True,
                                passs=['+*MSzg6n@4', '7Aco8%(,Lo'],
                                removes=['1qYf(Mpzen', '.TN1#%-Cli'],
                                sets=[model.MirrorHeadersSet(
                                    key='example-object-2.jpg',
                                    value='~5,%9@a*9H',
                                ), model.MirrorHeadersSet(
                                    key='example-object-2.jpg',
                                    value='~5,%9@a*9H',
                                )],
                            ),
                            http_redirect_code=2970,
                            mirror_sni=True,
                            protocol='H9.\LhRAs-',
                            replace_key_prefix_with='J-SMDz/4oU',
                            redirect_type='imyLg7kr82',
                            mirror_pass_query_string=False,
                            host_name='Hqhix,~8ez',
                            mirror_follow_redirect=True,
                            mirror_check_md5=True,
                            mirror_pass_original_slashes=True,
                        ),
                    )],
                ),
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutBucketWebsite',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutBucketWebsite', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.PutBucketWebsiteResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutBucketWebsiteResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                    'x-oss-version-id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('x-oss-version-id'))


class TestGetBucketWebsite(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketWebsiteRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetBucketWebsiteRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.GetBucketWebsiteRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketWebsite',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetBucketWebsite', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetBucketWebsiteResult()
        self.assertIsNone(result.website_configuration)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketWebsiteResult(
            website_configuration=model.WebsiteConfiguration(
                index_document=model.IndexDocument(
                    suffix='V&!gW*rebP',
                    support_sub_dir=True,
                    type=17107,
                ),
                error_document=model.ErrorDocument(
                    key='example-object-2.jpg',
                    http_status=47689,
                ),
                routing_rules=model.RoutingRules(
                    routing_rules=[model.RoutingRule(
                        rule_number=81851,
                        condition=model.RoutingRuleCondition(
                            key_suffix_equals='Bz+99LXI1c',
                            http_error_code_returned_equals=8083,
                            include_headers=[model.RoutingRuleIncludeHeader(
                                key='example-object-2.jpg',
                                equals='>~*J9ph+oh',
                            ), model.RoutingRuleIncludeHeader(
                                key='example-object-2.jpg',
                                equals='>~*J9ph+oh',
                            )],
                            key_prefix_equals='9O0!-yByC3',
                        ),
                        redirect=model.RoutingRuleRedirect(
                            mirror_url='.nKig&JHjX',
                            replace_key_with='-T6p@8.$&J',
                            enable_replace_prefix=False,
                            pass_query_string=True,
                            mirror_headers=model.MirrorHeaders(
                                pass_all=False,
                                passs=['&%ykVpAAq+', '#>~C_fKg$2'],
                                removes=['9TRpem&YL;', 'G.#9exGzdT'],
                                sets=[model.MirrorHeadersSet(
                                    key='example-object-2.jpg',
                                    value='+gJ1xjGAB:',
                                ), model.MirrorHeadersSet(
                                    key='example-object-2.jpg',
                                    value='+gJ1xjGAB:',
                                )],
                            ),
                            http_redirect_code=16375,
                            mirror_sni=False,
                            protocol='x?8oLtKh+1',
                            replace_key_prefix_with='yy@wr40git',
                            redirect_type='!+8Y>yjL3-',
                            mirror_pass_query_string=True,
                            host_name='#70b#w@pbm',
                            mirror_follow_redirect=True,
                            mirror_check_md5=False,
                            mirror_pass_original_slashes=False,
                        ),
                    ), model.RoutingRule(
                        rule_number=81851,
                        condition=model.RoutingRuleCondition(
                            key_suffix_equals='Bz+99LXI1c',
                            http_error_code_returned_equals=8083,
                            include_headers=[model.RoutingRuleIncludeHeader(
                                key='example-object-2.jpg',
                                equals='>~*J9ph+oh',
                            ), model.RoutingRuleIncludeHeader(
                                key='example-object-2.jpg',
                                equals='>~*J9ph+oh',
                            )],
                            key_prefix_equals='9O0!-yByC3',
                        ),
                        redirect=model.RoutingRuleRedirect(
                            mirror_url='.nKig&JHjX',
                            replace_key_with='-T6p@8.$&J',
                            enable_replace_prefix=True,
                            pass_query_string=True,
                            mirror_headers=model.MirrorHeaders(
                                pass_all=True,
                                passs=['QQ^5M|6j>7', 'QHf*,2<LwX'],
                                removes=['3aki wityf', '+:@2^j^%%,'],
                                sets=[model.MirrorHeadersSet(
                                    key='example-object-2.jpg',
                                    value='+gJ1xjGAB:',
                                ), model.MirrorHeadersSet(
                                    key='example-object-2.jpg',
                                    value='+gJ1xjGAB:',
                                )],
                            ),
                            http_redirect_code=16375,
                            mirror_sni=False,
                            protocol='x?8oLtKh+1',
                            replace_key_prefix_with='yy@wr40git',
                            redirect_type='!+8Y>yjL3-',
                            mirror_pass_query_string=True,
                            host_name='#70b#w@pbm',
                            mirror_follow_redirect=True,
                            mirror_check_md5=False,
                            mirror_pass_original_slashes=True,
                        ),
                    )],
                ),
            ),
        )
        self.assertEqual('V&!gW*rebP', result.website_configuration.index_document.suffix)
        self.assertEqual(True, result.website_configuration.index_document.support_sub_dir)
        self.assertEqual(17107, result.website_configuration.index_document.type)
        self.assertEqual('example-object-2.jpg', result.website_configuration.error_document.key)
        self.assertEqual(47689, result.website_configuration.error_document.http_status)
        self.assertEqual(81851, result.website_configuration.routing_rules.routing_rules[0].rule_number)
        self.assertEqual('Bz+99LXI1c', result.website_configuration.routing_rules.routing_rules[0].condition.key_suffix_equals)
        self.assertEqual(8083, result.website_configuration.routing_rules.routing_rules[0].condition.http_error_code_returned_equals)
        self.assertEqual('example-object-2.jpg', result.website_configuration.routing_rules.routing_rules[0].condition.include_headers[0].key)
        self.assertEqual('>~*J9ph+oh', result.website_configuration.routing_rules.routing_rules[0].condition.include_headers[0].equals)
        self.assertEqual('example-object-2.jpg', result.website_configuration.routing_rules.routing_rules[0].condition.include_headers[1].key)
        self.assertEqual('>~*J9ph+oh', result.website_configuration.routing_rules.routing_rules[0].condition.include_headers[1].equals)
        self.assertEqual('9O0!-yByC3', result.website_configuration.routing_rules.routing_rules[0].condition.key_prefix_equals)
        self.assertEqual('.nKig&JHjX', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_url)
        self.assertEqual('-T6p@8.$&J', result.website_configuration.routing_rules.routing_rules[0].redirect.replace_key_with)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[0].redirect.enable_replace_prefix)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.pass_query_string)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.pass_all)
        self.assertEqual('&%ykVpAAq+', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.passs[0])
        self.assertEqual('#>~C_fKg$2', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.passs[1])
        self.assertEqual('9TRpem&YL;', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.removes[0])
        self.assertEqual('G.#9exGzdT', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.removes[1])
        self.assertEqual('example-object-2.jpg', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[0].key)
        self.assertEqual('+gJ1xjGAB:', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[0].value)
        self.assertEqual('example-object-2.jpg', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[1].key)
        self.assertEqual('+gJ1xjGAB:', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[1].value)
        self.assertEqual(16375, result.website_configuration.routing_rules.routing_rules[0].redirect.http_redirect_code)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_sni)
        self.assertEqual('x?8oLtKh+1', result.website_configuration.routing_rules.routing_rules[0].redirect.protocol)
        self.assertEqual('yy@wr40git', result.website_configuration.routing_rules.routing_rules[0].redirect.replace_key_prefix_with)
        self.assertEqual('!+8Y>yjL3-', result.website_configuration.routing_rules.routing_rules[0].redirect.redirect_type)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_pass_query_string)
        self.assertEqual('#70b#w@pbm', result.website_configuration.routing_rules.routing_rules[0].redirect.host_name)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_follow_redirect)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_check_md5)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_pass_original_slashes)
        self.assertEqual(81851, result.website_configuration.routing_rules.routing_rules[1].rule_number)
        self.assertEqual('Bz+99LXI1c', result.website_configuration.routing_rules.routing_rules[1].condition.key_suffix_equals)
        self.assertEqual(8083, result.website_configuration.routing_rules.routing_rules[1].condition.http_error_code_returned_equals)
        self.assertEqual('example-object-2.jpg', result.website_configuration.routing_rules.routing_rules[1].condition.include_headers[0].key)
        self.assertEqual('>~*J9ph+oh', result.website_configuration.routing_rules.routing_rules[1].condition.include_headers[0].equals)
        self.assertEqual('example-object-2.jpg', result.website_configuration.routing_rules.routing_rules[1].condition.include_headers[1].key)
        self.assertEqual('>~*J9ph+oh', result.website_configuration.routing_rules.routing_rules[1].condition.include_headers[1].equals)
        self.assertEqual('9O0!-yByC3', result.website_configuration.routing_rules.routing_rules[1].condition.key_prefix_equals)
        self.assertEqual('.nKig&JHjX', result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_url)
        self.assertEqual('-T6p@8.$&J', result.website_configuration.routing_rules.routing_rules[1].redirect.replace_key_with)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[1].redirect.enable_replace_prefix)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[1].redirect.pass_query_string)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.pass_all)
        self.assertEqual('QQ^5M|6j>7', result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.passs[0])
        self.assertEqual('QHf*,2<LwX', result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.passs[1])
        self.assertEqual('3aki wityf', result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.removes[0])
        self.assertEqual('+:@2^j^%%,', result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.removes[1])
        self.assertEqual('example-object-2.jpg', result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.sets[0].key)
        self.assertEqual('+gJ1xjGAB:', result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.sets[0].value)
        self.assertEqual('example-object-2.jpg', result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.sets[1].key)
        self.assertEqual('+gJ1xjGAB:', result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.sets[1].value)
        self.assertEqual(16375, result.website_configuration.routing_rules.routing_rules[1].redirect.http_redirect_code)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_sni)
        self.assertEqual('x?8oLtKh+1', result.website_configuration.routing_rules.routing_rules[1].redirect.protocol)
        self.assertEqual('yy@wr40git', result.website_configuration.routing_rules.routing_rules[1].redirect.replace_key_prefix_with)
        self.assertEqual('!+8Y>yjL3-', result.website_configuration.routing_rules.routing_rules[1].redirect.redirect_type)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_pass_query_string)
        self.assertEqual('#70b#w@pbm', result.website_configuration.routing_rules.routing_rules[1].redirect.host_name)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_follow_redirect)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_check_md5)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_pass_original_slashes)

    def test_deserialize_result(self):
        xml_data = r'''
        <WebsiteConfiguration>
        </WebsiteConfiguration>'''

        result = model.GetBucketWebsiteResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <WebsiteConfiguration>
          <IndexDocument>
            <Suffix>index.html</Suffix>
          </IndexDocument>
          <ErrorDocument>
            <Key>error.html</Key>
            <HttpStatus>404</HttpStatus>
          </ErrorDocument>
          <RoutingRules>
            <RoutingRule>
              <RuleNumber>1</RuleNumber>
              <Condition>
                <KeyPrefixEquals>abc/</KeyPrefixEquals>
                <HttpErrorCodeReturnedEquals>404</HttpErrorCodeReturnedEquals>
              </Condition>
              <Redirect>
                <RedirectType>Mirror</RedirectType>
                <PassQueryString>true</PassQueryString>
                <MirrorURL>http://example.com/</MirrorURL>
                <MirrorPassQueryString>true</MirrorPassQueryString>
                <MirrorFollowRedirect>true</MirrorFollowRedirect>
                <MirrorCheckMd5>false</MirrorCheckMd5>
                <MirrorHeaders>
                  <PassAll>true</PassAll>
                  <Pass>myheader-key1</Pass>
                  <Pass>myheader-key2</Pass>
                  <Remove>myheader-key3</Remove>
                  <Remove>myheader-key4</Remove>
                  <Set>
                    <Key>myheader-key5</Key>
                    <Value>myheader-value5</Value>
                  </Set>
                </MirrorHeaders>
              </Redirect>
            </RoutingRule>
            <RoutingRule>
              <RuleNumber>2</RuleNumber>
              <Condition>
                <IncludeHeader>
                  <Key>host</Key>
                  <Equals>test.oss-cn-beijing-internal.aliyuncs.com</Equals>
                </IncludeHeader>
                <KeyPrefixEquals>abc/</KeyPrefixEquals>
                <HttpErrorCodeReturnedEquals>404</HttpErrorCodeReturnedEquals>
              </Condition>
              <Redirect>
                <RedirectType>AliCDN</RedirectType>
                <Protocol>http</Protocol>
                <HostName>example.com</HostName>
                <PassQueryString>false</PassQueryString>
                <ReplaceKeyWith>prefix/${key}.suffix</ReplaceKeyWith>
                <HttpRedirectCode>301</HttpRedirectCode>
              </Redirect>
            </RoutingRule>
          </RoutingRules>
        </WebsiteConfiguration>
        '''

        result = model.GetBucketWebsiteResult()
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=xml_data,
            )
        )
        deserializer = [serde.deserialize_output_xmlbody]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertEqual('index.html', result.website_configuration.index_document.suffix)
        self.assertEqual('error.html', result.website_configuration.error_document.key)
        self.assertEqual(404, result.website_configuration.error_document.http_status)
        self.assertEqual(1, result.website_configuration.routing_rules.routing_rules[0].rule_number)
        self.assertEqual('abc/', result.website_configuration.routing_rules.routing_rules[0].condition.key_prefix_equals)
        self.assertEqual(404, result.website_configuration.routing_rules.routing_rules[0].condition.http_error_code_returned_equals)
        self.assertEqual('Mirror', result.website_configuration.routing_rules.routing_rules[0].redirect.redirect_type)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.pass_query_string)
        self.assertEqual('http://example.com/', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_url)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_pass_query_string)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_follow_redirect)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_check_md5)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.pass_all)
        self.assertEqual('myheader-key1', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.passs[0])
        self.assertEqual('myheader-key2', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.passs[1])
        self.assertEqual('myheader-key3', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.removes[0])
        self.assertEqual('myheader-key4', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.removes[1])
        self.assertEqual('myheader-key5', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[0].key)
        self.assertEqual('myheader-value5', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[0].value)
        self.assertEqual(2, result.website_configuration.routing_rules.routing_rules[1].rule_number)
        self.assertEqual('host', result.website_configuration.routing_rules.routing_rules[1].condition.include_headers[0].key)
        self.assertEqual('test.oss-cn-beijing-internal.aliyuncs.com', result.website_configuration.routing_rules.routing_rules[1].condition.include_headers[0].equals)
        self.assertEqual('abc/', result.website_configuration.routing_rules.routing_rules[1].condition.key_prefix_equals)
        self.assertEqual(404, result.website_configuration.routing_rules.routing_rules[1].condition.http_error_code_returned_equals)
        self.assertEqual('AliCDN', result.website_configuration.routing_rules.routing_rules[1].redirect.redirect_type)
        self.assertEqual('http', result.website_configuration.routing_rules.routing_rules[1].redirect.protocol)
        self.assertEqual('example.com', result.website_configuration.routing_rules.routing_rules[1].redirect.host_name)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[1].redirect.pass_query_string)
        self.assertEqual('prefix/${key}.suffix', result.website_configuration.routing_rules.routing_rules[1].redirect.replace_key_with)
        self.assertEqual(301, result.website_configuration.routing_rules.routing_rules[1].redirect.http_redirect_code)


class TestDeleteBucketWebsite(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DeleteBucketWebsiteRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DeleteBucketWebsiteRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.DeleteBucketWebsiteRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteBucketWebsite',
            method='DELETE',
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteBucketWebsite', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.DeleteBucketWebsiteResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.DeleteBucketWebsiteResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                    'x-oss-version-id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('x-oss-version-id'))

