# pylint: skip-file
import io
from typing import cast
import unittest
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.crc as osscrc
from alibabacloud_oss_v2.aio.client import AsyncClient

from . import (
    TestIntegration, 
    random_bucket_name, 
    random_str, 
    REGION,
    ENDPOINT, 
    OBJECTNAME_PREFIX,
    ACCESS_ID,
    ACCESS_KEY,
    get_async_client,
)

class TestObjectBasicAsync(TestIntegration, unittest.IsolatedAsyncioTestCase):
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

    async def test_object_basic(self):
        len = 1 * 1024 * 1024 + 1234
        #len = 1234
        data = random_str(len)
        key = 'test-key'
        result = await self.async_client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.PutObjectResult)
        self.assertEqual(200, result.status_code)

        result = await self.async_client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.HeadObjectResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual(len, result.content_length)

        result = await self.async_client.get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.GetObjectResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual(len, result.content_length)

        self.assertEqual(data.encode(), result.body.content)
        #await result.body.close()

        result = await self.async_client.get_object_meta(oss.GetObjectMetaRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.GetObjectMetaResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual(len, result.content_length)

    async def test_put_object_fail(self):
        try:
            await self.invalid_async_client.put_object(oss.PutObjectRequest(
                bucket=self.bucket_name,
                key='invalid-key',
                body=b'hello world',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)
            self.assertIn('PutObject', str(e))
            self.assertIn('Endpoint: PUT', str(e))

    async def test_get_object_fail(self):
        try:
            await self.invalid_async_client.get_object(oss.GetObjectRequest(
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
            self.assertIn('GetObject', str(e))
            self.assertIn('Endpoint: GET', str(e))

    async def test_head_object_fail(self):
        try:
            await self.invalid_async_client.head_object(oss.HeadObjectRequest(
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
            self.assertIn('HeadObject', str(e))
            self.assertIn('Endpoint: HEAD', str(e))

    async def test_get_object_meta_fail(self):
        try:
            await self.invalid_async_client.get_object_meta(oss.GetObjectMetaRequest(
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
            self.assertIn('GetObjectMeta', str(e))
            self.assertIn('Endpoint: HEAD', str(e))

    async def test_get_object_range(self):
        len = 12345
        step = 2512
        data = random_str(len)
        key = 'test-key-range'
        result = await self.async_client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        rdata = b''
        for r in range(0, len, step):
            gresult = await self.async_client.get_object(oss.GetObjectRequest(
                bucket=self.bucket_name,
                key=key,
                range_header=f'bytes={r}-{r+step-1}',
                range_behavior='standard'
            ))
            self.assertIsNotNone(gresult)
            self.assertEqual(206, gresult.status_code)
            self.assertLessEqual(gresult.content_length, step)
            got = b''
            async for item in await gresult.body.iter_bytes():
                got += item
            rdata += got

        self.assertEqual(data.encode(), rdata)
        await gresult.body.close()

    async def test_append_object(self):
        data1 = b'hello'
        data2 = b' world'

        key = 'append_object'
        result = await self.async_client.append_object(oss.AppendObjectRequest(
            bucket=self.bucket_name,
            key=key,
            position=0,
            body=data1,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(5, result.next_position)

        result = await self.async_client.append_object(oss.AppendObjectRequest(
            bucket=self.bucket_name,
            key=key,
            position=result.next_position,
            body=data2,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(11, result.next_position)

        gresult = await self.async_client.get_object(oss.GetObjectRequest(
                bucket=self.bucket_name,
                key=key,
        ))

        self.assertEqual(b'hello world', gresult.body.content)
        await gresult.body.close()

    async def test_append_object_fail(self):
        try:
            await self.invalid_async_client.append_object(oss.AppendObjectRequest(
                bucket=self.bucket_name,
                key='invalid-key',
                position=0,
                body=b'hello world',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

    async def test_delete_object(self):
        length = 1234
        data = random_str(length)
        key = f'test-key-delete-object-{random_str(16)}'
        result = await self.async_client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        result = await self.async_client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(length, result.content_length)

        result = await self.async_client.delete_object(oss.DeleteObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(204, result.status_code)
        self.assertIsInstance(result, oss.DeleteObjectResult)

        try:
            result = await self.async_client.head_object(oss.HeadObjectRequest(
                bucket=self.bucket_name,
                key=key,
            ))
        except Exception as err:
            self.assertIsNotNone(result)
            self.assertIn('NoSuchKey', str(err))


        key = f'test-key-delete-object-no-exist-{random_str(16)}'
        result = await self.async_client.delete_object(oss.DeleteObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(204, result.status_code)
        self.assertIsNone(result.version_id)
        self.assertIsNone(result.delete_marker)
        self.assertIsInstance(result, oss.DeleteObjectResult)


    async def test_delete_object_fail(self):
        try:
            await self.invalid_async_client.delete_object(oss.DeleteObjectRequest(
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


    async def test_delete_multiple_objects(self):
        length = 1234
        data = random_str(length)
        key = OBJECTNAME_PREFIX + random_str(16)
        result = await self.async_client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        result = await self.async_client.delete_multiple_objects(oss.DeleteMultipleObjectsRequest(
            bucket=self.bucket_name,
            objects=[oss.DeleteObject(key=key)],
        ))
        self.assertIsInstance(result, oss.DeleteMultipleObjectsResult)
        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.headers.get('x-oss-request-id'))
        self.assertEqual(1, len(result.deleted_objects))
        self.assertEqual(key, result.deleted_objects[0].key)

        str1  = b'\x01\x02\x03\x04\x05\x06\a\b\t\n\v\f\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f'
        key = OBJECTNAME_PREFIX + random_str(16) + str1.decode()
        result = await self.async_client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        result = await self.async_client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(length, result.content_length)

        result = await self.async_client.delete_multiple_objects(oss.DeleteMultipleObjectsRequest(
            bucket=self.bucket_name,
            encoding_type='url',
            objects=[oss.DeleteObject(key=key)],
        ))
        self.assertIsInstance(result, oss.DeleteMultipleObjectsResult)
        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.headers.get('x-oss-request-id'))
        self.assertEqual(1, len(result.deleted_objects))
        self.assertEqual(key, result.deleted_objects[0].key)

        try:
            result = await self.async_client.head_object(oss.HeadObjectRequest(
                bucket=self.bucket_name,
                key=key,
            ))
        except Exception as err:
            self.assertIsInstance(err, oss.exceptions.OperationError)
            err = cast(oss.exceptions.OperationError, err)
            serr = err.unwrap()
            self.assertIsInstance(serr, oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, serr)
            self.assertIn('NoSuchKey', serr.code)

    async def test_delete_multiple_objects_with_delete_parameter(self):
        # Test the new Delete parameter mode
        length = 1234
        data = random_str(length)
        key1 = OBJECTNAME_PREFIX + random_str(16)
        key2 = OBJECTNAME_PREFIX + random_str(16)
        
        # Put objects to be deleted
        result1 = await self.async_client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key1,
            body=data,
        ))
        self.assertIsNotNone(result1)
        self.assertEqual(200, result1.status_code)
        
        result2 = await self.async_client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key2,
            body=data,
        ))
        self.assertIsNotNone(result2)
        self.assertEqual(200, result2.status_code)

        # Delete multiple objects using the new Delete parameter
        delete_request = oss.Delete(
            objects=[
                oss.ObjectIdentifier(key=key1),
                oss.ObjectIdentifier(key=key2)
            ],
            quiet=False
        )
        
        result = await self.async_client.delete_multiple_objects(oss.DeleteMultipleObjectsRequest(
            bucket=self.bucket_name,
            delete=delete_request,
        ))
        
        self.assertIsInstance(result, oss.DeleteMultipleObjectsResult)
        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.headers.get('x-oss-request-id'))
        self.assertEqual(2, len(result.deleted_objects))
        
        deleted_keys = [obj.key for obj in result.deleted_objects]
        self.assertIn(key1, deleted_keys)
        self.assertIn(key2, deleted_keys)

        # Verify objects are deleted
        try:
            await self.async_client.head_object(oss.HeadObjectRequest(
                bucket=self.bucket_name,
                key=key1,
            ))
            self.fail("Should have raised an exception")
        except Exception as err:
            self.assertIsInstance(err, oss.exceptions.OperationError)
            err = cast(oss.exceptions.OperationError, err)
            serr = err.unwrap()
            self.assertIsInstance(serr, oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, serr)
            self.assertIn('NoSuchKey', serr.code)
            
        try:
            await self.async_client.head_object(oss.HeadObjectRequest(
                bucket=self.bucket_name,
                key=key2,
            ))
            self.fail("Should have raised an exception")
        except Exception as err:
            self.assertIsInstance(err, oss.exceptions.OperationError)
            err = cast(oss.exceptions.OperationError, err)
            serr = err.unwrap()
            self.assertIsInstance(serr, oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, serr)
            self.assertIn('NoSuchKey', serr.code)

    async def test_restore_object(self):
        length = 123
        data = random_str(length)
        key = OBJECTNAME_PREFIX + random_str(16)
        result = await self.async_client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            storage_class=oss.StorageClassType.ARCHIVE,
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        result = await self.async_client.restore_object(oss.RestoreObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.RestoreObjectResult)
        self.assertEqual(202, result.status_code)

        try:
            result = await self.async_client.restore_object(oss.RestoreObjectRequest(
                bucket=self.bucket_name,
                key=key,
            ))
            self.fail("should not here")
        except Exception as err:
            self.assertIsInstance(err, oss.exceptions.OperationError)
            err = cast(oss.exceptions.OperationError, err)
            serr = err.unwrap()
            self.assertIsInstance(serr, oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, serr)
            self.assertIn('RestoreAlreadyInProgress', serr.code)
            self.assertIn('The restore operation is in progress.', serr.message)

    async def test_object_acl(self):
        length = 123
        data = random_str(length)
        key = OBJECTNAME_PREFIX + random_str(16)
        result = await self.async_client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            acl=oss.ObjectACLType.PRIVATE,
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        result = await self.async_client.get_object_acl(oss.GetObjectAclRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.GetObjectAclResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual('private', result.acl)

        result = await self.async_client.put_object_acl(oss.PutObjectAclRequest(
            bucket=self.bucket_name,
            key=key,
            acl=oss.ObjectACLType.PUBLICREAD
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.PutObjectAclResult)
        self.assertEqual(200, result.status_code)

        result = await self.async_client.get_object_acl(oss.GetObjectAclRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.GetObjectAclResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual('public-read', result.acl)

    async def test_get_object_acl_fail(self):
        try:
            await self.invalid_async_client.get_object_acl(oss.GetObjectAclRequest(
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
            self.assertIn('GetObjectAcl', str(e))
            self.assertIn('Endpoint: GET', str(e))

    async def test_put_object_acl_fail(self):
        try:
            await self.invalid_async_client.put_object_acl(oss.PutObjectAclRequest(
                bucket=self.bucket_name,
                key='invalid-key',
                acl='private',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertIn('PutObjectAcl', str(e))
            self.assertIn('Endpoint: PUT', str(e))

    async def test_put_object_with_defferent_body_type(self):
        len = 300 * 1024 + 1234
        data = random_str(len)

        crc64 = osscrc.Crc64(0)
        crc64.update(data.encode())
        ccrc = str(crc64.sum64())

        # str
        key = 'test-key-defferent_body-str'
        result = await self.async_client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.PutObjectResult)
        self.assertEqual(200, result.status_code)

        result = await self.async_client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.HeadObjectResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual(len, result.content_length)
        self.assertEqual(ccrc, result.hash_crc64)

        # bytes
        key = 'test-key-defferent_body-bytes'
        result = await self.async_client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data.encode(),
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.PutObjectResult)
        self.assertEqual(200, result.status_code)

        result = await self.async_client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.HeadObjectResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual(len, result.content_length)
        self.assertEqual(ccrc, result.hash_crc64)

        # IO[str]
        key = 'test-key-defferent_body-io-str'
        result = await self.async_client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=io.StringIO(data),
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.PutObjectResult)
        self.assertEqual(200, result.status_code)

        result = await self.async_client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.HeadObjectResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual(len, result.content_length)
        self.assertEqual(ccrc, result.hash_crc64)

        # IO[bytes]
        key = 'test-key-defferent_body-io-bytes'
        result = await self.async_client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=io.BytesIO(data.encode()),
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.PutObjectResult)
        self.assertEqual(200, result.status_code)

        result = await self.async_client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.HeadObjectResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual(len, result.content_length)
        self.assertEqual(ccrc, result.hash_crc64)

    async def test_put_object_with_defferent_body_type_disable_crc(self):
        len = 350 * 1024 + 1234
        data = random_str(len)

        crc64 = osscrc.Crc64(0)
        crc64.update(data.encode())
        ccrc = str(crc64.sum64())

        cfg = oss.config.load_default()
        cfg.credentials_provider = oss.credentials.StaticCredentialsProvider(ACCESS_ID, ACCESS_KEY)
        cfg.region = REGION
        cfg.endpoint = ENDPOINT
        cfg.disable_upload_crc64_check = True

        async with AsyncClient(cfg) as async_client:
            # str
            key = 'test-key-defferent_body-no-crc-str'
            result = await async_client.put_object(oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=key,
                body=data,
            ))
            self.assertIsNotNone(result)
            self.assertIsInstance(result, oss.PutObjectResult)
            self.assertEqual(200, result.status_code)

            result = await async_client.head_object(oss.HeadObjectRequest(
                bucket=self.bucket_name,
                key=key,
            ))
            self.assertIsNotNone(result)
            self.assertIsInstance(result, oss.HeadObjectResult)
            self.assertEqual(200, result.status_code)
            self.assertEqual(len, result.content_length)
            self.assertEqual(ccrc, result.hash_crc64)

            # bytes
            key = 'test-key-defferent_body-no-crc-bytes'
            result = await async_client.put_object(oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=key,
                body=data.encode(),
            ))
            self.assertIsNotNone(result)
            self.assertIsInstance(result, oss.PutObjectResult)
            self.assertEqual(200, result.status_code)

            result = await async_client.head_object(oss.HeadObjectRequest(
                bucket=self.bucket_name,
                key=key,
            ))
            self.assertIsNotNone(result)
            self.assertIsInstance(result, oss.HeadObjectResult)
            self.assertEqual(200, result.status_code)
            self.assertEqual(len, result.content_length)
            self.assertEqual(ccrc, result.hash_crc64)

            # IO[str]
            key = 'test-key-defferent_body-io-no-crc-str'
            result = await async_client.put_object(oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=key,
                body=io.StringIO(data),
            ))
            self.assertIsNotNone(result)
            self.assertIsInstance(result, oss.PutObjectResult)
            self.assertEqual(200, result.status_code)

            result = await async_client.head_object(oss.HeadObjectRequest(
                bucket=self.bucket_name,
                key=key,
            ))
            self.assertIsNotNone(result)
            self.assertIsInstance(result, oss.HeadObjectResult)
            self.assertEqual(200, result.status_code)
            self.assertEqual(len, result.content_length)
            self.assertEqual(ccrc, result.hash_crc64)

            # IO[bytes]
            key = 'test-key-defferent_body-io-no-crc-bytes'
            result = await async_client.put_object(oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=key,
                body=io.BytesIO(data.encode()),
            ))
            self.assertIsNotNone(result)
            self.assertIsInstance(result, oss.PutObjectResult)
            self.assertEqual(200, result.status_code)

            result = await async_client.head_object(oss.HeadObjectRequest(
                bucket=self.bucket_name,
                key=key,
            ))
            self.assertIsNotNone(result)
            self.assertIsInstance(result, oss.HeadObjectResult)
            self.assertEqual(200, result.status_code)
            self.assertEqual(len, result.content_length)
            self.assertEqual(ccrc, result.hash_crc64)


    @unittest.skip("Skip seal_append_object test until environment supports it")
    async def test_seal_append_object(self):
        # First create an appendable object
        data1 = b'hello'
        key = OBJECTNAME_PREFIX + random_str(16) + '-seal-async'

        # Append some data
        result = await self.async_client.append_object(oss.AppendObjectRequest(
            bucket=self.bucket_name,
            key=key,
            position=0,
            body=data1,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(5, result.next_position)

        # Seal the object
        seal_result = await self.async_client.seal_append_object(oss.SealAppendObjectRequest(
            bucket=self.bucket_name,
            key=key,
            position=result.next_position,
        ))
        self.assertIsNotNone(seal_result)
        self.assertEqual(200, seal_result.status_code)
        self.assertIsNotNone(seal_result.sealed_time)

        # Try to append more data - should fail
        try:
            await self.async_client.append_object(oss.AppendObjectRequest(
                bucket=self.bucket_name,
                key=key,
                position=seal_result.next_position if hasattr(seal_result, 'next_position') else result.next_position,
                body=b' world',
            ))
            # If we reach here, the seal didn't work properly
            self.fail("Expected to fail when appending to sealed object")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(400, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('AppendSealedObjectNotAllowed', serr.code)