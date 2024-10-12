import argparse
import requests
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="presign head object sample")
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

    pre_result = client.presign(oss.HeadObjectRequest(
        bucket=args.bucket,
        key=args.key,
    ))

    with requests.head(pre_result.url) as resp:
        print(f'status code: {resp.status_code},'
              f' request id: {resp.headers.get("x-oss-request-id")},'
              f' hash crc64: {resp.headers.get("x-oss-hash-crc64ecma")},'
              f' content md5: {resp.headers.get("Content-MD5")},'
              f' etag: {resp.headers.get("ETag")},'
              f' content length: {resp.headers.get("content-length")},'
              f' content type: {resp.headers.get("Content-Type")},'
              f' object type: {resp.headers.get("x-oss-object-type")},'
              f' storage class: {resp.headers.get("x-oss-storage-class")},'
              f' last modified: {resp.headers.get("Last-Modified")},'
              f' last access time: {resp.headers.get("x-oss-last-access-time")},'
              f' server time: {resp.headers.get("x-oss-server-time")},'
              )

    print(f'method: {pre_result.method},'
          f' expiration: {pre_result.expiration.strftime("%Y-%m-%dT%H:%M:%S.000Z")},'
          f' url: {pre_result.url}'
    )

    for key, value in pre_result.signed_headers.items():
        print(f'signed headers key: {key}, signed headers value: {value}')

if __name__ == "__main__":
    main()
