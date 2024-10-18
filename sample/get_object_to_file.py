import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="get object to file sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--key', help='The name of the object.', required=True)
parser.add_argument('--file_path', help='The path of Upload file.', required=True)


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


    result = client.get_object_to_file(oss.GetObjectRequest(
        bucket=args.bucket,
        key=args.key
    ), args.file_path)


    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' content length: {result.content_length},' 
          f' content range: {result.content_range},' 
          f' content type: {result.content_type},' 
          f' etag: {result.etag},' 
          f' last modified: {result.last_modified},' 
          f' content md5: {result.content_md5},' 
          f' cache control: {result.cache_control},' 
          f' content disposition: {result.content_disposition},' 
          f' content encoding: {result.content_encoding},' 
          f' expires: {result.expires},' 
          f' hash crc64: {result.hash_crc64},' 
          f' storage class: {result.storage_class},' 
          f' object type: {result.object_type},' 
          f' version id: {result.version_id},' 
          f' tagging count: {result.tagging_count},' 
          f' server side encryption: {result.server_side_encryption},' 
          f' server side data encryption: {result.server_side_data_encryption},' 
          f' sse kms key id: {result.sse_kms_key_id},' 
          f' next append position: {result.next_append_position},' 
          f' expiration: {result.expiration},' 
          f' restore: {result.restore},' 
          f' process status: {result.process_status},' 
          f' delete marker: {result.delete_marker},'
          f' server time: {result.headers.get("x-oss-server-time")},'
    )



if __name__ == "__main__":
    main()
