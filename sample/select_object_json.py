import argparse
import base64
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="select object json sample")
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

    data = "{\t\"name\":\"Eleanor Little\",\n\t\"age\":43,\n\t\"company\":\"Conectiv, Inc\"}\n{\t\"name\":\"Rosie Hughes\",\n\t\"age\":44,\n\t\"company\":\"Western Gas Resources Inc\"}\n"

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

    request = oss.SelectObjectRequest(
        bucket=args.bucket,
        key=args.key,
        select_request=oss.SelectRequest(
            expression=base64.b64encode(args.expression.encode()).decode(),
            input_serialization=oss.InputSerialization(
                compression_type=None,
                json=oss.JSONInput(
                    type='LINES',
                    parse_json_number_as_string=True,
                ),
            ),
            output_serialization=oss.OutputSerialization(
                json=oss.JSONOutput(
                    record_delimiter=base64.b64encode('\n'.encode()).decode(),
                ),
                output_raw_data=False,
                keep_all_columns=True,
                enable_payload_crc=True,
                output_header=False,
            ),
            options=oss.SelectRequestOptions(
                skip_partial_data_record=False,
            ),
        ),
    )

    result = client.select_object(request)

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' body: {result.body},'
    )

    # Load all the data into memory and then process it.
    with result.body as f:
        data = f.read()
        # TODO

    # # Read a block, process a block.
    # with result.body as f:
    #     # You can control the size of the data returned each time by setting the block_size parameter.
    #     # for chunk in f.iter_bytes(block_size=256*1024):
    #     for chunk in f.iter_bytes():
    #         # TODO
    #         pass


if __name__ == "__main__":
    main()