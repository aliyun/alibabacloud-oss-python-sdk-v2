import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.dataprocess as oss_dataprocess

parser = argparse.ArgumentParser(description="semantic query sample")
parser.add_argument('--region', help='The region of the bucket.', required=True)
parser.add_argument('--endpoint', help='The endpoint of OSS.')
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--dataset-name', help='The name of the dataset.', required=True)
parser.add_argument('--query', help='The semantic query text.', required=True)
parser.add_argument('--max-results', type=int, help='The maximum number of results to return.')

def main():
    args = parser.parse_args()
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint
    client = oss_dataprocess.Client(cfg)

    result = client.semantic_query(oss_dataprocess.models.SemanticQueryRequest(
        bucket=args.bucket,
        dataset_name=args.dataset_name,
        query=args.query,
        max_results=args.max_results,
    ))
    print(f'status code: {result.status_code}, request id: {result.request_id}')
    if result.files and result.files.file:
        for f in result.files.file:
            print(f'file: filename={f.filename}, uri={f.uri}, media type={f.media_type}')

if __name__ == "__main__":
    main()
