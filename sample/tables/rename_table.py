import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.tables as oss_tables

parser = argparse.ArgumentParser(description="rename table sample")
parser.add_argument('--region', help='The region in which the table bucket is located.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS Tables.')
parser.add_argument('--table-bucket-arn', help='The ARN of the table bucket.', required=True)
parser.add_argument('--namespace', help='The namespace of the table.', required=True)
parser.add_argument('--name', help='The current name of the table.', required=True)
parser.add_argument('--new-namespace-name', help='The new namespace name for the table.')
parser.add_argument('--new-name', help='The new name for the table.')
parser.add_argument('--version-token', help='The version token for the table.')

def main():
    args = parser.parse_args()

    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint

    client = oss_tables.Client(cfg)

    result = client.rename_table(oss_tables.models.RenameTableRequest(
        table_bucket_arn=args.table_bucket_arn,
        namespace=args.namespace,
        name=args.name,
        new_namespace_name=args.new_namespace_name,
        new_name=args.new_name,
        version_token=args.version_token,
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id}')
    print(f'successfully renamed table: {args.namespace}/{args.name}')


if __name__ == "__main__":
    main()
