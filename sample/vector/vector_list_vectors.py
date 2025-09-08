import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.vectors as oss_vectors

parser = argparse.ArgumentParser(description="list vectors sample")

parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--account_id', help='The account id.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--iindex_name', help='The name of the vector index.', required=True)

def main():

    args = parser.parse_args()

    # Loading credentials values from the environment variables
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    # Using the SDK's default configuration
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    cfg.account_id = args.account_id
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint

    client = oss_vectors.Client(cfg)

    # Create the Paginator for the ListVectors operation
    paginator = client.list_vectors_paginator()

    # Create request with bucket and index name
    request = oss_vectors.models.ListVectorsRequest(
        bucket=args.bucket,
        index_name=args.index_name
    )

    # Iterate through the vectors pages
    for page in paginator.iter_page(request):
        for o in page.vectors:
            print(f'Vector Key: {o.get("key")}')

if __name__ == "__main__":
    main()
