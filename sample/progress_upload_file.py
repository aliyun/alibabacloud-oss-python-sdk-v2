import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="progress upload file sample")
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

    up_loader = client.uploader(part_size=100*1024,
                                    parallel_num=5,
                                    leave_parts_on_error=True,
                                    enable_checkpoint=True,
                                )

    global progress_save_n
    progress_save_n = 0
    def _progress_fn(n, _written, total):
        global progress_save_n
        progress_save_n += n
        rate = int(100 * (float(_written) / float(total)))
        print('\r{0}% '.format(rate))

    result = up_loader.upload_file(oss.PutObjectRequest(
        bucket=args.bucket,
        key=args.key,
        progress_fn=_progress_fn,
    ), filepath=args.file_path)

    print(vars(result))



if __name__ == "__main__":
    main()

