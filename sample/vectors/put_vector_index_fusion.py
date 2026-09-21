import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.vectors as oss_vectors

parser = argparse.ArgumentParser(description="vector put vector index fusion sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--index_name', help='The name of the fusion vector index.', required=True)
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

    # A fusion index is described by a schema listing every field, instead of
    # the single vector field that put_vector_index configures. This is the
    # typical e-commerce product schema: two vector fields for text and image
    # dual recall, scalar fields for filtering and sorting, and a tokenized
    # title for full text search.
    #
    # The schema is a plain dict, so any field type or property the service
    # supports travels through unchanged. A text field defaults to the
    # "standard" analyzer, English by word and Chinese by single character.
    # Write a boolean out explicitly when false is what you mean, an omitted
    # property and a property set to false are not the same thing to the
    # service. mode defaults to "fusion", so it is left out here.
    schema_configuration = {
        "fields": [
            {
                "name": "text_vector",
                "type": "vector",
                "dataType": "float32",
                "dimension": 768,
                "distanceMetric": "euclidean"
            },
            {
                "name": "image_vector",
                "type": "vector",
                "dataType": "float32",
                "dimension": 512,
                "distanceMetric": "euclidean"
            },
            {
                "name": "title",
                "type": "string",
                "exactMatch": True,
                "text": {
                    "enabled": True,
                    "analyzer": "standard"
                }
            },
            {
                "name": "brand",
                "type": "string"
            },
            {
                "name": "category",
                "type": "string",
                "isArray": True
            },
            {
                "name": "price",
                "type": "double"
            },
            {
                "name": "stock",
                "type": "long"
            },
            {
                "name": "on_sale",
                "type": "bool"
            }
        ]
    }

    result = vector_client.put_vector_index_fusion(oss_vectors.models.PutVectorIndexFusionRequest(
        bucket=args.bucket,
        index_name=args.index_name,
        schema_configuration=schema_configuration
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
    )

if __name__ == "__main__":
    main()
