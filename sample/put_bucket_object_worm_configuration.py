import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="put bucket object worm configuration sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--mode', help='Object-level retention strategy pattern. Valid values: GOVERNANCE, COMPLIANCE', default='GOVERNANCE')
parser.add_argument('--days', help='Object-level retention policy days (max 36500)', type=int)
parser.add_argument('--years', help='Bucket object level retention policy years (max 100)', type=int)


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

    # Create default retention settings
    default_retention = oss.ObjectWormConfigurationRuleDefaultRetention(
        mode=args.mode,
        days=args.days,
        # days and years can only appear once
        # years=args.years,
    )

    # Create rule container
    rule = oss.ObjectWormConfigurationRule(
        default_retention=default_retention,
    )

    # Create configuration
    config = oss.ObjectWormConfiguration(
        object_worm_enabled='Enabled',
        rule=rule,
    )

    result = client.put_bucket_object_worm_configuration(oss.PutBucketObjectWormConfigurationRequest(
        bucket=args.bucket,
        object_worm_configuration=config,
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
    )


if __name__ == "__main__":
    main()
