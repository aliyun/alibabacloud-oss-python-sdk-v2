import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.vectors as oss_vectors

parser = argparse.ArgumentParser(description="vector query vectors fusion sample")
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

    # QueryVectorsFusion accepts three shapes of query:
    #
    #   knn        nearest neighbour search. A single dict for one vector
    #              field, or a list of dicts for up to three of them. knn and
    #              query can share one request, and their scores add up.
    #   query      scalar, full text and geo conditions. A logical operator
    #              takes the object form {"$and": {"clauses": [...]}}, and a
    #              full text match takes {"$textMatch": {"value": "..."}}. The
    #              field and operator names are dynamic, so this stays a dict.
    #   retriever  combines several retrievers into one ranked result, for
    #              example an rrf node holding a knn leaf and a text leaf. It
    #              is mutually exclusive with knn, query and sort, so it goes
    #              in a request of its own.
    #
    # The request below mixes knn and query on the e-commerce productindex:
    # two vector recalls plus a brand and title boost, sorted by _score, which
    # only accepts desc. Every hit carries a score. That score belongs to this
    # operation only, the standard QueryVectors result keeps reporting
    # distance and the two are never mixed.
    result = vector_client.query_vectors_fusion(oss_vectors.models.QueryVectorsFusionRequest(
        bucket=args.bucket,
        index_name=args.index_name,
        knn=[
            {
                "field": "text_vector",
                "queryVector": [0.1] * 768,
                "topK": 100,
                "boost": 2.0
            },
            {
                "field": "image_vector",
                "queryVector": [0.1] * 512,
                "topK": 100,
                "boost": 0.5
            }
        ],
        query={
            "$or": {
                "clauses": [
                    {"brand": {"$in": {"value": ["AliBrand"], "boost": 1.0}}},
                    {"title": {"$textMatch": {"value": "耳机", "boost": 4.0}}}
                ]
            }
        },
        return_metadata=True,
        return_metadata_fields=["title", "brand", "price"],
        sort=[{
            "_score": {
                "order": "desc"
            }
        }],
        limit=20
    ))

    # The third shape, retriever, cannot be mixed with knn, query or sort. An
    # rrf fusion of a vector leaf and a full text leaf looks like this:
    #
    # result = vector_client.query_vectors_fusion(oss_vectors.models.QueryVectorsFusionRequest(
    #     bucket=args.bucket,
    #     index_name=args.index_name,
    #     retriever={
    #         "rrf": {
    #             "k": 50,
    #             "windowSize": 100,
    #             "retrievers": [
    #                 {
    #                     "retriever": {
    #                         "knn": {
    #                             "field": "text_vector",
    #                             "queryVector": [0.1] * 768,
    #                             "topK": 100
    #                         }
    #                     },
    #                     "weight": 2.0
    #                 },
    #                 {
    #                     "retriever": {
    #                         "simple": {
    #                             "query": {
    #                                 "title": {"$textMatch": {"value": "无线 耳机"}}
    #                             }
    #                         }
    #                     },
    #                     "weight": 0.5
    #                 }
    #             ]
    #         }
    #     },
    #     limit=10,
    #     return_metadata=True,
    #     return_metadata_fields=["title", "brand"]
    # ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' next token: {result.next_token},'
          )

    if result.vectors:
        for vector in result.vectors:
            print(f'vector: {vector}')


if __name__ == "__main__":
    main()
