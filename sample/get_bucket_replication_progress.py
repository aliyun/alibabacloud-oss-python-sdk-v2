import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="get bucket replication progress sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--rule_id', help='The ID of the data replication rule for which you want to configure RTC.', required=True)

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

    result = client.get_bucket_replication_progress(oss.GetBucketReplicationProgressRequest(
            bucket=args.bucket,
            rule_id=args.rule_id,
    ))
    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
            f' replication progress: {result.replication_progress},'
            # f' historical object replication: {result.replication_progress.rules[0].historical_object_replication},'
            # f' progress: {result.replication_progress.rules[0].progress},'
            # f' historical object: {result.replication_progress.rules[0].progress.historical_object},'
            # f' new object: {result.replication_progress.rules[0].progress.new_object},'
            # f' id: {result.replication_progress.rules[0].id},'
            # f' prefix set: {result.replication_progress.rules[0].prefix_set},'
            # f' action: {result.replication_progress.rules[0].action},'
            # f' destination: {result.replication_progress.rules[0].destination},'
            # f' bucket: {result.replication_progress.rules[0].destination.bucket},'
            # f' location: {result.replication_progress.rules[0].destination.location},'
            # f' transfer type: {result.replication_progress.rules[0].destination.transfer_type},'
            # f' status: {result.replication_progress.rules[0].status},'
    )

    if result.replication_progress.rules:
        for r in result.replication_progress.rules:
            print(f'result: historical object replication: {r.historical_object_replication}, progress: {r.progress}, id: {r.id}, prefix set: {r.prefix_set}, action: {r.action}, destination: {r.destination}, status: {r.status}')

if __name__ == "__main__":
    main()