import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="append object sample")
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

    data1 = b'hello'
    data2 = b' world'

    result = client.append_object(oss.AppendObjectRequest(
        bucket=args.bucket,
        key=args.key,
        position=0,
        body=data1,
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' version id: {result.version_id},' 
          f' hash crc64: {result.hash_crc64},' 
          f' next position: {result.next_position},' 
          f' server side encryption: {result.server_side_encryption},' 
          f' server side data encryption: {result.server_side_data_encryption},' 
          f' sse kms key id: {result.server_side_encryption_key_id},'
    )

    result = client.append_object(oss.AppendObjectRequest(
        bucket=args.bucket,
        key=args.key,
        position=result.next_position,
        body=data2,
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' version id: {result.version_id},' 
          f' hash crc64: {result.hash_crc64},' 
          f' next position: {result.next_position},' 
          f' server side encryption: {result.server_side_encryption},' 
          f' server side data encryption: {result.server_side_data_encryption},' 
          f' sse kms key id: {result.server_side_encryption_key_id},'
    )

if __name__ == "__main__":
    main()
