import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.vectors as oss_vectors

parser = argparse.ArgumentParser(description="list vector indexes sample")

parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--uid', help='The user id.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)

def main():

    args = parser.parse_args()

    # Loading credentials values from the environment variables
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    # Using the SDK's default configuration
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    cfg.user_id = args.uid
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint

    client = oss_vectors.Client(cfg)

    # Create the Paginator for the ListVectorIndex operation
    paginator = client.list_vector_index_paginator()

    # Iterate through the vector index pages
    for page in paginator.iter_page(oss_vectors.models.ListVectorsIndexRequest(
        bucket=args.bucket
        )
    ):
        for o in page.indexes:
            print(f'Index: {o.get("indexName")}, {o.get("dataType")}, {o.get("dimension")}, {o.get("status")}')

if __name__ == "__main__":
    main()
