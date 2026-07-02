import asyncio
import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.aio as oss_aio

parser = argparse.ArgumentParser(description="list multipart uploads paginator sample")
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

    # Create the Paginator for the ListMultipartUploads operation
    paginator = client.list_multipart_uploads_paginator()

    # Iterate through the multipart upload pages
    async for page in paginator.iter_page(oss.ListMultipartUploadsRequest(
            bucket=args.bucket
        )
    ):
        if page.uploads:
            for u in page.uploads:
                print(f'MultipartUpload: {u.key}, {u.upload_id}, {u.initiated}')

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
