import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.dataprocess as oss_dataprocess

parser = argparse.ArgumentParser(description="get dataset sample")
parser.add_argument('--region', help='The region of the bucket.', required=True)
parser.add_argument('--endpoint', help='The endpoint of OSS.')
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--dataset-name', help='The name of the dataset.', required=True)

def main():
    args = parser.parse_args()
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint
    client = oss_dataprocess.Client(cfg)

    result = client.get_dataset(oss_dataprocess.models.GetDatasetRequest(
        bucket=args.bucket,
        dataset_name=args.dataset_name,
    ))
    print(f'status code: {result.status_code}, request id: {result.request_id}')
    if result.dataset:
        d = result.dataset
        print(f'dataset name: {d.dataset_name}, description: {d.description}, file count: {d.file_count}')

if __name__ == "__main__":
    main()
