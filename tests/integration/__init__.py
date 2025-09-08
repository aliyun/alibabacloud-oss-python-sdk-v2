# pylint: skip-file

import os
import random
import string
import datetime
import hmac
import hashlib
import base64
import json
import unittest
from urllib.parse import quote
import requests
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.vectors as oss_vectors


ACCESS_ID = os.getenv("OSS_TEST_ACCESS_KEY_ID")
ACCESS_KEY = os.getenv("OSS_TEST_ACCESS_KEY_SECRET")
ENDPOINT = os.getenv("OSS_TEST_ENDPOINT")
REGION = os.getenv("OSS_TEST_REGION", "cn-hangzhou")
RAM_ROLE_ARN = os.getenv("OSS_TEST_RAM_ROLE_ARN")
SIGNATURE_VERSION = os.getenv("OSS_TEST_SIGNATURE_VERSION")
USER_ID = os.getenv("OSS_TEST_USER_ID")
RAM_ROLE_NAME = RAM_ROLE_ARN[str.find(RAM_ROLE_ARN, ':role/') + 6:] if RAM_ROLE_ARN is not None else os.getenv("RAM_ROLE_NAME")

PAYER_ACCESS_ID = os.getenv("OSS_TEST_PAYER_ACCESS_KEY_ID")
PAYER_ACCESS_KEY = os.getenv("OSS_TEST_PAYER_ACCESS_KEY_SECRET")
PAYER_UID = os.getenv("OSS_TEST_PAYER_UID")

BUCKETNAME_PREFIX = "python-sdk-test-bucket-"
OBJECTNAME_PREFIX = "python-sdk-test-object-"

_defaultClient :oss.Client = None
_invalidAkClient :oss.Client = None
_signV1Client :oss.Client = None


class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = get_default_client()
        cls.invalid_client = get_invalid_ak_client()
        cls.signv1_client = get_signv1_client()
        cls.bucket_name = random_bucket_name()
        cls.client.put_bucket(oss.models.PutBucketRequest(bucket=cls.bucket_name))

    @classmethod
    def tearDownClass(cls):
        clean_buckets(BUCKETNAME_PREFIX)


def get_default_client() -> oss.Client:
    global _defaultClient
    if _defaultClient is not None:
        return _defaultClient

    cfg = oss.config.load_default()
    cfg.credentials_provider = oss.credentials.StaticCredentialsProvider(ACCESS_ID, ACCESS_KEY)
    cfg.region = REGION
    cfg.endpoint = ENDPOINT
    _defaultClient = oss.Client(cfg)

    return _defaultClient

def get_invalid_ak_client() -> oss.Client:
    global _invalidAkClient
    if _invalidAkClient is not None:
        return _invalidAkClient

    cfg = oss.config.load_default()
    cfg.credentials_provider = oss.credentials.StaticCredentialsProvider('invalid-ak', 'invalid')
    cfg.region = REGION
    cfg.endpoint = ENDPOINT
    _invalidAkClient = oss.Client(cfg)

    return _invalidAkClient

def get_signv1_client() -> oss.Client:
    global _signV1Client
    if _signV1Client is not None:
        return _signV1Client

    cfg = oss.config.load_default()
    cfg.credentials_provider = oss.credentials.StaticCredentialsProvider(ACCESS_ID, ACCESS_KEY)
    cfg.signature_version = 'v1'
    cfg.region = REGION
    cfg.endpoint = ENDPOINT
    _signV1Client = oss.Client(cfg)

    return _signV1Client

def get_client(region:str, endpoint:str) -> oss.Client:
    cfg = oss.config.load_default()
    cfg.credentials_provider = oss.credentials.StaticCredentialsProvider(ACCESS_ID, ACCESS_KEY)
    cfg.region = region
    cfg.endpoint = endpoint
    return oss.Client(cfg)

def get_vectors_client() -> oss_vectors.Client:
    cfg = oss.config.load_default()
    cfg.credentials_provider = oss.credentials.StaticCredentialsProvider(ACCESS_ID, ACCESS_KEY)
    cfg.region = REGION
    cfg.endpoint = ENDPOINT
    cfg.account_id = USER_ID
    return oss_vectors.Client(cfg)

def get_client_use_ststoken(region:str, endpoint:str) -> oss.Client:
    result = sts_assume_role(ACCESS_ID, ACCESS_KEY, RAM_ROLE_ARN)
    cfg = oss.config.load_default()
    cfg.credentials_provider = oss.credentials.StaticCredentialsProvider(
        result['Credentials']['AccessKeyId'],
        result['Credentials']['AccessKeySecret'],
        result['Credentials']['SecurityToken']
    )
    cfg.region = region
    cfg.endpoint = endpoint
    return oss.Client(cfg)


def get_kms_id(region:str) ->str:
    return

def random_lowstr(n):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(n))

def random_str(n):
    return ''.join(random.choice(string.ascii_letters) for i in range(n))

def random_bucket_name():
    return BUCKETNAME_PREFIX + random_lowstr(4) + '-' + str(int(datetime.datetime.now(datetime.timezone.utc).timestamp()))

def clean_objects(client:oss.Client, bucket_name:str) -> None:
    marker = ''
    is_truncated = True
    while is_truncated:
        result = client.list_objects(oss.ListObjectsRequest(bucket=bucket_name, marker=marker))
        if result.contents is not None:
            delete_object = []
            for o in result.contents:
                delete_object.append(oss.DeleteObject(key=o.key))

            if len(delete_object) > 0:
                client.delete_multiple_objects(oss.DeleteMultipleObjectsRequest(
                    bucket=bucket_name,
                    objects=delete_object))
        is_truncated = result.is_truncated
        marker = result.next_marker


def clean_parts(client:oss.Client, bucket_name:str) -> None:
    marker = ''
    is_truncated = True
    while is_truncated:
        result = client.list_multipart_uploads(oss.ListMultipartUploadsRequest(
            bucket=bucket_name,
            upload_id_marker=marker
        ))
        if result.uploads is not None:
            for o in result.uploads:
                client.abort_multipart_upload(oss.AbortMultipartUploadRequest(
                    bucket=bucket_name,
                    key=o.key,
                    upload_id=o.upload_id
                ))

        is_truncated = result.is_truncated
        marker = result.next_upload_id_marker


def clean_bucket(props:oss.BucketProperties) -> None:
    if props.intranet_endpoint == ENDPOINT or  props.extranet_endpoint == ENDPOINT:
        client = get_default_client()
    else:
        client = get_client(props.region, props.extranet_endpoint)
    clean_objects(client, props.name)
    clean_parts(client, props.name)
    client.delete_bucket(oss.DeleteBucketRequest(bucket=props.name))


def clean_buckets(prefix:str) -> None:
    client = get_default_client()
    result = client.list_buckets(oss.ListBucketsRequest(
        prefix=BUCKETNAME_PREFIX
    ))
    for props in result.buckets:
        clean_bucket(props)

def sts_assume_role(access_key_id:str, access_key_secret:str, role_arn:str) -> dict:
    # StsSignVersion sts sign version
    StsSignVersion = "1.0"
    # StsAPIVersion sts api version
    StsAPIVersion = "2015-04-01"
    # StsHost sts host
    StsHost = "https://sts.aliyuncs.com/"
    # TimeFormat time fomrat
    TimeFormat = '%Y-%m-%dT%H:%M:%SZ'
    # RespBodyFormat  respone body format
    RespBodyFormat = "JSON"
    # PercentEncode '/'
    PercentEncode = "%2F"
    # HTTPGet http get method
    HTTPGet = "GET"
    uuid = f"Nonce-{str(random.randint(0, 10000))}"
    queryStr = "SignatureVersion=" + StsSignVersion
    queryStr += "&Format=" + RespBodyFormat
    queryStr += "&Timestamp=" + quote(datetime.datetime.now(datetime.timezone.utc).strftime(TimeFormat), safe='')
    queryStr += "&RoleArn=" + quote(role_arn, safe='')
    queryStr += "&RoleSessionName=" + "oss_test_sess"
    queryStr += "&AccessKeyId=" + access_key_id
    queryStr += "&SignatureMethod=HMAC-SHA1"
    queryStr += "&Version=" + StsAPIVersion
    queryStr += "&Action=AssumeRole"
    queryStr += "&SignatureNonce=" + uuid
    queryStr += "&DurationSeconds=3600"

    #Sort query string
    key_val_pairs = []
    for pair in queryStr.split('&'):
        key, _, value = pair.partition('=')
        key_val_pairs.append((key, value))

    sorted_key_vals = []
    for key, value in sorted(key_val_pairs):
        sorted_key_vals.append(f'{key}={value}')

    str_to_sign = HTTPGet + "&" + PercentEncode + "&" + quote('&'.join(sorted_key_vals), safe='')

	# Generate signature
    h = hmac.new((access_key_secret+"&").encode(), str_to_sign.encode(), hashlib.sha1)
    signature = base64.b64encode(h.digest()).decode()

    # Build url
    assume_url = StsHost + "?" + queryStr + "&Signature=" + quote(signature, safe='')

    response = requests.get(assume_url)

    return json.loads(response.content)
    

class TestIntegrationVectors(TestIntegration):
    
    @classmethod
    def setUpClass(cls):
        TestIntegration.setUpClass()
        cls.vector_client = get_vectors_client()

    @classmethod
    def tearDownClass(cls):
        TestIntegration.tearDownClass()


