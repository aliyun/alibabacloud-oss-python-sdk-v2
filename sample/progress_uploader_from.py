import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="progress upload from sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--key', help='The name of the object.', required=True)
parser.add_argument('--file_path', help='The path of Upload file.', required=True)


class UploadProgress:
    def __init__(self):
        self.bytes_transferred = 0

    def __call__(self, increment, written, total):
        self.bytes_transferred += increment
        rate = int(100 * (float(written) / float(total)))
        print(f'\r{rate}% ')


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

    # Create progress tracker
    progress_tracker = UploadProgress()

    with open(file=args.file_path, mode='rb') as f:
        result = up_loader.upload_from(oss.PutObjectRequest(
            bucket=args.bucket,
            key=args.key,
            progress_fn=progress_tracker,
        ), reader=f)

        print(vars(result))

if __name__ == "__main__":
    main()

