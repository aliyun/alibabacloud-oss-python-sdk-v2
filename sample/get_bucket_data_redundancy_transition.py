import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="get bucket data redundancy transition sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--redundancy_transition_taskid', help='The ID of the redundancy change task.', required=True)


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

    result = client.get_bucket_data_redundancy_transition(oss.GetBucketDataRedundancyTransitionRequest(
            bucket=args.bucket,
            redundancy_transition_taskid=args.redundancy_transition_taskid,
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
            f' bucket: {result.bucket_data_redundancy_transition.bucket},'
            f' task id: {result.bucket_data_redundancy_transition.task_id},'
            f' status: {result.bucket_data_redundancy_transition.status},'
            f' create time: {result.bucket_data_redundancy_transition.create_time},'
            f' start time: {result.bucket_data_redundancy_transition.start_time},'
            f' end time: {result.bucket_data_redundancy_transition.end_time},'
            f' process percentage: {result.bucket_data_redundancy_transition.process_percentage},'
            f' estimated remaining time: {result.bucket_data_redundancy_transition.estimated_remaining_time},'
    )


if __name__ == "__main__":
    main()