import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="option object sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--key', help='The name of the object.', required=True)
parser.add_argument('--origin', help='It is used to identify a cross-origin request. By default, this header is left empty.', default='')
parser.add_argument('--access_control_request_method', help='The method to be used in the actual cross-origin request. By default, this header is left empty.', default='')
parser.add_argument('--access_control_request_headers', help='The custom headers to be sent in the actual cross-origin request. By default, this header is left empty.', default='')


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

    result = client.option_object(oss.OptionObjectRequest(
            bucket=args.bucket,
            key=args.key,
            origin=args.origin,
            access_control_request_method=args.access_control_request_method,
            access_control_request_headers=args.access_control_request_headers,
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
            f' access control allow origin: {result.access_control_allow_origin},'
            f' access control allow methods: {result.access_control_allow_methods},'
            f' access control allow headers: {result.access_control_allow_headers},'
            f' access control expose headers: {result.access_control_expose_headers},'
            f' access control max age: {result.access_control_max_age},'
    )


if __name__ == "__main__":
    main()