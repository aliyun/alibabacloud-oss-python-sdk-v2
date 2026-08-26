import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.agentic as oss_agentic

parser = argparse.ArgumentParser(description="list bucket spaces sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--account_id', help='The account id.', required=True)
parser.add_argument('--prefix', help='The prefix that returned bucket space names must contain.')

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

    # Create the Paginator for the ListBucketSpaces operation
    paginator = client.list_bucket_spaces_paginator()

    # Iterate through the bucket space pages
    for page in paginator.iter_page(oss_agentic.models.ListBucketSpacesRequest(
        bucket=args.bucket,
        prefix=args.prefix,
    )):
        for o in page.bucket_spaces:
            print(f'Bucket Space: {o.name}, {o.location}, {o.storage_class}')

if __name__ == "__main__":
    main()
