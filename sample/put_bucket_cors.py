import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="put bucket cors sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--response_vary', help='Indicates whether the Vary: Origin header was returned. Default value: false', default='false')


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

    result = client.put_bucket_cors(oss.PutBucketCorsRequest(
            bucket=args.bucket,
            cors_configuration=oss.CORSConfiguration(
                cors_rules=[oss.CORSRule(
                    allowed_origins=['*'],
                    allowed_methods=['GET', 'HEAD'],
                    allowed_headers=['GET'],
                    expose_headers=['x-oss-test', 'x-oss-test1'],
                    max_age_seconds=33012,
                ), oss.CORSRule(
                    allowed_origins=['http://www.example.com'],
                    allowed_methods=['PUT', 'POST'],
                    allowed_headers=['*'],
                    expose_headers=['x-oss-test2', 'x-oss-test3'],
                    max_age_seconds=33012,
                )],
                response_vary=args.response_vary,
            ),
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
    )


if __name__ == "__main__":
    main()