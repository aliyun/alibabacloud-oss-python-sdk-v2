import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="append file sample")
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
    data2 = b' world. '


    with client.append_file(bucket=args.bucket, key=args.key) as f:
        append_f = f
        f.write(data1)
    print(f'closed: {append_f.closed},'
          f' name: {append_f.name},'
    )

    with client.append_file(bucket=args.bucket, key=args.key) as f:
        append_f = f
        f.write(data2)
    print(f'closed: {append_f.closed},'
          f' name: {append_f.name},'
    )

    result = client.get_object(oss.GetObjectRequest(
        bucket=args.bucket,
        key=args.key,
    ))
    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' content: {  result.body.content},'
    )


if __name__ == "__main__":
    main()
