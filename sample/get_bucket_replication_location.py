import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="get bucket replication location sample")
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

    result = client.get_bucket_replication_location(oss.GetBucketReplicationLocationRequest(
            bucket=args.bucket,
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
            f' replication location: {result.replication_location},'
            f' location transfer type constraint: {result.replication_location.location_transfer_type_constraint},'
            # f' location: {result.replication_location.location_transfer_type_constraint.location_transfer_types[0].location},'
            # f' transfer types: {result.replication_location.location_transfer_type_constraint.location_transfer_types[0].transfer_types},'
            # f' location: {result.replication_location.location_transfer_type_constraint.location_transfer_types[1].location},'
            # f' transfer types: {result.replication_location.location_transfer_type_constraint.location_transfer_types[1].transfer_types},'
            f' locationrtc constraint: {result.replication_location.locationrtc_constraint},'
    )

    if result.replication_location.location_transfer_type_constraint.location_transfer_types:
        for r in result.replication_location.location_transfer_type_constraint.location_transfer_types:
            print(f'result: location: {r.location}, transfer types: {r.transfer_types}')

if __name__ == "__main__":
    main()