import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="get bucket referer sample")
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

    result = client.get_bucket_referer(oss.GetBucketRefererRequest(
            bucket=args.bucket,
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
            f' allow empty referer: {result.referer_configuration.allow_empty_referer},'
            f' allow truncate query string: {result.referer_configuration.allow_truncate_query_string},'
            f' truncate path: {result.referer_configuration.truncate_path},'
            f' referer list: {result.referer_configuration.referer_list},'
            f' referer blacklist: {result.referer_configuration.referer_blacklist},'
    )


if __name__ == "__main__":
    main()