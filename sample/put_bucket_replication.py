import argparse
import datetime
import random
import string

import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="put bucket replication sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--sync_role', help='The role that you want to authorize OSS to use to replicate data', required=True)
parser.add_argument('--target_bucket', help='The destination bucket to which data is replicated', required=True)
parser.add_argument('--target_location', help='The region in which the destination bucket is located', required=True)


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

    # source
    client = oss.Client(cfg)

    # put bucket replication
    result = client.put_bucket_replication(oss.PutBucketReplicationRequest(
            bucket=args.bucket,
            replication_configuration=oss.ReplicationConfiguration(
                rules=[oss.ReplicationRule(
                    source_selection_criteria=oss.ReplicationSourceSelectionCriteria(
                        sse_kms_encrypted_objects=oss.SseKmsEncryptedObjects(
                            status=oss.StatusType.ENABLED,
                        ),
                    ),
                    rtc=oss.ReplicationTimeControl(
                        status='disabled',
                    ),
                    destination=oss.ReplicationDestination(
                        bucket=args.target_bucket,
                        location=args.target_location,
                        transfer_type=oss.TransferType.INTERNAL,
                    ),
                    historical_object_replication=oss.HistoricalObjectReplicationType.DISABLED,
                    sync_role=args.sync_role,
                    status='Disabled',
                    prefix_set=oss.ReplicationPrefixSet(
                        prefixs=['aaa/', 'bbb/'],
                    ),
                    action='ALL',
                )],
            ),
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
    )

if __name__ == "__main__":
    main()