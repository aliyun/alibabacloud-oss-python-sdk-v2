import argparse
import alibabacloud_oss_v2 as oss
from datetime import datetime, timedelta, timezone

parser = argparse.ArgumentParser(description="put object retention sample")
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

    # Calculate retain until date (1 days from now) in ISO 8601 format
    # Use UTC time (recommended for OSS)
    retain_until_date = datetime.now(timezone.utc) + timedelta(days=1)
    retain_until_iso = retain_until_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')


    # Create retention configuration
    retention_config = oss.Retention(
        mode=oss.ObjectRetentionModeType.COMPLIANCE,
        retain_until_date=retain_until_iso,
    )

    # Set object retention
    result = client.put_object_retention(oss.PutObjectRetentionRequest(
        bucket=args.bucket,
        key=args.key,
        retention=retention_config,
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id}')


if __name__ == "__main__":
    main()
