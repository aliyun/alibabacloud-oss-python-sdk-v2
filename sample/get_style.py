import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="get style sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--style_name', help='The name of the image style.', required=True)


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

    result = client.get_style(oss.GetStyleRequest(
            bucket=args.bucket,
            style_name=args.style_name,
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
            f' name: {result.style.name},'
            f' content: {result.style.content},'
            f' create time: {result.style.create_time},'
            f' last modify time: {result.style.last_modify_time},'
            f' category: {result.style.category},'
    )


if __name__ == "__main__":
    main()