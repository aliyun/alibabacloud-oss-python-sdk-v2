# pylint: skip-file
from typing import cast
import xml.etree.ElementTree as ET
from alibabacloud_oss_v2 import exceptions
from alibabacloud_oss_v2.models import object_basic as model
from alibabacloud_oss_v2.operations import object_basic as operations
from . import TestOperations

class TestObjectBasic(TestOperations):

    def test_put_object(self):
        request = model.PutObjectRequest(
            bucket='bucket',
            key='key-test',
            acl='private',
            storage_class='ColdArchive',
            metadata={
                "client-side-encryption-key": "nyXOp7delQ/MQLjKQMhHLaTHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=",
                "client-side-encryption-start": "De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=",
                "client-side-encryption-cek-alg": "AES/CTR/NoPadding",
                "client-side-encryption-wrap-alg": "RSA/NONE/PKCS1Padding",
            },
            cache_control='no-cache',
            content_disposition='attachment',
            content_encoding='utf-8',
            content_length=101,
            content_md5='B5eJF1ptWaXm4bijSPyxw==',
            content_type='application/octet-stream',
            expires='2022-10-12T00:00:00.000Z',
            server_side_encryption='SM4',
            server_side_data_encryption='KMS',
            sse_kms_key_id='9468da86-3509-4f8d-a61e-6eab1eac****',
            tagging='tagging-test',
            callback='{\"callbackUrl\":\"www.abc.com/callback\",\"callbackBody\":\"${etag}\"}',
            callback_var='{\"x:var1\":\"value1\",\"x:var2\":\"value2\"}',
            forbid_overwrite=True,
            traffic_limit=100 * 1024 * 8,
            request_payer='request_payer-test',
            body='body-test',
            progress_fn='progress_fn-test',
        )

        result = operations.put_object(self.client, request)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/key-test', self.request_dump.url)
        self.assertEqual('PUT', self.request_dump.method)
        self.assertEqual('private', self.request_dump.headers.get('x-oss-object-acl'))
        self.assertEqual('ColdArchive', self.request_dump.headers.get('x-oss-storage-class'))
        self.assertEqual('nyXOp7delQ/MQLjKQMhHLaTHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=', self.request_dump.headers.get('x-oss-meta-client-side-encryption-key'))
        self.assertEqual('De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=', self.request_dump.headers.get('x-oss-meta-client-side-encryption-start'))
        self.assertEqual('AES/CTR/NoPadding', self.request_dump.headers.get('x-oss-meta-client-side-encryption-cek-alg'))
        self.assertEqual('RSA/NONE/PKCS1Padding', self.request_dump.headers.get('x-oss-meta-client-side-encryption-wrap-alg'))
        self.assertEqual('no-cache', self.request_dump.headers.get('Cache-Control'))
        self.assertEqual('attachment', self.request_dump.headers.get('Content-Disposition'))
        self.assertEqual('utf-8', self.request_dump.headers.get('Content-Encoding'))
        self.assertEqual(101, int(self.request_dump.headers.get('Content-Length')))
        self.assertEqual('B5eJF1ptWaXm4bijSPyxw==', self.request_dump.headers.get('Content-MD5'))
        self.assertEqual('application/octet-stream', self.request_dump.headers.get('Content-Type'))
        self.assertEqual('2022-10-12T00:00:00.000Z', self.request_dump.headers.get('Expires'))
        self.assertEqual('SM4', self.request_dump.headers.get('x-oss-server-side-encryption'))
        self.assertEqual('KMS', self.request_dump.headers.get('x-oss-server-side-data-encryption'))
        self.assertEqual('9468da86-3509-4f8d-a61e-6eab1eac****', self.request_dump.headers.get('x-oss-server-side-encryption-key-id'))
        self.assertEqual('tagging-test', self.request_dump.headers.get('x-oss-tagging'))
        self.assertEqual('{\"callbackUrl\":\"www.abc.com/callback\",\"callbackBody\":\"${etag}\"}', self.request_dump.headers.get('x-oss-callback'))
        self.assertEqual('{\"x:var1\":\"value1\",\"x:var2\":\"value2\"}', self.request_dump.headers.get('x-oss-callback-var'))
        self.assertEqual(True, bool(self.request_dump.headers.get('x-oss-forbid-overwrite')))
        self.assertEqual(100 * 1024 * 8, int(self.request_dump.headers.get('x-oss-traffic-limit')))
        self.assertEqual('request_payer-test', self.request_dump.headers.get('x-oss-request-payer'))


        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual('id-1234', result.request_id)

    def test_put_object_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.PutObjectRequest(
            bucket='bucket',
            key='key-test',
            acl='private',
            storage_class='ColdArchive',
        )

        try:
            result = operations.put_object(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/key-test', self.request_dump.url)
        self.assertEqual('PUT', self.request_dump.method)
        self.assertEqual('private', self.request_dump.headers.get('x-oss-object-acl'))


    def test_head_object(self):
        request = model.HeadObjectRequest(
            bucket='bucket',
            key='key-test',
            version_id='fba9dede5f27731c9771645a3986',
            if_match='D41D8CD98F00B204E9800998ECF8****',
            if_none_match='D41D8CD98F00B204E9800998ECF9****',
            if_modified_since='Fri, 13 Nov 2023 14:47:53 GMT',
            if_unmodified_since='Fri, 13 Nov 2015 14:47:53 GMT',
            request_payer='request_payer-test',
        )

        result = operations.head_object(self.client, request)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/key-test?versionId=fba9dede5f27731c9771645a3986', self.request_dump.url)
        self.assertEqual('HEAD', self.request_dump.method)
        self.assertEqual('D41D8CD98F00B204E9800998ECF8****', self.request_dump.headers.get('If-Match'))
        self.assertEqual('D41D8CD98F00B204E9800998ECF9****', self.request_dump.headers.get('If-None-Match'))
        self.assertEqual('Fri, 13 Nov 2023 14:47:53 GMT', self.request_dump.headers.get('If-Modified-Since'))
        self.assertEqual('Fri, 13 Nov 2015 14:47:53 GMT', self.request_dump.headers.get('If-Unmodified-Since'))
        self.assertEqual('request_payer-test', self.request_dump.headers.get('x-oss-request-payer'))


        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

    def test_head_object_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.HeadObjectRequest(
            bucket='bucket',
            key='key-test',
        )

        try:
            result = operations.head_object(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/key-test', self.request_dump.url)
        self.assertEqual('HEAD', self.request_dump.method)


    def test_get_object(self):
        request = model.GetObjectRequest(
            bucket='bucket',
            key='key-test',
            if_match='D41D8CD98F00B204E9800998ECF8****',
            if_none_match='D41D8CD98F00B204E9800998ECF9****',
            if_modified_since='Fri, 13 Nov 2023 14:47:53 GMT',
            if_unmodified_since='Fri, 13 Nov 2015 14:47:53 GMT',
            range_header='bytes 0~9/44',
            range_behavior='standard',
            response_cache_control='no-cache',
            response_content_disposition='attachment; filename=testing.txt',
            response_content_encoding='utf-8',
            response_content_language='中文',
            response_content_type='text',
            response_expires='Fri, 24 Feb 2012 17:00:00 GMT',
            version_id='CAEQNhiBgM0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY*****',
            traffic_limit=1022,
            process='process-test',
            request_payer='request_payer-test',
            progress_fn='progress_fn-test',
        )

        result = operations.get_object(self.client, request)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/key-test?response-cache-control=no-cache&response-content-disposition=attachment%3B%20filename%3Dtesting.txt&response-content-encoding=utf-8&response-content-language=%E4%B8%AD%E6%96%87&response-content-type=text&response-expires=Fri%2C%2024%20Feb%202012%2017%3A00%3A00%20GMT&versionId=CAEQNhiBgM0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY%2A%2A%2A%2A%2A&x-oss-process=process-test', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)

        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual('D41D8CD98F00B204E9800998ECF8****', self.request_dump.headers.get('If-Match'))
        self.assertEqual('D41D8CD98F00B204E9800998ECF9****', self.request_dump.headers.get('If-None-Match'))
        self.assertEqual('Fri, 13 Nov 2023 14:47:53 GMT', self.request_dump.headers.get('If-Modified-Since'))
        self.assertEqual('Fri, 13 Nov 2015 14:47:53 GMT', self.request_dump.headers.get('If-Unmodified-Since'))
        self.assertEqual('bytes 0~9/44', self.request_dump.headers.get('Range'))
        self.assertEqual('standard', self.request_dump.headers.get('x-oss-range-behavior'))
        self.assertEqual(1022, int(self.request_dump.headers.get('x-oss-traffic-limit')))
        self.assertEqual('request_payer-test', self.request_dump.headers.get('x-oss-request-payer'))

    def test_get_object_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.GetObjectRequest(
            bucket='bucket',
            key='key-test',
        )

        try:
            result = operations.get_object(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/key-test', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)

    def test_append_object(self):
        request = model.AppendObjectRequest(
            bucket='bucket',
            key='example-object-2.jpg',
            position=10,
            acl='private',
            storage_class='ColdArchive',
            metadata={
                "client-side-encryption-key": "nyXOp7delQ/MQLjKQMhHLaTHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=",
                "client-side-encryption-start": "De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=",
                "client-side-encryption-cek-alg": "AES/CTR/NoPadding",
                "client-side-encryption-wrap-alg": "RSA/NONE/PKCS1Padding",
            },
            cache_control='no-cache',
            content_disposition='attachment',
            content_encoding='utf-8',
            content_length=101,
            content_md5='B5eJF1ptWaXm4bijSPyx',
            content_type='application/octet-stream',
            expires='2022-10-12T00:00:00.000Z',
            server_side_encryption='SM4',
            server_side_data_encryption='KMS',
            sse_kms_key_id='9468da86-3509-4f8d-a61e-6eab1eac****',
            tagging='tagging-test',
            forbid_overwrite=True,
            traffic_limit=100*1024*8,
            request_payer='requester',
            body='xml_data',
            progress_fn='progress_fn-test',
        )

        result = operations.append_object(self.client, request)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/example-object-2.jpg?append=&position=10', self.request_dump.url)
        self.assertEqual('POST', self.request_dump.method)
        self.assertEqual('private', self.request_dump.headers.get('x-oss-object-acl'))
        self.assertEqual('ColdArchive', self.request_dump.headers.get('x-oss-storage-class'))
        self.assertEqual('nyXOp7delQ/MQLjKQMhHLaTHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=', self.request_dump.headers.get('x-oss-meta-client-side-encryption-key'))
        self.assertEqual('De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=', self.request_dump.headers.get('x-oss-meta-client-side-encryption-start'))
        self.assertEqual('AES/CTR/NoPadding', self.request_dump.headers.get('x-oss-meta-client-side-encryption-cek-alg'))
        self.assertEqual('RSA/NONE/PKCS1Padding', self.request_dump.headers.get('x-oss-meta-client-side-encryption-wrap-alg'))
        self.assertEqual('no-cache', self.request_dump.headers.get('Cache-Control'))
        self.assertEqual('attachment', self.request_dump.headers.get('Content-Disposition'))
        self.assertEqual('utf-8', self.request_dump.headers.get('Content-Encoding'))
        self.assertEqual('101', self.request_dump.headers.get('Content-Length'))
        self.assertEqual('B5eJF1ptWaXm4bijSPyx', self.request_dump.headers.get('Content-MD5'))
        self.assertEqual('application/octet-stream', self.request_dump.headers.get('Content-Type'))
        self.assertEqual('2022-10-12T00:00:00.000Z', self.request_dump.headers.get('Expires'))
        self.assertEqual('SM4', self.request_dump.headers.get('x-oss-server-side-encryption'))
        self.assertEqual('KMS', self.request_dump.headers.get('x-oss-server-side-data-encryption'))
        self.assertEqual('9468da86-3509-4f8d-a61e-6eab1eac****', self.request_dump.headers.get('x-oss-server-side-encryption-key-id'))
        self.assertEqual('tagging-test', self.request_dump.headers.get('x-oss-tagging'))
        self.assertEqual(True, bool(self.request_dump.headers.get('x-oss-forbid-overwrite')))
        self.assertEqual(100*1024*8, int(self.request_dump.headers.get('x-oss-traffic-limit')))
        self.assertEqual('requester', self.request_dump.headers.get('x-oss-request-payer'))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

    def test_append_object_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.AppendObjectRequest(
            bucket='bucket',
            key='key-test',
            position=10,
        )

        try:
            result = operations.append_object(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/key-test?append=&position=10', self.request_dump.url)
        self.assertEqual('POST', self.request_dump.method)

    def test_copy_object(self):
        request = model.CopyObjectRequest(
            bucket='bucket',
            key='example-object-2.jpg',
            source_key='source-invalid-key',
            source_bucket='source_bucket-test',
            source_version_id='source_version_id-test',
            if_match='D41D8CD98F00B204E9800998ECF8****',
            if_none_match='D41D8CD98F00B204E9800998ECF9****',
            if_modified_since='Fri, 13 Nov 2023 14:47:53 GMT',
            if_unmodified_since='Fri, 13 Nov 2015 14:47:53 GMT',
            acl='private',
            storage_class='ColdArchive',
            metadata={
                "client-side-encryption-key": "nyXOp7delQ/MQLjKQMhHLaTHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=",
                "client-side-encryption-start": "De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=",
                "client-side-encryption-cek-alg": "AES/CTR/NoPadding",
                "client-side-encryption-wrap-alg": "RSA/NONE/PKCS1Padding",
            },
            cache_control='no-cache',
            content_disposition='attachment',
            content_encoding='utf-8',
            content_length=101,
            content_md5='B5eJF1ptWaXm4bijSPyx',
            content_type='application/octet-stream',
            expires='2022-10-12T00:00:00.000Z',
            metadata_directive='metadata_directive-test',
            server_side_encryption='SM4',
            server_side_data_encryption='KMS',
            sse_kms_key_id='9468da86-3509-4f8d-a61e-6eab1eac****',
            tagging='tagging-test',
            tagging_directive='tagging_directive-test',
            forbid_overwrite=True,
            traffic_limit=100*1024*8,
            request_payer='requester',
            progress_fn='progress_fn-test',
        )

        result = operations.copy_object(self.client, request)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/example-object-2.jpg', self.request_dump.url)
        self.assertEqual('PUT', self.request_dump.method)
        self.assertEqual('D41D8CD98F00B204E9800998ECF8****', self.request_dump.headers.get('x-oss-copy-source-if-match'))
        self.assertEqual('D41D8CD98F00B204E9800998ECF9****', self.request_dump.headers.get('x-oss-copy-source-if-none-match'))
        self.assertEqual('Fri, 13 Nov 2023 14:47:53 GMT', self.request_dump.headers.get('x-oss-copy-source-if-modified-since'))
        self.assertEqual('Fri, 13 Nov 2015 14:47:53 GMT', self.request_dump.headers.get('x-oss-copy-source-if-unmodified-since'))
        self.assertEqual('private', self.request_dump.headers.get('x-oss-object-acl'))
        self.assertEqual('ColdArchive', self.request_dump.headers.get('x-oss-storage-class'))
        self.assertEqual('nyXOp7delQ/MQLjKQMhHLaTHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=', self.request_dump.headers.get('x-oss-meta-client-side-encryption-key'))
        self.assertEqual('De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=', self.request_dump.headers.get('x-oss-meta-client-side-encryption-start'))
        self.assertEqual('AES/CTR/NoPadding', self.request_dump.headers.get('x-oss-meta-client-side-encryption-cek-alg'))
        self.assertEqual('RSA/NONE/PKCS1Padding', self.request_dump.headers.get('x-oss-meta-client-side-encryption-wrap-alg'))
        self.assertEqual('no-cache', self.request_dump.headers.get('Cache-Control'))
        self.assertEqual('attachment', self.request_dump.headers.get('Content-Disposition'))
        self.assertEqual('utf-8', self.request_dump.headers.get('Content-Encoding'))
        self.assertEqual(101, int(self.request_dump.headers.get('Content-Length')))
        self.assertEqual('B5eJF1ptWaXm4bijSPyx', self.request_dump.headers.get('Content-MD5'))
        self.assertEqual('application/octet-stream', self.request_dump.headers.get('Content-Type'))
        self.assertEqual('2022-10-12T00:00:00.000Z', self.request_dump.headers.get('Expires'))
        self.assertEqual('metadata_directive-test', self.request_dump.headers.get('x-oss-metadata-directive'))
        self.assertEqual('SM4', self.request_dump.headers.get('x-oss-server-side-encryption'))
        self.assertEqual('KMS', self.request_dump.headers.get('x-oss-server-side-data-encryption'))
        self.assertEqual('9468da86-3509-4f8d-a61e-6eab1eac****', self.request_dump.headers.get('x-oss-server-side-encryption-key-id'))
        self.assertEqual('tagging-test', self.request_dump.headers.get('x-oss-tagging'))
        self.assertEqual('tagging_directive-test', self.request_dump.headers.get('x-oss-tagging-directive'))
        self.assertEqual(True, bool(self.request_dump.headers.get('x-oss-forbid-overwrite')))
        self.assertEqual(100*1024*8, int(self.request_dump.headers.get('x-oss-traffic-limit')))
        self.assertEqual('requester', self.request_dump.headers.get('x-oss-request-payer'))

    def test_copy_object_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.CopyObjectRequest(
            bucket='bucket',
            key='example-object-2.jpg',
            source_key='source-invalid-key',
        )

        try:
            result = operations.copy_object(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/example-object-2.jpg',self.request_dump.url)
        self.assertEqual('PUT', self.request_dump.method)

    def test_delete_object(self):
        request = model.DeleteObjectRequest(
            bucket='bucket',
            key='example-object-2.jpg',
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            request_payer='requester',
        )

        result = operations.delete_object(self.client, request)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/example-object-2.jpg?versionId=CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0%2A%2A%2A%2A', self.request_dump.url)
        self.assertEqual('DELETE', self.request_dump.method)
        self.assertEqual('requester', self.request_dump.headers.get('x-oss-request-payer'))

    def test_delete_object_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.DeleteObjectRequest(
            bucket='bucket',
            key='example-object-2.jpg',
        )

        try:
            result = operations.delete_object(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/example-object-2.jpg', self.request_dump.url)
        self.assertEqual('DELETE', self.request_dump.method)

    def test_delete_multiple_objects(self):
        request = model.DeleteMultipleObjectsRequest(
            bucket='bucket',
            objects=[model.DeleteObject(
                key='key1',
                version_id='ZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            ), model.DeleteObject(
                key='key2',
                version_id='CAEQNhiBgMDJgZCA0BYiIDZjhjYmY0****',
            )],
            encoding_type='url',
            content_length=101,
            quiet=True,
            request_payer='requester',
        )

        result = operations.delete_multiple_objects(self.client, request)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/?delete=&encoding-type=url', self.request_dump.url)
        self.assertEqual('POST', self.request_dump.method)
        self.assertEqual(101, int(self.request_dump.headers.get('Content-Length')))
        self.assertEqual('requester', self.request_dump.headers.get('x-oss-request-payer'))

    def test_delete_multiple_objects_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.DeleteMultipleObjectsRequest(
            bucket='bucket',
            objects=[model.DeleteObject(
                key='key1',
                version_id='ZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            ), model.DeleteObject(
                key='key2',
                version_id='CAEQNhiBgMDJgZCA0BYiIDZjhjYmY0****',
            )],
        )

        try:
            result = operations.delete_multiple_objects(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/?delete=&encoding-type=url', self.request_dump.url)
        self.assertEqual('POST', self.request_dump.method)

    def test_get_object_meta(self):
        request = model.GetObjectMetaRequest(
            bucket='bucket',
            key='example-object-2.jpg',
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            request_payer='requester',
        )

        result = operations.get_object_meta(self.client, request)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/example-object-2.jpg?objectMeta=&versionId=CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0%2A%2A%2A%2A', self.request_dump.url)
        self.assertEqual('HEAD', self.request_dump.method)
        self.assertEqual('requester', self.request_dump.headers.get('x-oss-request-payer'))

    def test_get_object_meta_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.GetObjectMetaRequest(
            bucket='bucket',
            key='example-object-2.jpg',
        )

        try:
            result = operations.get_object_meta(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/example-object-2.jpg?objectMeta=', self.request_dump.url)
        self.assertEqual('HEAD', self.request_dump.method)

    def test_restore_object(self):
        request = model.RestoreObjectRequest(
            bucket='bucket',
            key='example-object-2.jpg',
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            restore_request=model.RestoreRequest(
                days=7,
                tier='Expedited',
            ),
            request_payer='requester',
        )
        result = operations.restore_object(self.client, request)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/example-object-2.jpg?restore=&versionId=CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0%2A%2A%2A%2A', self.request_dump.url)
        self.assertEqual('POST', self.request_dump.method)
        self.assertEqual('requester', self.request_dump.headers.get('x-oss-request-payer'))

        root = ET.fromstring(self.request_dump.body)
        self.assertEqual('RestoreRequest', root.tag)
        self.assertEqual(7, int(root.findtext('Days')))
        self.assertEqual('Expedited', root.findtext('JobParameters.Tier'))

    def test_restore_object_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.RestoreObjectRequest(
            bucket='bucket',
            key='example-object-2.jpg',
        )

        try:
            result = operations.restore_object(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/example-object-2.jpg?restore=', self.request_dump.url)
        self.assertEqual('POST', self.request_dump.method)

    def test_put_object_acl(self):
        request = model.PutObjectAclRequest(
            bucket='bucket',
            key='example-object-2.jpg',
            acl='private',
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            request_payer='requester',
        )

        result = operations.put_object_acl(self.client, request)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/example-object-2.jpg?acl=&versionId=CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0%2A%2A%2A%2A', self.request_dump.url)
        self.assertEqual('PUT', self.request_dump.method)
        self.assertEqual('private', self.request_dump.headers.get('x-oss-object-acl'))
        self.assertEqual('requester', self.request_dump.headers.get('x-oss-request-payer'))


    def test_put_object_acl_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.PutObjectAclRequest(
            bucket='bucket',
            key='example-object-2.jpg',
            acl='private',
        )

        try:
            result = operations.put_object_acl(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/example-object-2.jpg?acl=', self.request_dump.url)
        self.assertEqual('PUT', self.request_dump.method)


    def test_get_object_acl(self):
        request = model.GetObjectAclRequest(
                bucket='bucket',
                key='example-object-2.jpg',
                version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                request_payer='requester',
        )

        result = operations.get_object_acl(self.client, request)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/example-object-2.jpg?acl=&versionId=CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0%2A%2A%2A%2A', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)
        self.assertEqual('requester', self.request_dump.headers.get('x-oss-request-payer'))

    def test_get_object_acl_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.GetObjectAclRequest(
                bucket='bucket',
                key='example-object-2.jpg',
            )

        try:
            result = operations.get_object_acl(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/example-object-2.jpg?acl=', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)


    def test_initiate_multipart_upload(self):
        request = model.InitiateMultipartUploadRequest(
            bucket='bucket',
            key='example-object-2.jpg',
            encoding_type='url',
            storage_class='ColdArchive',
            metadata={
                "client-side-encryption-key": "nyXOp7delQ/MQLjKQMhHLaTHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=",
                "client-side-encryption-start": "De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=",
                "client-side-encryption-cek-alg": "AES/CTR/NoPadding",
                "client-side-encryption-wrap-alg": "RSA/NONE/PKCS1Padding",
            },
            cache_control='no-cache',
            content_disposition='attachment',
            content_encoding='utf-8',
            content_length=101,
            content_md5='B5eJF1ptWaXm4bijSPyx',
            content_type='application/octet-stream',
            expires='2022-10-12T00:00:00.000Z',
            server_side_encryption='SM4',
            server_side_data_encryption='KMS',
            sse_kms_key_id='9468da86-3509-4f8d-a61e-6eab1eac****',
            tagging='tagging-test',
            forbid_overwrite=True,
            request_payer='requester',
            cse_data_size=26446,
            cse_part_size=6298,
        )

        result = operations.initiate_multipart_upload(self.client, request)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/example-object-2.jpg?uploads=&encoding-type=url', self.request_dump.url)
        self.assertEqual('POST', self.request_dump.method)
        self.assertEqual('ColdArchive', self.request_dump.headers.get('x-oss-storage-class'))
        self.assertEqual('nyXOp7delQ/MQLjKQMhHLaTHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=', self.request_dump.headers.get('x-oss-meta-client-side-encryption-key'))
        self.assertEqual('De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=', self.request_dump.headers.get('x-oss-meta-client-side-encryption-start'))
        self.assertEqual('AES/CTR/NoPadding', self.request_dump.headers.get('x-oss-meta-client-side-encryption-cek-alg'))
        self.assertEqual('RSA/NONE/PKCS1Padding', self.request_dump.headers.get('x-oss-meta-client-side-encryption-wrap-alg'))
        self.assertEqual('no-cache', self.request_dump.headers.get('Cache-Control'))
        self.assertEqual('attachment', self.request_dump.headers.get('Content-Disposition'))
        self.assertEqual('utf-8', self.request_dump.headers.get('Content-Encoding'))
        self.assertEqual('101', self.request_dump.headers.get('Content-Length'))
        self.assertEqual('B5eJF1ptWaXm4bijSPyx', self.request_dump.headers.get('Content-MD5'))
        self.assertEqual('application/octet-stream', self.request_dump.headers.get('Content-Type'))
        self.assertEqual('2022-10-12T00:00:00.000Z', self.request_dump.headers.get('Expires'))
        self.assertEqual('SM4', self.request_dump.headers.get('x-oss-server-side-encryption'))
        self.assertEqual('KMS', self.request_dump.headers.get('x-oss-server-side-data-encryption'))
        self.assertEqual('9468da86-3509-4f8d-a61e-6eab1eac****', self.request_dump.headers.get('x-oss-server-side-encryption-key-id'))
        self.assertEqual('tagging-test', self.request_dump.headers.get('x-oss-tagging'))
        self.assertEqual(True, bool(self.request_dump.headers.get('x-oss-forbid-overwrite')))
        self.assertEqual('requester', self.request_dump.headers.get('x-oss-request-payer'))


    def test_initiate_multipart_upload_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.InitiateMultipartUploadRequest(
                bucket='bucket',
                key='example-object-2.jpg',
            )

        try:
            result = operations.initiate_multipart_upload(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/example-object-2.jpg?uploads=&encoding-type=url', self.request_dump.url)
        self.assertEqual('POST', self.request_dump.method)


    def test_upload_part(self):
        request = model.UploadPartRequest(
                bucket='bucket',
                key='example-object-2.jpg',
                part_number=1,
                upload_id='0004B9895DBBB6EC9****',
                content_md5='B5eJF1ptWaXm4bijSPyx',
                content_length=101,
                traffic_limit=100*1024*8,
                body='xml_data',
                request_payer='requester',
                progress_fn='progress_fn-test',
                cse_multipart_context='cse_multipart_context-test',
        )

        result = operations.upload_part(self.client, request)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/example-object-2.jpg?partNumber=1&uploadId=0004B9895DBBB6EC9%2A%2A%2A%2A', self.request_dump.url)
        self.assertEqual('PUT', self.request_dump.method)
        self.assertEqual('B5eJF1ptWaXm4bijSPyx', self.request_dump.headers.get('Content-MD5'))
        self.assertEqual(101, int(self.request_dump.headers.get('Content-Length')))
        self.assertEqual(100*1024*8, int(self.request_dump.headers.get('x-oss-traffic-limit')))
        self.assertEqual('requester', self.request_dump.headers.get('x-oss-request-payer'))


    def test_upload_part_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.UploadPartRequest(
            bucket='bucket',
            key='example-object-2.jpg',
            part_number=1,
            upload_id='0004B9895DBBB6EC9****',
        )

        try:
            result = operations.upload_part(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/example-object-2.jpg?partNumber=1&uploadId=0004B9895DBBB6EC9%2A%2A%2A%2A', self.request_dump.url)
        self.assertEqual('PUT', self.request_dump.method)


    def test_upload_part_copy(self):
        request = model.UploadPartCopyRequest(
                bucket='bucket',
                key='example-object-2.jpg',
                part_number=1,
                upload_id='0004B9895DBBB6EC9',
                source_key='source-invalid-key',
                source_bucket='source_bucket-test',
                source_version_id='source_version_id-test',
                source_range='source_range-test',
                if_match='D41D8CD98F00B204E9800998ECF8****',
                if_none_match='D41D8CD98F00B204E9800998ECF9****',
                if_modified_since='Fri, 13 Nov 2023 14:47:53 GMT',
                if_unmodified_since='Fri, 13 Nov 2015 14:47:53 GMT',
                traffic_limit=100*1024*8,
                request_payer='requester',
        )

        result = operations.upload_part_copy(self.client, request)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/example-object-2.jpg?partNumber=1&uploadId=0004B9895DBBB6EC9', self.request_dump.url)
        self.assertEqual('PUT', self.request_dump.method)
        self.assertEqual('source_range-test', self.request_dump.headers.get('x-oss-copy-source-range'))
        self.assertEqual('D41D8CD98F00B204E9800998ECF8****', self.request_dump.headers.get('x-oss-copy-source-if-match'))
        self.assertEqual('D41D8CD98F00B204E9800998ECF9****', self.request_dump.headers.get('x-oss-copy-source-if-none-match'))
        self.assertEqual('Fri, 13 Nov 2023 14:47:53 GMT', self.request_dump.headers.get('x-oss-copy-source-if-modified-since'))
        self.assertEqual('Fri, 13 Nov 2015 14:47:53 GMT', self.request_dump.headers.get('x-oss-copy-source-if-unmodified-since'))
        self.assertEqual(100 * 1024 * 8, int(self.request_dump.headers.get('x-oss-traffic-limit')))
        self.assertEqual('requester', self.request_dump.headers.get('x-oss-request-payer'))


    def test_upload_part_copy_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.UploadPartCopyRequest(
            bucket='bucket',
            key='example-object-2.jpg',
            part_number=1,
            upload_id='0004B9895DBBB6EC9',
            source_key='source-invalid-key',
        )

        try:
            result = operations.upload_part_copy(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/example-object-2.jpg?partNumber=1&uploadId=0004B9895DBBB6EC9', self.request_dump.url)
        self.assertEqual('PUT', self.request_dump.method)


    def test_complete_multipart_upload(self):
        request = model.CompleteMultipartUploadRequest(
                bucket='bucket',
                key='example-object-2.jpg',
                upload_id='0004B9895DBBB6EC9',
                acl='private',
                complete_multipart_upload=model.CompleteMultipartUpload(
                    parts=[model.UploadPart(
                        part_number=1,
                        etag='ZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                    ), model.UploadPart(
                        part_number=2,
                        etag='jOTRmNTE5NmU5NmFhZjhjYmY0****',
                    )],
                ),
                complete_all='complete_all-test',
                callback='{\"callbackUrl\":\"www.abc.com/callback\",\"callbackBody\":\"${etag}\"}',
                callback_var='{\"x:var1\":\"value1\",\"x:var2\":\"value2\"}',
                forbid_overwrite=True,
                encoding_type='url',
                request_payer='requester',
        )

        result = operations.complete_multipart_upload(self.client, request)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/example-object-2.jpg?encoding-type=url&uploadId=0004B9895DBBB6EC9', self.request_dump.url)
        self.assertEqual('POST', self.request_dump.method)
        self.assertEqual('private', self.request_dump.headers.get('x-oss-object-acl'))
        self.assertEqual('jOTRmNTE5NmU5NmFhZjhjYmY0****', request.complete_multipart_upload.parts[1].etag)
        self.assertEqual('complete_all-test', self.request_dump.headers.get('x-oss-complete-all'))
        self.assertEqual('{\"callbackUrl\":\"www.abc.com/callback\",\"callbackBody\":\"${etag}\"}', self.request_dump.headers.get('x-oss-callback'))
        self.assertEqual('{\"x:var1\":\"value1\",\"x:var2\":\"value2\"}', self.request_dump.headers.get('x-oss-callback-var'))
        self.assertEqual(True, bool(self.request_dump.headers.get('x-oss-forbid-overwrite')))
        self.assertEqual('requester', self.request_dump.headers.get('x-oss-request-payer'))

        root = ET.fromstring(self.request_dump.body)
        self.assertEqual('CompleteMultipartUpload', root.tag)
        self.assertEqual(1, int(root.findall('Part')[0].findtext('PartNumber')))
        self.assertEqual('ZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', root.findall('Part')[0].findtext('ETag'))
        self.assertEqual(2, int(root.findall('Part')[1].findtext('PartNumber')))
        self.assertEqual('jOTRmNTE5NmU5NmFhZjhjYmY0****', root.findall('Part')[1].findtext('ETag'))

    def test_complete_multipart_upload_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.CompleteMultipartUploadRequest(
            bucket='bucket',
            key='example-object-2.jpg',
            upload_id='0004B9895DBBB6EC9',
        )

        try:
            result = operations.complete_multipart_upload(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/example-object-2.jpg?encoding-type=url&uploadId=0004B9895DBBB6EC9', self.request_dump.url)
        self.assertEqual('POST', self.request_dump.method)


    def test_abort_multipart_upload(self):
        request = model.AbortMultipartUploadRequest(
                bucket='bucket',
                key='example-object-2.jpg',
                upload_id='0004B9895DBBB6EC9',
                request_payer='requester',
        )

        result = operations.abort_multipart_upload(self.client, request)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/example-object-2.jpg?uploadId=0004B9895DBBB6EC9', self.request_dump.url)
        self.assertEqual('DELETE', self.request_dump.method)
        self.assertEqual('requester', self.request_dump.headers.get('x-oss-request-payer'))


    def test_abort_multipart_upload_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.AbortMultipartUploadRequest(
            bucket='bucket',
            key='example-object-2.jpg',
            upload_id='0004B9895DBBB6EC9',
        )

        try:
            result = operations.abort_multipart_upload(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/example-object-2.jpg?uploadId=0004B9895DBBB6EC9', self.request_dump.url)
        self.assertEqual('DELETE', self.request_dump.method)



    def test_list_multipart_uploads(self):
        request = model.ListMultipartUploadsRequest(
                bucket='bucket',
                delimiter='/',
                encoding_type='url',
                key_marker='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
                max_uploads=90009,
                prefix='aaa',
                upload_id_marker='upload_id_marker-test',
                request_payer='requester',
                key='example-object-2.jpg',
                upload_id='0004B9895DBBB6EC9',
                initiated='initiated-test',
        )

        result = operations.list_multipart_uploads(self.client, request)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/?encoding-type=url&uploads=&delimiter=%2F&key-marker=ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA&max-uploads=90009&prefix=aaa&upload-id-marker=upload_id_marker-test', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)
        self.assertEqual('requester', self.request_dump.headers.get('x-oss-request-payer'))



    def test_list_multipart_uploads_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.ListMultipartUploadsRequest(
            bucket='bucket',
        )

        try:
            result = operations.list_multipart_uploads(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/?encoding-type=url&uploads=', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)


    def test_list_parts(self):
        request = model.ListPartsRequest(
                bucket='bucket',
                key='example-object-2.jpg',
                upload_id='0004B9895DBBB6EC9',
                encoding_type='url',
                max_parts=12,
                part_mumber_marker='part_mumber_marker-test',
                request_payer='requester',
                part_number='1',
                etag='"D41D8CD98F00B204E9800998ECF8****"',
                last_modified='datetime.datetime.fromtimestamp(1702743657)',
                size='344606',
                hash_crc64='316181249502703****',
        )

        result = operations.list_parts(self.client, request)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/example-object-2.jpg?encoding-type=url&uploadId=0004B9895DBBB6EC9&max-parts=12&part-number-marker=part_mumber_marker-test', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)
        self.assertEqual('requester', self.request_dump.headers.get('x-oss-request-payer'))


    def test_list_parts_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.ListPartsRequest(
            bucket='bucket',
            key='example-object-2.jpg',
            upload_id='0004B9895DBBB6EC9',
        )

        try:
            result = operations.list_parts(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/example-object-2.jpg?encoding-type=url&uploadId=0004B9895DBBB6EC9', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)


