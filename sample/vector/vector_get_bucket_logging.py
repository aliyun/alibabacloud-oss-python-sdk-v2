import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.vectors as oss_vectors

parser = argparse.ArgumentParser(description="vector get bucket logging sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--account_id', help='The account id.', required=True)

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

    vector_client = oss_vectors.Client(cfg)

    result = vector_client.get_bucket_logging(oss_vectors.models.GetBucketLoggingRequest(
        bucket=args.bucket,
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          )

    if result.bucket_logging_status:
        print(f'logging enabled: target_bucket={result.bucket_logging_status.logging_enabled.target_bucket}, '
              f'target_prefix={result.bucket_logging_status.logging_enabled.target_prefix}')


if __name__ == "__main__":
    main()
