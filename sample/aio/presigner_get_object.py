import asyncio
import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.aio as oss_aio

parser = argparse.ArgumentParser(description="presign get object sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--key', help='The name of the object.', required=True)


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

    pre_result = await client.presign(oss.GetObjectRequest(
        bucket=args.bucket,
        key=args.key,
    ))

    print(f'method: {pre_result.method},'
          f' expiration: {pre_result.expiration.strftime("%Y-%m-%dT%H:%M:%S.000Z")},'
          f' url: {pre_result.url}'
    )

    for key, value in pre_result.signed_headers.items():
        print(f'signed headers key: {key}, signed headers value: {value}')

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
