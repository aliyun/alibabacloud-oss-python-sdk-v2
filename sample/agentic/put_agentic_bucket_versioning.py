import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.agentic as oss_agentic
from alibabacloud_oss_v2.models.bucket_basic import VersioningConfiguration

parser = argparse.ArgumentParser(description="put agentic bucket versioning sample")
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

    result = client.put_agentic_bucket_versioning(oss_agentic.models.PutAgenticBucketVersioningRequest(
        bucket=args.bucket,
        versioning_configuration=VersioningConfiguration(status='Enabled'),
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          )

if __name__ == "__main__":
    main()
