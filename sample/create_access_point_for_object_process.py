import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="create access point for object process sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--access_point_name', help='The name of the access point.', required=True)
parser.add_argument('--access_point_for_object_process_name', help='The name of the Object FC Access Point.', required=True)
parser.add_argument('--function_arn', help='The ARN of the function.', required=True)
parser.add_argument('--function_assume_role_arn', help='The Alibaba Cloud Resource Name (ARN) of the role that Function Compute uses to access your resources in other cloud services. ', required=True)


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

    result = client.create_access_point_for_object_process(oss.CreateAccessPointForObjectProcessRequest(
            bucket=args.bucket,
            access_point_for_object_process_name=args.access_point_for_object_process_name,
            create_access_point_for_object_process_configuration=oss.CreateAccessPointForObjectProcessConfiguration(
                # allow_anonymous_access_for_object_process=args.allow_anonymous_access_for_object_process,
                access_point_name=args.access_point_name,
                object_process_configuration=oss.ObjectProcessConfiguration(
                    allowed_features=oss.AllowedFeatures(
                        allowed_features=['GetObject-Range'],
                    ),
                    transformation_configurations=oss.TransformationConfigurations(
                        transformation_configurations=[oss.TransformationConfiguration(
                            actions=oss.AccessPointActions(
                                actions=['GetObject'],
                            ),
                            content_transformation=oss.ContentTransformation(
                                function_compute=oss.FunctionCompute(
                                    function_assume_role_arn=args.function_assume_role_arn,
                                    function_arn=args.function_arn,
                                ),
                                additional_features=oss.AdditionalFeatures(
                                    custom_forward_headers=oss.CustomForwardHeaders(
                                        custom_forward_headers=['header1', 'header2'],
                                    ),
                                ),
                            ),
                        )],
                    ),
                ),
            ),
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
            f' access point for object process alias: {result.access_point_for_object_process_alias},'
            f' access point for object process arn: {result.access_point_for_object_process_arn},'
    )


if __name__ == "__main__":
    main()