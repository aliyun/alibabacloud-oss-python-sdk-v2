import sys
import os
import time

# It is used only to execute sample code in the project directory
code_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(code_directory)

import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="restore object sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--key', help='The name of the object.', required=True)


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

    result = client.restore_object(oss.RestoreObjectRequest(
        bucket=args.bucket,
        key=args.key,
        restore_request=oss.RestoreRequest(
            days=1,
            # The restoration priority of Cold Archive or Deep Cold Archive objects.
            # Valid values:Expedited,Standard,Bulk
            tier="Expedited",
        )
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' version id: {result.version_id},'
          f' restore priority: {result.restore_priority},'
    )


    while True:
        result = client.head_object(oss.HeadObjectRequest(
            bucket=args.bucket,
            key=args.key,
        ))

        if result.restore and result.restore != 'ongoing-request="true"':
            print('restore is sucess')
            break
        time.sleep(5)
        print(result.restore)

if __name__ == "__main__":
    main()

