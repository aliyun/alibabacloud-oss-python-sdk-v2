import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="put bucket access monitor sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--status', help='The access tracking status of the bucket. Valid values:- Enabled: Access tracking is enabled.- Disabled: Access tracking is disabled.', required=True)

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

    # result = client.put_bucket_access_monitor(oss.PutBucketAccessMonitorRequest(
    #         bucket=args.bucket,
    #         access_monitor_configuration=oss.AccessMonitorConfiguration(
    #             status=oss.AccessMonitorStatusType.ENABLED
    #         ),
    # ))

    result = client.put_bucket_access_monitor(oss.PutBucketAccessMonitorRequest(
            bucket=args.bucket,
            access_monitor_configuration=oss.AccessMonitorConfiguration(
                status=args.status,
            ),
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
    )

if __name__ == "__main__":
    main()