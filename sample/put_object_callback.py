import base64
import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="put object sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--key', help='The name of the object.', required=True)
parser.add_argument('--callback_url', help='Callback server address.', required=True)


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

    data = "name,school,company,age\nLora Francis,School,Staples Inc,27\n#Lora Francis,School,Staples Inc,27\nEleanor Little,School,\"Conectiv, Inc\",43\nRosie Hughes,School,Western Gas Resources Inc,44\nLawrence Ross,School,MetLife Inc.,24\n"

    result = client.put_object(oss.PutObjectRequest(
        bucket=args.bucket,
        key=args.key,
        body=data,
        callback=base64.b64encode(str('{\"callbackUrl\":\"' + args.callback_url + '\",\"callbackBody\":\"bucket=${bucket}&object=${object}&my_var_1=${x:var1}&my_var_2=${x:var2}\"}').encode()).decode(),
        callback_var=base64.b64encode('{\"x:var1\":\"value1\",\"x:var2\":\"value2\"}'.encode()).decode(),
        headers={
            'Content-Type': 'text/plain',
            'Cache-Control': 'no-cache',
            'content-language': 'zh-CN',
            'content-encoding': 'gzip',
            'Content-Disposition': 'attachment;filename=aaa.txt',
            'Expires': '2022-10-12T00:00:00.000Z',
            'auth': 'owner',
            'x-oss-auth': 'owner2',
            'x-oss-meta-auth': 'owner3',
        }
    ))

    print(vars(result))


if __name__ == "__main__":
    main()
