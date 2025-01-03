import argparse
import base64

import alibabacloud_oss_v2 as oss


parser = argparse.ArgumentParser(description="select object json sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--key', help='The name of the object.', required=True)
parser.add_argument('--expression', default="select person.firstname as aaa as firstname, person.lastname, extra from ossobject'")
parser.add_argument('--json_file_path', default='../tests/data/sample_json.json')
parser.add_argument('--json_lines_path', default='../tests/data/sample_json_lines.json')


def main():
    str = ",".encode('utf-8')

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

    result = client.put_object_from_file(oss.PutObjectRequest(
        bucket=args.bucket,
        key=args.key
    ), args.json_lines_path)

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
        process='json/meta',
        select_meta_request=oss.JSONMetaRequest(
            input_serialization=oss.InputSerialization(
                json=oss.JSONInput(
                    type='LINES',
                ),
            ),
        ),
    )

    result = client.create_select_object_meta(request)

    result = client.select_object(oss.SelectObjectRequest(
        bucket=args.bucket,
        key=args.key,
        process='json/select',
        select_request=oss.SelectRequest(
            expression=base64.b64encode(args.expression.encode()).decode(),
            input_serialization=oss.InputSerialization(
                json=oss.JSONInput(
                    type='LINES',
                    range='line-range=10-50',
                ),

            ),
            output_serialization=oss.OutputSerialization(
                json=oss.JSONOutput(
                    record_delimiter=base64.b64encode(','.encode()).decode(),
                )
            )
        ),
    ))

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

