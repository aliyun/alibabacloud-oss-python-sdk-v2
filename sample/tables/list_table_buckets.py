import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.tables as oss_tables

parser = argparse.ArgumentParser(description="list table buckets sample")
parser.add_argument('--region', help='The region in which the table buckets are located.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS Tables.')
parser.add_argument('--prefix', help='The prefix used to filter the table buckets.')
parser.add_argument('--max-buckets', help='The maximum number of buckets to return.', type=int)

def main():
    args = parser.parse_args()

    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint

    client = oss_tables.Client(cfg)

    result = client.list_table_buckets(oss_tables.models.ListTableBucketsRequest(
        prefix=args.prefix,
        max_buckets=args.max_buckets,
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' continuation token: {result.continuation_token}')

    if result.table_buckets:
        for i, bucket in enumerate(result.table_buckets):
            print(f'bucket {i + 1}:'
                  f' arn: {bucket.arn},'
                  f' name: {bucket.name},'
                  f' id: {bucket.table_bucket_id},'
                  f' owner account id: {bucket.owner_account_id},'
                  f' created at: {bucket.created_at}')


if __name__ == "__main__":
    main()
