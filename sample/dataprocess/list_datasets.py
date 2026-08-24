import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.dataprocess as oss_dataprocess

parser = argparse.ArgumentParser(description="list datasets sample")
parser.add_argument('--region', help='The region of the bucket.', required=True)
parser.add_argument('--endpoint', help='The endpoint of OSS.')
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--max-results', type=int, help='The maximum number of datasets to return.')
parser.add_argument('--prefix', help='The prefix to filter datasets.')
parser.add_argument('--next-token', help='The next token for pagination.')

def main():
    args = parser.parse_args()
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint
    client = oss_dataprocess.Client(cfg)

    result = client.list_datasets(oss_dataprocess.models.ListDatasetsRequest(
        bucket=args.bucket,
        max_results=args.max_results,
        prefix=args.prefix,
        next_token=args.next_token,
    ))
    print(f'status code: {result.status_code}, request id: {result.request_id}, next token: {result.next_token}')
    if result.datasets and result.datasets.dataset:
        for i, d in enumerate(result.datasets.dataset):
            print(f'dataset {i + 1}: name: {d.dataset_name}, description: {d.description}')

if __name__ == "__main__":
    main()
