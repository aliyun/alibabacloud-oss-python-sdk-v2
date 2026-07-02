import asyncio
import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.aio as oss_aio

parser = argparse.ArgumentParser(description="list object versions paginator sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
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

    # Create the Paginator for the ListObjectVersions operation
    paginator = client.list_object_versions_paginator()

    # Iterate through the object version pages
    async for page in paginator.iter_page(oss.ListObjectVersionsRequest(
            bucket=args.bucket
        )
    ):
        if page.version:
            for v in page.version:
                print(f'Version: {v.key}, {v.version_id}, {v.size}, {v.last_modified}')
        if page.delete_marker:
            for d in page.delete_marker:
                print(f'DeleteMarker: {d.key}, {d.version_id}, {d.last_modified}')

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
