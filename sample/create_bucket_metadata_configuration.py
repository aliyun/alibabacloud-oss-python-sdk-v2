import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="create bucket metadata configuration sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')


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

    result = client.create_bucket_metadata_configuration(oss.CreateBucketMetadataConfigurationRequest(
            bucket=args.bucket,
            metadata_configuration=oss.MetadataConfiguration(
                journal_table_configuration=oss.JournalTableConfiguration(
                    record_expiration=oss.MetadataTableRecordExpiration(
                        expiration='ENABLED',
                        days=30,
                    ),
                ),
                inventory_table_configuration=oss.InventoryTableConfiguration(
                    configuration_state='DISABLED',
                ),
            ),
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
    )


if __name__ == "__main__":
    main()
