import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="list bucket inventory sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
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

    result = client.list_bucket_inventory(oss.ListBucketInventoryRequest(
            bucket=args.bucket,
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
            f' list inventory configurations result: {result.list_inventory_configurations_result},'
            # f' included object versions: {result.list_inventory_configurations_result.inventory_configurations[0].included_object_versions},'
            # f' optional fields: {result.list_inventory_configurations_result.inventory_configurations[0].optional_fields},'
            # f' id: {result.list_inventory_configurations_result.inventory_configurations[0].id},'
            # f' is enabled: {result.list_inventory_configurations_result.inventory_configurations[0].is_enabled},'
            # f' destination: {result.list_inventory_configurations_result.inventory_configurations[0].destination},'
            # f' oss bucket destination: {result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination},'
            # f' format: {result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.format},'
            # f' account id: {result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.account_id},'
            # f' role arn: {result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.role_arn},'
            # f' bucket: {result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.bucket},'
            # f' prefix: {result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.prefix},'
            # f' encryption: {result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.encryption},'
            # f' sse kms: {result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.encryption.sse_kms},'
            # f' key id: {result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.encryption.sse_kms.key_id},'
            # f' sse oss: {result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.encryption.sse_oss},'
            # f' schedule: {result.list_inventory_configurations_result.inventory_configurations[0].schedule},'
            # f' frequency: {result.list_inventory_configurations_result.inventory_configurations[0].schedule.frequency},'
            # f' filter: {result.list_inventory_configurations_result.inventory_configurations[0].filter},'
            # f' lower size bound: {result.list_inventory_configurations_result.inventory_configurations[0].filter.lower_size_bound},'
            # f' upper size bound: {result.list_inventory_configurations_result.inventory_configurations[0].filter.upper_size_bound},'
            # f' storage class: {result.list_inventory_configurations_result.inventory_configurations[0].filter.storage_class},'
            # f' prefix: {result.list_inventory_configurations_result.inventory_configurations[0].filter.prefix},'
            # f' last modify begin time stamp: {result.list_inventory_configurations_result.inventory_configurations[0].filter.last_modify_begin_time_stamp},'
            # f' last modify end time stamp: {result.list_inventory_configurations_result.inventory_configurations[0].filter.last_modify_end_time_stamp},'
            f' is truncated: {result.list_inventory_configurations_result.is_truncated},'
            f' next continuation token: {result.list_inventory_configurations_result.next_continuation_token},'
    )

    if result.list_inventory_configurations_result.inventory_configurations:
        for r in result.list_inventory_configurations_result.inventory_configurations:
            print(f'result: {r.included_object_versions}, {r.optional_fields}, {r.id}, {r.is_enabled}, {r.destination}, {r.schedule}, {r.filter}')



if __name__ == "__main__":
    main()