import asyncio
import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.aio as oss_aio

parser = argparse.ArgumentParser(description="list buckets paginator sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')


async def main():

    args = parser.parse_args()

    # Loading credentials values from the environment variables
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    # Using the SDK's default configuration
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint

    client = oss_aio.AsyncClient(cfg)

    # Create the Paginator for the ListBuckets operation
    paginator = client.list_buckets_paginator()

    # Iterate through the bucket pages
    async for page in paginator.iter_page(oss.ListBucketsRequest()):
        if page.buckets:
            for b in page.buckets:
                print(f'Bucket: {b.name}, {b.location}, {b.creation_date}')

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
