import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.agentic as oss_agentic

parser = argparse.ArgumentParser(description="put agentic bucket policy sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--account_id', help='The account id.', required=True)

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

    client = oss_agentic.AgenticBucketClient(cfg)

    policy = (
        '{"Version":"1","Statement":[{"Effect":"Allow",'
        '"Action":["oss:GetObject"],"Principal":["*"],'
        f'"Resource":["acs:oss:*:{args.account_id}:*"]}}]}}'
    )

    result = client.put_agentic_bucket_policy(oss_agentic.models.PutAgenticBucketPolicyRequest(
        bucket=args.bucket,
        body=policy.encode(),
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          )

if __name__ == "__main__":
    main()
