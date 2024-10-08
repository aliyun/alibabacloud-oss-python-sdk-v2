import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="get object meta sample")
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

    result = client.get_object_meta(oss.GetObjectMetaRequest(
        bucket=args.bucket,
        key=args.key,
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' content length: {result.content_length},' 
          f' etag: {result.etag},' 
          f' last modified: {result.last_modified},' 
          f' last access time: {result.last_access_time},' 
          f' version id: {result.version_id},' 
          f' hash crc64: {result.hash_crc64},'
    )

if __name__ == "__main__":
    main()

