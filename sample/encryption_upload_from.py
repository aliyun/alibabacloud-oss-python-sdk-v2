import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="encryption upload from sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--key', help='The name of the object.', required=True)
parser.add_argument('--file_path', help='The path of Upload file.', required=True)

RSA_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIGfMA0G6mse2QsIgz3******GBcom6kEF6MmR1EKixaQIDAQAB
-----END PUBLIC KEY-----"""

RSA_PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
MIICdQIBADANBgk******ItewfwXIL1Mqz53lO/gK+q6TR92gGc+4ajL
-----END PRIVATE KEY-----"""


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

    mc = oss.crypto.MasterRsaCipher(
        mat_desc={"desc": "your master encrypt key material describe information"},
        public_key=RSA_PUBLIC_KEY,
        private_key=RSA_PRIVATE_KEY
    )
    encryption_client = oss.EncryptionClient(client, mc)
    up_loader = encryption_client.uploader(part_size=1000 * 1024,
                                           parallel_num=5,
                                           leave_parts_on_error=True,
                                           enable_checkpoint=True)


    with open(file=args.file_path, mode='rb') as f:
        result = up_loader.upload_from(oss.PutObjectRequest(
            bucket=args.bucket,
            key=args.key,
        ), reader=f)

    print(vars(result))

if __name__ == "__main__":
    main()

