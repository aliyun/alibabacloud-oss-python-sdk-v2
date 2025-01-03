import argparse
import base64
import alibabacloud_oss_v2 as oss


parser = argparse.ArgumentParser(description="select object csv sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--key', help='The name of the object.', required=True)
parser.add_argument('--expression', default='select * from ossobject')



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

    data = "name,school,company,age\nLora Francis,School,Staples Inc,27\n#Lora Francis,School,Staples Inc,27\nEleanor Little,School,\"Conectiv, Inc\",43\nRosie Hughes,School,Western Gas Resources Inc,44\nLawrence Ross,School,MetLife Inc.,24\n"


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

    result = client.select_object(oss.SelectObjectRequest(
        bucket=args.bucket,
        key=args.key,
        select_request=oss.SelectRequest(
            expression=base64.b64encode(args.expression.encode()).decode(),
            input_serialization=oss.InputSerialization(
                compression_type='None',
                csv_input=oss.CSVInput(
                    file_header_info='Ignore',
                    record_delimiter=base64.b64encode('\n'.encode()).decode(),
                    field_delimiter=base64.b64encode(','.encode()).decode(),
                    quote_character=base64.b64encode('\"'.encode()).decode(),
                    comment_character=base64.b64encode('#'.encode()).decode(),
                    allow_quoted_record_delimiter=True,
                ),
            ),
            output_serialization=oss.OutputSerialization(
                csv_output=oss.CSVOutput(
                    record_delimiter=base64.b64encode('\n'.encode()).decode(),
                    field_delimiter=base64.b64encode(','.encode()).decode(),
                    quote_character=base64.b64encode('\"'.encode()).decode(),
                ),
                output_raw_data=False,
                keep_all_columns=True,
                enable_payload_crc=True,
                output_header=False,
            ),
            options=oss.SelectOptions(
                skip_partial_data_record=False,
            ),
        ),
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' body: {result.body},'
    )

    content = b''
    try:
        for chunk in result.body:
            content += chunk
    except Exception as e:
        print(e)
    print(f'content: {content}')


if __name__ == "__main__":
    main()