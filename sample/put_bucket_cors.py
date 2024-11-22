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
                    allowed_origins=['$WK5+C/suC', 'fjFyF^a%TV'],
                    allowed_methods=['GET', 'HEAD'],
                    allowed_headers=['SGJ|4n_Ujl', ':uApl!EGv@'],
                    expose_headers=['n@_1\Spz#5', 'f xq)N)O;E'],
                    max_age_seconds=100,
                ), oss.CORSRule(
                    allowed_origins=['/b:*pr@:E:', 'u@,6)ZG1gF'],
                    allowed_methods=['PUT', 'POST'],
                    allowed_headers=['.Cbae&pq_/', 'wF>2+g4m%1'],
                    expose_headers=['d7+_+s8++h', 'hOD$BB:/Fq'],
                    max_age_seconds=200,
                )],
                response_vary=args.response_vary,
            ),
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
    )


if __name__ == "__main__":
    main()