import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="create access point sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--access_point_name', help='The name of the access point.', required=True)
parser.add_argument('--network_origin', help='The network origin of the access point.', required=True)
parser.add_argument('--vpc_id', help='The ID of the VPC that is required only when the NetworkOrigin parameter is set to vpc.')


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

    # result = client.create_access_point(oss.CreateAccessPointRequest(
    #     bucket=args.bucket,
    #     create_access_point_configuration=oss.CreateAccessPointConfiguration(
    #         access_point_name=args.access_point_name,
    #         network_origin=args.network_origin,
    #         vpc_configuration=oss.AccessPointVpcConfiguration(
    #             vpc_id=args.vpc_id,
    #         ),
    #     ),
    # ))

    result = client.create_access_point(oss.CreateAccessPointRequest(
        bucket=args.bucket,
        create_access_point_configuration=oss.CreateAccessPointConfiguration(
            access_point_name=args.access_point_name,
            network_origin=args.network_origin,
        ),
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' access point arn: {result.access_point_arn},' 
          f' alias: {result.alias},'
    )

if __name__ == "__main__":
    main()