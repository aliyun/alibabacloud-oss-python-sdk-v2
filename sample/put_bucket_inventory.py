import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="put bucket inventory sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--user_id', help='User account ID.', required=True)
parser.add_argument('--arn', help='The Alibaba Cloud Resource Name (ARN) of the role that has the permissions to read all objects from the source bucket and write objects to the destination bucket. Format: `acs:ram::uid:role/rolename.', required=True)
parser.add_argument('--inventory_id', help='The name of the inventory.', required=True)


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

    result = client.put_bucket_inventory(oss.PutBucketInventoryRequest(
            bucket=args.bucket,
            inventory_id=args.inventory_id,
            inventory_configuration=oss.InventoryConfiguration(
                included_object_versions='All',
                optional_fields=oss.OptionalFields(
                    fields=[oss.InventoryOptionalFieldType.SIZE, oss.InventoryOptionalFieldType.LAST_MODIFIED_DATE],
                ),
                id=args.inventory_id,
                is_enabled=True,
                destination=oss.InventoryDestination(
                    oss_bucket_destination=oss.InventoryOSSBucketDestination(
                        format=oss.InventoryFormatType.CSV,
                        account_id=args.user_id,
                        role_arn=args.arn,
                        bucket=f'acs:oss:::{args.bucket}',
                        prefix='aaa',
                    ),
                ),
                schedule=oss.InventorySchedule(
                    frequency=oss.InventoryFrequencyType.DAILY,
                ),
                filter=oss.InventoryFilter(
                    lower_size_bound=1024,
                    upper_size_bound=1048576,
                    storage_class='ColdArchive',
                    prefix='aaa',
                    last_modify_begin_time_stamp=1637883649,
                    last_modify_end_time_stamp=1638347592,
                ),
                # incremental inventory
                # incremental_inventory=oss.IncrementalInventory(
                #     is_enabled=True,
                #     schedule=oss.IncrementInventorySchedule(
                #         frequency=600
                #     ),
                #     optional_fields=oss.IncrementalInventoryOptionalFields(
                #         fields=[
                #             oss.IncrementalInventoryOptionalFieldType.SEQUENCE_NUMBER,
                #             oss.IncrementalInventoryOptionalFieldType.RECORD_TYPE,
                #             oss.IncrementalInventoryOptionalFieldType.RECORD_TIMESTAMP,
                #             oss.IncrementalInventoryOptionalFieldType.REQUESTER,
                #             oss.IncrementalInventoryOptionalFieldType.SOURCE_IP,
                #             oss.IncrementalInventoryOptionalFieldType.REQUEST_ID,
                #             oss.IncrementalInventoryOptionalFieldType.SIZE,
                #             oss.IncrementalInventoryOptionalFieldType.STORAGE_CLASS,
                #             oss.IncrementalInventoryOptionalFieldType.LAST_MODIFIED_DATE,
                #             oss.IncrementalInventoryOptionalFieldType.E_TAG,
                #             oss.IncrementalInventoryOptionalFieldType.IS_MULTIPART_UPLOADED,
                #             oss.IncrementalInventoryOptionalFieldType.OBJECT_TYPE,
                #             oss.IncrementalInventoryOptionalFieldType.OBJECT_ACL,
                #             oss.IncrementalInventoryOptionalFieldType.CRC64,
                #             oss.IncrementalInventoryOptionalFieldType.ENCRYPTION_STATUS
                #         ]
                #     )
                # )
            ),
    ))


    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
    )


if __name__ == "__main__":
    main()