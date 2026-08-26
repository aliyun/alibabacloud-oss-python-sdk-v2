import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.dataprocess as oss_dataprocess

parser = argparse.ArgumentParser(description="list smart clusters sample")
parser.add_argument('--region', help='The region of the bucket.', required=True)
parser.add_argument('--endpoint', help='The endpoint of OSS.')
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--dataset-name', help='The name of the dataset.', required=True)
parser.add_argument('--max-results', type=int, help='The maximum number of smart clusters to return.')
parser.add_argument('--next-token', help='The next token for pagination.')
parser.add_argument('--cluster-type', help='The type of the smart cluster to filter.')

def main():
    args = parser.parse_args()
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint
    client = oss_dataprocess.Client(cfg)

    result = client.list_smart_clusters(oss_dataprocess.models.ListSmartClustersRequest(
        bucket=args.bucket,
        dataset_name=args.dataset_name,
        max_results=args.max_results,
        next_token=args.next_token,
        cluster_type=args.cluster_type,
    ))
    print(f'status code: {result.status_code}, request id: {result.request_id}, next token: {result.next_token}')
    if result.smart_clusters and result.smart_clusters.smart_cluster:
        for i, sc in enumerate(result.smart_clusters.smart_cluster):
            print(f'smart cluster {i + 1}: object id={sc.object_id}, name={sc.name}, cluster type={sc.cluster_type}')

if __name__ == "__main__":
    main()
