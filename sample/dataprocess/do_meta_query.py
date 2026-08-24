import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.dataprocess as oss_dataprocess

parser = argparse.ArgumentParser(description="do meta query sample")
parser.add_argument('--region', help='The region of the bucket.', required=True)
parser.add_argument('--endpoint', help='The endpoint of OSS.')
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--query', help='The JSON query body.', required=True)
parser.add_argument('--mode', help='The mode of the meta query.')

def main():
    args = parser.parse_args()
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint
    client = oss_dataprocess.Client(cfg)

    query_body = oss_dataprocess.models.MetaQueryDoBody(
        query=args.query,
        max_results=100,
    )

    result = client.do_meta_query(oss_dataprocess.models.DoMetaQueryRequest(
        bucket=args.bucket,
        mode=args.mode,
        meta_query_body=query_body,
    ))
    print(f'status code: {result.status_code}, request id: {result.request_id}')
    print(f'total hits: {result.total_hits}, next token: {result.next_token}')
    if result.files and result.files.file:
        for f in result.files.file:
            print(f'file: filename={f.filename}, uri={f.uri}, size={f.size}')

if __name__ == "__main__":
    main()
