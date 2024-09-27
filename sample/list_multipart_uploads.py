import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="list multipart uploads sample")

parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
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

    # Create the Paginator for the ListMultipartUploads operation
    paginator = client.list_multipart_uploads_paginator()

    # Iterate through the multipart upload pages
    for page in paginator.iter_page(oss.ListMultipartUploadsRequest(
            bucket=args.bucket
        )
    ):
        for o in page.uploads:
            print(f'Multipart Upload: {o.key}, {o.upload_id}')

if __name__ == "__main__":
    main()
