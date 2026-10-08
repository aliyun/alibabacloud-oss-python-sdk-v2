import asyncio
import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.aio as oss_aio


parser = argparse.ArgumentParser(description="update bucket metadata inventory table configuration async sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--state', help='The state of the inventory metadata table. Valid values: ENABLED, DISABLED.', choices=['ENABLED', 'DISABLED'], default='ENABLED')


async def main():

    args = parser.parse_args()

    # Loading credentials values from the environment variables
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    # Using the SDK's default configuration
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint

    client = oss_aio.AsyncClient(cfg)

    try:
        result = await client.update_bucket_metadata_inventory_table_configuration(oss.UpdateBucketMetadataInventoryTableConfigurationRequest(
                bucket=args.bucket,
                inventory_table_configuration=oss.InventoryTableConfiguration(
                    configuration_state=args.state,
                ),
        ))

        print(f'status code: {result.status_code},'
              f' request id: {result.request_id},'
        )
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
