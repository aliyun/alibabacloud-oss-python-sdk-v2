import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="list user data redundancy transition sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--max_keys', default='10')
parser.add_argument('--continuation_token', default='')


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

    result = client.list_user_data_redundancy_transition(oss.ListUserDataRedundancyTransitionRequest(
            max_keys=args.max_keys,
            continuation_token=args.continuation_token,
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
            f' list bucket data redundancy transition: {result.list_bucket_data_redundancy_transition},'
            # f' bucket: {result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].bucket},'
            # f' task id: {result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].task_id},'
            # f' status: {result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].status},'
            # f' create time: {result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].create_time},'
            # f' start time: {result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].start_time},'
            # f' end time: {result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].end_time},'
            # f' process percentage: {result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].process_percentage},'
            # f' estimated remaining time: {result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].estimated_remaining_time},'
            f' is truncated: {result.list_bucket_data_redundancy_transition.is_truncated},'
            f' next continuation token: {result.list_bucket_data_redundancy_transition.next_continuation_token},'
    )

    if result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition:
        for r in result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition:
            print(f'result: bucket: {r.bucket}, task id: {r.task_id}, status: {r.status}, create time: {r.create_time}, start time: {r.start_time}, end time: {r.end_time}, process percentage: {r.process_percentage}, estimated remaining time: {r.estimated_remaining_time}')

if __name__ == "__main__":
    main()