import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="put bucket referer sample")
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

    result = client.put_bucket_referer(oss.PutBucketRefererRequest(
            bucket=args.bucket,
            referer_configuration=oss.RefererConfiguration(
                allow_empty_referer=True,
                allow_truncate_query_string=False,
                truncate_path=False,
                referer_list=oss.RefererList(
                    referers=['http://www.aliyun.com', 'https://www.aliyun.com'],
                ),
                referer_blacklist=oss.RefererBlacklist(
                    referers=['http://www.refuse.com', 'http://www.refuse1.com'],
                ),
            ),
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
    )


if __name__ == "__main__":
    main()