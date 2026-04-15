import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.tables as oss_tables

parser = argparse.ArgumentParser(description="get table policy sample")
parser.add_argument('--region', help='The region in which the table bucket is located.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS Tables.')
parser.add_argument('--table-bucket-arn', help='The ARN of the table bucket.', required=True)
parser.add_argument('--namespace', help='The namespace of the table.', required=True)
parser.add_argument('--name', help='The name of the table.', required=True)

def main():
    args = parser.parse_args()

    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint

    client = oss_tables.Client(cfg)

    result = client.get_table_policy(oss_tables.models.GetTablePolicyRequest(
        table_bucket_arn=args.table_bucket_arn,
        namespace=args.namespace,
        name=args.name,
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' resource policy: {result.resource_policy}')


if __name__ == "__main__":
    main()
