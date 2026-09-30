import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="put bucket storage quota sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--storage_quota', help='The storage capacity limit in bytes, a positive integer.', type=int, default=10737418240)
parser.add_argument('--mode', help='The quota mode. Valid values: Strict and Warning.', default='Strict')


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

    result = client.put_bucket_storage_quota(oss.PutBucketStorageQuotaRequest(
            bucket=args.bucket,
            quota_configuration=oss.QuotaConfiguration(
                storage_quota=args.storage_quota,
                mode=args.mode,
            ),
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
    )


if __name__ == "__main__":
    main()
