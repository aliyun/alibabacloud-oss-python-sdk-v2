import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="get bucket website sample")
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

    result = client.get_bucket_website(oss.GetBucketWebsiteRequest(
            bucket=args.bucket,
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
            f' website configuration: {result.website_configuration},'
            f' index document: {result.website_configuration.index_document},'
            f' suffix: {result.website_configuration.index_document.suffix},'
            f' support sub dir: {result.website_configuration.index_document.support_sub_dir},'
            f' type: {result.website_configuration.index_document.type},'
            f' error document: {result.website_configuration.error_document},'
            f' key: {result.website_configuration.error_document.key},'
            f' http status: {result.website_configuration.error_document.http_status},'
            f' routing rules: {result.website_configuration.routing_rules},'
            f' rule number: {result.website_configuration.routing_rules.routing_rules[0].rule_number},'
            f' condition: {result.website_configuration.routing_rules.routing_rules[0].condition},'
            f' key suffix equals: {result.website_configuration.routing_rules.routing_rules[0].condition.key_suffix_equals},'
            f' http error code returned equals: {result.website_configuration.routing_rules.routing_rules[0].condition.http_error_code_returned_equals},'
            f' key: {result.website_configuration.routing_rules.routing_rules[0].condition.include_headers[0].key},'
            f' equals: {result.website_configuration.routing_rules.routing_rules[0].condition.include_headers[0].equals},'
            f' key: {result.website_configuration.routing_rules.routing_rules[0].condition.include_headers[1].key},'
            f' equals: {result.website_configuration.routing_rules.routing_rules[0].condition.include_headers[1].equals},'
            f' key prefix equals: {result.website_configuration.routing_rules.routing_rules[0].condition.key_prefix_equals},'
            f' redirect: {result.website_configuration.routing_rules.routing_rules[0].redirect},'
            f' mirror url: {result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_url},'
            f' replace key with: {result.website_configuration.routing_rules.routing_rules[0].redirect.replace_key_with},'
            f' enable replace prefix: {result.website_configuration.routing_rules.routing_rules[0].redirect.enable_replace_prefix},'
            f' pass query string: {result.website_configuration.routing_rules.routing_rules[0].redirect.pass_query_string},'
            f' mirror headers: {result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers},'
            f' pass all: {result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.pass_all},'
            f' key: {result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[0].key},'
            f' value: {result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[0].value},'
            f' key: {result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[1].key},'
            f' value: {result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_headers.sets[1].value},'
            f' http redirect code: {result.website_configuration.routing_rules.routing_rules[0].redirect.http_redirect_code},'
            f' mirror sni: {result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_sni},'
            f' protocol: {result.website_configuration.routing_rules.routing_rules[0].redirect.protocol},'
            f' replace key prefix with: {result.website_configuration.routing_rules.routing_rules[0].redirect.replace_key_prefix_with},'
            f' redirect type: {result.website_configuration.routing_rules.routing_rules[0].redirect.redirect_type},'
            f' mirror pass query string: {result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_pass_query_string},'
            f' host name: {result.website_configuration.routing_rules.routing_rules[0].redirect.host_name},'
            f' mirror follow redirect: {result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_follow_redirect},'
            f' mirror check md5: {result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_check_md5},'
            f' mirror pass original slashes: {result.website_configuration.routing_rules.routing_rules[0].redirect.mirror_pass_original_slashes},'
            f' rule number: {result.website_configuration.routing_rules.routing_rules[1].rule_number},'
            f' condition: {result.website_configuration.routing_rules.routing_rules[1].condition},'
            f' key suffix equals: {result.website_configuration.routing_rules.routing_rules[1].condition.key_suffix_equals},'
            f' http error code returned equals: {result.website_configuration.routing_rules.routing_rules[1].condition.http_error_code_returned_equals},'
            f' key: {result.website_configuration.routing_rules.routing_rules[1].condition.include_headers[0].key},'
            f' equals: {result.website_configuration.routing_rules.routing_rules[1].condition.include_headers[0].equals},'
            f' key: {result.website_configuration.routing_rules.routing_rules[1].condition.include_headers[1].key},'
            f' equals: {result.website_configuration.routing_rules.routing_rules[1].condition.include_headers[1].equals},'
            f' key prefix equals: {result.website_configuration.routing_rules.routing_rules[1].condition.key_prefix_equals},'
            f' redirect: {result.website_configuration.routing_rules.routing_rules[1].redirect},'
            f' mirror url: {result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_url},'
            f' replace key with: {result.website_configuration.routing_rules.routing_rules[1].redirect.replace_key_with},'
            f' enable replace prefix: {result.website_configuration.routing_rules.routing_rules[1].redirect.enable_replace_prefix},'
            f' pass query string: {result.website_configuration.routing_rules.routing_rules[1].redirect.pass_query_string},'
            f' mirror headers: {result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_headers},'
            f' http redirect code: {result.website_configuration.routing_rules.routing_rules[1].redirect.http_redirect_code},'
            f' mirror sni: {result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_sni},'
            f' protocol: {result.website_configuration.routing_rules.routing_rules[1].redirect.protocol},'
            f' replace key prefix with: {result.website_configuration.routing_rules.routing_rules[1].redirect.replace_key_prefix_with},'
            f' redirect type: {result.website_configuration.routing_rules.routing_rules[1].redirect.redirect_type},'
            f' mirror pass query string: {result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_pass_query_string},'
            f' host name: {result.website_configuration.routing_rules.routing_rules[1].redirect.host_name},'
            f' mirror follow redirect: {result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_follow_redirect},'
            f' mirror check md5: {result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_check_md5},'
            f' mirror pass original slashes: {result.website_configuration.routing_rules.routing_rules[1].redirect.mirror_pass_original_slashes},'
    )

    if result.website_configuration.routing_rules.routing_rules:
        for r in result.website_configuration.routing_rules.routing_rules:
            print(f'result: rule number: {r.rule_number}, condition: {r.condition}, redirect: {r.redirect}')


if __name__ == "__main__":
    main()