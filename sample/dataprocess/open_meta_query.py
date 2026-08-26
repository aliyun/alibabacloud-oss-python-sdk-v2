import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.dataprocess as oss_dataprocess

parser = argparse.ArgumentParser(description="open meta query sample")
parser.add_argument('--region', help='The region of the bucket.', required=True)
parser.add_argument('--endpoint', help='The endpoint of OSS.')
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--mode', help='The mode of the meta query.')
parser.add_argument('--role', help='The role for the meta query.')

def main():
    args = parser.parse_args()
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint
    client = oss_dataprocess.Client(cfg)

    result = client.open_meta_query(oss_dataprocess.models.OpenMetaQueryRequest(
        bucket=args.bucket,
        mode=args.mode,
        role=args.role,
    ))
    print(f'status code: {result.status_code}, request id: {result.request_id}')

if __name__ == "__main__":
    main()
