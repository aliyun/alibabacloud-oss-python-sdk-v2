import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="get bucket replication sample")
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

    client = oss.Client(cfg)

    result = client.get_bucket_replication(oss.GetBucketReplicationRequest(
            bucket=args.bucket,
    ))
    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
            f' replication configuration: {result.replication_configuration},'
            # f' source selection criteria: {result.replication_configuration.rules[0].source_selection_criteria},'
            # f' sse kms encrypted objects: {result.replication_configuration.rules[0].source_selection_criteria.sse_kms_encrypted_objects},'
            # f' status: {result.replication_configuration.rules[0].source_selection_criteria.sse_kms_encrypted_objects.status},'
            # f' rtc: {result.replication_configuration.rules[0].rtc},'
            # f' destination: {result.replication_configuration.rules[0].destination},'
            # f' bucket: {result.replication_configuration.rules[0].destination.bucket},'
            # f' location: {result.replication_configuration.rules[0].destination.location},'
            # f' transfer type: {result.replication_configuration.rules[0].destination.transfer_type},'
            # f' historical object replication: {result.replication_configuration.rules[0].historical_object_replication},'
            # f' sync role: {result.replication_configuration.rules[0].sync_role},'
            # f' status: {result.replication_configuration.rules[0].status},'
            # f' encryption configuration: {result.replication_configuration.rules[0].encryption_configuration},'
            # f' id: {result.replication_configuration.rules[0].id},'
            # f' prefix set: {result.replication_configuration.rules[0].prefix_set},'
            # f' action: {result.replication_configuration.rules[0].action},'
    )


    if result.replication_configuration.rules:
        for r in result.replication_configuration.rules:
            print(f'result: source selection criteria: {r.source_selection_criteria}, rtc: {r.rtc}, destination: {r.destination}, historical object replication: {r.historical_object_replication}, sync role: {r.sync_role}, status: {r.status}, encryption configuration: {r.encryption_configuration}, id: {r.id}, prefix set: {r.prefix_set}, action: {r.action}')

if __name__ == "__main__":
    main()