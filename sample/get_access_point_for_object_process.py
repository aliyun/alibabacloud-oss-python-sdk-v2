import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="get access point for object process sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--access_point_for_object_process_name', help='The name of the Object FC Access Point.', required=True)



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

    result = client.get_access_point_for_object_process(oss.GetAccessPointForObjectProcessRequest(
            bucket=args.bucket,
            access_point_for_object_process_name=args.access_point_for_object_process_name,
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
            f' access point name for object process: {result.access_point_name_for_object_process},'
            f' access point for object process alias: {result.access_point_for_object_process_alias},'
            f' account id: {result.account_id},'
            f' access point for object process arn: {result.access_point_for_object_process_arn},'
            f' status: {result.status},'
            f' access point name: {result.access_point_name},'
            f' creation date: {result.creation_date},'
            f' endpoints: {result.endpoints},'
            f' public endpoint: {result.endpoints.public_endpoint},'
            f' internal endpoint: {result.endpoints.internal_endpoint},'
            f' allow anonymous access for object process: {result.allow_anonymous_access_for_object_process},'
            f' public access block configuration: {result.public_access_block_configuration},'
            f' block public access: {result.public_access_block_configuration.block_public_access},'
    )


if __name__ == "__main__":
    main()