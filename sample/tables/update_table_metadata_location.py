import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.tables as oss_tables

parser = argparse.ArgumentParser(description="update table metadata location sample")
parser.add_argument('--region', help='The region in which the table bucket is located.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS Tables.')
parser.add_argument('--table-bucket-arn', help='The ARN of the table bucket.', required=True)
parser.add_argument('--namespace', help='The namespace of the table.', required=True)
parser.add_argument('--name', help='The name of the table.', required=True)
parser.add_argument('--version-token', help='The version token.', required=True)
parser.add_argument('--metadata-location', help='The new metadata location.', required=True)

def main():
    args = parser.parse_args()

    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint

    client = oss_tables.Client(cfg)

    result = client.update_table_metadata_location(
        oss_tables.models.UpdateTableMetadataLocationRequest(
            table_bucket_arn=args.table_bucket_arn,
            namespace=args.namespace,
            name=args.name,
            version_token=args.version_token,
            metadata_location=args.metadata_location,
        )
    )

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' name: {result.name},'
          f' version token: {result.version_token},'
          f' metadata location: {result.metadata_location},'
          f' table arn: {result.table_arn}')


if __name__ == "__main__":
    main()
