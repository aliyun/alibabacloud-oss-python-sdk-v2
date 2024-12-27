import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="get access point config for object process sample")
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

    result = client.get_access_point_config_for_object_process(oss.GetAccessPointConfigForObjectProcessRequest(
        bucket=args.bucket,
        access_point_for_object_process_name=args.access_point_for_object_process_name,
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' public access block configuration: {result.public_access_block_configuration},'
          f' block public access: {result.public_access_block_configuration.block_public_access},'
          f' object process configuration: {result.object_process_configuration},'
          f' allowed features: {result.object_process_configuration.allowed_features},'
          f' transformation configurations: {result.object_process_configuration.transformation_configurations},'
          f' actions: {result.object_process_configuration.transformation_configurations.transformation_configurations[0].actions},'
          f' content transformation: {result.object_process_configuration.transformation_configurations.transformation_configurations[0].content_transformation},'
          f' function compute: {result.object_process_configuration.transformation_configurations.transformation_configurations[0].content_transformation.function_compute},'
          f' function assume role arn: {result.object_process_configuration.transformation_configurations.transformation_configurations[0].content_transformation.function_compute.function_assume_role_arn},'
          f' function arn: {result.object_process_configuration.transformation_configurations.transformation_configurations[0].content_transformation.function_compute.function_arn},'
          f' additional features: {result.object_process_configuration.transformation_configurations.transformation_configurations[0].content_transformation.additional_features},'
          f' custom forward headers: {result.object_process_configuration.transformation_configurations.transformation_configurations[0].content_transformation.additional_features.custom_forward_headers},'
          f' allow anonymous access for object process: {result.allow_anonymous_access_for_object_process},'
          )

    if result.object_process_configuration.transformation_configurations.transformation_configurations:
        for r in result.object_process_configuration.transformation_configurations.transformation_configurations:
            print(f'result: actions: {r.actions}, content transformation: {r.content_transformation}')


if __name__ == "__main__":
    main()