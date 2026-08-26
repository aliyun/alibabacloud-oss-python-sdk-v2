import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.dataprocess as oss_dataprocess

parser = argparse.ArgumentParser(description="get smart cluster sample")
parser.add_argument('--region', help='The region of the bucket.', required=True)
parser.add_argument('--endpoint', help='The endpoint of OSS.')
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--dataset-name', help='The name of the dataset.', required=True)
parser.add_argument('--object-id', help='The object ID of the smart cluster.', required=True)

def main():
    args = parser.parse_args()
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint
    client = oss_dataprocess.Client(cfg)

    result = client.get_smart_cluster(oss_dataprocess.models.GetSmartClusterRequest(
        bucket=args.bucket,
        dataset_name=args.dataset_name,
        object_id=args.object_id,
    ))
    print(f'status code: {result.status_code}, request id: {result.request_id}')
    if result.smart_cluster:
        sc = result.smart_cluster
        print(f'smart cluster: object id={sc.object_id}, name={sc.name}, description={sc.description}, cluster type={sc.cluster_type}')

if __name__ == "__main__":
    main()
