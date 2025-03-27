import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="progress copier sample")
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

    global progress_save_n
    progress_save_n = 0
    def _progress_fn(n, _written, total):
        global progress_save_n
        progress_save_n += n
        rate = int(100 * (float(_written) / float(total)))
        print('\r{0}% '.format(rate))

    copier = client.copier()

    result = copier.copy(oss.CopyObjectRequest(
            bucket=args.bucket,
            key=args.key,
            source_bucket=args.source_bucket,
            source_key=args.source_key,
            progress_fn=_progress_fn,
        ),
        part_size=300 * 1024 * 1024,
        parallel_num=5,
        leave_parts_on_error=True,
    )

    print(vars(result))

if __name__ == "__main__":
    main()

