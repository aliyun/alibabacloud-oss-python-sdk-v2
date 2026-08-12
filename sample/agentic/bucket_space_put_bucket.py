import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.agentic as oss_agentic

parser = argparse.ArgumentParser(description="bucket space put bucket sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The bucket space prefix name.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--account_id', help='The account id.', required=True)
parser.add_argument('--agentic_bucket', help='The agentic bucket that the bucket space belongs to.', required=True)

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

    # The BucketSpace client resolves the bucket prefix to a full bucket space
    # name and reuses the standard OSS bucket/object operations.
    client = oss_agentic.BucketSpaceClient.create(cfg)

    # The bucket space must be created under an agentic bucket, identified by its
    # full name '{bucket}-{account_id}-{region}-ab-apsr'.
    result = client.put_bucket(oss.models.PutBucketRequest(
        bucket=args.bucket,
        agentic_bucket=f'{args.agentic_bucket}-{args.account_id}-{args.region}-ab-apsr',
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          )

if __name__ == "__main__":
    main()
