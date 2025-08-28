import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.vectors as oss_vectors

parser = argparse.ArgumentParser(description="vector query vectors sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--index_name', help='The name of the vector index.', required=True)
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

    vector_client = oss_vectors.Client(cfg)

    query_filter = {
        "$and": [{
            "type": {
                "$in": ["comedy", "documentary"]
            }
        }, {
            "year": {
                "$gte": 2020
            }
        }]
    }

    query_vector = {"float32": [0.1, 0.2, 0.3]}

    result = vector_client.query_vectors(oss_vectors.models.QueryVectorsRequest(
        bucket=args.bucket,
        index_name=args.index_name,
        filter=query_filter,
        query_vector=query_vector,
        return_distance=True,
        return_metadata=False,
        top_k=10
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          )

    if result.vectors:
        for vector in result.vectors:
            print(f'vector: {vector}')


if __name__ == "__main__":
    main()
