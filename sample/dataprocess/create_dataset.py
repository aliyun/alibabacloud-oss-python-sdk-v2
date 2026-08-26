import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.dataprocess as oss_dataprocess

parser = argparse.ArgumentParser(description="create dataset sample")
parser.add_argument('--region', help='The region of the bucket.', required=True)
parser.add_argument('--endpoint', help='The endpoint of OSS.')
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--dataset-name', help='The name of the dataset.', required=True)
parser.add_argument('--description', help='The description of the dataset.')

def main():
    args = parser.parse_args()
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint
    client = oss_dataprocess.Client(cfg)

    result = client.create_dataset(oss_dataprocess.models.CreateDatasetRequest(
        bucket=args.bucket,
        dataset_name=args.dataset_name,
        description=args.description,
    ))
    print(f'status code: {result.status_code}, request id: {result.request_id}')
    if result.dataset:
        print(f'dataset name: {result.dataset.dataset_name}')

if __name__ == "__main__":
    main()
