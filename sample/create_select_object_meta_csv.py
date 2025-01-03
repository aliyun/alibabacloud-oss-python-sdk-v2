import argparse
import base64
import alibabacloud_oss_v2 as oss


parser = argparse.ArgumentParser(description="create select object meta csv sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--key', help='The name of the object.', required=True)
parser.add_argument('--expression', default='select * from ossobject as s where cast(s.age as int) > 40')



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

    data = "name,school,company,age\nLora Francis,School,Staples Inc,27\nEleanor Little,School,\"Conectiv, Inc\",43\nRosie Hughes,School,Western Gas Resources Inc,44\nLawrence Ross,School,MetLife Inc.,24\n"

    result = client.put_object(oss.PutObjectRequest(
        bucket=args.bucket,
        key=args.key,
        body=data,
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' content md5: {result.content_md5},'
          f' etag: {result.etag},'
          f' hash crc64: {result.hash_crc64},'
          f' version id: {result.version_id},'
    )

    request = oss.CreateSelectObjectMetaRequest(
        bucket=args.bucket,
        key=args.key,
        process='csv/meta',
        select_meta_request=oss.CSVMetaRequest(
            overwrite_if_exists=True,
            input_serialization=oss.InputSerialization(
                compression_type=None,
                csv=oss.CSVInput(
                    file_header_info='NONE',
                    record_delimiter=base64.b64encode('\n'.encode()).decode(),
                    field_delimiter=base64.b64encode(','.encode()).decode(),
                    quote_character=base64.b64encode('\"'.encode()).decode(),
                ),
            ),
        ),
    )

    result = client.create_select_object_meta(request)

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' splits: {result.splits_count},'
          f' row: {result.rows_count},'
          f' columns: {result.cols_count},'
    )


if __name__ == "__main__":
    main()

