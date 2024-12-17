import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="create bucket data redundancy transition sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--target_redundancy_type', help='The redundancy type to which you want to convert the bucket. You can only convert the redundancy type of a bucket from LRS to ZRS.', default='ZRS')


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

    result = client.create_bucket_data_redundancy_transition(oss.CreateBucketDataRedundancyTransitionRequest(
            bucket=args.bucket,
            target_redundancy_type=args.target_redundancy_type,
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
            f' task id: {result.bucket_data_redundancy_transition.task_id},'
    )


if __name__ == "__main__":
    main()