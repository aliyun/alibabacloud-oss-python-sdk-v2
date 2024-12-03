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
                    suffix='index.html',
                    support_sub_dir=True,
                    type=0,
                ),
                error_document=model.ErrorDocument(
                    key='error.html',
                    http_status=404,
                ),
                routing_rules=model.RoutingRules(
                    routing_rules=[model.RoutingRule(
                        rule_number=6052,
                        condition=model.RoutingRuleCondition(
                            key_suffix_equals='abc/',
                            http_error_code_returned_equals=404,
                            include_headers=[model.RoutingRuleIncludeHeader(
                                key='key1',
                                equals='value1',
                            ), model.RoutingRuleIncludeHeader(
                                key='key2',
                                equals='value2',
                            )],
                            key_prefix_equals='aaa/',
                        ),
                        redirect=model.RoutingRuleRedirect(
                            mirror_url='http://example.com/',
                            replace_key_with='aab/',
                            enable_replace_prefix=True,
                            pass_query_string=True,
                            mirror_headers=model.MirrorHeaders(
                                pass_all=True,
                                passs=['myheader-key1', 'myheader-key2'],
                                removes=['myheader-key3', 'myheader-key4'],
                                sets=[model.MirrorHeadersSet(
                                    key='myheader-key5',
                                    value='myheader-value',
                                ), model.MirrorHeadersSet(
                                    key='myheader-key6',
                                    value='myheader-valu2',
                                )],
                            ),
                            http_redirect_code=203,
                            mirror_sni=False,
                            protocol='http',
                            replace_key_prefix_with='abc/',
                            redirect_type='Mirror',
                            mirror_pass_query_string=False,
                            host_name='example.com',
                            mirror_follow_redirect=True,
                            mirror_check_md5=False,
                            mirror_pass_original_slashes=False,
                        ),
                    ), model.RoutingRule(
                        rule_number=6052,
                        condition=model.RoutingRuleCondition(
                            key_suffix_equals='bbc/',
                            http_error_code_returned_equals=403,
                            include_headers=[model.RoutingRuleIncludeHeader(
                                key='key21',
                                equals='value21',
                            ), model.RoutingRuleIncludeHeader(
                                key='key22',
                                equals='value22U',
                            )],
                            key_prefix_equals='abc/',
                        ),
                        redirect=model.RoutingRuleRedirect(
                            mirror_url='http://example.com/',
                            replace_key_with='prefix/${key}',
                            enable_replace_prefix=True,
                            pass_query_string=True,
                            mirror_headers=model.MirrorHeaders(
                                pass_all=True,
                                passs=['myheader-key21', 'myheader-key22'],
                                removes=['myheader-key23', 'myheader-key24'],
                                sets=[model.MirrorHeadersSet(
                                    key='myheader-key25',
                                    value='myheader-value2',
                                ), model.MirrorHeadersSet(
                                    key='myheader-key26',
                                    value='myheader-value22',
                                )],
                            ),
                            http_redirect_code=2970,
                            mirror_sni=True,
                            protocol='https',
                            replace_key_prefix_with='prefix/${key}.suffix',
                            redirect_type='AliCDN',
                            mirror_pass_query_string=False,
                            host_name='example.com',
                            mirror_follow_redirect=True,
                            mirror_check_md5=False,
                            mirror_pass_original_slashes=True,
                        ),
                    )],
                ),
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('index.html', request.website_configuration.index_document.suffix)
        self.assertEqual(True, request.website_configuration.index_document.support_sub_dir)
        self.assertEqual(0, request.website_configuration.index_document.type)
        self.assertEqual('error.html', request.website_configuration.error_document.key)
        self.assertEqual(404, request.website_configuration.error_document.http_status)
        self.assertEqual(6052, request.website_configuration.routing_rules.routing_rules[0].rule_number)
        self.assertEqual('abc/', request.website_configuration.routing_rules.routing_rules[0].condition.key_suffix_equals)
        self.assertEqual(404, request.website_configuration.routing_rules.routing_rules[0].condition.http_error_code_returned_equals)
        self.assertEqual('key1', request.website_configuration.routing_rules.routing_rules[0].condition.include_headers[0].key)
        self.assertEqual('value1', request.website_configuration.routing_rules.routing_rules[0].condition.include_headers[0].equals)
        self.assertEqual('key2', request.website_configuration.routing_rules.routing_rules[0].condition.include_headers[1].key)
        self.assertEqual('value2', request.website_configuration.routing_rules.routing_rules[0].condition.include_headers[1].equals)
        self.assertEqual('aaa/', request.website_configuration.routing_rules.routing_rules[0].condition.key_prefix_equals)
        self.assertEqual('http://example.com/', request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_url)
        self.assertEqual('aab/', request.website_configuration.routing_rules.routing_rules[0].redirect.replace_key_with)
        self.assertEqual(True, request.website_configuration.routing_rules.routing_rules[0].redirect.enable_replace_prefix)
        self.assertEqual(True, request.website_configuration.routing_rules.routing_rules[0].redirect.pass_query_string)
        self.assertEqual(True, request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.pass_all)
        self.assertEqual('myheader-key1', request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.passs[0])
        self.assertEqual('myheader-key2', request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.passs[1])
        self.assertEqual('myheader-key3', request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.removes[0])
        self.assertEqual('myheader-key4', request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.removes[1])
        self.assertEqual('myheader-key5', request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[0].key)
        self.assertEqual('myheader-value', request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[0].value)
        self.assertEqual('myheader-key6', request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[1].key)
        self.assertEqual('myheader-valu2', request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[1].value)
        self.assertEqual(203, request.website_configuration.routing_rules.routing_rules[0].redirect.http_redirect_code)
        self.assertEqual(False, request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_sni)
        self.assertEqual('http', request.website_configuration.routing_rules.routing_rules[0].redirect.protocol)
        self.assertEqual('abc/', request.website_configuration.routing_rules.routing_rules[0].redirect.replace_key_prefix_with)
        self.assertEqual('Mirror', request.website_configuration.routing_rules.routing_rules[0].redirect.redirect_type)
        self.assertEqual(False, request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_pass_query_string)
        self.assertEqual('example.com', request.website_configuration.routing_rules.routing_rules[0].redirect.host_name)
        self.assertEqual(True, request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_follow_redirect)
        self.assertEqual(False, request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_check_md5)
        self.assertEqual(False, request.website_configuration.routing_rules.routing_rules[0].redirect.mirror_pass_original_slashes)
        self.assertEqual(6052, request.website_configuration.routing_rules.routing_rules[1].rule_number)
        self.assertEqual('bbc/', request.website_configuration.routing_rules.routing_rules[1].condition.key_suffix_equals)
        self.assertEqual(403, request.website_configuration.routing_rules.routing_rules[1].condition.http_error_code_returned_equals)
        self.assertEqual('key21', request.website_configuration.routing_rules.routing_rules[1].condition.include_headers[0].key)
        self.assertEqual('value21', request.website_configuration.routing_rules.routing_rules[1].condition.include_headers[0].equals)
        self.assertEqual('key22', request.website_configuration.routing_rules.routing_rules[1].condition.include_headers[1].key)
        self.assertEqual('value22U', request.website_configuration.routing_rules.routing_rules[1].condition.include_headers[1].equals)
        self.assertEqual('abc/', request.website_configuration.routing_rules.routing_rules[1].condition.key_prefix_equals)
        self.assertEqual('http://example.com/', request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_url)
        self.assertEqual('prefix/${key}', request.website_configuration.routing_rules.routing_rules[1].redirect.replace_key_with)
        self.assertEqual(True, request.website_configuration.routing_rules.routing_rules[1].redirect.enable_replace_prefix)
        self.assertEqual(True, request.website_configuration.routing_rules.routing_rules[1].redirect.pass_query_string)
        self.assertEqual(True, request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.pass_all)
        self.assertEqual('myheader-key21', request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.passs[0])
        self.assertEqual('myheader-key22', request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.passs[1])
        self.assertEqual('myheader-key23', request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.removes[0])
        self.assertEqual('myheader-key24', request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.removes[1])
        self.assertEqual('myheader-key25', request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.sets[0].key)
        self.assertEqual('myheader-value2', request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.sets[0].value)
        self.assertEqual('myheader-key26', request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.sets[1].key)
        self.assertEqual('myheader-value22', request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.sets[1].value)
        self.assertEqual(2970, request.website_configuration.routing_rules.routing_rules[1].redirect.http_redirect_code)
        self.assertEqual(True, request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_sni)
        self.assertEqual('https', request.website_configuration.routing_rules.routing_rules[1].redirect.protocol)
        self.assertEqual('prefix/${key}.suffix', request.website_configuration.routing_rules.routing_rules[1].redirect.replace_key_prefix_with)
        self.assertEqual('AliCDN', request.website_configuration.routing_rules.routing_rules[1].redirect.redirect_type)
        self.assertEqual(False, request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_pass_query_string)
        self.assertEqual('example.com', request.website_configuration.routing_rules.routing_rules[1].redirect.host_name)
        self.assertEqual(True, request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_follow_redirect)
        self.assertEqual(False, request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_check_md5)
        self.assertEqual(True, request.website_configuration.routing_rules.routing_rules[1].redirect.mirror_pass_original_slashes)

    def test_serialize_request(self):
        request = model.PutBucketWebsiteRequest(
            bucket='bucketexampletest',
            website_configuration=model.WebsiteConfiguration(
                index_document=model.IndexDocument(
                    suffix='index.html',
                    support_sub_dir=True,
                    type=0,
                ),
                error_document=model.ErrorDocument(
                    key='error.html',
                    http_status=404,
                ),
                routing_rules=model.RoutingRules(
                    routing_rules=[model.RoutingRule(
                        rule_number=6052,
                        condition=model.RoutingRuleCondition(
                            key_suffix_equals='abc/',
                            http_error_code_returned_equals=404,
                            include_headers=[model.RoutingRuleIncludeHeader(
                                key='key1',
                                equals='value1',
                            ), model.RoutingRuleIncludeHeader(
                                key='key2',
                                equals='value2',
                            )],
                            key_prefix_equals='aaa/',
                        ),
                        redirect=model.RoutingRuleRedirect(
                            mirror_url='http://example.com/',
                            replace_key_with='aab/',
                            enable_replace_prefix=True,
                            pass_query_string=True,
                            mirror_headers=model.MirrorHeaders(
                                pass_all=True,
                                passs=['myheader-key1', 'myheader-key2'],
                                removes=['myheader-key3', 'myheader-key4'],
                                sets=[model.MirrorHeadersSet(
                                    key='myheader-key5',
                                    value='myheader-value',
                                ), model.MirrorHeadersSet(
                                    key='myheader-key6',
                                    value='myheader-valu2',
                                )],
                            ),
                            http_redirect_code=203,
                            mirror_sni=False,
                            protocol='http',
                            replace_key_prefix_with='abc/',
                            redirect_type='Mirror',
                            mirror_pass_query_string=False,
                            host_name='example.com',
                            mirror_follow_redirect=True,
                            mirror_check_md5=False,
                            mirror_pass_original_slashes=False,
                        ),
                    ), model.RoutingRule(
                        rule_number=6052,
                        condition=model.RoutingRuleCondition(
                            key_suffix_equals='bbc/',
                            http_error_code_returned_equals=403,
                            include_headers=[model.RoutingRuleIncludeHeader(
                                key='key21',
                                equals='value21',
                            ), model.RoutingRuleIncludeHeader(
                                key='key22',
                                equals='value22U',
                            )],
                            key_prefix_equals='abc/',
                        ),
                        redirect=model.RoutingRuleRedirect(
                            mirror_url='http://example.com/',
                            replace_key_with='prefix/${key}',
                            enable_replace_prefix=True,
                            pass_query_string=True,
                            mirror_headers=model.MirrorHeaders(
                                pass_all=True,
                                passs=['myheader-key21', 'myheader-key22'],
                                removes=['myheader-key23', 'myheader-key24'],
                                sets=[model.MirrorHeadersSet(
                                    key='myheader-key25',
                                    value='myheader-value2',
                                ), model.MirrorHeadersSet(
                                    key='myheader-key26',
                                    value='myheader-value22',
                                )],
                            ),
                            http_redirect_code=2970,
                            mirror_sni=True,
                            protocol='https',
                            replace_key_prefix_with='prefix/${key}.suffix',
                            redirect_type='AliCDN',
                            mirror_pass_query_string=False,
                            host_name='example.com',
                            mirror_follow_redirect=True,
                            mirror_check_md5=False,
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
                    suffix='index.html',
                    support_sub_dir=True,
                    type=0,
                ),
                error_document=model.ErrorDocument(
                    key='error.html',
                    http_status=404,
                ),
                routing_rules=model.RoutingRules(
                    routing_rules=[model.RoutingRule(
                        rule_number=6052,
                        condition=model.RoutingRuleCondition(
                            key_suffix_equals='abc/',
                            http_error_code_returned_equals=404,
                            include_headers=[model.RoutingRuleIncludeHeader(
                                key='key1',
                                equals='value1',
                            ), model.RoutingRuleIncludeHeader(
                                key='key2',
                                equals='value2',
                            )],
                            key_prefix_equals='aaa/',
                        ),
                        redirect=model.RoutingRuleRedirect(
                            mirror_url='http://example.com/',
                            replace_key_with='aab/',
                            enable_replace_prefix=True,
                            pass_query_string=True,
                            mirror_headers=model.MirrorHeaders(
                                pass_all=True,
                                passs=['myheader-key1', 'myheader-key2'],
                                removes=['myheader-key3', 'myheader-key4'],
                                sets=[model.MirrorHeadersSet(
                                    key='myheader-key5',
                                    value='myheader-value',
                                ), model.MirrorHeadersSet(
                                    key='myheader-key6',
                                    value='myheader-valu2',
                                )],
                            ),
                            http_redirect_code=203,
                            mirror_sni=False,
                            protocol='http',
                            replace_key_prefix_with='abc/',
                            redirect_type='Mirror',
                            mirror_pass_query_string=False,
                            host_name='example.com',
                            mirror_follow_redirect=True,
                            mirror_check_md5=False,
                            mirror_pass_original_slashes=False,
                        ),
                    ), model.RoutingRule(
                        rule_number=6052,
                        condition=model.RoutingRuleCondition(
                            key_suffix_equals='bbc/',
                            http_error_code_returned_equals=403,
                            include_headers=[model.RoutingRuleIncludeHeader(
                                key='key21',
                                equals='value21',
                            ), model.RoutingRuleIncludeHeader(
                                key='key22',
                                equals='value22U',
                            )],
                            key_prefix_equals='abc/',
                        ),
                        redirect=model.RoutingRuleRedirect(
                            mirror_url='http://example.com/',
                            replace_key_with='prefix/${key}',
                            enable_replace_prefix=True,
                            pass_query_string=True,
                            mirror_headers=model.MirrorHeaders(
                                pass_all=True,
                                passs=['myheader-key21', 'myheader-key22'],
                                removes=['myheader-key23', 'myheader-key24'],
                                sets=[model.MirrorHeadersSet(
                                    key='myheader-key25',
                                    value='myheader-value2',
                                ), model.MirrorHeadersSet(
                                    key='myheader-key26',
                                    value='myheader-value22',
                                )],
                            ),
                            http_redirect_code=2970,
                            mirror_sni=True,
                            protocol='https',
                            replace_key_prefix_with='prefix/${key}.suffix',
                            redirect_type='AliCDN',
                            mirror_pass_query_string=False,
                            host_name='example.com',
                            mirror_follow_redirect=True,
                            mirror_check_md5=False,
                            mirror_pass_original_slashes=True,
                        ),
                    )],
                ),
            ),
        )
        self.assertEqual('index.html', result.website_configuration.index_document.suffix)
        self.assertEqual(True, result.website_configuration.index_document.support_sub_dir)
        self.assertEqual(0, result.website_configuration.index_document.type)
        self.assertEqual('error.html', result.website_configuration.error_document.key)
        self.assertEqual(404, result.website_configuration.error_document.http_status)
        self.assertEqual(6052, result.website_configuration.routing_rules.routing_rules[0].rule_number)
        self.assertEqual('abc/', result.website_configuration.routing_rules.routing_rules[0].condition.key_suffix_equals)
        self.assertEqual(404, result.website_configuration.routing_rules.routing_rules[0].condition.http_error_code_returned_equals)
        self.assertEqual('key1', result.website_configuration.routing_rules.routing_rules[0].condition.include_headers[0].key)
        self.assertEqual('value1', result.website_configuration.routing_rules.routing_rules[0].condition.include_headers[0].equals)
        self.assertEqual('key2', result.website_configuration.routing_rules.routing_rules[0].condition.include_headers[1].key)
        self.assertEqual('value2', result.website_configuration.routing_rules.routing_rules[0].condition.include_headers[1].equals)
        self.assertEqual('aaa/', result.website_configuration.routing_rules.routing_rules[0].condition.key_prefix_equals)
        self.assertEqual('http://example.com/', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_url)
        self.assertEqual('aab/', result.website_configuration.routing_rules.routing_rules[0].redirect.replace_key_with)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.enable_replace_prefix)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.pass_query_string)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.pass_all)
        self.assertEqual('myheader-key1', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.passs[0])
        self.assertEqual('myheader-key2', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.passs[1])
        self.assertEqual('myheader-key3', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.removes[0])
        self.assertEqual('myheader-key4', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.removes[1])
        self.assertEqual('myheader-key5', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[0].key)
        self.assertEqual('myheader-value', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[0].value)
        self.assertEqual('myheader-key6', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[1].key)
        self.assertEqual('myheader-valu2', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[1].value)
        self.assertEqual(203, result.website_configuration.routing_rules.routing_rules[0].redirect.http_redirect_code)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_sni)
        self.assertEqual('http', result.website_configuration.routing_rules.routing_rules[0].redirect.protocol)
        self.assertEqual('abc/', result.website_configuration.routing_rules.routing_rules[0].redirect.replace_key_prefix_with)
        self.assertEqual('Mirror', result.website_configuration.routing_rules.routing_rules[0].redirect.redirect_type)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_pass_query_string)
        self.assertEqual('example.com', result.website_configuration.routing_rules.routing_rules[0].redirect.host_name)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_follow_redirect)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_check_md5)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_pass_original_slashes)
        self.assertEqual(6052, result.website_configuration.routing_rules.routing_rules[1].rule_number)
        self.assertEqual('bbc/', result.website_configuration.routing_rules.routing_rules[1].condition.key_suffix_equals)
        self.assertEqual(403, result.website_configuration.routing_rules.routing_rules[1].condition.http_error_code_returned_equals)
        self.assertEqual('key21', result.website_configuration.routing_rules.routing_rules[1].condition.include_headers[0].key)
        self.assertEqual('value21', result.website_configuration.routing_rules.routing_rules[1].condition.include_headers[0].equals)
        self.assertEqual('key22', result.website_configuration.routing_rules.routing_rules[1].condition.include_headers[1].key)
        self.assertEqual('value22U', result.website_configuration.routing_rules.routing_rules[1].condition.include_headers[1].equals)
        self.assertEqual('abc/', result.website_configuration.routing_rules.routing_rules[1].condition.key_prefix_equals)
        self.assertEqual('http://example.com/', result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_url)
        self.assertEqual('prefix/${key}', result.website_configuration.routing_rules.routing_rules[1].redirect.replace_key_with)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[1].redirect.enable_replace_prefix)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[1].redirect.pass_query_string)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.pass_all)
        self.assertEqual('myheader-key21', result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.passs[0])
        self.assertEqual('myheader-key22', result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.passs[1])
        self.assertEqual('myheader-key23', result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.removes[0])
        self.assertEqual('myheader-key24', result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.removes[1])
        self.assertEqual('myheader-key25', result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.sets[0].key)
        self.assertEqual('myheader-value2', result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.sets[0].value)
        self.assertEqual('myheader-key26', result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.sets[1].key)
        self.assertEqual('myheader-value22', result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers.sets[1].value)
        self.assertEqual(2970, result.website_configuration.routing_rules.routing_rules[1].redirect.http_redirect_code)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_sni)
        self.assertEqual('https', result.website_configuration.routing_rules.routing_rules[1].redirect.protocol)
        self.assertEqual('prefix/${key}.suffix', result.website_configuration.routing_rules.routing_rules[1].redirect.replace_key_prefix_with)
        self.assertEqual('AliCDN', result.website_configuration.routing_rules.routing_rules[1].redirect.redirect_type)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_pass_query_string)
        self.assertEqual('example.com', result.website_configuration.routing_rules.routing_rules[1].redirect.host_name)
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

