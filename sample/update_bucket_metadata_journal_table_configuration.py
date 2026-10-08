import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="update bucket metadata journal table configuration sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--expiration', help='The expiration state of journal table records. Valid values: ENABLED, DISABLED.', choices=['ENABLED', 'DISABLED'], default='ENABLED')
parser.add_argument('--days', help='The number of days to retain journal records. The minimum value is 7.', type=int, default=30)


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

    result = client.update_bucket_metadata_journal_table_configuration(oss.UpdateBucketMetadataJournalTableConfigurationRequest(
            bucket=args.bucket,
            journal_table_configuration=oss.JournalTableConfiguration(
                record_expiration=oss.MetadataTableRecordExpiration(
                    expiration=args.expiration,
                    days=args.days if args.expiration == 'ENABLED' else None,
                ),
            ),
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
    )


if __name__ == "__main__":
    main()
