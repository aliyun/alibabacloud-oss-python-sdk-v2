import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="get bucket object worm configuration sample")
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

    result = client.get_bucket_object_worm_configuration(oss.GetBucketObjectWormConfigurationRequest(
        bucket=args.bucket,
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          )

    if result.object_worm_configuration:
        worm_config = result.object_worm_configuration
        print(f'object worm enabled: {worm_config.object_worm_enabled}')

        if worm_config.rule and worm_config.rule.default_retention:
            retention = worm_config.rule.default_retention
            print(f'retention mode: {retention.mode}')
            print(f'retention days: {retention.days}')
            print(f'retention years: {retention.years}')


if __name__ == "__main__":
    main()
