import sys
import os

# It is used only to execute sample code in the project directory
code_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(code_directory)

import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="multipart upload sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--key', help='The name of the object.', required=True)
parser.add_argument('--file_path', help='The path of Upload file.', required=True)


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

    result = client.initiate_multipart_upload(oss.InitiateMultipartUploadRequest(
        bucket=args.bucket,
        key=args.key,
    ))

    part_size = 100 * 1024
    data_size = os.path.getsize(args.file_path)
    part_number = 1
    upload_parts = []
    with open(args.file_path, 'rb') as f:
        for start in range(0, data_size, part_size):
            n = part_size
            if start + n > data_size:
                n = data_size - start
            reader = oss.io_utils.SectionReader(oss.io_utils.ReadAtReader(f), start, n)
            up_result = client.upload_part(oss.UploadPartRequest(
                bucket=args.bucket,
                key=args.key,
                upload_id=result.upload_id,
                part_number=part_number,
                body=reader
            ))
            print(f'status code: {up_result.status_code},'
                  f' request id: {up_result.request_id},'
                  f' part number: {part_number},'
                  f' content md5: {up_result.content_md5},'
                  f' etag: {up_result.etag},'
                  f' hash crc64: {up_result.hash_crc64},'
                  )
            upload_parts.append(oss.UploadPart(part_number=part_number, etag=up_result.etag))
            part_number += 1

    parts = sorted(upload_parts, key=lambda p: p.part_number)
    result = client.complete_multipart_upload(oss.CompleteMultipartUploadRequest(
        bucket=args.bucket,
        key=args.key,
        upload_id=result.upload_id,
        complete_multipart_upload=oss.CompleteMultipartUpload(
            parts=parts
        )
    ))

    # Merge fragmented data into a complete Object through the server-side List method
    # result = client.complete_multipart_upload(oss.CompleteMultipartUploadRequest(
    #     bucket=args.bucket,
    #     key=args.key,
    #     upload_id=result.upload_id,
    #     complete_all='yes'
    # ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' bucket: {result.bucket},' 
          f' key: {result.key},' 
          f' location: {result.location},' 
          f' etag: {result.etag},' 
          f' encoding type: {result.encoding_type},' 
          f' hash crc64: {result.hash_crc64},' 
          f' version id: {result.version_id},'
    )

if __name__ == "__main__":
    main()