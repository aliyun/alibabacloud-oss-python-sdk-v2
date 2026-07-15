import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.agentic as oss_agentic

parser = argparse.ArgumentParser(description="list agentic buckets sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--account_id', help='The account id.', required=True)

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

    client = oss_agentic.AgenticBucketClient(cfg)

    # Create the Paginator for the ListAgenticBuckets operation
    paginator = client.list_agentic_buckets_paginator()

    # Iterate through the agentic bucket pages
    for page in paginator.iter_page(oss_agentic.models.ListAgenticBucketsRequest()):
        for o in page.agentic_buckets:
            print(f'Agentic Bucket: {o.name}, {o.storage_class}')

if __name__ == "__main__":
    main()
