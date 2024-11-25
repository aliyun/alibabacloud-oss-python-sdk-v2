import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="put bucket logging sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--target_bucket', help='The bucket that stores access logs', required=True)
parser.add_argument('--target_prefix', help='The prefix of the log objects. This parameter can be left empty.', default='')


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

    result = client.put_bucket_logging(oss.PutBucketLoggingRequest(
            bucket=args.bucket,
            bucket_logging_status=oss.BucketLoggingStatus(
                logging_enabled=oss.LoggingEnabled(
                    target_bucket=args.target_bucket,
                    target_prefix=args.target_prefix,
                ),
            ),
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
    )


if __name__ == "__main__":
    main()