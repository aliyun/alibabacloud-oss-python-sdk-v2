import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="put bucket rtc sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--status', help='Specifies whether to enable RTC.Valid values: disabled, enabled', default='disabled')
parser.add_argument('--rule_id', help='The ID of the data replication rule for which you want to configure RTC.', required=True)

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

    result = client.put_bucket_rtc(oss.PutBucketRtcRequest(
            bucket=args.bucket,
            rtc_configuration=oss.RtcConfiguration(
                rtc=oss.ReplicationTimeControl(
                    status=args.status,
                ),
                id=args.rule_id,
            ),
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
    )


if __name__ == "__main__":
    main()