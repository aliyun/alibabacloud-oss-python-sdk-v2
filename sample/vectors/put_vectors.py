import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.vectors as oss_vectors

parser = argparse.ArgumentParser(description="vector put vectors sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--index_name', help='The name of the vector index.', required=True)
parser.add_argument('--account_id', help='The account id.', required=True)

def main():
    args = parser.parse_args()

    # Loading credentials values from the environment variables
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    # Using the SDK's default configuration
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    cfg.account_id = args.account_id
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint

    vector_client = oss_vectors.Client(cfg)

    vectors = [
        {
            "data": {"float32":  [0.1] * 128},
            "key": "key1",
            "metadata": {"metadata1": "value1", "metadata2": "value2"}
        },
        {
            "data": {"float32": [0.2] * 128},
            "key": "key2",
            "metadata": {"metadata3": "value3", "metadata4": "value4"}
        }
    ]

    result = vector_client.put_vectors(oss_vectors.models.PutVectorsRequest(
        bucket=args.bucket,
        index_name=args.index_name,
        vectors=vectors,
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
    )

if __name__ == "__main__":
    main()
