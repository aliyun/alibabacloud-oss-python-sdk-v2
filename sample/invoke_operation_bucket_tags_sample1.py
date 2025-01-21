import argparse
import base64
import hashlib
from requests.structures import CaseInsensitiveDict
from alibabacloud_oss_v2 import OperationInput
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="invoke operation bucket tags sample")
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


    xml_data = r'''
<?xml version="1.0" encoding="UTF-8"?>
<Tagging>
  <TagSet>
    <Tag>
      <Key>testa</Key>
      <Value>value1-test</Value>
    </Tag>
    <Tag>
      <Key>testb</Key>
      <Value>value2-test</Value>
    </Tag>
  </TagSet>
</Tagging>
    '''
    h = hashlib.md5()
    h.update(xml_data.encode())
    md5 = base64.b64encode(h.digest()).decode()

    op_input=OperationInput(
        op_name='PutBucketTags',
        method='PUT',
        headers=CaseInsensitiveDict({
            'Content-Type': 'application/xml',
            'Content-MD5': md5,
        }),
        parameters={
            'tagging': '',
        },
        bucket=args.bucket,
        op_metadata={'sub-resource': ['tagging']},
        body=xml_data.encode(),
    )

    op_output = client.invoke_operation(op_input)

    print(f'status code: {op_output.status_code},'
            f' request id: {op_output.headers.get("x-oss-request-id", "")},'
    )


    # get bucket tags
    op_input=OperationInput(
        op_name='GetBucketTags',
        method='GET',
        parameters={
            'tagging': '',
        },
        bucket=args.bucket,
        op_metadata={'sub-resource': ['tagging']},
    )

    op_output = client.invoke_operation(op_input)

    print(f'status code: {op_output.status_code},'
            f' request id: {op_output.headers.get("x-oss-request-id", "")},'
            f' content: {op_output.http_response.content},'
    )


    # delete bucket tags
    op_input=OperationInput(
        op_name='DeleteBucketTags',
        method='DELETE',
        parameters={
            'tagging': '',
        },
        bucket=args.bucket,
        op_metadata={'sub-resource': ['tagging']},
    )

    op_output = client.invoke_operation(op_input)

    print(f'status code: {op_output.status_code},'
            f' request id: {op_output.headers.get("x-oss-request-id", "")},'
    )



if __name__ == "__main__":
    main()