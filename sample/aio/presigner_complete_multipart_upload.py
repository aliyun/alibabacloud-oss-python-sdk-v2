import asyncio
import argparse
import os
import aiohttp
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.aio as oss_aio

parser = argparse.ArgumentParser(description="presign multipart upload sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--key', help='The name of the object.', required=True)
parser.add_argument('--file_path', help='The path of Upload file.', required=True)


async def main():
    args = parser.parse_args()

    # Loading credentials values from the environment variables
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    # Using the SDK's default configuration
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint

    client = oss_aio.AsyncClient(cfg)

    part_size = 100 * 1024
    data_size = os.path.getsize(args.file_path)
    part_number = 1
    upload_parts = []

    # Step 1: Presign InitiateMultipartUpload (POST)
    init_pre_result = await client.presign(oss.InitiateMultipartUploadRequest(
        bucket=args.bucket,
        key=args.key,
    ))

    print(f'InitiateMultipartUpload presign:'
          f' method: {init_pre_result.method},'
          f' url: {init_pre_result.url}')

    async with aiohttp.ClientSession() as session:
        async with session.post(
            init_pre_result.url,
            headers=init_pre_result.signed_headers,
            skip_auto_headers=['Content-Type'],
        ) as resp:
            content = await resp.read()
            obj = oss.InitiateMultipartUploadResult()
            oss.serde.deserialize_xml(xml_data=content, obj=obj)

            # Step 2: Presign UploadPart (PUT) for each part
            with open(args.file_path, 'rb') as f:
                for start in range(0, data_size, part_size):
                    n = part_size
                    if start + n > data_size:
                        n = data_size - start

                    data = f.read(n)

                    up_pre_result = await client.presign(oss.UploadPartRequest(
                        bucket=args.bucket,
                        key=args.key,
                        upload_id=obj.upload_id,
                        part_number=part_number,
                    ))

                    async with session.put(
                        up_pre_result.url,
                        headers=up_pre_result.signed_headers,
                        data=data,
                        skip_auto_headers=['Content-Type'],
                    ) as up_resp:
                        print(f'UploadPart presign: part number: {part_number},'
                              f' status code: {up_resp.status},'
                              f' etag: {up_resp.headers.get("ETag")}')

                        upload_parts.append(oss.UploadPart(
                            part_number=part_number,
                            etag=up_resp.headers.get("ETag")))
                    part_number += 1

            parts = sorted(upload_parts, key=lambda p: p.part_number)

            # Step 3: Presign CompleteMultipartUpload (POST)
            request = oss.CompleteMultipartUploadRequest(
                bucket=args.bucket,
                key=args.key,
                upload_id=obj.upload_id,
                complete_multipart_upload=oss.CompleteMultipartUpload(
                    parts=parts
                )
            )

            op_input = oss.serde.serialize_input(request, oss.OperationInput(
                op_name='CompleteMultipartUpload',
                method='POST',
                bucket=request.bucket,
            ))

            complete_pre_result = await client.presign(request)

            print(f'CompleteMultipartUpload presign:'
                  f' method: {complete_pre_result.method},'
                  f' url: {complete_pre_result.url}')

            for key, value in complete_pre_result.signed_headers.items():
                print(f'signed headers key: {key}, signed headers value: {value}')

            async with session.post(
                complete_pre_result.url,
                headers=complete_pre_result.signed_headers,
                data=op_input.body,
                skip_auto_headers=['Content-Type'],
            ) as complete_resp:
                resp_content = await complete_resp.read()
                result = oss.CompleteMultipartUploadResult()
                oss.serde.deserialize_xml(xml_data=resp_content, obj=result)
                print(f'status code: {complete_resp.status},'
                      f' request id: {complete_resp.headers.get("x-oss-request-id")},'
                      f' hash crc64: {complete_resp.headers.get("x-oss-hash-crc64ecma")},'
                      f' etag: {complete_resp.headers.get("ETag")},'
                      f' location: {result.location},'
                      )

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
