import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="put access point config for object process sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--access_point_for_object_process_name', help='The name of the Object FC Access Point.', required=True)
parser.add_argument('--function_arn', help='The ARN of the function.', required=True)
parser.add_argument('--function_assume_role_arn', help='The Alibaba Cloud Resource Name (ARN) of the role that Function Compute uses to access your resources in other cloud services. ', required=True)
parser.add_argument('--block_public_access', help='Specifies whether to enable Block Public Access.true: enables Block Public Access.false (default): disables Block Public Access.', default=False)



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

    result = client.put_access_point_config_for_object_process(oss.PutAccessPointConfigForObjectProcessRequest(
            bucket=args.bucket,
            access_point_for_object_process_name=args.access_point_for_object_process_name,
            put_access_point_config_for_object_process_configuration=oss.PutAccessPointConfigForObjectProcessConfiguration(
                # allow_anonymous_access_for_object_process=args.allow_anonymous_access_for_object_process,
                public_access_block_configuration=oss.PublicAccessBlockConfiguration(
                    block_public_access=args.block_public_access,
                ),
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
    )


if __name__ == "__main__":
    main()