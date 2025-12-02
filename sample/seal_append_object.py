import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="seal append object sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--key', help='The name of the object.', required=True)
parser.add_argument('--position', type=int, help='The position to seal the object.', required=True)


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

    # Seal the appendable object
    result = client.seal_append_object(oss.SealAppendObjectRequest(
        bucket=args.bucket,
        key=args.key,
        position=args.position,
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' sealed time: {result.sealed_time}'
    )


if __name__ == "__main__":
    main()