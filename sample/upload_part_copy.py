import sys
import os

# It is used only to execute sample code in the project directory
code_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(code_directory)

import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="upload part copy synchronously sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--key', help='The name of the object.', required=True)
parser.add_argument('--source_bucket', help='The name of the source bucket.', required=True)
parser.add_argument('--source_key', help='The name of the source object.', required=True)


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

    result_meta = client.get_object_meta(oss.GetObjectMetaRequest(
        bucket=args.source_bucket,
        key=args.source_key,
    ))

    result = client.initiate_multipart_upload(oss.InitiateMultipartUploadRequest(
        bucket=args.bucket,
        key=args.key,
    ))

    part_size = 100 * 1024
    total_size = result_meta.content_length
    part_number = 1
    upload_parts = []
    offset = 0
    while offset < total_size:
        num_to_upload = min(part_size, total_size - offset)
        end = offset + num_to_upload - 1
        up_result = client.upload_part_copy(oss.UploadPartCopyRequest(
            bucket=args.bucket,
            key=args.key,
            upload_id=result.upload_id,
            part_number=part_number,
            source_bucket=args.source_bucket,
            source_key=args.source_key,
            source_range='bytes=' + str(offset) + '-' + str(end),
        ))
        print(f'status code: {up_result.status_code},'
              f' request id: {up_result.request_id},'
              f' part number: {part_number},'
              f' last modified: {up_result.last_modified},'
              f' etag: {up_result.etag},'
              f' source version id: {up_result.source_version_id},'
              )
        upload_parts.append(oss.UploadPart(part_number=part_number, etag=up_result.etag))
        offset += num_to_upload
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