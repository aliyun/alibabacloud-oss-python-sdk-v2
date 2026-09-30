import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.agentic as oss_agentic

parser = argparse.ArgumentParser(description="put agentic bucket storage quota sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The prefix of the Agent Bucket name.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--account_id', help='The account id.', required=True)
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
    cfg.account_id = args.account_id
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint

    client = oss_agentic.AgenticBucketClient(cfg)

    # The quota set on an Agent Bucket is the default value applied to bucket spaces
    # created afterwards; it does not change existing bucket spaces.
    result = client.put_agentic_bucket_storage_quota(oss_agentic.models.PutAgenticBucketStorageQuotaRequest(
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
