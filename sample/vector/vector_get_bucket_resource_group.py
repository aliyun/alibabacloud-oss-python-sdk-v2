import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.vectors.models as vector_model
import alibabacloud_oss_v2.vectors as oss_vector

parser = argparse.ArgumentParser(description="vector get bucket resource group sample")
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

    vector_client = oss_vector.Client(cfg)

    result = vector_client.get_bucket_resource_group(vector_model.GetBucketResourceGroupRequest(
        bucket=args.bucket,
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          )

    if result.bucket_resource_group_configuration.resource_group_id:
        print(f'resource group id: {result.bucket_resource_group_configuration.resource_group_id}')


if __name__ == "__main__":
    main()
