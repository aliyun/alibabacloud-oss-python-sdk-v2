# pylint: skip-file

from typing import cast
import alibabacloud_oss_v2 as oss
from . import TestIntegration, random_bucket_name


class TestBucketWebsite(TestIntegration):

    def test_bucket_website(self):
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

        # put bucket website
        result = self.client.put_bucket_website(oss.PutBucketWebsiteRequest(
            bucket=bucket_name,
            website_configuration=oss.WebsiteConfiguration(
                index_document=oss.IndexDocument(
                    suffix='index.html',
                    support_sub_dir=True,
                    type=0,
                ),
                error_document=oss.ErrorDocument(
                    key='error.html',
                    http_status=404,
                ),
                routing_rules=oss.RoutingRules(
                    routing_rules=[oss.RoutingRule(
                        rule_number=1,
                        condition=oss.RoutingRuleCondition(
                            key_suffix_equals='abc/',
                            http_error_code_returned_equals=404,
                            include_headers=[oss.RoutingRuleIncludeHeader(
                                key='key1',
                                equals='value1',
                            ), oss.RoutingRuleIncludeHeader(
                                key='key2',
                                equals='value2',
                            )],
                            key_prefix_equals='key',
                        ),
                        redirect=oss.RoutingRuleRedirect(
                            mirror_url='http://example.com/',
                            enable_replace_prefix=True,
                            pass_query_string=False,
                            mirror_headers=oss.MirrorHeaders(
                                pass_all=True,
                                passs=['myheader-key1', 'myheader-key2'],
                                removes=['myheader-key3', 'myheader-key4'],
                                sets=[oss.MirrorHeadersSet(
                                    key='myheader-key5',
                                    value='myheader-value',
                                ), oss.MirrorHeadersSet(
                                    key='myheader-key6',
                                    value='myheader-value2',
                                )],
                            ),
                            mirror_sni=True,
                            replace_key_prefix_with='abc/',
                            redirect_type='Mirror',
                            mirror_pass_query_string=False,
                            mirror_follow_redirect=True,
                            mirror_check_md5=True,
                            mirror_pass_original_slashes=True,
                        ),
                    ), oss.RoutingRule(
                        rule_number=2,
                        condition=oss.RoutingRuleCondition(
                            key_suffix_equals='bbc/',
                            http_error_code_returned_equals=403,
                            include_headers=[oss.RoutingRuleIncludeHeader(
                                key='key21',
                                equals='value21',
                            ), oss.RoutingRuleIncludeHeader(
                                key='key22',
                                equals='value22U',
                            )],
                            key_prefix_equals='abc/',
                        ),
                        redirect=oss.RoutingRuleRedirect(
                            replace_key_with='prefix/${key}.suffix',
                            pass_query_string=False,
                            http_redirect_code=301,
                            protocol='http',
                            redirect_type='AliCDN',
                            host_name='example.com',
                        ),
                    ), oss.RoutingRule(
                        rule_number=3,
                        condition=oss.RoutingRuleCondition(
                            http_error_code_returned_equals=404,
                        ),
                        redirect=oss.RoutingRuleRedirect(
                            replace_key_with='prefix/${key}',
                            pass_query_string=False,
                            enable_replace_prefix=False,
                            http_redirect_code=302,
                            protocol='http',
                            redirect_type='External',
                            host_name='example.com',
                        ),
                    )],
                ),
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket website
        result = self.client.get_bucket_website(oss.GetBucketWebsiteRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('index.html', result.website_configuration.index_document.suffix)
        self.assertEqual(True, result.website_configuration.index_document.support_sub_dir)
        self.assertEqual(0, result.website_configuration.index_document.type)
        self.assertEqual('error.html', result.website_configuration.error_document.key)
        self.assertEqual(404, result.website_configuration.error_document.http_status)
        self.assertEqual(1, result.website_configuration.routing_rules.routing_rules[0].rule_number)
        self.assertEqual('abc/', result.website_configuration.routing_rules.routing_rules[0].condition.key_suffix_equals)
        self.assertEqual(404, result.website_configuration.routing_rules.routing_rules[0].condition.http_error_code_returned_equals)
        self.assertEqual('key1', result.website_configuration.routing_rules.routing_rules[0].condition.include_headers[0].key)
        self.assertEqual('value1', result.website_configuration.routing_rules.routing_rules[0].condition.include_headers[0].equals)
        self.assertEqual('key2', result.website_configuration.routing_rules.routing_rules[0].condition.include_headers[1].key)
        self.assertEqual('value2', result.website_configuration.routing_rules.routing_rules[0].condition.include_headers[1].equals)
        self.assertEqual('key', result.website_configuration.routing_rules.routing_rules[0].condition.key_prefix_equals)
        self.assertEqual('http://example.com/', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_url)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.enable_replace_prefix)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[0].redirect.pass_query_string)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.pass_all)
        self.assertEqual('myheader-key1', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.passs[0])
        self.assertEqual('myheader-key2', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.passs[1])
        self.assertEqual('myheader-key3', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.removes[0])
        self.assertEqual('myheader-key4', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.removes[1])
        self.assertEqual('myheader-key5', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[0].key)
        self.assertEqual('myheader-value', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[0].value)
        self.assertEqual('myheader-key6', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[1].key)
        self.assertEqual('myheader-value2', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[1].value)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_sni)
        self.assertEqual('abc/', result.website_configuration.routing_rules.routing_rules[0].redirect.replace_key_prefix_with)
        self.assertEqual('Mirror', result.website_configuration.routing_rules.routing_rules[0].redirect.redirect_type)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_pass_query_string)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_follow_redirect)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_check_md5)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_pass_original_slashes)
        self.assertEqual(2, result.website_configuration.routing_rules.routing_rules[1].rule_number)
        self.assertEqual('bbc/', result.website_configuration.routing_rules.routing_rules[1].condition.key_suffix_equals)
        self.assertEqual(403, result.website_configuration.routing_rules.routing_rules[1].condition.http_error_code_returned_equals)
        self.assertEqual('key21', result.website_configuration.routing_rules.routing_rules[1].condition.include_headers[0].key)
        self.assertEqual('value21', result.website_configuration.routing_rules.routing_rules[1].condition.include_headers[0].equals)
        self.assertEqual('key22', result.website_configuration.routing_rules.routing_rules[1].condition.include_headers[1].key)
        self.assertEqual('value22U', result.website_configuration.routing_rules.routing_rules[1].condition.include_headers[1].equals)
        self.assertEqual('abc/', result.website_configuration.routing_rules.routing_rules[1].condition.key_prefix_equals)
        self.assertEqual('prefix/${key}.suffix', result.website_configuration.routing_rules.routing_rules[1].redirect.replace_key_with)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[1].redirect.pass_query_string)
        self.assertEqual(301, result.website_configuration.routing_rules.routing_rules[1].redirect.http_redirect_code)
        self.assertEqual('http', result.website_configuration.routing_rules.routing_rules[1].redirect.protocol)
        self.assertEqual('AliCDN', result.website_configuration.routing_rules.routing_rules[1].redirect.redirect_type)
        self.assertEqual('example.com', result.website_configuration.routing_rules.routing_rules[1].redirect.host_name)
        self.assertEqual(3, result.website_configuration.routing_rules.routing_rules[2].rule_number)
        self.assertEqual(404, result.website_configuration.routing_rules.routing_rules[2].condition.http_error_code_returned_equals)
        self.assertEqual('prefix/${key}', result.website_configuration.routing_rules.routing_rules[2].redirect.replace_key_with)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[2].redirect.pass_query_string)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[2].redirect.enable_replace_prefix)
        self.assertEqual(302, result.website_configuration.routing_rules.routing_rules[2].redirect.http_redirect_code)
        self.assertEqual('http', result.website_configuration.routing_rules.routing_rules[2].redirect.protocol)
        self.assertEqual('External', result.website_configuration.routing_rules.routing_rules[2].redirect.redirect_type)
        self.assertEqual('example.com', result.website_configuration.routing_rules.routing_rules[2].redirect.host_name)

        # delete bucket website
        result = self.client.delete_bucket_website(oss.DeleteBucketWebsiteRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

    def test_bucket_website_v1(self):
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

        # put bucket website
        result = self.signv1_client.put_bucket_website(oss.PutBucketWebsiteRequest(
            bucket=bucket_name,
            website_configuration=oss.WebsiteConfiguration(
                index_document=oss.IndexDocument(
                    suffix='index.html',
                    support_sub_dir=True,
                    type=0,
                ),
                error_document=oss.ErrorDocument(
                    key='error.html',
                    http_status=404,
                ),
                routing_rules=oss.RoutingRules(
                    routing_rules=[oss.RoutingRule(
                        rule_number=1,
                        condition=oss.RoutingRuleCondition(
                            key_suffix_equals='abc/',
                            http_error_code_returned_equals=404,
                            include_headers=[oss.RoutingRuleIncludeHeader(
                                key='key1',
                                equals='value1',
                            ), oss.RoutingRuleIncludeHeader(
                                key='key2',
                                equals='value2',
                            )],
                            key_prefix_equals='key',
                        ),
                        redirect=oss.RoutingRuleRedirect(
                            mirror_url='http://example.com/',
                            enable_replace_prefix=True,
                            pass_query_string=True,
                            mirror_headers=oss.MirrorHeaders(
                                pass_all=True,
                                passs=['myheader-key1', 'myheader-key2'],
                                removes=['myheader-key3', 'myheader-key4'],
                                sets=[oss.MirrorHeadersSet(
                                    key='myheader-key5',
                                    value='myheader-value',
                                ), oss.MirrorHeadersSet(
                                    key='myheader-key6',
                                    value='myheader-valu2',
                                )],
                            ),
                            mirror_sni=True,
                            replace_key_prefix_with='abc/',
                            redirect_type='Mirror',
                            mirror_pass_query_string=False,
                            mirror_follow_redirect=True,
                            mirror_check_md5=True,
                            mirror_pass_original_slashes=True,
                        ),
                    ), oss.RoutingRule(
                        rule_number=2,
                        condition=oss.RoutingRuleCondition(
                            key_suffix_equals='bbc/',
                            http_error_code_returned_equals=403,
                            include_headers=[oss.RoutingRuleIncludeHeader(
                                key='key21',
                                equals='value21',
                            ), oss.RoutingRuleIncludeHeader(
                                key='key22',
                                equals='value22U',
                            )],
                            key_prefix_equals='abc/',
                        ),
                        redirect=oss.RoutingRuleRedirect(
                            replace_key_with='prefix/${key}.suffix',
                            pass_query_string=False,
                            mirror_headers=oss.MirrorHeaders(
                                pass_all=True,
                            ),
                            http_redirect_code=301,
                            protocol='http',
                            redirect_type='AliCDN',
                            host_name='example.com',
                        ),
                    ), oss.RoutingRule(
                        rule_number=3,
                        condition=oss.RoutingRuleCondition(
                            http_error_code_returned_equals=404,
                        ),
                        redirect=oss.RoutingRuleRedirect(
                            replace_key_with='prefix/${key}',
                            pass_query_string=False,
                            enable_replace_prefix=False,
                            http_redirect_code=302,
                            protocol='http',
                            redirect_type='External',
                            host_name='example.com',
                        ),
                    )],
                ),
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))


        # get bucket website
        result = self.signv1_client.get_bucket_website(oss.GetBucketWebsiteRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('index.html', result.website_configuration.index_document.suffix)
        self.assertEqual(True, result.website_configuration.index_document.support_sub_dir)
        self.assertEqual(0, result.website_configuration.index_document.type)
        self.assertEqual('error.html', result.website_configuration.error_document.key)
        self.assertEqual(404, result.website_configuration.error_document.http_status)
        self.assertEqual(1, result.website_configuration.routing_rules.routing_rules[0].rule_number)
        self.assertEqual('abc/', result.website_configuration.routing_rules.routing_rules[0].condition.key_suffix_equals)
        self.assertEqual(404, result.website_configuration.routing_rules.routing_rules[0].condition.http_error_code_returned_equals)
        self.assertEqual('key1', result.website_configuration.routing_rules.routing_rules[0].condition.include_headers[0].key)
        self.assertEqual('value1', result.website_configuration.routing_rules.routing_rules[0].condition.include_headers[0].equals)
        self.assertEqual('key2', result.website_configuration.routing_rules.routing_rules[0].condition.include_headers[1].key)
        self.assertEqual('value2', result.website_configuration.routing_rules.routing_rules[0].condition.include_headers[1].equals)
        self.assertEqual('key', result.website_configuration.routing_rules.routing_rules[0].condition.key_prefix_equals)
        self.assertEqual('http://example.com/', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_url)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.enable_replace_prefix)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[0].redirect.pass_query_string)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.pass_all)
        self.assertEqual('myheader-key1', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.passs[0])
        self.assertEqual('myheader-key2', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.passs[1])
        self.assertEqual('myheader-key3', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.removes[0])
        self.assertEqual('myheader-key4', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.removes[1])
        self.assertEqual('myheader-key5', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[0].key)
        self.assertEqual('myheader-value', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[0].value)
        self.assertEqual('myheader-key6', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[1].key)
        self.assertEqual('myheader-valu2', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[1].value)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_sni)
        self.assertEqual('abc/', result.website_configuration.routing_rules.routing_rules[0].redirect.replace_key_prefix_with)
        self.assertEqual('Mirror', result.website_configuration.routing_rules.routing_rules[0].redirect.redirect_type)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_pass_query_string)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_follow_redirect)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_check_md5)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_pass_original_slashes)
        self.assertEqual(2, result.website_configuration.routing_rules.routing_rules[1].rule_number)
        self.assertEqual('bbc/', result.website_configuration.routing_rules.routing_rules[1].condition.key_suffix_equals)
        self.assertEqual(403, result.website_configuration.routing_rules.routing_rules[1].condition.http_error_code_returned_equals)
        self.assertEqual('key21', result.website_configuration.routing_rules.routing_rules[1].condition.include_headers[0].key)
        self.assertEqual('value21', result.website_configuration.routing_rules.routing_rules[1].condition.include_headers[0].equals)
        self.assertEqual('key22', result.website_configuration.routing_rules.routing_rules[1].condition.include_headers[1].key)
        self.assertEqual('value22U', result.website_configuration.routing_rules.routing_rules[1].condition.include_headers[1].equals)
        self.assertEqual('abc/', result.website_configuration.routing_rules.routing_rules[1].condition.key_prefix_equals)
        self.assertEqual('prefix/${key}.suffix', result.website_configuration.routing_rules.routing_rules[1].redirect.replace_key_with)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[1].redirect.pass_query_string)
        self.assertEqual(301, result.website_configuration.routing_rules.routing_rules[1].redirect.http_redirect_code)
        self.assertEqual('http', result.website_configuration.routing_rules.routing_rules[1].redirect.protocol)
        self.assertEqual('AliCDN', result.website_configuration.routing_rules.routing_rules[1].redirect.redirect_type)
        self.assertEqual('example.com', result.website_configuration.routing_rules.routing_rules[1].redirect.host_name)
        self.assertEqual(3, result.website_configuration.routing_rules.routing_rules[2].rule_number)
        self.assertEqual(404, result.website_configuration.routing_rules.routing_rules[2].condition.http_error_code_returned_equals)
        self.assertEqual('prefix/${key}', result.website_configuration.routing_rules.routing_rules[2].redirect.replace_key_with)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[2].redirect.pass_query_string)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[2].redirect.enable_replace_prefix)
        self.assertEqual(302, result.website_configuration.routing_rules.routing_rules[2].redirect.http_redirect_code)
        self.assertEqual('http', result.website_configuration.routing_rules.routing_rules[2].redirect.protocol)
        self.assertEqual('External', result.website_configuration.routing_rules.routing_rules[2].redirect.redirect_type)
        self.assertEqual('example.com', result.website_configuration.routing_rules.routing_rules[2].redirect.host_name)

        # delete bucket website
        result = self.signv1_client.delete_bucket_website(oss.DeleteBucketWebsiteRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

    def test_bucket_website_fail(self):
        # create bucket
        bucket_name = random_bucket_name()
        self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))

        # put bucket website
        try:
            self.invalid_client.put_bucket_website(oss.PutBucketWebsiteRequest(
                bucket=bucket_name,
                website_configuration=oss.WebsiteConfiguration(
                    index_document=oss.IndexDocument(
                        suffix='index.html',
                        support_sub_dir=True,
                        type=0,
                    ),
                    error_document=oss.ErrorDocument(
                        key='error.html',
                        http_status=404,
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

        # get bucket website
        try:
            self.invalid_client.get_bucket_website(oss.GetBucketWebsiteRequest(
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

        # delete bucket website
        try:
            self.invalid_client.delete_bucket_website(oss.DeleteBucketWebsiteRequest(
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

    def test_bucket_website_lua_config(self):
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

        # put bucket website with lua_config
        result = self.client.put_bucket_website(oss.PutBucketWebsiteRequest(
            bucket=bucket_name,
            website_configuration=oss.WebsiteConfiguration(
                index_document=oss.IndexDocument(
                    suffix='index.html',
                ),
                routing_rules=oss.RoutingRules(
                    routing_rules=[oss.RoutingRule(
                        rule_number=1,
                        condition=oss.RoutingRuleCondition(
                            key_prefix_equals='key',
                        ),
                        redirect=oss.RoutingRuleRedirect(
                            redirect_type='Mirror',
                            mirror_url='http://example.com/',
                        ),
                        lua_config=oss.RoutingRuleLuaConfig(
                            script='test.lua',
                        ),
                    )],
                ),
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        # get bucket website and verify lua_config
        result = self.client.get_bucket_website(oss.GetBucketWebsiteRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual('test.lua', result.website_configuration.routing_rules.routing_rules[0].lua_config.script)

        # delete bucket website
        result = self.client.delete_bucket_website(oss.DeleteBucketWebsiteRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))