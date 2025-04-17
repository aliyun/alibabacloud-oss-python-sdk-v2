import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="upload from sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--src_key', help='The name of the object.', required=True)
parser.add_argument('--dst_key', help='The name of the object.', required=True)

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

    up_loader = client.uploader()

    # up_loader = client.uploader(part_size=100*1024,
    #                                 parallel_num=5,
    #                                 leave_parts_on_error=True,
    #                                 enable_checkpoint=True,
    #                                 checkpoint_dir=args.file_path)
    #  
    with client.open_file(
        bucket=args.bucket,
        key=args.src_key, 
        enable_prefetch=True,
        #prefetch_num=3, 
        #chunk_size=6*1024*1024, 
        prefetch_threshold = 0) as f:

        # set seekable to False to read source sequentially
        f._seekable = False
        
        result = up_loader.upload_from(oss.PutObjectRequest(
            bucket=args.bucket,
            key=args.dst_key,
        ), reader=f)

        print(f'status code: {result.status_code},'
              f' request id: {result.request_id},'
              f' content md5: {result.headers.get("Content-MD5")},'
              f' etag: {result.etag},'
              f' hash crc64: {result.hash_crc64},'
              f' version id: {result.version_id},'
              f' server time: {result.headers.get("x-oss-server-time")},'
              )

if __name__ == "__main__":
    main()

