import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="list buckets sample")

parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')


def main():

    args = parser.parse_args()

    # Loading credentials values from the environment variables
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    # Using the SDK's default configuration
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint

    client = oss.Client(cfg)

    # Create the Paginator for the ListBuckets operation
    paginator = client.list_buckets_paginator()

    # Iterate through the bucket pages
    for page in paginator.iter_page(oss.ListBucketsRequest(
        )
    ):
        for o in page.buckets:
            print(f'Bucket: {o.name}, {o.location}, {o.creation_date} {o.resource_group_id}')


    # Example with all available parameters configured:
    # paginator = client.list_buckets_paginator()
    # for page in paginator.iter_page(oss.ListBucketsRequest(
    #     marker='example-marker',              # marker: Sets the starting point for returning results. If not set, results start from the beginning.
    #     max_keys=100,                         # max-keys: Specifies the maximum number of buckets to return. Range: 1-1000. Default: 100
    #     prefix='example-prefix',              # prefix: Limits results to bucket names that start with the specified prefix. No filtering if not set.
    #     resource_group_id='rg-xxxxxx',        # x-oss-resource-group-id: The ID of the resource group to which the bucket belongs
    #     tag_key='environment',                # tag-key: Filters results to buckets with the specified tag key
    #     tag_value='production',               # tag-value: Filters results to buckets with the specified tag value. Must be used with tag_key
    #     tagging='owner:finance'               # tagging: Filters results to buckets matching all specified tag key-value pairs. Cannot be used with tag-key/tag-value
    # )): 
    #     for o in page.buckets:
    #         print(f'Bucket with params: {o.name}, {o.location}, {o.creation_date} {o.resource_group_id}')

if __name__ == "__main__":
    main()