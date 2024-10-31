import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="list access points sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.')
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

    # Bucket level
    result = client.list_access_points(oss.ListAccessPointsRequest(
            bucket=args.bucket,
            # max_keys=args.max_keys,
            # continuation_token=args.continuation_token,
    ))

    # # User level
    # result = client.list_access_points(oss.ListAccessPointsRequest(
    #         max_keys=args.max_keys,
    #         continuation_token=args.continuation_token,
    # ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
            # f' network origin: {result.access_points[0].network_origin},'
            # f' vpc id: {result.access_points[0].vpc_configuration.vpc_id},'
            # f' status: {result.access_points[0].status},'
            # f' bucket: {result.access_points[0].bucket},'
            # f' access point name: {result.access_points[0].access_point_name},'
            # f' alias: {result.access_points[0].alias},'
            f' max keys: {result.max_keys},'
            f' is truncated: {result.is_truncated},'
            f' next continuation token: {result.next_continuation_token},'
            f' account id: {result.account_id},'
    )

    if result.access_points:
        for r in result.access_points:
            print(f'result: {r.network_origin}, {r.vpc_configuration.vpc_id}, {r.status}, {r.bucket}, {r.access_point_name}, {r.alias}')

if __name__ == "__main__":
    main()