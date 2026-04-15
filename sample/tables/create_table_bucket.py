import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.tables as oss_tables

parser = argparse.ArgumentParser(description="create table bucket sample")
parser.add_argument('--region', help='The region in which the table bucket is located.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS Tables.')
parser.add_argument('--name', help='The name of the table bucket.', required=True)
parser.add_argument('--sse-algorithm', help='The server-side encryption algorithm.')
parser.add_argument('--kms-key-arn', help='The KMS key ARN for encryption.')

def main():
    args = parser.parse_args()

    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint

    client = oss_tables.Client(cfg)

    encryption_configuration = None
    if args.sse_algorithm is not None or args.kms_key_arn is not None:
        encryption_configuration = oss_tables.models.EncryptionConfiguration(
            sse_algorithm=args.sse_algorithm,
            kms_key_arn=args.kms_key_arn,
        )

    result = client.create_table_bucket(oss_tables.models.CreateTableBucketRequest(
        name=args.name,
        encryption_configuration=encryption_configuration,
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' arn: {result.arn}')


if __name__ == "__main__":
    main()
