import argparse
import datetime
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="put bucket lifecycle sample")
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

    result = client.put_bucket_lifecycle(oss.PutBucketLifecycleRequest(
            bucket=args.bucket,
            lifecycle_configuration=oss.LifecycleConfiguration(
                rules=[oss.LifecycleRule(
                    id='test-001****',
                    transitions=[oss.Transition(
                        # created_before_date=datetime.datetime.fromtimestamp(1702743657),
                        created_before_date=datetime.datetime.strptime("2023-10-01T00:00:00.000Z", '%Y-%m-%dT00:00:00.000Z'),
                        storage_class=oss.StorageClassType.COLDARCHIVE,
                        is_access_time=False,
                    )],
                    prefix='python-test',
                    status='Enabled',
                ), oss.LifecycleRule(
                    id='test-002****',
                    transitions=[oss.Transition(
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                        # created_before_date=datetime.datetime.strptime("2023-10-01T00:00:00.000Z", '%Y-%m-%dT00:00:00.000Z'),
                        storage_class='Archive',
                    )],
                    prefix='java-test',
                    status='Enabled',
                )]
            ),
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
    )


if __name__ == "__main__":
    main()