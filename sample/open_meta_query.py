import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="open meta query sample")
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

    # Basic open meta query
    result = client.open_meta_query(oss.OpenMetaQueryRequest(
            bucket=args.bucket,
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
    )

    # Open meta query with workflow parameters and filters
    result = client.open_meta_query(oss.OpenMetaQueryRequest(
            bucket=args.bucket,
            mode='semantic',
            role='OSSServiceRole',
            meta_query=oss.MetaQueryOpenRequest(
                workflow_parameters=oss.WorkflowParameters(
                    workflow_parameters=[
                        oss.WorkflowParameter(name='VideoInsightEnable', value='True'),
                        oss.WorkflowParameter(name='ImageInsightEnable', value='True')
                    ]
                ),
                filters=oss.Filters(
                    filters=[
                        'Size > 1024, FileModifiedTime > 2025-06-03T09:20:47.999Z',
                        'Filename prefix (YWEvYmIv)'
                    ]
                )
            )
    ))

    print(f'status code with workflow and filters: {result.status_code},'
            f' request id: {result.request_id},'
    )


if __name__ == "__main__":
    main()