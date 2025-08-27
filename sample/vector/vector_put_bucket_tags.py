import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.vectors as oss_vector

parser = argparse.ArgumentParser(description="vector put bucket tags sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--uid', help='The user id.', required=True)

def main():

    args = parser.parse_args()

    # Loading credentials values from the environment variables
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    # Using the SDK's default configuration
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    cfg.user_id = args.uid
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint

    vector_client = oss_vector.Client(cfg)

    result = vector_client.put_bucket_tags(oss_vector.models.PutBucketTagsRequest(
            bucket=args.bucket,
            tagging=oss_vector.models.Tagging(
                tag_set=oss_vector.models.TagSet(
                    tags=[oss_vector.models.Tag(
                        key='test_key',
                        value='test_value',
                    ), oss_vector.models.Tag(
                        key='test_key2',
                        value='test_value2',
                    )],
                ),
            ),
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
    )


if __name__ == "__main__":
    main()