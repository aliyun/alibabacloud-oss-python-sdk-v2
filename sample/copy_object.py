import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="copy object sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--key', help='The name of the object.', required=True)
parser.add_argument('--source_key', help='The name of the source address for object.', required=True)
parser.add_argument('--source_bucket', help='The name of the source address for bucket.', required=True)


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

    result = client.copy_object(oss.CopyObjectRequest(
        bucket=args.bucket,
        key=args.key,
        source_key=args.source_key,
        source_bucket=args.source_bucket,
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' version id: {result.version_id},' 
          f' hash crc64: {result.hash_crc64},' 
          f' source version id: {result.source_version_id},' 
          f' server side encryption: {result.server_side_encryption},' 
          f' server side data encryption: {result.server_side_data_encryption},' 
          f' server side encryption key id: {result.server_side_encryption_key_id},' 
          f' last modified: {result.last_modified},' 
          f' etag: {result.etag},'
    )

if __name__ == "__main__":
    main()

