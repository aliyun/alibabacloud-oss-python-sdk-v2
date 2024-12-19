import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="do meta query sample")
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

    result = client.do_meta_query(oss.DoMetaQueryRequest(
            bucket=args.bucket,
            meta_query=oss.MetaQuery(
                aggregations=oss.MetaQueryAggregations(
                    aggregations=[oss.MetaQueryAggregation(
                        field='Size',
                        operation='sum',
                    ), oss.MetaQueryAggregation(
                        field='Size',
                        operation='max',
                    )],
                ),
                next_token='',
                max_results=80369,
                query='{"Field": "Size","Value": "1048576","Operation": "gt"}',
                sort='Size',
                order=oss.MetaQueryOrderType.DESC,
            ),
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
            # f' files: {result.files},'
            # f' file: {result.files.file},'
            # f' file modified time: {result.files.file.file_modified_time},'
            # f' etag: {result.files.file.etag},'
            # f' server side encryption: {result.files.file.server_side_encryption},'
            # f' oss tagging count: {result.files.file.oss_tagging_count},'
            # f' oss tagging: {result.files.file.oss_tagging},'
            # f' key: {result.files.file.oss_tagging.taggings[0].key},'
            # f' value: {result.files.file.oss_tagging.taggings[0].value},'
            # f' key: {result.files.file.oss_tagging.taggings[1].key},'
            # f' value: {result.files.file.oss_tagging.taggings[1].value},'
            # f' oss user meta: {result.files.file.oss_user_meta},'
            # f' key: {result.files.file.oss_user_meta.user_metas[0].key},'
            # f' value: {result.files.file.oss_user_meta.user_metas[0].value},'
            # f' key: {result.files.file.oss_user_meta.user_metas[1].key},'
            # f' value: {result.files.file.oss_user_meta.user_metas[1].value},'
            # f' filename: {result.files.file.filename},'
            # f' size: {result.files.file.size},'
            # f' oss object type: {result.files.file.oss_object_type},'
            # f' oss storage class: {result.files.file.oss_storage_class},'
            # f' object acl: {result.files.file.object_acl},'
            # f' oss crc64: {result.files.file.oss_crc64},'
            # f' server side encryption customer algorithm: {result.files.file.server_side_encryption_customer_algorithm},'
            # f' aggregations: {result.aggregations},'
            f' field: {result.aggregations.aggregations[0].field},'
            f' operation: {result.aggregations.aggregations[0].operation},'
            f' field: {result.aggregations.aggregations[1].field},'
            f' operation: {result.aggregations.aggregations[1].operation},'
            f' next token: {result.next_token},'
    )

    if result.files:
        if result.files.file.oss_tagging.taggings:
            for r in result.files.file.oss_tagging.taggings:
                print(f'result: key: {r.key}, value: {r.value}')
        if result.files.file.oss_user_meta.user_metas:
            for r in result.files.file.oss_user_meta.user_metas:
                print(f'result: key: {r.key}, value: {r.value}')
    if result.aggregations.aggregations:
        for r in result.aggregations.aggregations:
            print(f'result: field: {r.field}, operation: {r.operation}')

if __name__ == "__main__":
    main()