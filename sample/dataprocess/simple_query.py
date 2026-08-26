import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.dataprocess as oss_dataprocess

parser = argparse.ArgumentParser(description="simple query sample")
parser.add_argument('--region', help='The region of the bucket.', required=True)
parser.add_argument('--endpoint', help='The endpoint of OSS.')
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--dataset-name', help='The name of the dataset.', required=True)
parser.add_argument('--query', help='The JSON query string.', required=True)
parser.add_argument('--sort', help='The field to sort by.')
parser.add_argument('--order', help='The sort order (asc/desc).')

def main():
    args = parser.parse_args()
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint
    client = oss_dataprocess.Client(cfg)

    result = client.simple_query(oss_dataprocess.models.SimpleQueryRequest(
        bucket=args.bucket,
        dataset_name=args.dataset_name,
        query=args.query,
        sort=args.sort,
        order=args.order,
    ))
    print(f'status code: {result.status_code}, request id: {result.request_id}')
    print(f'next token: {result.next_token}')
    if result.files and result.files.file:
        for f in result.files.file:
            print(f'file: filename={f.filename}, uri={f.uri}, size={f.size}')
    if result.aggregations and result.aggregations.aggregation:
        for agg in result.aggregations.aggregation:
            print(f'aggregation: field={agg.field}, operation={agg.operation}, groups={agg.groups}')

if __name__ == "__main__":
    main()
