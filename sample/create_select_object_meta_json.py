import argparse
import base64
import alibabacloud_oss_v2 as oss


parser = argparse.ArgumentParser(description="create select object meta json sample")
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

    data = "{\n\t\"name\": \"Lora Francis\",\n\t\"age\": 27,\n\t\"company\": \"Staples Inc\"\n}\n{\n\t\"k2\": [-1, 79, 90],\n\t\"k3\": {\n\t\t\"k2\": 5,\n\t\t\"k3\": 1,\n\t\t\"k4\": 0\n\t}\n}\n{\n\t\"k1\": 1,\n\t\"k2\": {\n\t\t\"k2\": 5\n\t},\n\t\"k3\": []\n}"

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
        process='json/meta',
        select_meta_request=oss.JSONMetaRequest(
            overwrite_if_exists=True,
            input_serialization=oss.InputSerialization(
                json=oss.JSONInput(
                    type='LINES',
                ),
                compression_type=None,
            ),
        ),
    )

    result = client.create_select_object_meta(request)

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' splits: {result.splits_count},'
          f' row: {result.rows_count},'
    )


if __name__ == "__main__":
    main()

