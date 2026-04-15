import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.tables as oss_tables

parser = argparse.ArgumentParser(description="list tables sample")
parser.add_argument('--region', help='The region in which the table bucket is located.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS Tables.')
parser.add_argument('--table-bucket-arn', help='The ARN of the table bucket.', required=True)
parser.add_argument('--namespace', help='The namespace of the tables.', required=True)
parser.add_argument('--prefix', help='The prefix to filter tables.')
parser.add_argument('--max-tables', type=int, help='The maximum number of tables to return.')

def main():
    args = parser.parse_args()

    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint

    client = oss_tables.Client(cfg)

    result = client.list_tables(oss_tables.models.ListTablesRequest(
        table_bucket_arn=args.table_bucket_arn,
        namespace=args.namespace,
        prefix=args.prefix,
        max_tables=args.max_tables,
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' continuation token: {result.continuation_token}')

    if result.table_summaries:
        for i, table in enumerate(result.table_summaries):
            print(f'table {i + 1}:'
                  f' name: {table.name},'
                  f' namespace: {table.namespace},'
                  f' type: {table.type},'
                  f' table arn: {table.table_arn},'
                  f' created at: {table.created_at},'
                  f' modified at: {table.modified_at}')


if __name__ == "__main__":
    main()
