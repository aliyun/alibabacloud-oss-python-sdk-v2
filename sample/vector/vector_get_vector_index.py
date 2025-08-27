import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.vectors.models as vector_model
import alibabacloud_oss_v2.vectors as oss_vector

parser = argparse.ArgumentParser(description="vector get vector index sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--index_name', help='The name of the vector index.', required=True)


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

    vector_client = oss_vector.Client(cfg)

    result = vector_client.get_vector_index(vector_model.GetVectorIndexRequest(
        bucket=args.bucket,
        index_name=args.index_name,
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          )

    if result.index:
        print(f'index name: {result.index}')
        print(f'vector bucket name: {result.vector_bucket_name}')



if __name__ == "__main__":
    main()
