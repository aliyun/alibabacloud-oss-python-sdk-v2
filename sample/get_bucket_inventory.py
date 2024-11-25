import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="get bucket inventory sample")
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

    result = client.get_bucket_inventory(oss.GetBucketInventoryRequest(
            bucket=args.bucket,
            inventory_id=args.inventory_id,
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
            f' included object versions: {result.inventory_configuration.included_object_versions},'
            f' id: {result.inventory_configuration.id},'
            f' is enabled: {result.inventory_configuration.is_enabled},'
            f' account id: {result.inventory_configuration.destination.oss_bucket_destination.account_id},'
            f' role arn: {result.inventory_configuration.destination.oss_bucket_destination.role_arn},'
            f' bucket: {result.inventory_configuration.destination.oss_bucket_destination.bucket},'
            f' prefix: {result.inventory_configuration.destination.oss_bucket_destination.prefix},'
            # f' key id: {result.inventory_configuration.destination.oss_bucket_destination.encryption.sse_kms.key_id},'
            # f' sse oss: {result.inventory_configuration.destination.oss_bucket_destination.encryption.sse_oss},'
            f' lower size bound: {result.inventory_configuration.filter.lower_size_bound},'
            f' upper size bound: {result.inventory_configuration.filter.upper_size_bound},'
            f' storage class: {result.inventory_configuration.filter.storage_class},'
            f' prefix: {result.inventory_configuration.filter.prefix},'
            f' last modify begin time stamp: {result.inventory_configuration.filter.last_modify_begin_time_stamp},'
            f' last modify end time stamp: {result.inventory_configuration.filter.last_modify_end_time_stamp},'
    )


if __name__ == "__main__":
    main()