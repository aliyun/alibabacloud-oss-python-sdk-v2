import sys
import os

# It is used only to execute sample code in the project directory
code_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(code_directory)

import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="put object tagging sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--key', help='The name of the object.', required=True)
parser.add_argument('--tag_key', help='The name of the tag key.', required=True)
parser.add_argument('--tag_value', help='The name of the tag value.', required=True)


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

    # If multiple tags are set, please follow the following format
    # tags = [oss.Tag(
    #     key=args.tag_key,
    #     value=args.tag_value,
    # ), oss.Tag(
    #     key=args.tag_key2,
    #     value=args.tag_value2,
    # )]

    result = client.put_object_tagging(oss.PutObjectTaggingRequest(
        bucket=args.bucket,
        key=args.key,
        tagging=oss.Tagging(
            tag_set=oss.TagSet(
                tags=[oss.Tag(
                    key=args.tag_key,
                    value=args.tag_value,
                )],
            ),
        ),
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' version id: {result.version_id},'
    )

if __name__ == "__main__":
    main()
