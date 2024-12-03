import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="put bucket website sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')


def main():

    args = parser.parse_args()

    # Loading credentials values from the environment variables
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    # Using the SDK's default configuration
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint

    client = oss.Client(cfg)

    result = client.put_bucket_website(oss.PutBucketWebsiteRequest(
        bucket=args.bucket,
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
                        key_prefix_equals='bbb/',
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

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
    )


if __name__ == "__main__":
    main()