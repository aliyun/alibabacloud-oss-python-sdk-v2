import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="do meta query semantic sample")
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

    result = client.do_meta_query(oss.DoMetaQueryRequest(
            bucket=args.bucket,
            mode='semantic',
            meta_query=oss.MetaQuery(
                max_results=1000,
                query='俯瞰白雪覆盖的森林',
                order='desc',
                media_types=oss.MediaTypes(
                    media_type=['image']
                ),
                simple_query='{"Operation":"gt", "Field": "Size", "Value": "30"}',
            ),
    ))

    print(vars(result))

if __name__ == "__main__":
    main()