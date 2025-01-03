import argparse
import base64
import csv
import json
import re

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
        json_meta_request=oss.JsonMetaRequest(
            input_serialization=oss.InputSerialization(
                json_input=oss.JSONInput(
                    type='LINES',
                ),
            ),
        ),
    )

    result = client.create_select_object_meta(request)

    result = client.select_object(oss.SelectObjectRequest(
        bucket=args.bucket,
        key=args.key,
        select_request=oss.SelectRequest(
            expression=base64.b64encode(args.expression.encode()).decode(),
            input_serialization=oss.InputSerialization(
                json_input=oss.JSONInput(
                    type='LINES',
                    range='line-range=10-50',
                ),

            ),
            output_serialization=oss.OutputSerialization(
                json_output=oss.JSONOutput(
                    record_delimiter=base64.b64encode(','.encode()).decode(),
                )
            )
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

    content = content[0:len(content) - 1]  # remove the last ','
    content = b"[" + content + b"]"  # make json parser happy
    result = json.loads(content.decode('utf-8'))

    result_index = 0
    with open(args.json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        index = 0
        for row in data['objects']:
            select_row = {}
            if index >= 10 and index < 50:
                select_row['firstname'] = row['person']['firstname']
                select_row['lastname'] = row['person']['lastname']
                select_row['extra'] = row['extra']
                assert result[result_index] == select_row
                result_index += 1
            elif index >= 50:
                break
            index += 1


if __name__ == "__main__":
    main()

