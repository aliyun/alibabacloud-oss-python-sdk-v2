import argparse
import requests
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="presign put object sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--key', help='The name of the object.', required=True)


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

    data = b'hello world'

    pre_result = client.presign(oss.PutObjectRequest(
        bucket=args.bucket,
        key=args.key,
        content_type='text/txt'
    ))


    with requests.put(pre_result.url, headers=pre_result.signed_headers, data=data) as resp:
        print(f'status code: {resp.status_code},'
              f' request id: {resp.headers.get("x-oss-request-id")},'
              f' hash crc64: {resp.headers.get("x-oss-hash-crc64ecma")},'
              f' content md5: {resp.headers.get("Content-MD5")},'
              f' server time: {resp.headers.get("x-oss-server-time")},'
        )


if __name__ == "__main__":
    main()
