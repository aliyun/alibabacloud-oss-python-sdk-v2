import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.tables as oss_tables

parser = argparse.ArgumentParser(description="list namespaces sample")
parser.add_argument('--region', help='The region in which the table bucket is located.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS Tables.')
parser.add_argument('--table-bucket-arn', help='The ARN of the table bucket.', required=True)
parser.add_argument('--prefix', help='The prefix to filter namespaces.')
parser.add_argument('--max-namespaces', type=int, help='The maximum number of namespaces to return.')

def main():
    args = parser.parse_args()

    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint

    client = oss_tables.Client(cfg)

    result = client.list_namespaces(oss_tables.models.ListNamespacesRequest(
        table_bucket_arn=args.table_bucket_arn,
        prefix=args.prefix,
        max_namespaces=args.max_namespaces,
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' continuation token: {result.continuation_token}')

    if result.namespaces:
        for i, ns in enumerate(result.namespaces):
            print(f'namespace {i + 1}:'
                  f' namespace: {ns.namespace},'
                  f' namespace id: {ns.namespace_id},'
                  f' owner account id: {ns.owner_account_id},'
                  f' created at: {ns.created_at},'
                  f' created by: {ns.created_by}')


if __name__ == "__main__":
    main()
