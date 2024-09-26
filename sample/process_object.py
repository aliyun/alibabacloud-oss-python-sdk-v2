import base64
import sys
import os

# It is used only to execute sample code in the project directory
code_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(code_directory)

import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="process object sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--key', help='The name of the object.', required=True)
parser.add_argument('--style', help='The name of the object style.', required=True)
parser.add_argument('--target_image', help='Specify the name of the processed image.', required=True)
parser.add_argument('--target_bucket', help='Specify the name of the bucket used to store processed images.', required=True)


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

    # Scale the image to a fixed width and height of 100 px.
    # style = 'image/resize,m_fixed,w_100,h_100'
    style = args.style
    target_bucket_base64 = base64.b64encode(args.target_bucket.encode()).decode()
    target_key_base64 = base64.b64encode(args.target_image.encode()).decode()
    process = f"{style}|sys/saveas,o_{target_key_base64},b_{target_bucket_base64}"

    result = client.process_object(oss.ProcessObjectRequest(
        bucket=args.bucket,
        key=args.key,
        process=process,
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' bucket: {result.bucket},' 
          f' file size: {result.file_size},' 
          f' key: {result.key},' 
          f' process status: {result.process_status},'
    )


if __name__ == "__main__":
    main()
