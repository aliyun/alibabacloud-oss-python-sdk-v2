import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="list style sample")
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

    result = client.list_style(oss.ListStyleRequest(
            bucket=args.bucket,
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
            # f' name: {result.style_list.styles[0].name},'
            # f' content: {result.style_list.styles[0].content},'
            # f' create time: {result.style_list.styles[0].create_time},'
            # f' last modify time: {result.style_list.styles[0].last_modify_time},'
            # f' category: {result.style_list.styles[0].category},'
            # f' name: {result.style_list.styles[1].name},'
            # f' content: {result.style_list.styles[1].content},'
            # f' create time: {result.style_list.styles[1].create_time},'
            # f' last modify time: {result.style_list.styles[1].last_modify_time},'
            # f' category: {result.style_list.styles[1].category},'
    )

    if result.style_list.styles:
        for r in result.style_list.styles:
            print(f'result: name: {r.name}, content: {r.content}, create time: {r.create_time}, last modify time: {r.last_modify_time}, category: {r.category}')

if __name__ == "__main__":
    main()