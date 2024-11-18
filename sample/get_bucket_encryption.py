import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="get bucket encryption sample")
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

    result = client.get_bucket_encryption(oss.GetBucketEncryptionRequest(
            bucket=args.bucket,
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
            f' kms master key id: {result.server_side_encryption_rule.apply_server_side_encryption_by_default.kms_master_key_id},'
            f' kms data encryption: {result.server_side_encryption_rule.apply_server_side_encryption_by_default.kms_data_encryption},'
            f' sse algorithm: {result.server_side_encryption_rule.apply_server_side_encryption_by_default.sse_algorithm},'
    )


if __name__ == "__main__":
    main()