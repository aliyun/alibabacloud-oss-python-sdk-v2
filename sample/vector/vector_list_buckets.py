import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.vectors as oss_vector

parser = argparse.ArgumentParser(description="vector list buckets sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
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

    result = vector_client.list_vector_buckets(oss_vector.models.ListVectorBucketsRequest())

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
    )

    if result.buckets:
        for bucket in result.buckets:
            print(f'bucket: {bucket.name}, location: {bucket.location}, creation_date: {bucket.creation_date}')

if __name__ == "__main__":
    main()
