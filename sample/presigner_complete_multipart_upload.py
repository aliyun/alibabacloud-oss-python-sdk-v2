import argparse
import os
import requests
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="presign multipart upload sample")
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

    part_size = 100 * 1024
    data_size = os.path.getsize(args.file_path)
    part_number = 1
    upload_parts = []

    init_pre_result = client.presign(oss.InitiateMultipartUploadRequest(
        bucket=args.bucket,
        key=args.key,
    ))
    with requests.post(init_pre_result.url, headers=init_pre_result.signed_headers) as resp:
        obj = oss.InitiateMultipartUploadResult()
        oss.serde.deserialize_xml(xml_data=resp.content, obj=obj)

        with open(args.file_path, 'rb') as f:
            for start in range(0, data_size, part_size):
                n = part_size
                if start + n > data_size:
                    n = data_size - start
                reader = oss.io_utils.SectionReader(oss.io_utils.ReadAtReader(f), start, n)
                up_pre_result = client.presign(oss.UploadPartRequest(
                    bucket=args.bucket,
                    key=args.key,
                    upload_id=obj.upload_id,
                    part_number=part_number,
                ))

                with requests.put(up_pre_result.url, headers=up_pre_result.signed_headers, data=reader) as up_result:
                    print(f'status code: {up_result.status_code},'
                          f' request id: {up_result.headers.get("x-oss-request-id")},'
                          f' part number: {part_number},'
                          f' hash crc64: {up_result.headers.get("x-oss-hash-crc64ecma")},'
                          f' content md5: {up_result.headers.get("Content-MD5")},'
                          f' etag: {up_result.headers.get("ETag")},'
                          f' server time: {up_result.headers.get("x-oss-server-time")},'
                          )

                    upload_parts.append(oss.UploadPart(part_number=part_number, etag=up_result.headers.get("ETag")))
                part_number += 1

        parts = sorted(upload_parts, key=lambda p: p.part_number)


        request = oss.CompleteMultipartUploadRequest(
            bucket=args.bucket,
            key=args.key,
            upload_id=obj.upload_id,
            complete_multipart_upload=oss.CompleteMultipartUpload(
                parts=parts
            )
        )

        # Merge fragmented data into a complete Object through the server-side List method
        # request = oss.CompleteMultipartUploadRequest(
        #     bucket=args.bucket,
        #     key=args.key,
        #     upload_id=obj.upload_id,
        #     complete_all='yes'
        # )


        op_input = oss.serde.serialize_input(request, oss.OperationInput(
            op_name='CompleteMultipartUpload',
            method='POST',
            bucket=request.bucket,
        ))

        complete_pre_result = client.presign(request)

        with requests.post(complete_pre_result.url, headers=complete_pre_result.signed_headers, data=op_input.body) as complete_resp:
            result = oss.CompleteMultipartUploadResult()
            oss.serde.deserialize_xml(xml_data=complete_resp.content, obj=result)
            print(f'status code: {complete_resp.status_code},'
                  f' request id: {complete_resp.headers.get("x-oss-request-id")},'
                  f' hash crc64: {complete_resp.headers.get("x-oss-hash-crc64ecma")},'
                  f' content md5: {complete_resp.headers.get("Content-MD5")},'
                  f' etag: {complete_resp.headers.get("ETag")},'
                  f' content length: {complete_resp.headers.get("content-length")},'
                  f' content type: {complete_resp.headers.get("Content-Type")},'
                  f' url: {result.location},'
                  f' encoding type: {result.encoding_type},'
                  f' server time: {complete_resp.headers.get("x-oss-server-time")},'
                  )

        print(f'method: {complete_pre_result.method},'
              f' expiration: {complete_pre_result.expiration.strftime("%Y-%m-%dT%H:%M:%S.000Z")},'
              f' url: {complete_pre_result.url}'
              )

        for key, value in complete_pre_result.signed_headers.items():
            print(f'signed headers key: {key}, signed headers value: {value}')


if __name__ == "__main__":
    main()
