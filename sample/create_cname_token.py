import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="create cname token sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--domain', help='The custom domain name.', required=True)


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

    result = client.create_cname_token(oss.CreateCnameTokenRequest(
            bucket=args.bucket,
            bucket_cname_configuration=oss.BucketCnameConfiguration(
                cname=oss.Cname(
                    domain=args.domain,
                ),
            ),
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
            f' cname: {result.cname_token.cname},'
            f' token: {result.cname_token.token},'
            f' expire time: {result.cname_token.expire_time},'
            f' bucket: {result.cname_token.bucket},'
    )

if __name__ == "__main__":
    main()