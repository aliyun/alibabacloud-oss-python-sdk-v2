import base64
import os
import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="upload part sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--key', help='The name of the object.', required=True)
parser.add_argument('--file_path', help='The path of Upload file.', required=True)
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

    result = client.initiate_multipart_upload(oss.InitiateMultipartUploadRequest(
        bucket=args.bucket,
        key=args.key,
    ))
    print(vars(result))

    part_size = 100 * 1024
    data_size = os.path.getsize(args.filename)
    part_number = 1
    upload_parts = []
    with open(args.filename, 'rb') as f:
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
            print(vars(result))

            upload_parts.append(oss.UploadPart(part_number=part_number, etag=up_result.etag))
            part_number += 1

    parts = sorted(upload_parts, key=lambda p: p.part_number)
    result = client.complete_multipart_upload(oss.CompleteMultipartUploadRequest(
        bucket=args.bucket,
        key=args.key,
        upload_id=result.upload_id,
        complete_multipart_upload=oss.CompleteMultipartUpload(
            parts=parts
        ),
        callback=base64.b64encode(str('{\"callbackUrl\":\"'+args.callback_url+'\",\"callbackBody\":\"bucket=${bucket}&object=${object}&my_var_1=${x:var1}&my_var_2=${x:var2}\"}').encode()).decode(),
        callback_var=base64.b64encode('{\"x:var1\":\"value1\",\"x:var2\":\"value2\"}'.encode()).decode(),
    ))

    print(vars(result))

if __name__ == "__main__":
    main()