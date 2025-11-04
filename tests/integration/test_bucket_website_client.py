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


    def test_bucket_website_new_redirect(self):
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
                            mirror_sni=False,
                            replace_key_prefix_with='abc/',
                            redirect_type='Mirror',
                            mirror_pass_query_string=False,
                            mirror_follow_redirect=True,
                            mirror_check_md5=True,
                            mirror_pass_original_slashes=True,
                            mirror_allow_video_snapshot=True,
                            # mirror_async_status=302,
                            mirror_taggings=oss.MirrorTaggings(
                                taggings=[oss.RuleTaggings(
                                    key='tag-key1',
                                    value='tag-value1',
                                ), oss.RuleTaggings(
                                    key='tag-key2',
                                    value='tag-value2',
                                )],
                            ),
                            mirror_auth=oss.MirrorAuth(
                                access_key_id='test-access-key-id',
                                access_key_secret='test-access-key-secret',
                                auth_type='S3V4',
                                region='cn-hangzhou',
                            ),
                            mirror_dst_region='oss-cn-hangzhou',
                            # mirror_dst_vpc_id='vpc-123456',
                            # mirror_tunnel_id='tunnel-123456',
                            mirror_role='test-role',
                            mirror_using_role=True,
                            mirror_return_headers=oss.MirrorReturnHeaders(
                                return_headers=[oss.ReturnHeader(
                                    key='header-key1',
                                    value='header-value1',
                                ), oss.ReturnHeader(
                                    key='header-key2',
                                    value='header-value2',
                                )],
                            ),
                            mirror_proxy_pass=False,
                            mirror_is_express_tunnel=True,
                            # mirror_dst_slave_vpc_id='vpc-slave-123456',
                            mirror_allow_head_object=True,
                            transparent_mirror_response_codes='404,500',
                            mirror_save_oss_meta=True,
                            mirror_allow_get_image_info=True,
                            mirror_url_probe='http://probe.example.com/',
                            # mirror_url_slave='http://slave.example.com/',
                            mirror_user_last_modified=True,
                            mirror_switch_all_errors=False,
                            mirror_multi_alternates=oss.MirrorMultiAlternates(
                                mirror_multi_alternates=[oss.MirrorMultiAlternate(
                                    mirror_multi_alternate_number=1,
                                    mirror_multi_alternate_url='http://alternate1.example.com/',
                                    mirror_multi_alternate_vpc_id='vpc-alternate-1',
                                    mirror_multi_alternate_dst_region='oss-cn-shanghai',
                                ), oss.MirrorMultiAlternate(
                                    mirror_multi_alternate_number=2,
                                    mirror_multi_alternate_url='http://alternate2.example.com/',
                                    mirror_multi_alternate_vpc_id='vpc-alternate-2',
                                    mirror_multi_alternate_dst_region='oss-cn-beijing',
                                )],
                            ),
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
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_sni)
        self.assertEqual('abc/', result.website_configuration.routing_rules.routing_rules[0].redirect.replace_key_prefix_with)
        self.assertEqual('Mirror', result.website_configuration.routing_rules.routing_rules[0].redirect.redirect_type)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_pass_query_string)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_follow_redirect)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_check_md5)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_pass_original_slashes)
        # New fields verification
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_allow_video_snapshot)
        self.assertEqual('tag-key1', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_taggings.taggings[0].key)
        self.assertEqual('tag-value1', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_taggings.taggings[0].value)
        self.assertEqual('tag-key2', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_taggings.taggings[1].key)
        self.assertEqual('tag-value2', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_taggings.taggings[1].value)
        self.assertEqual('test-access-key-id', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_auth.access_key_id)
        self.assertEqual('S3V4', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_auth.auth_type)
        self.assertEqual('cn-hangzhou', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_auth.region)
        self.assertEqual('oss-cn-hangzhou', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_dst_region)
        self.assertEqual('test-role', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_role)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_using_role)
        self.assertEqual('header-key1', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_return_headers.return_headers[0].key)
        self.assertEqual('header-value1', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_return_headers.return_headers[0].value)
        self.assertEqual('header-key2', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_return_headers.return_headers[1].key)
        self.assertEqual('header-value2', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_return_headers.return_headers[1].value)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_is_express_tunnel)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_allow_head_object)
        self.assertEqual('404,500', result.website_configuration.routing_rules.routing_rules[0].redirect.transparent_mirror_response_codes)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_save_oss_meta)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_allow_get_image_info)
        self.assertEqual('http://probe.example.com/', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_url_probe)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_user_last_modified)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_switch_all_errors)
        self.assertEqual(1, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_multi_alternates.mirror_multi_alternates[0].mirror_multi_alternate_number)
        self.assertEqual('http://alternate1.example.com/', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_multi_alternates.mirror_multi_alternates[0].mirror_multi_alternate_url)
        self.assertEqual('vpc-alternate-1', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_multi_alternates.mirror_multi_alternates[0].mirror_multi_alternate_vpc_id)
        self.assertEqual('oss-cn-shanghai', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_multi_alternates.mirror_multi_alternates[0].mirror_multi_alternate_dst_region)
        self.assertEqual(2, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_multi_alternates.mirror_multi_alternates[1].mirror_multi_alternate_number)
        self.assertEqual('http://alternate2.example.com/', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_multi_alternates.mirror_multi_alternates[1].mirror_multi_alternate_url)
        self.assertEqual('vpc-alternate-2', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_multi_alternates.mirror_multi_alternates[1].mirror_multi_alternate_vpc_id)
        self.assertEqual('oss-cn-beijing', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_multi_alternates.mirror_multi_alternates[1].mirror_multi_alternate_dst_region)

        # delete bucket website
        result = self.client.delete_bucket_website(oss.DeleteBucketWebsiteRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

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

    def test_bucket_website_new_redirect_v1(self):
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
                            mirror_sni=False,
                            replace_key_prefix_with='abc/',
                            redirect_type='Mirror',
                            mirror_pass_query_string=False,
                            mirror_follow_redirect=True,
                            mirror_check_md5=True,
                            mirror_pass_original_slashes=True,
                            mirror_allow_video_snapshot=True,
                            # mirror_async_status=302,
                            mirror_taggings=oss.MirrorTaggings(
                                taggings=[oss.RuleTaggings(
                                    key='tag-key1',
                                    value='tag-value1',
                                ), oss.RuleTaggings(
                                    key='tag-key2',
                                    value='tag-value2',
                                )],
                            ),
                            mirror_auth=oss.MirrorAuth(
                                access_key_id='test-access-key-id',
                                access_key_secret='test-access-key-secret',
                                auth_type='S3V4',
                                region='cn-hangzhou',
                            ),
                            mirror_dst_region='oss-cn-hangzhou',
                            # mirror_dst_vpc_id='vpc-123456',
                            # mirror_tunnel_id='tunnel-123456',
                            mirror_role='test-role',
                            mirror_using_role=True,
                            mirror_return_headers=oss.MirrorReturnHeaders(
                                return_headers=[oss.ReturnHeader(
                                    key='header-key1',
                                    value='header-value1',
                                ), oss.ReturnHeader(
                                    key='header-key2',
                                    value='header-value2',
                                )],
                            ),
                            mirror_proxy_pass=False,
                            mirror_is_express_tunnel=True,
                            # mirror_dst_slave_vpc_id='vpc-slave-123456',
                            mirror_allow_head_object=True,
                            transparent_mirror_response_codes='404,500',
                            mirror_save_oss_meta=True,
                            mirror_allow_get_image_info=True,
                            mirror_url_probe='http://probe.example.com/',
                            # mirror_url_slave='http://slave.example.com/',
                            mirror_user_last_modified=True,
                            mirror_switch_all_errors=False,
                            mirror_multi_alternates=oss.MirrorMultiAlternates(
                                mirror_multi_alternates=[oss.MirrorMultiAlternate(
                                    mirror_multi_alternate_number=1,
                                    mirror_multi_alternate_url='http://alternate1.example.com/',
                                    mirror_multi_alternate_vpc_id='vpc-alternate-1',
                                    mirror_multi_alternate_dst_region='oss-cn-shanghai',
                                ), oss.MirrorMultiAlternate(
                                    mirror_multi_alternate_number=2,
                                    mirror_multi_alternate_url='http://alternate2.example.com/',
                                    mirror_multi_alternate_vpc_id='vpc-alternate-2',
                                    mirror_multi_alternate_dst_region='oss-cn-beijing',
                                )],
                            ),
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
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_sni)
        self.assertEqual('abc/', result.website_configuration.routing_rules.routing_rules[0].redirect.replace_key_prefix_with)
        self.assertEqual('Mirror', result.website_configuration.routing_rules.routing_rules[0].redirect.redirect_type)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_pass_query_string)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_follow_redirect)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_check_md5)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_pass_original_slashes)
        # New fields verification
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_allow_video_snapshot)
        self.assertEqual('tag-key1', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_taggings.taggings[0].key)
        self.assertEqual('tag-value1', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_taggings.taggings[0].value)
        self.assertEqual('tag-key2', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_taggings.taggings[1].key)
        self.assertEqual('tag-value2', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_taggings.taggings[1].value)
        self.assertEqual('test-access-key-id', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_auth.access_key_id)
        self.assertEqual('S3V4', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_auth.auth_type)
        self.assertEqual('cn-hangzhou', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_auth.region)
        self.assertEqual('oss-cn-hangzhou', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_dst_region)
        self.assertEqual('test-role', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_role)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_using_role)
        self.assertEqual('header-key1', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_return_headers.return_headers[0].key)
        self.assertEqual('header-value1', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_return_headers.return_headers[0].value)
        self.assertEqual('header-key2', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_return_headers.return_headers[1].key)
        self.assertEqual('header-value2', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_return_headers.return_headers[1].value)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_is_express_tunnel)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_allow_head_object)
        self.assertEqual('404,500', result.website_configuration.routing_rules.routing_rules[0].redirect.transparent_mirror_response_codes)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_save_oss_meta)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_allow_get_image_info)
        self.assertEqual('http://probe.example.com/', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_url_probe)
        self.assertEqual(True, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_user_last_modified)
        self.assertEqual(False, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_switch_all_errors)
        self.assertEqual(1, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_multi_alternates.mirror_multi_alternates[0].mirror_multi_alternate_number)
        self.assertEqual('http://alternate1.example.com/', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_multi_alternates.mirror_multi_alternates[0].mirror_multi_alternate_url)
        self.assertEqual('vpc-alternate-1', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_multi_alternates.mirror_multi_alternates[0].mirror_multi_alternate_vpc_id)
        self.assertEqual('oss-cn-shanghai', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_multi_alternates.mirror_multi_alternates[0].mirror_multi_alternate_dst_region)
        self.assertEqual(2, result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_multi_alternates.mirror_multi_alternates[1].mirror_multi_alternate_number)
        self.assertEqual('http://alternate2.example.com/', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_multi_alternates.mirror_multi_alternates[1].mirror_multi_alternate_url)
        self.assertEqual('vpc-alternate-2', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_multi_alternates.mirror_multi_alternates[1].mirror_multi_alternate_vpc_id)
        self.assertEqual('oss-cn-beijing', result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_multi_alternates.mirror_multi_alternates[1].mirror_multi_alternate_dst_region)

        # delete bucket website
        result = self.signv1_client.delete_bucket_website(oss.DeleteBucketWebsiteRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

    def test_bucket_website_lua_config_v1(self):
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

        # put bucket website with lua_config
        result = self.signv1_client.put_bucket_website(oss.PutBucketWebsiteRequest(
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
        result = self.signv1_client.get_bucket_website(oss.GetBucketWebsiteRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual('test.lua', result.website_configuration.routing_rules.routing_rules[0].lua_config.script)

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
