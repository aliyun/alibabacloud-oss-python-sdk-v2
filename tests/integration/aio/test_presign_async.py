# pylint: skip-file
"""Integration tests for presign functionality (async)."""
import datetime
import unittest
import aiohttp
import alibabacloud_oss_v2 as oss
from .. import (
    TestIntegration,
    random_str,
    REGION,
    ENDPOINT,
    OBJECTNAME_PREFIX,
    get_async_client,
    ACCESS_ID,
    ACCESS_KEY,
)


def _get_async_signv1_client():
    """Create an async client with v1 signature."""
    cfg = oss.config.load_default()
    cfg.credentials_provider = oss.credentials.StaticCredentialsProvider(ACCESS_ID, ACCESS_KEY)
    cfg.signature_version = 'v1'
    cfg.region = REGION
    cfg.endpoint = ENDPOINT
    return oss.aio.AsyncClient(cfg)


class TestPresignAsync(TestIntegration, unittest.IsolatedAsyncioTestCase):
    """Integration tests for async presign functionality."""

    async def asyncSetUp(self):
        self.async_client = get_async_client(REGION, ENDPOINT)
        self.async_signv1_client = _get_async_signv1_client()

    async def asyncTearDown(self):
        await self.async_client.close()
        await self.async_signv1_client.close()

    async def test_presign_get_object_v1(self):
        """Test presign GET with v1 signature and actual HTTP download."""
        key = OBJECTNAME_PREFIX + random_str(16)
        data = random_str(128)

        # Upload object using signv1_client
        result = await self.async_signv1_client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data,
        ))
        self.assertEqual(200, result.status_code)

        # Generate presigned GET URL
        expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        pre_result = await self.async_signv1_client.presign(
            oss.GetObjectRequest(
                bucket=self.bucket_name,
                key=key,
            ),
            expiration=expiration,
        )

        # Verify presign result fields
        self.assertEqual('GET', pre_result.method)
        self.assertIsNotNone(pre_result.url)
        self.assertIn(self.bucket_name, pre_result.url)
        self.assertIn(key, pre_result.url)
        self.assertIn('Expires=', pre_result.url)
        self.assertIn('OSSAccessKeyId=', pre_result.url)
        self.assertIn('Signature=', pre_result.url)
        self.assertEqual(expiration, pre_result.expiration)

        # Actually download using aiohttp
        # Note: skip_auto_headers prevents aiohttp from adding Content-Type
        # which would break the v1 signature (same as SDK's own AioHttpClient)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                pre_result.url,
                headers=pre_result.signed_headers,
                skip_auto_headers=['Content-Type'],
            ) as resp:
                if resp.status != 200:
                    body = await resp.text()
                    self.fail(f'GET failed: status={resp.status}, body={body}, '
                              f'headers={dict(resp.request_info.headers)}')
                content = await resp.read()
                self.assertEqual(data.encode(), content)
                self.assertIsNotNone(resp.headers.get('x-oss-request-id'))
                self.assertIsNotNone(resp.headers.get('ETag'))

    async def test_presign_put_object_v1(self):
        """Test presign PUT with v1 signature and actual HTTP upload."""
        key = OBJECTNAME_PREFIX + 'presign-put-' + random_str(16)
        data = random_str(256)
        expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)

        # Generate presigned PUT URL
        pre_result = await self.async_signv1_client.presign(
            oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=key,
            ),
            expiration=expiration,
        )

        # Verify presign result fields
        self.assertEqual('PUT', pre_result.method)
        self.assertIsNotNone(pre_result.url)
        self.assertIn(self.bucket_name, pre_result.url)
        self.assertIn('Expires=', pre_result.url)
        self.assertIn('Signature=', pre_result.url)

        # Actually upload using aiohttp
        # Note: skip_auto_headers prevents aiohttp from adding Content-Type
        # which would break the v1 signature (same as SDK's own AioHttpClient)
        async with aiohttp.ClientSession() as session:
            async with session.put(
                pre_result.url,
                headers=pre_result.signed_headers,
                data=data,
                skip_auto_headers=['Content-Type'],
            ) as resp:
                if resp.status != 200:
                    body = await resp.text()
                    self.fail(f'PUT failed: status={resp.status}, body={body}, '
                              f'signed_headers={pre_result.signed_headers}')
                self.assertIsNotNone(resp.headers.get('x-oss-request-id'))

        # Verify uploaded content using SDK
        get_result = await self.async_signv1_client.get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertEqual(200, get_result.status_code)
        self.assertEqual(data.encode(), get_result.body.content)

    async def test_presign_put_object_with_content_type_v1(self):
        """Test presign PUT with Content-Type and actual HTTP upload."""
        key = OBJECTNAME_PREFIX + 'presign-put-ct-' + random_str(16)
        data = b'{"name": "test", "value": 123}'
        content_type = 'application/json'
        expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)

        # Generate presigned PUT URL with content_type
        pre_result = await self.async_signv1_client.presign(
            oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=key,
                content_type=content_type,
            ),
            expiration=expiration,
        )

        self.assertEqual('PUT', pre_result.method)
        self.assertIsNotNone(pre_result.url)

        # signed_headers should include Content-Type
        self.assertIn('Content-Type', pre_result.signed_headers)
        self.assertEqual(content_type, pre_result.signed_headers['Content-Type'])

        # Actually upload using aiohttp with signed headers
        # signed_headers contains Content-Type, skip_auto_headers prevents override
        async with aiohttp.ClientSession() as session:
            async with session.put(
                pre_result.url,
                headers=pre_result.signed_headers,
                data=data,
                skip_auto_headers=['Content-Type'],
            ) as resp:
                if resp.status != 200:
                    body = await resp.text()
                    self.fail(f'PUT with Content-Type failed: status={resp.status}, body={body}, '
                              f'signed_headers={pre_result.signed_headers}')

        # Verify uploaded content and content type
        head_result = await self.async_signv1_client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertEqual(200, head_result.status_code)
        self.assertEqual(content_type, head_result.content_type)
        self.assertEqual(len(data), head_result.content_length)

    async def test_presign_head_object_v1(self):
        """Test presign HEAD with v1 signature and actual HTTP HEAD request."""
        key = OBJECTNAME_PREFIX + 'presign-head-' + random_str(16)
        data = random_str(256)

        # Upload object first
        result = await self.async_signv1_client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data,
        ))
        self.assertEqual(200, result.status_code)

        # Generate presigned HEAD URL
        expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        pre_result = await self.async_signv1_client.presign(
            oss.HeadObjectRequest(
                bucket=self.bucket_name,
                key=key,
            ),
            expiration=expiration,
        )

        # Verify presign result fields
        self.assertEqual('HEAD', pre_result.method)
        self.assertIsNotNone(pre_result.url)
        self.assertIn(self.bucket_name, pre_result.url)

        # Actually perform HEAD request using aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.head(
                pre_result.url,
                headers=pre_result.signed_headers,
                skip_auto_headers=['Content-Type'],
            ) as resp:
                if resp.status != 200:
                    body = await resp.text()
                    self.fail(f'HEAD failed: status={resp.status}, body={body}')
                self.assertEqual(str(len(data.encode())), resp.headers.get('Content-Length'))
                self.assertIsNotNone(resp.headers.get('ETag'))
                self.assertIsNotNone(resp.headers.get('x-oss-request-id'))
                self.assertIsNotNone(resp.headers.get('Last-Modified'))
                self.assertIsNotNone(resp.headers.get('x-oss-object-type'))

    async def test_presign_get_object_v4(self):
        """Test presign GET with v4 (default) signature and actual HTTP download."""
        key = OBJECTNAME_PREFIX + 'presign-v4-get-' + random_str(16)
        data = random_str(128)

        # Upload using default async client (v4 signature)
        result = await self.async_client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data,
        ))
        self.assertEqual(200, result.status_code)

        # Generate presigned GET URL with default (v4) signature
        pre_result = await self.async_client.presign(
            oss.GetObjectRequest(
                bucket=self.bucket_name,
                key=key,
            ),
            expires=datetime.timedelta(hours=1),
        )

        self.assertEqual('GET', pre_result.method)
        self.assertIsNotNone(pre_result.url)
        self.assertIn('x-oss-signature-version=OSS4-HMAC-SHA256', pre_result.url)

        # Actually download using aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(
                pre_result.url,
                headers=pre_result.signed_headers,
                skip_auto_headers=['Content-Type'],
            ) as resp:
                if resp.status != 200:
                    body = await resp.text()
                    self.fail(f'GET v4 failed: status={resp.status}, body={body}')
                content = await resp.read()
                self.assertEqual(data.encode(), content)

    async def test_presign_put_object_v4(self):
        """Test presign PUT with v4 (default) signature and actual HTTP upload."""
        key = OBJECTNAME_PREFIX + 'presign-v4-put-' + random_str(16)
        data = random_str(256)

        # Generate presigned PUT URL with default (v4) signature
        pre_result = await self.async_client.presign(
            oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=key,
            ),
            expires=datetime.timedelta(hours=1),
        )

        self.assertEqual('PUT', pre_result.method)
        self.assertIsNotNone(pre_result.url)
        self.assertIn('x-oss-signature-version=OSS4-HMAC-SHA256', pre_result.url)

        # Actually upload using aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.put(
                pre_result.url,
                headers=pre_result.signed_headers,
                data=data,
                skip_auto_headers=['Content-Type'],
            ) as resp:
                if resp.status != 200:
                    body = await resp.text()
                    self.fail(f'PUT v4 failed: status={resp.status}, body={body}, '
                              f'signed_headers={pre_result.signed_headers}')

        # Verify uploaded content
        get_result = await self.async_client.get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertEqual(200, get_result.status_code)
        self.assertEqual(data.encode(), get_result.body.content)

    async def test_presign_multipart_upload_v1(self):
        """Test presign multipart upload flow: Init -> UploadPart -> Complete."""
        key = OBJECTNAME_PREFIX + 'presign-multipart-' + random_str(16)
        part_data = b'a' * 100 * 1024  # 100KB minimum part size
        expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)

        # Step 1: Presign InitiateMultipartUpload (POST)
        init_pre = await self.async_signv1_client.presign(
            oss.InitiateMultipartUploadRequest(
                bucket=self.bucket_name,
                key=key),
            expiration=expiration)
        self.assertEqual('POST', init_pre.method)
        self.assertIn('uploads', init_pre.url)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                init_pre.url,
                headers=init_pre.signed_headers,
                skip_auto_headers=['Content-Type'],
            ) as resp:
                if resp.status != 200:
                    body = await resp.text()
                    self.fail(f'InitiateMultipartUpload failed: status={resp.status}, body={body}')
                content = await resp.read()
                init_result = oss.InitiateMultipartUploadResult()
                oss.serde.deserialize_xml(xml_data=content, obj=init_result)
                upload_id = init_result.upload_id
                self.assertIsNotNone(upload_id)

        # Step 2: Presign UploadPart (PUT)
        part_pre = await self.async_signv1_client.presign(
            oss.UploadPartRequest(
                bucket=self.bucket_name,
                key=key,
                upload_id=upload_id,
                part_number=1),
            expiration=expiration)
        self.assertEqual('PUT', part_pre.method)
        self.assertIn('partNumber=1', part_pre.url)
        self.assertIn(f'uploadId={upload_id}', part_pre.url)

        async with aiohttp.ClientSession() as session:
            async with session.put(
                part_pre.url,
                headers=part_pre.signed_headers,
                data=part_data,
                skip_auto_headers=['Content-Type'],
            ) as resp:
                if resp.status != 200:
                    body = await resp.text()
                    self.fail(f'UploadPart failed: status={resp.status}, body={body}')
                etag = resp.headers.get('ETag')
                self.assertIsNotNone(etag)

        # Step 3: Presign CompleteMultipartUpload (POST)
        complete_request = oss.CompleteMultipartUploadRequest(
            bucket=self.bucket_name,
            key=key,
            upload_id=upload_id,
            complete_multipart_upload=oss.CompleteMultipartUpload(
                parts=[oss.UploadPart(part_number=1, etag=etag)]))

        op_input = oss.serde.serialize_input(complete_request, oss.OperationInput(
            op_name='CompleteMultipartUpload',
            method='POST',
            bucket=complete_request.bucket))

        complete_pre = await self.async_signv1_client.presign(
            complete_request, expiration=expiration)
        self.assertEqual('POST', complete_pre.method)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                complete_pre.url,
                headers=complete_pre.signed_headers,
                data=op_input.body,
                skip_auto_headers=['Content-Type'],
            ) as resp:
                if resp.status != 200:
                    body = await resp.text()
                    self.fail(f'CompleteMultipartUpload failed: status={resp.status}, body={body}')

        # Step 4: Verify uploaded object
        head_result = await self.async_signv1_client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=key))
        self.assertEqual(200, head_result.status_code)
        self.assertEqual(len(part_data), head_result.content_length)
        self.assertEqual('Multipart', head_result.object_type)

    async def test_presign_abort_multipart_upload_v1(self):
        """Test presign AbortMultipartUpload with actual HTTP DELETE."""
        key = OBJECTNAME_PREFIX + 'presign-abort-' + random_str(16)
        expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)

        # Step 1: Initiate multipart upload using SDK
        init_result = await self.async_signv1_client.initiate_multipart_upload(
            oss.InitiateMultipartUploadRequest(
                bucket=self.bucket_name,
                key=key))
        self.assertEqual(200, init_result.status_code)
        upload_id = init_result.upload_id

        # Step 2: Presign AbortMultipartUpload (DELETE)
        abort_pre = await self.async_signv1_client.presign(
            oss.AbortMultipartUploadRequest(
                bucket=self.bucket_name,
                key=key,
                upload_id=upload_id),
            expiration=expiration)
        self.assertEqual('DELETE', abort_pre.method)
        self.assertIn(f'uploadId={upload_id}', abort_pre.url)

        # Step 3: Actually abort using the presigned URL
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                abort_pre.url,
                headers=abort_pre.signed_headers,
                skip_auto_headers=['Content-Type'],
            ) as resp:
                if resp.status != 204:
                    body = await resp.text()
                    self.fail(f'AbortMultipartUpload failed: status={resp.status}, body={body}')
                self.assertEqual(204, resp.status)

        # Step 4: Verify upload is aborted by listing multipart uploads
        list_result = await self.async_signv1_client.list_multipart_uploads(
            oss.ListMultipartUploadsRequest(
                bucket=self.bucket_name,
                prefix=key))
        upload_ids = [u.upload_id for u in (list_result.uploads or [])]
        self.assertNotIn(upload_id, upload_ids)

    async def test_presign_get_object_fail(self):
        """Test presign with unsupported request type."""
        try:
            await self.async_client.presign(
                oss.ListObjectsV2Request(bucket=self.bucket_name)
            )
            self.fail("should not here")
        except Exception as err:
            self.assertIsInstance(err, oss.exceptions.ParamInvalidError)
