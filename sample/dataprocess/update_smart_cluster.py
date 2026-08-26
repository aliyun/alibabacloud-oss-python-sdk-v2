import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.dataprocess as oss_dataprocess

parser = argparse.ArgumentParser(description="update smart cluster sample")
parser.add_argument('--region', help='The region of the bucket.', required=True)
parser.add_argument('--endpoint', help='The endpoint of OSS.')
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--dataset-name', help='The name of the dataset.', required=True)
parser.add_argument('--object-id', help='The object ID of the smart cluster.', required=True)
parser.add_argument('--name', help='The updated name of the smart cluster.')
parser.add_argument('--description', help='The updated description of the smart cluster.')

def main():
    args = parser.parse_args()
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint
    client = oss_dataprocess.Client(cfg)

    result = client.update_smart_cluster(oss_dataprocess.models.UpdateSmartClusterRequest(
        bucket=args.bucket,
        dataset_name=args.dataset_name,
        object_id=args.object_id,
        name=args.name,
        description=args.description,
    ))
    print(f'status code: {result.status_code}, request id: {result.request_id}')

if __name__ == "__main__":
    main()
