import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.dataprocess as oss_dataprocess

parser = argparse.ArgumentParser(description="get meta query status sample")
parser.add_argument('--region', help='The region of the bucket.', required=True)
parser.add_argument('--endpoint', help='The endpoint of OSS.')
parser.add_argument('--bucket', help='The name of the bucket.', required=True)

def main():
    args = parser.parse_args()
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint
    client = oss_dataprocess.Client(cfg)

    result = client.get_meta_query_status(oss_dataprocess.models.GetMetaQueryStatusRequest(
        bucket=args.bucket,
    ))
    print(f'status code: {result.status_code}, request id: {result.request_id}')
    if result.status:
        print(f'meta query state: {result.status.state}, phase={result.status.phase}, '
              f'create time={result.status.create_time}, update time={result.status.update_time}')

if __name__ == "__main__":
    main()
