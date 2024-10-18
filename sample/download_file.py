import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="download file sample")
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

    down_loader = client.downloader()

    # down_loader = client.downloader(part_size=100*1024,
    #                                 parallel_num=5,
    #                                 block_size=1024,
    #                                 use_temp_file=True,
    #                                 enable_checkpoint=True,
    #                                 checkpoint_dir=args.file_path,
    #                                 verify_data=True)

    result = down_loader.download_file(oss.GetObjectRequest(
        bucket=args.bucket,
        key=args.key,
    ), filepath=args.file_path)

    print(f'written: {result.written}')



if __name__ == "__main__":
    main()

