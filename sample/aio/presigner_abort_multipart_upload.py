import asyncio
import argparse
import os
import aiohttp
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.aio as oss_aio

parser = argparse.ArgumentParser(description="presign abort multipart upload sample")
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
            print(f'[Init] status code: {resp.status},'
                  f' request id: {resp.headers.get("x-oss-request-id")},'
                  f' upload id: {obj.upload_id},'
                  )

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
                        print(f'[UploadPart] part number: {part_number},'
                              f' status code: {up_resp.status},'
                              f' etag: {up_resp.headers.get("ETag")},'
                              f' hash crc64: {up_resp.headers.get("x-oss-hash-crc64ecma")},'
                              )

                        upload_parts.append(oss.UploadPart(
                            part_number=part_number,
                            etag=up_resp.headers.get("ETag")))
                    part_number += 1

            # Step 3: Presign AbortMultipartUpload (DELETE) to discard uploaded parts
            abort_pre_result = await client.presign(oss.AbortMultipartUploadRequest(
                bucket=args.bucket,
                key=args.key,
                upload_id=obj.upload_id,
            ))

            print(f'AbortMultipartUpload presign:'
                  f' method: {abort_pre_result.method},'
                  f' expiration: {abort_pre_result.expiration.strftime("%Y-%m-%dT%H:%M:%S.000Z")},'
                  f' url: {abort_pre_result.url}')

            for key, value in abort_pre_result.signed_headers.items():
                print(f'signed headers key: {key}, signed headers value: {value}')

            async with session.delete(
                abort_pre_result.url,
                headers=abort_pre_result.signed_headers,
                skip_auto_headers=['Content-Type'],
            ) as abort_resp:
                print(f'[Abort] status code: {abort_resp.status},'
                      f' request id: {abort_resp.headers.get("x-oss-request-id")},'
                      f' server time: {abort_resp.headers.get("x-oss-server-time")},'
                      )

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
