import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.tables as oss_tables

parser = argparse.ArgumentParser(description="get table bucket encryption sample")
parser.add_argument('--region', help='The region in which the table bucket is located.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS Tables.')
parser.add_argument('--table-bucket-arn', help='The ARN of the table bucket.', required=True)

def main():
    args = parser.parse_args()

    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint

    client = oss_tables.Client(cfg)

    result = client.get_table_bucket_encryption(oss_tables.models.GetTableBucketEncryptionRequest(
        table_bucket_arn=args.table_bucket_arn,
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id}')

    if result.encryption_configuration:
        print(f'sse algorithm: {result.encryption_configuration.sse_algorithm},'
              f' kms key arn: {result.encryption_configuration.kms_key_arn}')


if __name__ == "__main__":
    main()
