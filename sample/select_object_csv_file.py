import argparse
import base64
import csv
import re

import alibabacloud_oss_v2 as oss


parser = argparse.ArgumentParser(description="select object csv sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--key', help='The name of the object.', required=True)
parser.add_argument('--expression', default="select Year,StateAbbr, CityName, Short_Question_Text from ossobject where (data_value || data_value_unit) = '14.8%'")
parser.add_argument('--file_path', default='../tests/data/sample_data.csv')



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
    ), args.file_path)

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
                csv_input=oss.CSVInput(
                    file_header_info='Use',
                ),
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

    select_data = b''
    with open(args.file_path, 'r', encoding='utf-8') as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            line = b''
            if row['Data_Value_Unit'] == '%' and row['Data_Value'] == '14.8':
                line += row['Year'].encode('utf-8')
                line += ','.encode('utf-8')
                line += row['StateAbbr'].encode('utf-8')
                line += ','.encode('utf-8')
                line += row['CityName'].encode('utf-8')
                line += ','.encode('utf-8')
                line += row['Short_Question_Text'].encode('utf-8')
                line += '\n'.encode('utf-8')
                select_data += line

        print(select_data)
        assert select_data == content


if __name__ == "__main__":
    main()

