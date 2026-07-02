# pylint: skip-file
import datetime
import unittest
from urllib.parse import quote
from alibabacloud_oss_v2 import models as model
from alibabacloud_oss_v2 import config
from alibabacloud_oss_v2 import credentials
from alibabacloud_oss_v2.aio.client import AsyncClient
from alibabacloud_oss_v2 import exceptions


class TestPresignAsync(unittest.IsolatedAsyncioTestCase):
    async def test_presign_v1(self):
        cfg = config.load_default()
        cfg.region = 'cn-hangzhou'
        cfg.signature_version = 'v1'
        cfg.credentials_provider = credentials.StaticCredentialsProvider("ak", "sk")
        client = AsyncClient(cfg)

        request = model.GetObjectRequest(
            bucket='bucket',
            key='key'
        )

        expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        result = await client.presign(request, expiration=expiration)

        self.assertEqual('GET', result.method)
        self.assertEqual(expiration, result.expiration)
        self.assertEqual(0, len(result.signed_headers))
        self.assertIn("bucket.oss-cn-hangzhou.aliyuncs.com/key?", result.url)
        self.assertIn("OSSAccessKeyId=ak", result.url)
        self.assertIn(f'Expires={int(expiration.timestamp())}', result.url)
        self.assertIn("Signature=", result.url)

        expires = datetime.timedelta(minutes=50)
        expiration = datetime.datetime.now(datetime.timezone.utc) + expires
        result = await client.presign(request, expires=expires)
        self.assertEqual('GET', result.method)
        self.assertLess((result.expiration - expiration).seconds, 2)
        self.assertEqual(0, len(result.signed_headers))
        self.assertIn("bucket.oss-cn-hangzhou.aliyuncs.com/key?", result.url)
        self.assertIn("OSSAccessKeyId=ak", result.url)
        self.assertIn(f'Expires={int(result.expiration.timestamp())}', result.url)
        self.assertIn("Signature=", result.url)

        await client.close()

    async def test_presign_token_v1(self):
        cfg = config.load_default()
        cfg.region = 'cn-hangzhou'
        cfg.signature_version = 'v1'
        cfg.credentials_provider = credentials.StaticCredentialsProvider("ak", "sk", "token")
        client = AsyncClient(cfg)

        request = model.GetObjectRequest(
            bucket='bucket',
            key='key'
        )

        expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        result = await client.presign(request, expiration=expiration)

        self.assertEqual('GET', result.method)
        self.assertEqual(expiration, result.expiration)
        self.assertEqual(0, len(result.signed_headers))
        self.assertIn("bucket.oss-cn-hangzhou.aliyuncs.com/key?", result.url)
        self.assertIn("OSSAccessKeyId=ak", result.url)
        self.assertIn(f'Expires={int(expiration.timestamp())}', result.url)
        self.assertIn("Signature=", result.url)
        self.assertIn("security-token=token", result.url)

        await client.close()

    async def test_presign_with_header_v1(self):
        cfg = config.load_default()
        cfg.region = 'cn-hangzhou'
        cfg.signature_version = 'v1'
        cfg.credentials_provider = credentials.StaticCredentialsProvider("ak", "sk", "token")
        client = AsyncClient(cfg)

        request = model.GetObjectRequest(
            bucket='bucket',
            key='key',
            headers={"Content-Type": "application/octet-stream"},
        )

        expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        result = await client.presign(request, expiration=expiration)

        self.assertEqual('GET', result.method)
        self.assertEqual(expiration, result.expiration)
        self.assertEqual(1, len(result.signed_headers))
        self.assertEqual("application/octet-stream", result.signed_headers.get('Content-Type'))
        self.assertIn("bucket.oss-cn-hangzhou.aliyuncs.com/key?", result.url)
        self.assertIn("OSSAccessKeyId=ak", result.url)
        self.assertIn(f'Expires={int(expiration.timestamp())}', result.url)
        self.assertIn("Signature=", result.url)
        self.assertIn("security-token=token", result.url)

        await client.close()

    async def test_presign_v4(self):
        cfg = config.load_default()
        cfg.region = 'cn-hangzhou'
        cfg.signature_version = 'v4'
        cfg.credentials_provider = credentials.StaticCredentialsProvider("ak", "sk")
        client = AsyncClient(cfg)

        request = model.GetObjectRequest(
            bucket='bucket',
            key='key'
        )

        timedelta = datetime.timedelta(hours=1)
        datetime_now = datetime.datetime.now(datetime.timezone.utc)
        expiration = datetime_now + timedelta
        credential = f'ak/{datetime_now.strftime("%Y%m%d")}/cn-hangzhou/oss/aliyun_v4_request'

        result = await client.presign(request, expiration=expiration)

        self.assertEqual('GET', result.method)
        self.assertEqual(expiration, result.expiration)
        self.assertEqual(0, len(result.signed_headers))
        self.assertIn("bucket.oss-cn-hangzhou.aliyuncs.com/key?", result.url)
        self.assertIn(f'x-oss-date={datetime_now.strftime("%Y%m%dT%H%M%SZ")}', result.url)
        self.assertTrue(f'x-oss-expires={int(timedelta.seconds)}' in result.url or f'x-oss-expires={int(timedelta.seconds-1)}' in result.url)
        self.assertIn("x-oss-signature=", result.url)
        self.assertIn(f'x-oss-credential={quote(credential, safe="")}', result.url)
        self.assertIn("x-oss-signature-version=OSS4-HMAC-SHA256", result.url)

        timedelta = datetime.timedelta(minutes=50)
        datetime_now = datetime.datetime.now(datetime.timezone.utc)
        expiration = datetime_now + timedelta
        credential = f'ak/{datetime_now.strftime("%Y%m%d")}/cn-hangzhou/oss/aliyun_v4_request'

        result = await client.presign(request, expires=timedelta)

        self.assertEqual('GET', result.method)
        self.assertLess((result.expiration - expiration).seconds, 2)
        self.assertEqual(0, len(result.signed_headers))
        self.assertIn("bucket.oss-cn-hangzhou.aliyuncs.com/key?", result.url)
        self.assertIn(f'x-oss-date={datetime_now.strftime("%Y%m%dT%H%M%SZ")}', result.url)
        self.assertTrue(f'x-oss-expires={int(timedelta.seconds)}' in result.url or f'x-oss-expires={int(timedelta.seconds-1)}' in result.url)
        self.assertIn("x-oss-signature=", result.url)
        self.assertIn(f'x-oss-credential={quote(credential, safe="")}', result.url)
        self.assertIn("x-oss-signature-version=OSS4-HMAC-SHA256", result.url)

        await client.close()

    async def test_presign_token_v4(self):
        cfg = config.load_default()
        cfg.region = 'cn-hangzhou'
        cfg.signature_version = 'v4'
        cfg.credentials_provider = credentials.StaticCredentialsProvider("ak", "sk", "token")
        client = AsyncClient(cfg)

        request = model.GetObjectRequest(
            bucket='bucket',
            key='key'
        )

        timedelta = datetime.timedelta(hours=1)
        datetime_now = datetime.datetime.now(datetime.timezone.utc)
        expiration = datetime_now + timedelta
        credential = f'ak/{datetime_now.strftime("%Y%m%d")}/cn-hangzhou/oss/aliyun_v4_request'

        result = await client.presign(request, expiration=expiration)

        self.assertEqual('GET', result.method)
        self.assertEqual(expiration, result.expiration)
        self.assertEqual(0, len(result.signed_headers))
        self.assertIn("bucket.oss-cn-hangzhou.aliyuncs.com/key?", result.url)
        self.assertIn(f'x-oss-date={datetime_now.strftime("%Y%m%dT%H%M%SZ")}', result.url)
        self.assertTrue(f'x-oss-expires={int(timedelta.seconds)}' in result.url or f'x-oss-expires={int(timedelta.seconds-1)}' in result.url)
        self.assertIn("x-oss-signature=", result.url)
        self.assertIn(f'x-oss-credential={quote(credential, safe="")}', result.url)
        self.assertIn("x-oss-signature-version=OSS4-HMAC-SHA256", result.url)
        self.assertIn("x-oss-security-token=token", result.url)

        await client.close()

    async def test_presign_with_header_v4(self):
        cfg = config.load_default()
        cfg.region = 'cn-hangzhou'
        cfg.signature_version = 'v4'
        cfg.credentials_provider = credentials.StaticCredentialsProvider("ak", "sk", "token")
        client = AsyncClient(cfg)

        request = model.GetObjectRequest(
            bucket='bucket',
            key='key',
            headers={"Content-Type": "application/octet-stream"},
        )

        timedelta = datetime.timedelta(hours=1)
        datetime_now = datetime.datetime.now(datetime.timezone.utc)
        expiration = datetime_now + timedelta
        credential = f'ak/{datetime_now.strftime("%Y%m%d")}/cn-hangzhou/oss/aliyun_v4_request'

        result = await client.presign(request, expiration=expiration)

        self.assertEqual('GET', result.method)
        self.assertEqual(expiration, result.expiration)
        self.assertEqual(1, len(result.signed_headers))
        self.assertEqual("application/octet-stream", result.signed_headers.get('Content-Type'))
        self.assertIn("bucket.oss-cn-hangzhou.aliyuncs.com/key?", result.url)
        self.assertIn(f'x-oss-date={datetime_now.strftime("%Y%m%dT%H%M%SZ")}', result.url)
        self.assertTrue(f'x-oss-expires={int(timedelta.seconds)}' in result.url or f'x-oss-expires={int(timedelta.seconds-1)}' in result.url)
        self.assertIn("x-oss-signature=", result.url)
        self.assertIn(f'x-oss-credential={quote(credential, safe="")}', result.url)
        self.assertIn("x-oss-signature-version=OSS4-HMAC-SHA256", result.url)
        self.assertIn("x-oss-security-token=token", result.url)

        await client.close()

    async def test_presign_query_v1(self):
        cfg = config.load_default()
        cfg.region = 'cn-hangzhou'
        cfg.signature_version = 'v1'
        cfg.credentials_provider = credentials.StaticCredentialsProvider("ak", "sk")
        client = AsyncClient(cfg)

        request = model.GetObjectRequest(
            bucket='bucket',
            key='key',
            parameters={"x-oss-process": "abc"}
        )

        expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        result = await client.presign(request, expiration=expiration)

        self.assertEqual('GET', result.method)
        self.assertEqual(expiration, result.expiration)
        self.assertEqual(0, len(result.signed_headers))
        self.assertIn("bucket.oss-cn-hangzhou.aliyuncs.com/key?", result.url)
        self.assertIn("OSSAccessKeyId=ak", result.url)
        self.assertIn(f'Expires={int(expiration.timestamp())}', result.url)
        self.assertIn("Signature=", result.url)
        self.assertIn("x-oss-process=abc", result.url)

        expires = datetime.timedelta(minutes=50)
        expiration = datetime.datetime.now(datetime.timezone.utc) + expires
        result = await client.presign(request, expires=expires)
        self.assertEqual('GET', result.method)
        self.assertLess((result.expiration - expiration).seconds, 2)
        self.assertEqual(0, len(result.signed_headers))
        self.assertIn("bucket.oss-cn-hangzhou.aliyuncs.com/key?", result.url)
        self.assertIn("OSSAccessKeyId=ak", result.url)
        self.assertIn(f'Expires={int(result.expiration.timestamp())}', result.url)
        self.assertIn("Signature=", result.url)
        self.assertIn("x-oss-process=abc", result.url)

        await client.close()

    async def test_presign_query_v4(self):
        cfg = config.load_default()
        cfg.region = 'cn-hangzhou'
        cfg.signature_version = 'v4'
        cfg.credentials_provider = credentials.StaticCredentialsProvider("ak", "sk")
        client = AsyncClient(cfg)

        request = model.GetObjectRequest(
            bucket='bucket',
            key='key',
            parameters={"x-oss-process": "abc"}
        )

        timedelta = datetime.timedelta(hours=1)
        datetime_now = datetime.datetime.now(datetime.timezone.utc)
        expiration = datetime_now + timedelta
        credential = f'ak/{datetime_now.strftime("%Y%m%d")}/cn-hangzhou/oss/aliyun_v4_request'

        result = await client.presign(request, expiration=expiration)

        self.assertEqual('GET', result.method)
        self.assertEqual(expiration, result.expiration)
        self.assertEqual(0, len(result.signed_headers))
        self.assertIn("bucket.oss-cn-hangzhou.aliyuncs.com/key?", result.url)
        self.assertIn(f'x-oss-date={datetime_now.strftime("%Y%m%dT%H%M%SZ")}', result.url)
        self.assertTrue(f'x-oss-expires={int(timedelta.seconds)}' in result.url or f'x-oss-expires={int(timedelta.seconds-1)}' in result.url)
        self.assertIn("x-oss-signature=", result.url)
        self.assertIn(f'x-oss-credential={quote(credential, safe="")}', result.url)
        self.assertIn("x-oss-signature-version=OSS4-HMAC-SHA256", result.url)
        self.assertIn("x-oss-process=abc", result.url)

        await client.close()

    async def test_presign(self):
        cfg = config.load_default()
        cfg.region = 'cn-hangzhou'
        cfg.signature_version = 'v1'
        cfg.credentials_provider = credentials.StaticCredentialsProvider("ak", "sk")
        client = AsyncClient(cfg)

        request = model.GetObjectRequest(
            bucket='bucket',
            key='key',
            version_id='versionId'
        )

        expiration = datetime.datetime.fromtimestamp(1699807420)
        result = await client.presign(request, expiration=expiration)

        self.assertEqual('GET', result.method)
        self.assertEqual(0, len(result.signed_headers))
        self.assertIn("bucket.oss-cn-hangzhou.aliyuncs.com/key?", result.url)
        self.assertIn("OSSAccessKeyId=ak", result.url)
        self.assertIn('Expires=1699807420', result.url)
        self.assertIn("Signature=dcLTea%2BYh9ApirQ8o8dOPqtvJXQ%3D", result.url)

        await client.close()

        cfg.credentials_provider = credentials.StaticCredentialsProvider("ak", "sk", "token")
        client = AsyncClient(cfg)
        request = model.GetObjectRequest(
            bucket='bucket',
            key='key+123',
            version_id='versionId'
        )

        expiration = datetime.datetime.fromtimestamp(1699808204)
        result = await client.presign(request, expiration=expiration)

        self.assertEqual('GET', result.method)
        self.assertEqual(0, len(result.signed_headers))
        self.assertIn("bucket.oss-cn-hangzhou.aliyuncs.com/key%2B123?", result.url)
        self.assertIn("OSSAccessKeyId=ak", result.url)
        self.assertIn('Expires=1699808204', result.url)
        self.assertIn("Signature=jzKYRrM5y6Br0dRFPaTGOsbrDhY%3D", result.url)
        self.assertIn('security-token=token', result.url)

        await client.close()

    async def test_presign_fail(self):
        cfg = config.load_default()
        cfg.region = 'cn-hangzhou'
        cfg.signature_version = 'v4'
        cfg.credentials_provider = credentials.StaticCredentialsProvider("ak", "sk")
        client = AsyncClient(cfg)

        # unsupported request
        request = model.ListObjectsV2Request(
            bucket='bucket'
        )

        try:
            await client.presign(request)
            self.fail("should not here")
        except Exception as err:
            self.assertIsInstance(err, exceptions.ParamInvalidError)

        # greater than 7 days
        request = model.GetObjectRequest(
            bucket='bucket',
            key='key+123',
            version_id='versionId'
        )
        try:
            timedelta = datetime.timedelta(days=8)
            datetime_now = datetime.datetime.now(datetime.timezone.utc)
            expiration = datetime_now + timedelta
            await client.presign(request, expiration=expiration)
            self.fail("should not here")
        except Exception as err:
            self.assertIsInstance(err, exceptions.PresignExpirationError)

        await client.close()
