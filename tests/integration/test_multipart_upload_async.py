# pylint: skip-file
from typing import cast
import tempfile
import datetime
import requests
import unittest
import alibabacloud_oss_v2 as oss
from . import (
    TestIntegration, 
    random_bucket_name, 
    random_str, 
    REGION,
    ENDPOINT, 
    OBJECTNAME_PREFIX, 
    get_async_client,
)

class TestMultipartUpload(TestIntegration, unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.async_client = get_async_client(REGION, ENDPOINT)
        self.invalid_async_client = get_async_client(
            REGION, 
            ENDPOINT,
            oss.credentials.StaticCredentialsProvider('invalid-ak', 'invalid')
        )

    async def asyncTearDown(self):
        await self.async_client.close() 
        await self.invalid_async_client.close() 

    async def test_multipart_upload_object(self):
        length1 = 100*1024
        data1 = random_str(length1)
        length2 = 1234
        data2 = random_str(length2)
        key = OBJECTNAME_PREFIX + random_str(16)

        result = await self.async_client.initiate_multipart_upload(oss.InitiateMultipartUploadRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.InitiateMultipartUploadResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual(self.bucket_name, result.bucket)
        self.assertEqual(key, result.key)
        self.assertIsNotNone(key, result.upload_id)

        presult1 = await self.async_client.upload_part(oss.UploadPartRequest(
            bucket=self.bucket_name,
            key=key,
            part_number=1,
            upload_id=result.upload_id,
            body=data1,
        ))
        self.assertIsNotNone(presult1)
        self.assertIsInstance(presult1, oss.UploadPartResult)
        self.assertEqual(200, presult1.status_code)
        self.assertIsNotNone(presult1.content_md5)
        self.assertIsNotNone(presult1.etag)
        self.assertIsNotNone(presult1.hash_crc64)

        presult2 = await self.async_client.upload_part(oss.UploadPartRequest(
            bucket=self.bucket_name,
            key=key,
            part_number=2,
            upload_id=result.upload_id,
            body=data2,
        ))
        self.assertIsNotNone(presult2)
        self.assertIsInstance(presult2, oss.UploadPartResult)
        self.assertEqual(200, presult2.status_code)
        self.assertIsNotNone(presult2.content_md5)
        self.assertIsNotNone(presult2.etag)
        self.assertIsNotNone(presult2.hash_crc64)

        lpresult = await self.async_client.list_parts(oss.ListPartsRequest(
            bucket=self.bucket_name,
            key=key,
            upload_id=result.upload_id,
        ))
        self.assertIsNotNone(lpresult)
        self.assertIsInstance(lpresult, oss.ListPartsResult)
        self.assertEqual(200, lpresult.status_code)
        self.assertEqual(self.bucket_name, lpresult.bucket)
        self.assertEqual(key, lpresult.key)
        self.assertEqual(2, lpresult.next_part_number_marker)
        self.assertEqual(0, lpresult.part_number_marker)
        self.assertEqual(False, lpresult.is_truncated)
        self.assertEqual(1000, lpresult.max_parts)
        self.assertEqual('Standard', lpresult.storage_class)
        self.assertEqual(2, len(lpresult.parts))
        self.assertEqual(1, lpresult.parts[0].part_number)
        self.assertEqual(length1, lpresult.parts[0].size)
        self.assertEqual(presult1.etag, lpresult.parts[0].etag)
        self.assertEqual(presult1.hash_crc64, lpresult.parts[0].hash_crc64)
        self.assertEqual(2, lpresult.parts[1].part_number)
        self.assertEqual(length2, lpresult.parts[1].size)
        self.assertEqual(presult2.etag, lpresult.parts[1].etag)
        self.assertEqual(presult2.hash_crc64, lpresult.parts[1].hash_crc64)

        cresult = await self.async_client.complete_multipart_upload(oss.CompleteMultipartUploadRequest(
            bucket=self.bucket_name,
            key=key,
            upload_id=result.upload_id,
            body=data2,
            complete_multipart_upload=oss.CompleteMultipartUpload(
                parts=[
                    oss.UploadPart(part_number=1, etag=presult1.etag),
                    oss.UploadPart(part_number=2, etag=presult2.etag),                    
                ]
            )
        ))
        self.assertIsNotNone(cresult)
        self.assertIsInstance(cresult, oss.CompleteMultipartUploadResult)
        self.assertEqual(200, cresult.status_code)
        self.assertEqual(self.bucket_name, cresult.bucket)
        self.assertEqual(key, cresult.key)
        self.assertIsNotNone(cresult.etag)
        self.assertIsNotNone(cresult.hash_crc64)

        gresult = await self.async_client.get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(gresult)
        self.assertEqual(200, gresult.status_code)
        self.assertEqual(length1 + length2, gresult.content_length)
        items = []
        async for item in await gresult.body.iter_bytes():
            items.append(item)
        rdata = b''.join(items) or b''
        self.assertEqual(data1 + data2, rdata.decode())

    async def test_multipart_upload_object_special_key(self):
        length1 = 100*1024
        data1 = random_str(length1)
        length2 = 1234
        data2 = random_str(length2)        
        str1  = b'\x01\x02\x03\x04\x05\x06\a\b\t\n\v\f\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f'
        key = OBJECTNAME_PREFIX + random_str(16) + str1.decode()

        result = await self.async_client.initiate_multipart_upload(oss.InitiateMultipartUploadRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.InitiateMultipartUploadResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual(self.bucket_name, result.bucket)
        self.assertEqual(key, result.key)
        self.assertIsNotNone(key, result.upload_id)

        presult1 = await self.async_client.upload_part(oss.UploadPartRequest(
            bucket=self.bucket_name,
            key=key,
            part_number=1,
            upload_id=result.upload_id,
            body=data1,
        ))
        self.assertIsNotNone(presult1)
        self.assertIsInstance(presult1, oss.UploadPartResult)
        self.assertEqual(200, presult1.status_code)
        self.assertIsNotNone(presult1.content_md5)
        self.assertIsNotNone(presult1.etag)
        self.assertIsNotNone(presult1.hash_crc64)

        presult2 = await self.async_client.upload_part(oss.UploadPartRequest(
            bucket=self.bucket_name,
            key=key,
            part_number=2,
            upload_id=result.upload_id,
            body=data2,
        ))
        self.assertIsNotNone(presult2)
        self.assertIsInstance(presult2, oss.UploadPartResult)
        self.assertEqual(200, presult2.status_code)
        self.assertIsNotNone(presult2.content_md5)
        self.assertIsNotNone(presult2.etag)
        self.assertIsNotNone(presult2.hash_crc64)

        cresult = await self.async_client.complete_multipart_upload(oss.CompleteMultipartUploadRequest(
            bucket=self.bucket_name,
            key=key,
            upload_id=result.upload_id,
            body=data2,
            complete_multipart_upload=oss.CompleteMultipartUpload(
                parts=[
                    oss.UploadPart(part_number=1, etag=presult1.etag),
                    oss.UploadPart(part_number=2, etag=presult2.etag),                    
                ]
            )
        ))
        self.assertIsNotNone(cresult)
        self.assertIsInstance(cresult, oss.CompleteMultipartUploadResult)
        self.assertEqual(200, cresult.status_code)
        self.assertEqual(self.bucket_name, cresult.bucket)
        self.assertEqual(key, cresult.key)
        self.assertIsNotNone(cresult.etag)
        self.assertIsNotNone(cresult.hash_crc64)

        gresult = await self.async_client.get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(gresult)
        self.assertEqual(200, gresult.status_code)
        self.assertEqual(length1 + length2, gresult.content_length)
        self.assertEqual((data1 + data2).encode(), gresult.body.content)


    async def test_multipart_upload_object_encoding_type(self):
        str1  = b'\x01\x02\x03\x04\x05\x06\a\b\t\n\v\f\r\x0e\x0f\x10'
        key = OBJECTNAME_PREFIX + random_str(16) + str1.decode()

        result = await self.async_client.initiate_multipart_upload(oss.InitiateMultipartUploadRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.InitiateMultipartUploadResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual(self.bucket_name, result.bucket)
        self.assertEqual(key, result.key)
        self.assertIsNotNone(key, result.upload_id)

        presult1 = await self.async_client.upload_part(oss.UploadPartRequest(
            bucket=self.bucket_name,
            key=key,
            part_number=1,
            upload_id=result.upload_id,
            body='hello world',
        ))
        self.assertIsNotNone(presult1)
        self.assertIsInstance(presult1, oss.UploadPartResult)
        self.assertEqual(200, presult1.status_code)
        self.assertIsNotNone(presult1.content_md5)
        self.assertIsNotNone(presult1.etag)
        self.assertIsNotNone(presult1.hash_crc64)

        lpresult = await self.async_client.list_parts(oss.ListPartsRequest(
            bucket=self.bucket_name,
            key=key,
            upload_id=result.upload_id,
        ))
        self.assertIsNotNone(lpresult)
        self.assertIsInstance(lpresult, oss.ListPartsResult)
        self.assertEqual(200, lpresult.status_code)
        self.assertEqual(self.bucket_name, lpresult.bucket)
        self.assertEqual(key, lpresult.key)

        luresult = await self.async_client.list_multipart_uploads(oss.ListMultipartUploadsRequest(
            bucket=self.bucket_name,
        ))
        self.assertIsNotNone(luresult)
        self.assertIsInstance(luresult, oss.ListMultipartUploadsResult)
        self.assertEqual(200, luresult.status_code)
        self.assertEqual(self.bucket_name, luresult.bucket)
        self.assertEqual(False, luresult.is_truncated)
        self.assertEqual(None, luresult.key_marker)
        self.assertEqual(key, luresult.next_key_marker)
        self.assertEqual(1, len(luresult.uploads))
        self.assertEqual(key, luresult.uploads[0].key)
        self.assertEqual(result.upload_id, luresult.uploads[0].upload_id)

        abresult = await self.async_client.abort_multipart_upload(oss.AbortMultipartUploadRequest(
            bucket=self.bucket_name,
            key=key,
            upload_id=result.upload_id,
        ))
        self.assertIsNotNone(abresult)
        self.assertIsInstance(abresult, oss.AbortMultipartUploadResult)
        self.assertEqual(204, abresult.status_code)

    async def test_multipart_upload_from_file(self):
        part_size = 100 * 1024
        data_size = 3 * part_size + 1245
        data = random_str(data_size).encode()
        key = 'multipart-file.bin'

        #init
        initresult = await self.async_client.initiate_multipart_upload(oss.InitiateMultipartUploadRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(initresult)
        self.assertIsInstance(initresult, oss.InitiateMultipartUploadResult)
        self.assertEqual(200, initresult.status_code)

        #upload part
        part_number = 1
        upload_parts = []
        with tempfile.TemporaryFile('w+b') as f:
            f.write(data)
            for start in range(0, data_size, part_size):
                n = part_size
                if start + n > data_size:
                    n =  data_size - start
                reader = oss.io_utils.SectionReader(oss.io_utils.ReadAtReader(f), start, n)
                upresult = await self.async_client.upload_part(oss.UploadPartRequest(
                    bucket=self.bucket_name,
                    key=key,
                    upload_id=initresult.upload_id,
                    part_number=part_number,
                    body=reader
                ))
                self.assertIsNotNone(upresult)
                self.assertIsInstance(upresult, oss.UploadPartResult)
                self.assertEqual(200, upresult.status_code)
                upload_parts.append(oss.UploadPart(part_number=part_number, etag=upresult.etag))
                part_number += 1

            self.assertEqual(4, len(upload_parts))

        #listpart
        lpresult = await self.async_client.list_parts(oss.ListPartsRequest(
            bucket=self.bucket_name,
            key=key,
            upload_id=initresult.upload_id
        ))
        self.assertIsNotNone(lpresult)
        self.assertIsInstance(lpresult, oss.ListPartsResult)
        self.assertEqual(200, lpresult.status_code)

        #complete
        parts = sorted(upload_parts, key=lambda p: p.part_number)
        cmresult = await self.async_client.complete_multipart_upload(oss.CompleteMultipartUploadRequest(
            bucket=self.bucket_name,
            key=key,
            upload_id=initresult.upload_id,
            complete_multipart_upload=oss.CompleteMultipartUpload(
                parts=parts
            )
        ))
        self.assertIsNotNone(cmresult)
        self.assertIsInstance(cmresult, oss.CompleteMultipartUploadResult)
        self.assertEqual(200, cmresult.status_code)

        # get object and check
        gowresult = await self.async_client.get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key
        ))
        self.assertIsNotNone(gowresult)
        self.assertIsInstance(gowresult, oss.GetObjectResult)
        self.assertEqual(200, gowresult.status_code)
        self.assertEqual(data_size, len(gowresult.body.content))
        self.assertEqual(data, gowresult.body.content)

    async def test_initiate_multipart_upload_fail(self):
        try:
            await self.invalid_async_client.initiate_multipart_upload(oss.InitiateMultipartUploadRequest(
                bucket=self.bucket_name,
                key='invalid-key',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)
            self.assertIn('InitiateMultipartUpload', str(e))
            self.assertIn('Endpoint: POST', str(e))

    async def test_upload_part_fail(self):
        try:
            await self.invalid_async_client.upload_part(oss.UploadPartRequest(
                bucket=self.bucket_name,
                key='invalid-key',
                upload_id='upload-id',
                part_number=1,
                body='hello world'
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)
            self.assertIn('UploadPart', str(e))
            self.assertIn('Endpoint: PUT', str(e))

    async def test_upload_part_copy_fail(self):
        try:
            await self.invalid_async_client.upload_part_copy(oss.UploadPartCopyRequest(
                bucket=self.bucket_name,
                key='invalid-key',
                source_key='source-invalid-key',
                upload_id='upload-id',
                part_number=1,
                body='hello world'
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)
            self.assertIn('UploadPartCopy', str(e))
            self.assertIn('Endpoint: PUT', str(e))

    async def test_complete_multipart_upload_fail(self):
        try:
            await self.invalid_async_client.complete_multipart_upload(oss.CompleteMultipartUploadRequest(
                bucket=self.bucket_name,
                key='invalid-key',
                upload_id='upload-id',
                complete_all='yes'
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)
            self.assertIn('CompleteMultipartUpload', str(e))
            self.assertIn('Endpoint: POST', str(e))

    async def test_abort_multipart_upload_fail(self):
        try:
            await self.invalid_async_client.abort_multipart_upload(oss.AbortMultipartUploadRequest(
                bucket=self.bucket_name,
                key='invalid-key',
                upload_id='upload-id',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)
            self.assertIn('AbortMultipartUpload', str(e))
            self.assertIn('Endpoint: DELETE', str(e))

    async def test_list_multipart_uploads_fail(self):
        try:
            await self.invalid_async_client.list_multipart_uploads(oss.ListMultipartUploadsRequest(
                bucket=self.bucket_name,
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)
            self.assertIn('ListMultipartUploads', str(e))
            self.assertIn('Endpoint: GET', str(e))

    async def test_list_parts_fail(self):
        try:
            await self.invalid_async_client.list_parts(oss.ListPartsRequest(
                bucket=self.bucket_name,
                key='invalid-key',
                upload_id='upload-id',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)
            self.assertIn('ListParts', str(e))
            self.assertIn('Endpoint: GET', str(e))
