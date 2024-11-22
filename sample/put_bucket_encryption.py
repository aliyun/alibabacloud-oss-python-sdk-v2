import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="put bucket encryption sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--sse_algorithm', help='The default server-side encryption method. Valid values: KMS, AES256, and SM4.', default='KMS')
parser.add_argument('--kms_master_key_id', help='The CMK ID that is specified when SSEAlgorithm is set to KMS and a specified CMK is used for encryption. In other cases, leave this parameter empty.', default='')
parser.add_argument('--kms_data_encryption', help='The algorithm that is used to encrypt objects. If this parameter is not specified, objects are encrypted by using AES256. This parameter is valid only when SSEAlgorithm is set to KMS. Valid value: SM4', default='SM4')


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

    result = client.put_bucket_encryption(oss.PutBucketEncryptionRequest(
            bucket=args.bucket,
            server_side_encryption_rule=oss.ServerSideEncryptionRule(
                apply_server_side_encryption_by_default=oss.ApplyServerSideEncryptionByDefault(
                    kms_master_key_id=args.kms_master_key_id,
                    kms_data_encryption=args.kms_data_encryption,
                    sse_algorithm=args.sse_algorithm,
                ),
            ),
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
    )


if __name__ == "__main__":
    main()