import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="put access point policy sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--access_point_name', help='The name of the access point.', required=True)
parser.add_argument('--user_id', help='User account ID.', required=True)


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


    policy = "{\"Version\":\"1\",\"Statement\":[{\"Action\":[\"oss:PutObject\",\"oss:GetObject\"],\"Effect\":\"Deny\",\"Principal\":[\"" + args.user_id + "\"],\"Resource\":[\"acs:oss:" + args.region + ":" + args.user_id + ":accesspoint/" + args.access_point_name + "\",\"acs:oss:" + args.region + ":" + args.user_id + ":accesspoint/" + args.access_point_name + "/object/*\"]}]}"

    result = client.put_access_point_policy(oss.PutAccessPointPolicyRequest(
            bucket=args.bucket,
            access_point_name=args.access_point_name,
            body=policy,
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
    )

if __name__ == "__main__":
    main()