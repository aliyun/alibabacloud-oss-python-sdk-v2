# pylint: skip-file
import unittest
from typing import cast
import alibabacloud_oss_v2 as oss
from . import (
    TestIntegration, 
    random_str, 
    OBJECTNAME_PREFIX,
)
from urllib.parse import quote, unquote

class TestObjectBasicV2(TestIntegration):

    def test_put_object_acl(self):
        length = 123
        data = random_str(length)
        key = OBJECTNAME_PREFIX + random_str(16)

        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            acl=oss.ObjectACLType.PRIVATE,
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        result = self.client.get_object_acl(oss.GetObjectAclRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.GetObjectAclResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual('private', result.acl)

    def test_put_object_object_acl(self):
        length = 123
        data = random_str(length)
        key = OBJECTNAME_PREFIX + random_str(16)

        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            object_acl=oss.ObjectACLType.PRIVATE,
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        result = self.client.get_object_acl(oss.GetObjectAclRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.GetObjectAclResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual('private', result.acl)

        result = self.client.put_object_acl(oss.PutObjectAclRequest(
            bucket=self.bucket_name,
            key=key,
            object_acl=oss.ObjectACLType.DEFAULT
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.PutObjectAclResult)
        self.assertEqual(200, result.status_code)

        result = self.client.get_object_acl(oss.GetObjectAclRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.GetObjectAclResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual('default', result.acl)

    def test_append_object_acl(self):
        data1 = b'hello'
        key = OBJECTNAME_PREFIX + random_str(16) + 'append_object'
        result = self.client.append_object(oss.AppendObjectRequest(
            bucket=self.bucket_name,
            key=key,
            position=0,
            body=data1,
            acl='private'
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(5, result.next_position)

        result = self.client.get_object_acl(oss.GetObjectAclRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.GetObjectAclResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual('private', result.acl)

    def test_append_object_object_acl(self):
        data1 = b'hello'
        key = OBJECTNAME_PREFIX + random_str(16) + 'append_object'
        result = self.client.append_object(oss.AppendObjectRequest(
            bucket=self.bucket_name,
            key=key,
            position=0,
            body=data1,
            object_acl='private'
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(5, result.next_position)

        result = self.client.get_object_acl(oss.GetObjectAclRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.GetObjectAclResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual('private', result.acl)

    def test_copy_object_acl(self):
        length = 123
        data = random_str(length)
        key = OBJECTNAME_PREFIX + random_str(16)
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            acl=oss.ObjectACLType.PRIVATE,
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        dst_key = key + '-copy'
        result = self.client.copy_object(oss.CopyObjectRequest(
            bucket=self.bucket_name,
            key=dst_key,
            source_key=key,
            acl=oss.ObjectACLType.DEFAULT,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        result = self.client.get_object_acl(oss.GetObjectAclRequest(
            bucket=self.bucket_name,
            key=dst_key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.GetObjectAclResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual('default', result.acl)

    def test_copy_object_object_acl(self):
        length = 123
        data = random_str(length)
        key = OBJECTNAME_PREFIX + random_str(16)
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            object_acl=oss.ObjectACLType.PRIVATE,
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        dst_key = key + '-copy'
        result = self.client.copy_object(oss.CopyObjectRequest(
            bucket=self.bucket_name,
            key=dst_key,
            source_key=key,
            object_acl=oss.ObjectACLType.DEFAULT,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        result = self.client.get_object_acl(oss.GetObjectAclRequest(
            bucket=self.bucket_name,
            key=dst_key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.GetObjectAclResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual('default', result.acl)

    def test_mutilpart_object_acl(self):
        length1 = 100*1024
        data1 = random_str(length1)
        key = OBJECTNAME_PREFIX + random_str(16)

        result = self.client.initiate_multipart_upload(oss.InitiateMultipartUploadRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.InitiateMultipartUploadResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual(self.bucket_name, result.bucket)
        self.assertEqual(key, result.key)
        self.assertIsNotNone(key, result.upload_id)

        presult1 = self.client.upload_part(oss.UploadPartRequest(
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

        cresult = self.client.complete_multipart_upload(oss.CompleteMultipartUploadRequest(
            bucket=self.bucket_name,
            key=key,
            upload_id=result.upload_id,
            complete_multipart_upload=oss.CompleteMultipartUpload(
                parts=[
                    oss.UploadPart(part_number=1, etag=presult1.etag),
                ]
            ),
            acl='private',
        ))
        self.assertIsNotNone(cresult)
        self.assertIsInstance(cresult, oss.CompleteMultipartUploadResult)
        self.assertEqual(200, cresult.status_code)
        self.assertEqual(self.bucket_name, cresult.bucket)
        self.assertEqual(key, cresult.key)

        result = self.client.get_object_acl(oss.GetObjectAclRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.GetObjectAclResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual('private', result.acl)

    def test_mutilpart_object_object_acl(self):
        length1 = 100*1024
        data1 = random_str(length1)
        length2 = 1234
        data2 = random_str(length2)
        key = OBJECTNAME_PREFIX + random_str(16)

        result = self.client.initiate_multipart_upload(oss.InitiateMultipartUploadRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.InitiateMultipartUploadResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual(self.bucket_name, result.bucket)
        self.assertEqual(key, result.key)
        self.assertIsNotNone(key, result.upload_id)

        presult1 = self.client.upload_part(oss.UploadPartRequest(
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

        presult2 = self.client.upload_part(oss.UploadPartRequest(
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

        cresult = self.client.complete_multipart_upload(oss.CompleteMultipartUploadRequest(
            bucket=self.bucket_name,
            key=key,
            upload_id=result.upload_id,
            body=data2,
            complete_multipart_upload=oss.CompleteMultipartUpload(
                parts=[
                    oss.UploadPart(part_number=1, etag=presult1.etag),
                    oss.UploadPart(part_number=2, etag=presult2.etag),                    
                ]
            ),
            object_acl='private',
        ))
        self.assertIsNotNone(cresult)
        self.assertIsInstance(cresult, oss.CompleteMultipartUploadResult)
        self.assertEqual(200, cresult.status_code)
        self.assertEqual(self.bucket_name, cresult.bucket)
        self.assertEqual(key, cresult.key)
        self.assertIsNotNone(cresult.etag)
        self.assertIsNotNone(cresult.hash_crc64)

        result = self.client.get_object_acl(oss.GetObjectAclRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.GetObjectAclResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual('private', result.acl)

    def test_symlink_object_object_acl(self):
        length = 123
        data = random_str(length)
        key = OBJECTNAME_PREFIX + random_str(16)
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            acl=oss.ObjectACLType.PRIVATE,
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        result = self.client.get_object_acl(oss.GetObjectAclRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.GetObjectAclResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual('private', result.acl)

        sym_key = key + '-sym'
        result = self.client.put_symlink(oss.PutSymlinkRequest(
            bucket=self.bucket_name,
            key=sym_key,
            acl='private',
            target=key,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        result = self.client.get_object_acl(oss.GetObjectAclRequest(
            bucket=self.bucket_name,
            key=sym_key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.GetObjectAclResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual('private', result.acl)

    def test_symlink_object_object_acl(self):
        length = 123
        data = random_str(length)
        key = OBJECTNAME_PREFIX + random_str(16)
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            object_acl=oss.ObjectACLType.PRIVATE,
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        result = self.client.get_object_acl(oss.GetObjectAclRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.GetObjectAclResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual('private', result.acl)

        sym_key = key + '-sym'
        result = self.client.put_symlink(oss.PutSymlinkRequest(
            bucket=self.bucket_name,
            key=sym_key,
            object_acl='default',
            symlink_target=key,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        result = self.client.get_object_acl(oss.GetObjectAclRequest(
            bucket=self.bucket_name,
            key=sym_key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.GetObjectAclResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual('default', result.acl)

    @unittest.skip("Skip seal_append_object test until environment supports it")
    def test_seal_append_object(self):
        # First create an appendable object
        data1 = b'hello'
        key = OBJECTNAME_PREFIX + random_str(16) + '-seal'

        # Append some data
        result = self.client.append_object(oss.AppendObjectRequest(
            bucket=self.bucket_name,
            key=key,
            position=0,
            body=data1,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(5, result.next_position)

        # Seal the object
        seal_result = self.client.seal_append_object(oss.SealAppendObjectRequest(
            bucket=self.bucket_name,
            key=key,
            position=result.next_position,
        ))
        self.assertIsNotNone(seal_result)
        self.assertEqual(200, seal_result.status_code)
        self.assertIsNotNone(seal_result.sealed_time)

        # Try to append more data - should fail
        try:
            self.client.append_object(oss.AppendObjectRequest(
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
