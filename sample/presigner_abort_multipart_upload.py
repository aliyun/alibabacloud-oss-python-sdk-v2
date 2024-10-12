import argparse
import requests
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="presign abort multipart upload sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--key', help='The name of the object.', required=True)
parser.add_argument('--upload_id', help='The ID of the multipart upload task.', required=True)


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


    abort_result = client.presign(oss.AbortMultipartUploadRequest(
        bucket=args.bucket,
        key=args.key,
        upload_id=args.upload_id,
    ))

    with requests.delete(abort_result.url, headers=abort_result.signed_headers) as result:
        print(f'status code: {result.status_code},'
              f' request id: {result.headers.get("x-oss-request-id")},'
              )

if __name__ == "__main__":
    main()