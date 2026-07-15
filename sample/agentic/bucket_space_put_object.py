import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.agentic as oss_agentic

parser = argparse.ArgumentParser(description="bucket space put object sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The bucket space prefix name.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--account_id', help='The account id.', required=True)
parser.add_argument('--key', help='The name of the object.', required=True)

def main():
    args = parser.parse_args()

    # Loading credentials values from the environment variables
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    # Using the SDK's default configuration
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    cfg.account_id = args.account_id
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint

    # The BucketSpace client resolves the bucket prefix to a full bucket space
    # name and reuses the standard OSS bucket/object operations.
    client = oss_agentic.BucketSpaceClient.create(cfg)

    result = client.put_object(oss.models.PutObjectRequest(
        bucket=args.bucket,
        key=args.key,
        body=b'hello agentic bucket space',
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' etag: {result.etag},'
          )

if __name__ == "__main__":
    main()
