import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="list access points for object process sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--max_keys', help='The maximum number of return.', default='100')
parser.add_argument('--continuation_token', help='The token from which the list operation must start. You can obtain this token from the NextContinuationToken element in the returned result.', default='')



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

    result = client.list_access_points_for_object_process(oss.ListAccessPointsForObjectProcessRequest(
            max_keys=args.max_keys,
            continuation_token=args.continuation_token,
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
            f' is truncated: {result.is_truncated},'
            f' next continuation token: {result.next_continuation_token},'
            f' account id: {result.account_id},'
            f' access points for object process: {result.access_points_for_object_process},'
            f' status: {result.access_points_for_object_process.access_point_for_object_processs[0].status},'
            f' allow anonymous access for object process: {result.access_points_for_object_process.access_point_for_object_processs[0].allow_anonymous_access_for_object_process},'
            f' access point name for object process: {result.access_points_for_object_process.access_point_for_object_processs[0].access_point_name_for_object_process},'
            f' access point for object process alias: {result.access_points_for_object_process.access_point_for_object_processs[0].access_point_for_object_process_alias},'
            f' access point name: {result.access_points_for_object_process.access_point_for_object_processs[0].access_point_name},'
    )

    if result.access_points_for_object_process.access_point_for_object_processs:
        for r in result.access_points_for_object_process.access_point_for_object_processs:
            print(f'result: status: {r.status}, allow anonymous access for object process: {r.allow_anonymous_access_for_object_process}, access point name for object process: {r.access_point_name_for_object_process}, access point for object process alias: {r.access_point_for_object_process_alias}, access point name: {r.access_point_name}')

if __name__ == "__main__":
    main()