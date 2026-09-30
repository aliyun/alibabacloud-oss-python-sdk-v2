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

    # Standard index: one vector field keyed by its data type. This is the
    # shape put_vector_index.py creates, and it stays the default so this
    # sample keeps working against a standard index exactly as before.
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

    # Fusion index: PutVectors keeps a dynamic data shape, so the very same
    # call also writes several named vector fields declared by a fusion schema.
    # To target a fusion index, comment out the block above and uncomment the
    # one below. The field names match the text_vector and image_vector
    # declared by put_vector_index_fusion.py.
    # vectors = [
    #     {
    #         "data": {
    #             "text_vector": [0.1] * 4,
    #             "image_vector": [0.2] * 4
    #         },
    #         "key": "key1",
    #         "metadata": {"metadata1": "value1", "metadata2": "value2"}
    #     },
    #     {
    #         "data": {
    #             "text_vector": [0.3] * 4,
    #             "image_vector": [0.4] * 4
    #         },
    #         "key": "key2",
    #         "metadata": {"metadata3": "value3", "metadata4": "value4"}
    #     }
    # ]

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
