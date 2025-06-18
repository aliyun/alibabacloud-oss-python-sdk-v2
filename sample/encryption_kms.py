import argparse
import base64
import json
from aliyunsdkkms.request.v20160120.DecryptRequest import DecryptRequest
from aliyunsdkkms.request.v20160120.EncryptRequest import EncryptRequest
from alibabacloud_dkms_transfer.kms_transfer_acs_client import KmsTransferAcsClient
from typing import Optional, Dict
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.crypto
from alibabacloud_oss_v2.encryption_client import EncryptionClient, EncryptionMultiPartContext


parser = argparse.ArgumentParser(description="encryption kms sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--key', help='The name of the object.', required=True)
parser.add_argument('--kms_id', help='The id of the your CMK ID.', required=True)


class MasterKmsCipher(oss.crypto.MasterCipher):

    def __init__(
        self,
        mat_desc: Optional[Dict] = None,
        kms_client: Optional[KmsTransferAcsClient] = None,
        kms_id: Optional[str] = None,
    ):
        self.kms_client = kms_client
        self.kms_id = kms_id
        self._mat_desc = None
        if mat_desc is not None and len(mat_desc.items()) > 0:
            self._mat_desc = json.dumps(mat_desc)


    def get_wrap_algorithm(self) -> str:
        return 'KMS/ALICLOUD'

    def get_mat_desc(self) -> str:
        return self._mat_desc or ''

    def encrypt(self, data: bytes) -> bytes:
        
        base64_crypto = base64.b64encode(data)
        request = EncryptRequest()
        request.set_KeyId(self.kms_id)
        request.set_Plaintext(base64_crypto)
        response = self.kms_client.do_action_with_exception(request)

        return base64.b64decode(json.loads(response).get('CiphertextBlob'))

    def decrypt(self, data: bytes) -> bytes:
        base64_crypto = base64.b64encode(data)
        request = DecryptRequest()
        request.set_CiphertextBlob(base64_crypto)
        response = self.kms_client.do_action_with_exception(request)

        return base64.b64decode(json.loads(response).get('Plaintext'))

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

    kms_client = KmsTransferAcsClient(ak=credentials_provider._credentials.access_key_id, secret=credentials_provider._credentials.access_key_secret, region_id=args.region)

    mc = MasterKmsCipher(
        mat_desc={"desc": "your master encrypt key material describe information"},
        kms_client=kms_client,
        kms_id=args.kms_id,
    )
    encryption_client = oss.EncryptionClient(client, mc)

    data = b'hello world'

    result = encryption_client.put_object(oss.PutObjectRequest(
        bucket=args.bucket,
        key=args.key,
        body=data,
    ))
    print(vars(result))


    result = encryption_client.get_object(oss.GetObjectRequest(
        bucket=args.bucket,
        key=args.key,
    ))
    print(vars(result))
    print(result.body.read())


if __name__ == "__main__":
    main()