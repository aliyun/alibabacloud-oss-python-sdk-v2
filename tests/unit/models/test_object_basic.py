# pylint: skip-file
import datetime
import unittest
import xml.etree.ElementTree as ET
from alibabacloud_oss_v2 import serde, serde_utils
from alibabacloud_oss_v2.models import object_basic as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict
from .. import MockHttpResponse

class TestPutObject(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutObjectRequest(
            bucket='bucket-test',
            key='key-test',
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsNotNone(request.key)
        self.assertIsNone(request.acl)
        self.assertIsNone(request.storage_class)
        self.assertIsNone(request.metadata)
        self.assertIsNone(request.cache_control)
        self.assertIsNone(request.content_disposition)
        self.assertIsNone(request.content_encoding)
        self.assertIsNone(request.content_length)
        self.assertIsNone(request.content_md5)
        self.assertIsNone(request.content_type)
        self.assertIsNone(request.expires)
        self.assertIsNone(request.server_side_encryption)
        self.assertIsNone(request.server_side_data_encryption)
        self.assertIsNone(request.server_side_encryption_key_id)
        self.assertIsNone(request.tagging)
        self.assertIsNone(request.callback)
        self.assertIsNone(request.callback_var)
        self.assertIsNone(request.forbid_overwrite)
        self.assertIsNone(request.traffic_limit)
        self.assertIsNone(request.request_payer)
        self.assertIsNone(request.body)
        self.assertIsNone(request.progress_fn)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutObjectRequest(
            bucket='bucket-test',
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
            server_side_encryption_key_id='9468da86-3509-4f8d-a61e-6eab1eac****',
            tagging='tagging-test',
            callback='{\"callbackUrl\":\"www.abc.com/callback\",\"callbackBody\":\"${etag}\"}',
            callback_var='{\"x:var1\":\"value1\",\"x:var2\":\"value2\"}',
            forbid_overwrite=True,
            traffic_limit=100*1024*8,
            request_payer='request_payer-test',
            body='body-test',
            progress_fn='progress_fn-test',
        )
        self.assertEqual('bucket-test', request.bucket)
        self.assertEqual('key-test', request.key)
        self.assertEqual('private', request.acl)
        self.assertEqual('ColdArchive', request.storage_class)
        self.assertEqual('nyXOp7delQ/MQLjKQMhHLaTHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=', request.metadata.get("client-side-encryption-key"))
        self.assertEqual('De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=', request.metadata.get("client-side-encryption-start"))
        self.assertEqual('AES/CTR/NoPadding', request.metadata.get("client-side-encryption-cek-alg"))
        self.assertEqual('RSA/NONE/PKCS1Padding', request.metadata.get("client-side-encryption-wrap-alg"))
        self.assertEqual('no-cache', request.cache_control)
        self.assertEqual('attachment', request.content_disposition)
        self.assertEqual('utf-8', request.content_encoding)
        self.assertEqual(101, request.content_length)
        self.assertEqual('B5eJF1ptWaXm4bijSPyxw==',request.content_md5)
        self.assertEqual('application/octet-stream', request.content_type)
        self.assertEqual('2022-10-12T00:00:00.000Z', request.expires)
        self.assertEqual('SM4', request.server_side_encryption)
        self.assertEqual('KMS', request.server_side_data_encryption)
        self.assertEqual('9468da86-3509-4f8d-a61e-6eab1eac****', request.server_side_encryption_key_id)
        self.assertEqual('tagging-test', request.tagging)
        self.assertEqual('{\"callbackUrl\":\"www.abc.com/callback\",\"callbackBody\":\"${etag}\"}', request.callback)
        self.assertEqual('{\"x:var1\":\"value1\",\"x:var2\":\"value2\"}', request.callback_var)
        self.assertEqual(True, request.forbid_overwrite)
        self.assertEqual(100 * 1024 * 8, request.traffic_limit)
        self.assertEqual('request_payer-test', request.request_payer)
        self.assertEqual('body-test', request.body)
        self.assertEqual('progress_fn-test', request.progress_fn)


        request = model.PutObjectRequest(
            bucket='bucket-test',
            key='key-test',
            invalid_field='invalid_field',
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('bucket-test', request.bucket)
        self.assertTrue(hasattr(request, 'key'))
        self.assertEqual('key-test', request.key)
        self.assertFalse(hasattr(request, 'invalid_field'))

        request = model.PutObjectRequest(
            bucket='bucket-test',
            key='key-test',
            headers={'key1': 'value1'},
            parameters={'parm1': 'value1'},
            payload='hello world',
        )
        self.assertEqual('bucket-test', request.bucket)
        self.assertEqual('key-test', request.key)
        self.assertDictEqual({'key1': 'value1'}, request.headers)
        self.assertDictEqual({'parm1': 'value1'}, request.parameters)
        self.assertEqual('hello world', request.payload)


    def test_serialize_request(self):
        request = model.PutObjectRequest(
            bucket='bucket-test',
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
            server_side_encryption_key_id='9468da86-3509-4f8d-a61e-6eab1eac****',
            tagging='tagging-test',
            callback='{\"callbackUrl\":\"www.abc.com/callback\",\"callbackBody\":\"${etag}\"}',
            callback_var='{\"x:var1\":\"value1\",\"x:var2\":\"value2\"}',
            forbid_overwrite=True,
            traffic_limit=100 * 1024 * 8,
            request_payer='request_payer-test',
            body='body-test',
            progress_fn='progress_fn-test',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutObject',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutObject', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucket-test', op_input.bucket)
        self.assertEqual('private', op_input.headers.get('x-oss-object-acl'))
        self.assertEqual('ColdArchive', op_input.headers.get('x-oss-storage-class'))
        self.assertEqual('nyXOp7delQ/MQLjKQMhHLaTHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=', op_input.headers.get('x-oss-meta-client-side-encryption-key'))
        self.assertEqual('De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=', op_input.headers.get('x-oss-meta-client-side-encryption-start'))
        self.assertEqual('AES/CTR/NoPadding', op_input.headers.get('x-oss-meta-client-side-encryption-cek-alg'))
        self.assertEqual('RSA/NONE/PKCS1Padding', op_input.headers.get('x-oss-meta-client-side-encryption-wrap-alg'))
        self.assertEqual('no-cache', op_input.headers.get('Cache-Control'))
        self.assertEqual('attachment', op_input.headers.get('Content-Disposition'))
        self.assertEqual('utf-8', op_input.headers.get('Content-Encoding'))
        self.assertEqual(101, int(op_input.headers.get('Content-Length')))
        self.assertEqual('B5eJF1ptWaXm4bijSPyxw==', op_input.headers.get('Content-MD5'))
        self.assertEqual('application/octet-stream', op_input.headers.get('Content-Type'))
        self.assertEqual('2022-10-12T00:00:00.000Z', op_input.headers.get('Expires'))
        self.assertEqual('SM4', op_input.headers.get('x-oss-server-side-encryption'))
        self.assertEqual('KMS', op_input.headers.get('x-oss-server-side-data-encryption'))
        self.assertEqual('9468da86-3509-4f8d-a61e-6eab1eac****', op_input.headers.get('x-oss-server-side-encryption-key-id'))
        self.assertEqual('tagging-test', op_input.headers.get('x-oss-tagging'))
        self.assertEqual('{\"callbackUrl\":\"www.abc.com/callback\",\"callbackBody\":\"${etag}\"}', op_input.headers.get('x-oss-callback'))
        self.assertEqual('{\"x:var1\":\"value1\",\"x:var2\":\"value2\"}', op_input.headers.get('x-oss-callback-var'))
        self.assertEqual(True, bool(op_input.headers.get('x-oss-forbid-overwrite')))
        self.assertEqual(100 * 1024 * 8, int(op_input.headers.get('x-oss-traffic-limit')))
        self.assertEqual('request_payer-test', op_input.headers.get('x-oss-request-payer'))


    def test_constructor_result(self):
        result = model.PutObjectResult()
        self.assertIsNone(result.content_md5)
        self.assertIsNone(result.etag)
        self.assertIsNone(result.hash_crc64)
        self.assertIsNone(result.version_id)
        self.assertIsNone(result.callback_result)
        self.assertIsInstance(result, serde.Model)

        result = model.PutObjectResult(
            content_md5='1B2M2Y8AsgTpgAmY7PhC****',
            etag='"D41D8CD98F00B204E9800998ECF8****"',
            hash_crc64='316181249502703****',
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            callback_result={"callbackUrl":"www.abc.com/callback","callbackBody":"${etag}"},
        )
        self.assertEqual('1B2M2Y8AsgTpgAmY7PhC****', result.content_md5)
        self.assertEqual('"D41D8CD98F00B204E9800998ECF8****"', result.etag)
        self.assertEqual('316181249502703****', result.hash_crc64)
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.version_id)
        self.assertEqual({"callbackUrl": "www.abc.com/callback", "callbackBody": "${etag}"}, result.callback_result)

        result = model.PutObjectResult(
            version_id='version_id-test',
            invalid_field='invalid_field',
        )
        self.assertEqual('version_id-test', result.version_id)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutObjectResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'content_md5': '1B2M2Y8AsgTpgAmY7PhC****',
                    'etag': '"D41D8CD98F00B204E9800998ECF8****"',
                    'hash_crc64': '316181249502703****',
                    'version_id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={
                        'x-oss-request-id': 'id-1234',
                    },
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('1B2M2Y8AsgTpgAmY7PhC****', result.headers.get('content_md5'))
        self.assertEqual('"D41D8CD98F00B204E9800998ECF8****"', result.headers.get('etag'))
        self.assertEqual('316181249502703****', result.headers.get('hash_crc64'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('version_id'))


class TestHeadObject(unittest.TestCase):
    def test_constructor_request(self):
        request = model.HeadObjectRequest(
            bucket='bucket-test',
            key='key-test',
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsNotNone(request.key)
        self.assertIsNone(request.version_id)
        self.assertIsNone(request.if_match)
        self.assertIsNone(request.if_none_match)
        self.assertIsNone(request.if_modified_since)
        self.assertIsNone(request.if_unmodified_since)
        self.assertIsNone(request.request_payer)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.HeadObjectRequest(
            bucket='bucket-test',
            key='key-test',
            version_id='fba9dede5f27731c9771645a3986****',
            if_match='D41D8CD98F00B204E9800998ECF8****',
            if_none_match='D41D8CD98F00B204E9800998ECF9****',
            if_modified_since='Fri, 13 Nov 2023 14:47:53 GMT',
            if_unmodified_since='Fri, 13 Nov 2015 14:47:53 GMT',
            request_payer='request_payer-test',
        )
        self.assertEqual('bucket-test', request.bucket)
        self.assertEqual('key-test', request.key)
        self.assertEqual('fba9dede5f27731c9771645a3986****', request.version_id)
        self.assertEqual('D41D8CD98F00B204E9800998ECF8****', request.if_match)
        self.assertEqual('D41D8CD98F00B204E9800998ECF9****', request.if_none_match)
        self.assertEqual('Fri, 13 Nov 2023 14:47:53 GMT', request.if_modified_since)
        self.assertEqual('Fri, 13 Nov 2015 14:47:53 GMT', request.if_unmodified_since)
        self.assertEqual('request_payer-test', request.request_payer)

        request = model.HeadObjectRequest(
            bucket='bucket-test',
            key='key-test',
            invalid_field='invalid_field',
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('bucket-test', request.bucket)
        self.assertTrue(hasattr(request, 'key'))
        self.assertEqual('key-test', request.key)
        self.assertFalse(hasattr(request, 'invalid_field'))

        request = model.HeadObjectRequest(
            bucket='bucket-test',
            key='key-test',
            headers={'key1': 'value1'},
            parameters={'parm1': 'value1'},
            payload='hello world',
        )
        self.assertEqual('bucket-test', request.bucket)
        self.assertEqual('key-test', request.key)
        self.assertDictEqual({'key1': 'value1'}, request.headers)
        self.assertDictEqual({'parm1': 'value1'}, request.parameters)
        self.assertEqual('hello world', request.payload)

    def test_serialize_request(self):
        request = model.HeadObjectRequest(
            bucket='bucket-test',
            key='key-test',
            version_id='fba9dede5f27731c9771645a3986****',
            if_match='D41D8CD98F00B204E9800998ECF8****',
            if_none_match='D41D8CD98F00B204E9800998ECF9****',
            if_modified_since='Fri, 13 Nov 2023 14:47:53 GMT',
            if_unmodified_since='Fri, 13 Nov 2015 14:47:53 GMT',
            request_payer='request_payer-test',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='HeadObject',
            method='HEAD',
            bucket=request.bucket,
        ))
        self.assertEqual('HeadObject', op_input.op_name)
        self.assertEqual('HEAD', op_input.method)
        self.assertEqual('bucket-test', op_input.bucket)
        self.assertEqual('D41D8CD98F00B204E9800998ECF8****', op_input.headers.get('If-Match'))
        self.assertEqual('D41D8CD98F00B204E9800998ECF9****', op_input.headers.get('If-None-Match'))
        self.assertEqual('Fri, 13 Nov 2023 14:47:53 GMT', op_input.headers.get('If-Modified-Since'))
        self.assertEqual('Fri, 13 Nov 2015 14:47:53 GMT', op_input.headers.get('If-Unmodified-Since'))
        self.assertEqual('request_payer-test', op_input.headers.get('x-oss-request-payer'))


    def test_constructor_result(self):
        result = model.HeadObjectResult()
        self.assertIsNone(result.content_length)
        self.assertIsNone(result.content_type)
        self.assertIsNone(result.etag)
        self.assertIsNone(result.last_modified)
        self.assertIsNone(result.content_md5)
        self.assertIsNone(result.metadata)
        self.assertIsNone(result.cache_control)
        self.assertIsNone(result.content_disposition)
        self.assertIsNone(result.content_encoding)
        self.assertIsNone(result.expires)
        self.assertIsNone(result.hash_crc64)
        self.assertIsNone(result.storage_class)
        self.assertIsNone(result.object_type)
        self.assertIsNone(result.version_id)
        self.assertIsNone(result.tagging_count)
        self.assertIsNone(result.server_side_encryption)
        self.assertIsNone(result.server_side_data_encryption)
        self.assertIsNone(result.server_side_encryption_key_id)
        self.assertIsNone(result.next_append_position)
        self.assertIsNone(result.expiration)
        self.assertIsNone(result.restore)
        self.assertIsNone(result.process_status)
        self.assertIsNone(result.request_charged)
        self.assertIsNone(result.allow_origin)
        self.assertIsNone(result.allow_methods)
        self.assertIsNone(result.allow_age)
        self.assertIsNone(result.allow_headers)
        self.assertIsNone(result.expose_headers)
        self.assertIsNone(result.transition_time)
        self.assertIsInstance(result, serde.Model)

        result = model.HeadObjectResult(
            content_length=1024,
            content_type='text/xml',
            etag='"A082B659EF78733A5A042FA253B1****"',
            last_modified=datetime.datetime.fromtimestamp(1702743657, datetime.timezone.utc),
            content_md5='B5eJF1ptWaXm4bijSPyxw==',
            metadata={
                "client-side-encryption-key": "nyXOp7delQ/MQLjKQMhHLaTHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=",
                "client-side-encryption-start": "De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=",
                "client-side-encryption-cek-alg": "AES/CTR/NoPadding",
                "client-side-encryption-wrap-alg": "RSA/NONE/PKCS1Padding",
            },
            cache_control='no-cache',
            content_disposition='attachment; filename=testing.txt',
            content_encoding='utf-8',
            expires='2023-10-12T00:00:00.000Z',
            hash_crc64='8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCU',
            storage_class='Archive',
            object_type='public-read-write',
            version_id='version_id-test',
            tagging_count=111,
            server_side_encryption='SM4',
            server_side_data_encryption='AES256',
            server_side_encryption_key_id='9468da86-3509-4f8d-a61e-6eab1eac****',
            next_append_position='222',
            expiration='2022-10-12T00:00:00.000Z',
            restore='ongoing-request=\"false\", expiry-date=\"Sun, 16 Apr 2017 08:12:33 GMT\"',
            process_status='process_status-test',
            request_charged='request_charged-test',
            allow_origin='*',
            allow_methods='PUT,GET',
            allow_age='1111',
            allow_headers='{a:a1, b:b2}',
            expose_headers='{a:a1, b:b2}',
            transition_time='2024-10-12T00:00:00.000Z',
        )
        self.assertEqual(1024, result.content_length)
        self.assertEqual('text/xml', result.content_type)
        self.assertEqual('"A082B659EF78733A5A042FA253B1****"', result.etag)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657, datetime.timezone.utc), result.last_modified)
        self.assertEqual('2023-12-16T16:20:57.000Z', result.last_modified.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('B5eJF1ptWaXm4bijSPyxw==',result.content_md5)
        self.assertEqual('no-cache', result.cache_control)
        self.assertEqual('attachment; filename=testing.txt',result.content_disposition)
        self.assertEqual('utf-8', result.content_encoding)
        self.assertEqual('2023-10-12T00:00:00.000Z', result.expires)
        self.assertEqual('8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCU', result.hash_crc64)
        self.assertEqual('Archive', result.storage_class)
        self.assertEqual('public-read-write', result.object_type)
        self.assertEqual('version_id-test', result.version_id)
        self.assertEqual(111, result.tagging_count)
        self.assertEqual('SM4', result.server_side_encryption)
        self.assertEqual('AES256', result.server_side_data_encryption)
        self.assertEqual('9468da86-3509-4f8d-a61e-6eab1eac****', result.server_side_encryption_key_id)
        self.assertEqual('222', result.next_append_position)
        self.assertEqual('2022-10-12T00:00:00.000Z', result.expiration)
        self.assertEqual('ongoing-request=\"false\", expiry-date=\"Sun, 16 Apr 2017 08:12:33 GMT\"',result.restore)
        self.assertEqual('process_status-test', result.process_status)
        self.assertEqual('request_charged-test', result.request_charged)
        self.assertEqual('*', result.allow_origin)
        self.assertEqual('PUT,GET', result.allow_methods)
        self.assertEqual('1111', result.allow_age)
        self.assertEqual('{a:a1, b:b2}', result.allow_headers)
        self.assertEqual('{a:a1, b:b2}', result.expose_headers)
        self.assertEqual('2024-10-12T00:00:00.000Z', result.transition_time)

        result = model.HeadObjectResult(
            expose_headers='expose_headers-test',
            invalid_field='invalid_field',
        )
        self.assertEqual('expose_headers-test', result.expose_headers)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = None
        result = model.HeadObjectResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'content_md5': '1B2M2Y8AsgTpgAmY7PhC****',
                    'etag': '"D41D8CD98F00B204E9800998ECF8****"',
                    'hash_crc64': '316181249502703****',
                    'version_id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('1B2M2Y8AsgTpgAmY7PhC****', result.headers.get('content_md5'))
        self.assertEqual('"D41D8CD98F00B204E9800998ECF8****"', result.headers.get('etag'))
        self.assertEqual('316181249502703****', result.headers.get('hash_crc64'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('version_id'))


class TestGetObject(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetObjectRequest(
            bucket='bucket-test',
            key='key-test',
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsNotNone(request.key)
        self.assertIsNone(request.if_match)
        self.assertIsNone(request.if_none_match)
        self.assertIsNone(request.if_modified_since)
        self.assertIsNone(request.if_unmodified_since)
        self.assertIsNone(request.range_header)
        self.assertIsNone(request.range_behavior)
        self.assertIsNone(request.response_cache_control)
        self.assertIsNone(request.response_content_disposition)
        self.assertIsNone(request.response_content_encoding)
        self.assertIsNone(request.response_content_language)
        self.assertIsNone(request.response_content_type)
        self.assertIsNone(request.response_expires)
        self.assertIsNone(request.version_id)
        self.assertIsNone(request.traffic_limit)
        self.assertIsNone(request.process)
        self.assertIsNone(request.request_payer)
        self.assertIsNone(request.progress_fn)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetObjectRequest(
            bucket='bucket-test',
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
        self.assertEqual('bucket-test', request.bucket)
        self.assertEqual('key-test', request.key)
        self.assertEqual('D41D8CD98F00B204E9800998ECF8****', request.if_match)
        self.assertEqual('D41D8CD98F00B204E9800998ECF9****', request.if_none_match)
        self.assertEqual('Fri, 13 Nov 2023 14:47:53 GMT', request.if_modified_since)
        self.assertEqual('Fri, 13 Nov 2015 14:47:53 GMT', request.if_unmodified_since)
        self.assertEqual('bytes 0~9/44', request.range_header)
        self.assertEqual('standard', request.range_behavior)
        self.assertEqual('no-cache', request.response_cache_control)
        self.assertEqual('attachment; filename=testing.txt',request.response_content_disposition)
        self.assertEqual('utf-8', request.response_content_encoding)
        self.assertEqual('中文', request.response_content_language)
        self.assertEqual('text', request.response_content_type)
        self.assertEqual('Fri, 24 Feb 2012 17:00:00 GMT', request.response_expires)
        self.assertEqual('CAEQNhiBgM0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY*****', request.version_id)
        self.assertEqual(1022, request.traffic_limit)
        self.assertEqual('process-test', request.process)
        self.assertEqual('request_payer-test', request.request_payer)
        self.assertEqual('progress_fn-test', request.progress_fn)

        request = model.GetObjectRequest(
            bucket='bucket-test',
            key='key-test',
            invalid_field='invalid_field',
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('bucket-test', request.bucket)
        self.assertTrue(hasattr(request, 'key'))
        self.assertEqual('key-test', request.key)
        self.assertFalse(hasattr(request, 'invalid_field'))

        request = model.GetObjectRequest(
            bucket='bucket-test',
            key='key-test',
            headers={'key1': 'value1'},
            parameters={'parm1': 'value1'},
            payload='hello world',
        )
        self.assertEqual('bucket-test', request.bucket)
        self.assertEqual('key-test', request.key)
        self.assertDictEqual({'key1': 'value1'}, request.headers)
        self.assertDictEqual({'parm1': 'value1'}, request.parameters)
        self.assertEqual('hello world', request.payload)

    def test_serialize_request(self):
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

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetObject',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetObject', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucket', op_input.bucket)
        self.assertEqual('D41D8CD98F00B204E9800998ECF8****', op_input.headers.get('If-Match'))
        self.assertEqual('D41D8CD98F00B204E9800998ECF9****', op_input.headers.get('If-None-Match'))
        self.assertEqual('Fri, 13 Nov 2023 14:47:53 GMT', op_input.headers.get('If-Modified-Since'))
        self.assertEqual('Fri, 13 Nov 2015 14:47:53 GMT', op_input.headers.get('If-Unmodified-Since'))
        self.assertEqual('bytes 0~9/44', op_input.headers.get('Range'))
        self.assertEqual('standard', op_input.headers.get('x-oss-range-behavior'))
        self.assertEqual(1022, int(op_input.headers.get('x-oss-traffic-limit')))
        self.assertEqual('request_payer-test', op_input.headers.get('x-oss-request-payer'))


    def test_constructor_result(self):
        result = model.GetObjectResult()
        self.assertIsNone(result.content_length)
        self.assertIsNone(result.content_range)
        self.assertIsNone(result.content_type)
        self.assertIsNone(result.etag)
        self.assertIsNone(result.last_modified)
        self.assertIsNone(result.content_md5)
        self.assertIsNone(result.metadata)
        self.assertIsNone(result.cache_control)
        self.assertIsNone(result.content_disposition)
        self.assertIsNone(result.content_encoding)
        self.assertIsNone(result.expires)
        self.assertIsNone(result.hash_crc64)
        self.assertIsNone(result.storage_class)
        self.assertIsNone(result.object_type)
        self.assertIsNone(result.version_id)
        self.assertIsNone(result.tagging_count)
        self.assertIsNone(result.server_side_encryption)
        self.assertIsNone(result.server_side_data_encryption)
        self.assertIsNone(result.server_side_encryption_key_id)
        self.assertIsNone(result.next_append_position)
        self.assertIsNone(result.expiration)
        self.assertIsNone(result.restore)
        self.assertIsNone(result.process_status)
        self.assertIsNone(result.delete_marker)
        self.assertIsNone(result.body)
        self.assertIsInstance(result, serde.Model)

        result = model.GetObjectResult(
            content_length=1024*10,
            content_range='bytes 0~9/44',
            content_type='application/octet-stream',
            etag='etag-test',
            last_modified=datetime.datetime.fromtimestamp(1702743657, datetime.timezone.utc),
            content_md5='B5eJF1ptWaXm4bijSPyxw==',
            metadata={
                "client-side-encryption-key": "nyXOp7delQ/MQLjKQMhHLaTHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=",
                "client-side-encryption-start": "De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=",
                "client-side-encryption-cek-alg": "AES/CTR/NoPadding",
                "client-side-encryption-wrap-alg": "RSA/NONE/PKCS1Padding",
            },
            cache_control='no-cache',
            content_disposition='attachment',
            content_encoding='utf-8',
            expires='2022-10-12T00:00:00.000Z',
            hash_crc64='316181249502703****',
            storage_class='Archive',
            object_type='public-read-write',
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            tagging_count=2048,
            server_side_encryption='AES256',
            server_side_data_encryption='SM4',
            server_side_encryption_key_id='9468da86-3509-4f8d-a61e-6eab1eac****',
            next_append_position='234',
            expiration='2022-10-12T00:00:00.000Z',
            restore='ongoing-request=\"false\", expiry-date=\"Sun, 16 Apr 2017 08:12:33 GMT\"',
            process_status='process_status-test',
            delete_marker=True,
        )
        self.assertEqual(1024 * 10, int(result.content_length))
        self.assertEqual('bytes 0~9/44', result.content_range)
        self.assertEqual('application/octet-stream', result.content_type)
        self.assertEqual('etag-test', result.etag)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657, datetime.timezone.utc), result.last_modified)
        self.assertEqual('B5eJF1ptWaXm4bijSPyxw==',result.content_md5)
        self.assertEqual('no-cache', result.cache_control)
        self.assertEqual('attachment', result.content_disposition)
        self.assertEqual('utf-8', result.content_encoding)
        self.assertEqual('2022-10-12T00:00:00.000Z', result.expires)
        self.assertEqual('316181249502703****', result.hash_crc64)
        self.assertEqual('Archive', result.storage_class)
        self.assertEqual('public-read-write', result.object_type)
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.version_id)
        self.assertEqual(2048, int(result.tagging_count))
        self.assertEqual('AES256', result.server_side_encryption)
        self.assertEqual('SM4', result.server_side_data_encryption)
        self.assertEqual('9468da86-3509-4f8d-a61e-6eab1eac****', result.server_side_encryption_key_id)
        self.assertEqual('234', result.next_append_position)
        self.assertEqual('2022-10-12T00:00:00.000Z', result.expiration)
        self.assertEqual('ongoing-request=\"false\", expiry-date=\"Sun, 16 Apr 2017 08:12:33 GMT\"',result.restore)
        self.assertEqual('process_status-test', result.process_status)
        self.assertEqual(True, bool(result.delete_marker))

        result = model.GetObjectResult(
            delete_marker=True,
            invalid_field='invalid_field',
        )
        self.assertEqual(True, result.delete_marker)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = None
        result = model.HeadObjectResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'content_md5': '1B2M2Y8AsgTpgAmY7PhC****',
                    'etag': '"D41D8CD98F00B204E9800998ECF8****"',
                    'hash_crc64': '316181249502703****',
                    'version_id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('1B2M2Y8AsgTpgAmY7PhC****', result.headers.get('content_md5'))
        self.assertEqual('"D41D8CD98F00B204E9800998ECF8****"', result.headers.get('etag'))
        self.assertEqual('316181249502703****', result.headers.get('hash_crc64'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('version_id'))


class TestAppendObject(unittest.TestCase):
    def test_constructor_request(self):
        request = model.AppendObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            position=0,
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsNotNone(request.key)
        self.assertIsNotNone(request.position)
        self.assertIsNone(request.acl)
        self.assertIsNone(request.storage_class)
        self.assertIsNone(request.metadata)
        self.assertIsNone(request.cache_control)
        self.assertIsNone(request.content_disposition)
        self.assertIsNone(request.content_encoding)
        self.assertIsNone(request.content_length)
        self.assertIsNone(request.content_md5)
        self.assertIsNone(request.content_type)
        self.assertIsNone(request.expires)
        self.assertIsNone(request.server_side_encryption)
        self.assertIsNone(request.server_side_data_encryption)
        self.assertIsNone(request.server_side_encryption_key_id)
        self.assertIsNone(request.tagging)
        self.assertIsNone(request.forbid_overwrite)
        self.assertIsNone(request.traffic_limit)
        self.assertIsNone(request.request_payer)
        self.assertIsNone(request.body)
        self.assertIsNone(request.progress_fn)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.AppendObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            position=0,
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
            server_side_encryption_key_id='9468da86-3509-4f8d-a61e-6eab1eac****',
            tagging='tagging-test',
            forbid_overwrite=True,
            traffic_limit=100*1024*8,
            request_payer='requester',
            body='xml_data',
            progress_fn='progress_fn-test',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual(0, request.position)
        self.assertEqual('private', request.acl)
        self.assertEqual('ColdArchive', request.storage_class)
        self.assertEqual('nyXOp7delQ/MQLjKQMhHLaTHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=', request.metadata.get("client-side-encryption-key"))
        self.assertEqual('De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=', request.metadata.get("client-side-encryption-start"))
        self.assertEqual('AES/CTR/NoPadding', request.metadata.get("client-side-encryption-cek-alg"))
        self.assertEqual('RSA/NONE/PKCS1Padding', request.metadata.get("client-side-encryption-wrap-alg"))
        self.assertEqual('no-cache', request.cache_control)
        self.assertEqual('attachment', request.content_disposition)
        self.assertEqual('utf-8', request.content_encoding)
        self.assertEqual(101, request.content_length)
        self.assertEqual('B5eJF1ptWaXm4bijSPyx', request.content_md5)
        self.assertEqual('application/octet-stream', request.content_type)
        self.assertEqual('2022-10-12T00:00:00.000Z', request.expires)
        self.assertEqual('SM4', request.server_side_encryption)
        self.assertEqual('KMS', request.server_side_data_encryption)
        self.assertEqual('9468da86-3509-4f8d-a61e-6eab1eac****', request.server_side_encryption_key_id)
        self.assertEqual('tagging-test', request.tagging)
        self.assertEqual(True, request.forbid_overwrite)
        self.assertEqual(100 * 1024 * 8, request.traffic_limit)
        self.assertEqual('requester', request.request_payer)
        self.assertEqual('xml_data', request.body)
        self.assertEqual('progress_fn-test', request.progress_fn)


        request = model.AppendObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            position=0,
            invalid_field='invalid_field',
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('bucket_name', request.bucket)
        self.assertTrue(hasattr(request, 'key'))
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertTrue(hasattr(request, 'position'))
        self.assertEqual(0, request.position)
        self.assertFalse(hasattr(request, 'invalid_field'))

        request = model.AppendObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            position=0,
            headers={'key1': 'value1'},
            parameters={'parm1': 'value1'},
            payload='hello world',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual(0, request.position)
        self.assertDictEqual({'key1': 'value1'}, request.headers)
        self.assertDictEqual({'parm1': 'value1'}, request.parameters)
        self.assertEqual('hello world', request.payload)

    def test_serialize_request(self):
        request = model.AppendObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            position=0,
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
            server_side_encryption_key_id='9468da86-3509-4f8d-a61e-6eab1eac****',
            tagging='tagging-test',
            forbid_overwrite=True,
            traffic_limit=100*1024*8,
            request_payer='requester',
            body='xml_data',
            progress_fn='progress_fn-test',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='AppendObject',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('AppendObject', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)
        self.assertEqual('private', op_input.headers.get('x-oss-object-acl'))
        self.assertEqual('ColdArchive', op_input.headers.get('x-oss-storage-class'))
        self.assertEqual('nyXOp7delQ/MQLjKQMhHLaTHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=', op_input.headers.get('x-oss-meta-client-side-encryption-key'))
        self.assertEqual('De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=', op_input.headers.get('x-oss-meta-client-side-encryption-start'))
        self.assertEqual('AES/CTR/NoPadding', op_input.headers.get('x-oss-meta-client-side-encryption-cek-alg'))
        self.assertEqual('RSA/NONE/PKCS1Padding', op_input.headers.get('x-oss-meta-client-side-encryption-wrap-alg'))
        self.assertEqual('no-cache', op_input.headers.get('Cache-Control'))
        self.assertEqual('attachment', op_input.headers.get('Content-Disposition'))
        self.assertEqual('utf-8', op_input.headers.get('Content-Encoding'))
        self.assertEqual('101', op_input.headers.get('Content-Length'))
        self.assertEqual('B5eJF1ptWaXm4bijSPyx', op_input.headers.get('Content-MD5'))
        self.assertEqual('application/octet-stream', op_input.headers.get('Content-Type'))
        self.assertEqual('2022-10-12T00:00:00.000Z', op_input.headers.get('Expires'))
        self.assertEqual('SM4', op_input.headers.get('x-oss-server-side-encryption'))
        self.assertEqual('KMS', op_input.headers.get('x-oss-server-side-data-encryption'))
        self.assertEqual('9468da86-3509-4f8d-a61e-6eab1eac****', op_input.headers.get('x-oss-server-side-encryption-key-id'))
        self.assertEqual('tagging-test', op_input.headers.get('x-oss-tagging'))
        self.assertEqual(True, bool(op_input.headers.get('x-oss-forbid-overwrite')))
        self.assertEqual(100*1024*8, int(op_input.headers.get('x-oss-traffic-limit')))
        self.assertEqual('requester', op_input.headers.get('x-oss-request-payer'))

    def test_constructor_result(self):
        result = model.AppendObjectResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.AppendObjectResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                    'x-oss-version-id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                    'x-oss-next-append-position': 47,
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('x-oss-version-id'))
        self.assertEqual(47, result.headers.get('x-oss-next-append-position'))


class TestCopyObject(unittest.TestCase):
    def test_constructor_request(self):
        request = model.CopyObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            source_key='source-invalid-key',
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsNotNone(request.key)
        self.assertIsNotNone(request.source_key)
        self.assertIsNone(request.source_bucket)
        self.assertIsNone(request.source_version_id)
        self.assertIsNone(request.if_match)
        self.assertIsNone(request.if_none_match)
        self.assertIsNone(request.if_modified_since)
        self.assertIsNone(request.if_unmodified_since)
        self.assertIsNone(request.acl)
        self.assertIsNone(request.storage_class)
        self.assertIsNone(request.metadata)
        self.assertIsNone(request.cache_control)
        self.assertIsNone(request.content_disposition)
        self.assertIsNone(request.content_encoding)
        self.assertIsNone(request.content_length)
        self.assertIsNone(request.content_md5)
        self.assertIsNone(request.content_type)
        self.assertIsNone(request.expires)
        self.assertIsNone(request.metadata_directive)
        self.assertIsNone(request.server_side_encryption)
        self.assertIsNone(request.server_side_data_encryption)
        self.assertIsNone(request.server_side_encryption_key_id)
        self.assertIsNone(request.tagging)
        self.assertIsNone(request.tagging_directive)
        self.assertIsNone(request.forbid_overwrite)
        self.assertIsNone(request.traffic_limit)
        self.assertIsNone(request.request_payer)
        self.assertIsNone(request.progress_fn)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.CopyObjectRequest(
            bucket='bucket_name',
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
            metadata_directive='COPY',
            server_side_encryption='SM4',
            server_side_data_encryption='KMS',
            server_side_encryption_key_id='9468da86-3509-4f8d-a61e-6eab1eac****',
            tagging='tagging-test',
            tagging_directive='tagging_directive-test',
            forbid_overwrite=True,
            traffic_limit=100*1024*8,
            request_payer='requester',
            progress_fn='progress_fn-test',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('source-invalid-key', request.source_key)
        self.assertEqual('source_bucket-test', request.source_bucket)
        self.assertEqual('source_version_id-test', request.source_version_id)
        self.assertEqual('D41D8CD98F00B204E9800998ECF8****', request.if_match)
        self.assertEqual('D41D8CD98F00B204E9800998ECF9****', request.if_none_match)
        self.assertEqual('Fri, 13 Nov 2023 14:47:53 GMT', request.if_modified_since)
        self.assertEqual('Fri, 13 Nov 2015 14:47:53 GMT', request.if_unmodified_since)
        self.assertEqual('private', request.acl)
        self.assertEqual('ColdArchive', request.storage_class)
        self.assertEqual('nyXOp7delQ/MQLjKQMhHLaTHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=', request.metadata.get("client-side-encryption-key"))
        self.assertEqual('De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=', request.metadata.get("client-side-encryption-start"))
        self.assertEqual('AES/CTR/NoPadding', request.metadata.get("client-side-encryption-cek-alg"))
        self.assertEqual('RSA/NONE/PKCS1Padding', request.metadata.get("client-side-encryption-wrap-alg"))
        self.assertEqual('no-cache', request.cache_control)
        self.assertEqual('attachment', request.content_disposition)
        self.assertEqual('utf-8', request.content_encoding)
        self.assertEqual(101, request.content_length)
        self.assertEqual('B5eJF1ptWaXm4bijSPyx', request.content_md5)
        self.assertEqual('application/octet-stream', request.content_type)
        self.assertEqual('2022-10-12T00:00:00.000Z', request.expires)
        self.assertEqual('COPY', request.metadata_directive)
        self.assertEqual('SM4', request.server_side_encryption)
        self.assertEqual('KMS', request.server_side_data_encryption)
        self.assertEqual('9468da86-3509-4f8d-a61e-6eab1eac****', request.server_side_encryption_key_id)
        self.assertEqual('tagging-test', request.tagging)
        self.assertEqual('tagging_directive-test', request.tagging_directive)
        self.assertEqual(True, request.forbid_overwrite)
        self.assertEqual(100 * 1024 * 8, request.traffic_limit)
        self.assertEqual('requester', request.request_payer)
        self.assertEqual('progress_fn-test', request.progress_fn)


        request = model.CopyObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            source_key='source-invalid-key',
            invalid_field='invalid_field',
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('bucket_name', request.bucket)
        self.assertTrue(hasattr(request, 'key'))
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertTrue(hasattr(request, 'source_key'))
        self.assertEqual('source-invalid-key', request.source_key)
        self.assertFalse(hasattr(request, 'invalid_field'))

        request = model.CopyObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            source_key='source-invalid-key',
            headers={'key1': 'value1'},
            parameters={'parm1': 'value1'},
            payload='hello world',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('source-invalid-key', request.source_key)
        self.assertDictEqual({'key1': 'value1'}, request.headers)
        self.assertDictEqual({'parm1': 'value1'}, request.parameters)
        self.assertEqual('hello world', request.payload)

    def test_serialize_request(self):
        request = model.CopyObjectRequest(
            bucket='bucket_name',
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
            server_side_encryption_key_id='9468da86-3509-4f8d-a61e-6eab1eac****',
            tagging='tagging-test',
            tagging_directive='tagging_directive-test',
            forbid_overwrite=True,
            traffic_limit=100*1024*8,
            request_payer='requester',
            progress_fn='progress_fn-test',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='CopyObject',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('CopyObject', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)
        self.assertEqual('D41D8CD98F00B204E9800998ECF8****', op_input.headers.get('x-oss-copy-source-if-match'))
        self.assertEqual('D41D8CD98F00B204E9800998ECF9****', op_input.headers.get('x-oss-copy-source-if-none-match'))
        self.assertEqual('Fri, 13 Nov 2023 14:47:53 GMT', op_input.headers.get('x-oss-copy-source-if-modified-since'))
        self.assertEqual('Fri, 13 Nov 2015 14:47:53 GMT', op_input.headers.get('x-oss-copy-source-if-unmodified-since'))
        self.assertEqual('private', op_input.headers.get('x-oss-object-acl'))
        self.assertEqual('ColdArchive', op_input.headers.get('x-oss-storage-class'))
        self.assertEqual('nyXOp7delQ/MQLjKQMhHLaTHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=', op_input.headers.get('x-oss-meta-client-side-encryption-key'))
        self.assertEqual('De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=', op_input.headers.get('x-oss-meta-client-side-encryption-start'))
        self.assertEqual('AES/CTR/NoPadding', op_input.headers.get('x-oss-meta-client-side-encryption-cek-alg'))
        self.assertEqual('RSA/NONE/PKCS1Padding', op_input.headers.get('x-oss-meta-client-side-encryption-wrap-alg'))
        self.assertEqual('no-cache', op_input.headers.get('Cache-Control'))
        self.assertEqual('attachment', op_input.headers.get('Content-Disposition'))
        self.assertEqual('utf-8', op_input.headers.get('Content-Encoding'))
        self.assertEqual(101, int(op_input.headers.get('Content-Length')))
        self.assertEqual('B5eJF1ptWaXm4bijSPyx', op_input.headers.get('Content-MD5'))
        self.assertEqual('application/octet-stream', op_input.headers.get('Content-Type'))
        self.assertEqual('2022-10-12T00:00:00.000Z', op_input.headers.get('Expires'))
        self.assertEqual('metadata_directive-test', op_input.headers.get('x-oss-metadata-directive'))
        self.assertEqual('SM4', op_input.headers.get('x-oss-server-side-encryption'))
        self.assertEqual('KMS', op_input.headers.get('x-oss-server-side-data-encryption'))
        self.assertEqual('9468da86-3509-4f8d-a61e-6eab1eac****', op_input.headers.get('x-oss-server-side-encryption-key-id'))
        self.assertEqual('tagging-test', op_input.headers.get('x-oss-tagging'))
        self.assertEqual('tagging_directive-test', op_input.headers.get('x-oss-tagging-directive'))
        self.assertEqual(True, bool(op_input.headers.get('x-oss-forbid-overwrite')))
        self.assertEqual(100*1024*8, int(op_input.headers.get('x-oss-traffic-limit')))
        self.assertEqual('requester', op_input.headers.get('x-oss-request-payer'))

    def test_constructor_result(self):
        result = model.CopyObjectResult()
        self.assertIsNone(result.version_id)
        self.assertIsNone(result.hash_crc64)
        self.assertIsNone(result.source_version_id)
        self.assertIsNone(result.server_side_encryption)
        self.assertIsNone(result.server_side_data_encryption)
        self.assertIsNone(result.server_side_encryption_key_id)
        self.assertIsNone(result.last_modified)
        self.assertIsNone(result.etag)
        self.assertIsInstance(result, serde.Model)

        result = model.CopyObjectResult(
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            hash_crc64='316181249502703****',
            source_version_id='source_version_id-test',
            server_side_encryption='SM4',
            server_side_data_encryption='KMS',
            server_side_encryption_key_id='9468da86-3509-4f8d-a61e-6eab1eac****',
            last_modified=datetime.datetime.fromtimestamp(1702743657, datetime.timezone.utc),
            etag='"D41D8CD98F00B204E9800998ECF8****"',
        )
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.version_id)
        self.assertEqual('316181249502703****', result.hash_crc64)
        self.assertEqual('source_version_id-test', result.source_version_id)
        self.assertEqual('SM4', result.server_side_encryption)
        self.assertEqual('KMS', result.server_side_data_encryption)
        self.assertEqual('9468da86-3509-4f8d-a61e-6eab1eac****', result.server_side_encryption_key_id)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657, datetime.timezone.utc), result.last_modified)
        self.assertEqual('2023-12-16T16:20:57.000Z', result.last_modified.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('"D41D8CD98F00B204E9800998ECF8****"', result.etag)

        result = model.CopyObjectResult(
            etag='"D41D8CD98F00B204E9800998ECF8****"',
            invalid_field='invalid_field',
        )
        self.assertEqual('"D41D8CD98F00B204E9800998ECF8****"', result.etag)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = r'''
<CopyObjectResult>
  <ETag>"C4CA4238A0B923820DCC509A6F75****"</ETag>
  <LastModified>2019-04-09T03:45:32.000Z</LastModified>
</CopyObjectResult>'''

        result = model.CopyObjectResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)
        self.assertEqual('"C4CA4238A0B923820DCC509A6F75****"', result.etag)
        self.assertEqual("2019-04-09T03:45:32.000Z", result.last_modified.strftime('%Y-%m-%dT%H:%M:%S.000Z'))


class TestDeleteObject(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DeleteObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsNotNone(request.key)
        self.assertIsNone(request.version_id)
        self.assertIsNone(request.request_payer)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DeleteObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            request_payer='requester',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', request.version_id)
        self.assertEqual('requester', request.request_payer)

        request = model.DeleteObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            invalid_field='invalid_field',
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('bucket_name', request.bucket)
        self.assertTrue(hasattr(request, 'key'))
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertFalse(hasattr(request, 'invalid_field'))

        request = model.DeleteObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            headers={'key1': 'value1'},
            parameters={'parm1': 'value1'},
            payload='hello world',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertDictEqual({'key1': 'value1'}, request.headers)
        self.assertDictEqual({'parm1': 'value1'}, request.parameters)
        self.assertEqual('hello world', request.payload)

    def test_serialize_request(self):
        request = model.DeleteObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            request_payer='requester',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteObject',
            method='DELETE',
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteObject', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)
        self.assertEqual('requester', op_input.headers.get('x-oss-request-payer'))

    def test_constructor_result(self):
        result = model.DeleteObjectResult()
        self.assertIsNone(result.version_id)
        self.assertIsNone(result.delete_marker)
        self.assertIsInstance(result, serde.Model)

        result = model.DeleteObjectResult(
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            delete_marker=True,
        )
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.version_id)
        self.assertEqual(True, result.delete_marker)

    def test_deserialize_result(self):
        xml_data = None
        result = model.DeleteObjectResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                    'x-oss-version-id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('x-oss-version-id'))


class TestDeleteMultipleObjects(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DeleteMultipleObjectsRequest(
            bucket='bucket_name',
            objects=[model.DeleteObject(
            ),model.DeleteObject(
            )],
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsNotNone(request.objects)
        self.assertIsNone(request.encoding_type)
        self.assertIsNone(request.quiet)
        self.assertIsNone(request.request_payer)
        self.assertIsNone(request.objects[0].key)
        self.assertIsNone(request.objects[0].version_id)
        self.assertIsNone(request.objects[1].key)
        self.assertIsNone(request.objects[1].version_id)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DeleteMultipleObjectsRequest(
            bucket='bucket_name',
            objects=[model.DeleteObject(
                    key='key1',
                    version_id='ZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                ),model.DeleteObject(
                    key='key2',
                    version_id='CAEQNhiBgMDJgZCA0BYiIDZjhjYmY0****',
                ),
            ],
            encoding_type='url',
            content_length=101,
            quiet=True,
            request_payer='requester',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('key1', request.objects[0].key)
        self.assertEqual('ZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', request.objects[0].version_id)
        self.assertEqual('key2', request.objects[1].key)
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDZjhjYmY0****', request.objects[1].version_id)
        self.assertEqual('url', request.encoding_type)
        self.assertEqual(True, request.quiet)
        self.assertEqual('requester', request.request_payer)

        request = model.DeleteMultipleObjectsRequest(
            bucket='bucket_name',
            objects=[model.DeleteObject(
                    key='key1',
                    version_id='ZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                ),
                model.DeleteObject(
                    key='key2',
                    version_id='CAEQNhiBgMDJgZCA0BYiIDZjhjYmY0****',
                ),
            ],
            invalid_field='invalid_field',
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('bucket_name', request.bucket)
        self.assertTrue(hasattr(request, 'objects'))
        self.assertEqual('key1', request.objects[0].key)
        self.assertEqual('ZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', request.objects[0].version_id)
        self.assertEqual('key2', request.objects[1].key)
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDZjhjYmY0****', request.objects[1].version_id)
        self.assertFalse(hasattr(request, 'invalid_field'))

        request = model.DeleteMultipleObjectsRequest(
            bucket='bucket_name',
            objects=[model.DeleteObject(
                    key='key1',
                    version_id='ZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                ),
                model.DeleteObject(
                    key='key2',
                    version_id='CAEQNhiBgMDJgZCA0BYiIDZjhjYmY0****',
                ),
            ],
            headers={'key1': 'value1'},
            parameters={'parm1': 'value1'},
            payload='hello world',
        )
        self.assertEqual('bucket_name', request.bucket)

        self.assertDictEqual({'key1': 'value1'}, request.headers)
        self.assertDictEqual({'parm1': 'value1'}, request.parameters)
        self.assertEqual('hello world', request.payload)

    def test_delete_multiple_objects_request_with_delete(self):
        # Test constructor with Delete parameter
        request = model.DeleteMultipleObjectsRequest(
            bucket='bucket_name',
            delete=model.Delete(
                quiet=True,
                objects=[
                    model.ObjectIdentifier(
                        key='key1',
                        version_id='version1'
                    ),
                    model.ObjectIdentifier(
                        key='key2',
                        version_id='version2'
                    )
                ]
            )
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsNotNone(request.delete)
        self.assertIsNone(request.encoding_type)
        self.assertIsNone(request.objects)
        self.assertIsNone(request.quiet)
        self.assertIsNone(request.request_payer)
        self.assertEqual('bucket_name', request.bucket)
        self.assertTrue(request.delete.quiet)
        self.assertEqual(2, len(request.delete.objects))
        self.assertEqual('key1', request.delete.objects[0].key)
        self.assertEqual('version1', request.delete.objects[0].version_id)
        self.assertEqual('key2', request.delete.objects[1].key)
        self.assertEqual('version2', request.delete.objects[1].version_id)
        self.assertIsInstance(request, serde.RequestModel)

        # Test constructor with both old and new parameters - should work for construction
        request = model.DeleteMultipleObjectsRequest(
            bucket='bucket_name',
            objects=[model.DeleteObject(key='old_key')],
            quiet=False,
            delete=model.Delete(
                quiet=True,
                objects=[
                    model.ObjectIdentifier(key='new_key')
                ]
            ),
            encoding_type='url',
            request_payer='requester'
        )
        self.assertEqual('bucket_name', request.bucket)
        # New parameter should be preserved
        self.assertIsNotNone(request.delete)
        self.assertTrue(request.delete.quiet)
        self.assertEqual(1, len(request.delete.objects))
        self.assertEqual('new_key', request.delete.objects[0].key)
        # Old parameters should also be preserved
        self.assertIsNotNone(request.objects)
        self.assertEqual(1, len(request.objects))
        self.assertEqual('old_key', request.objects[0].key)
        self.assertFalse(request.quiet)
        self.assertEqual('url', request.encoding_type)
        self.assertEqual('requester', request.request_payer)

    def test_serialize_delete_multiple_objects_request_with_delete(self):
        # Test serialization with new Delete parameter
        request_new = model.DeleteMultipleObjectsRequest(
            bucket='bucket_name',
            delete=model.Delete(
                quiet=True,
                objects=[
                    model.ObjectIdentifier(
                        key='key1',
                        version_id='version1'
                    ),
                    model.ObjectIdentifier(
                        key='key2'
                    )
                ]
            ),
            request_payer='requester'
        )

        op_input_new = serde.serialize_input(
            request_new,
            OperationInput(
                op_name='DeleteMultipleObjects',
                method='POST',
                bucket=request_new.bucket,
            ),
            custom_serializer=[
                serde_utils.serialize_delete_objects,
                serde_utils.add_content_md5,
            ],
        )
        self.assertEqual('DeleteMultipleObjects', op_input_new.op_name)
        self.assertEqual('POST', op_input_new.method)
        self.assertEqual('bucket_name', op_input_new.bucket)
        self.assertEqual('requester', op_input_new.headers.get('x-oss-request-payer'))
        
        # Check if the body contains the correct XML for new parameter
        import xml.etree.ElementTree as ET
        root_new = ET.fromstring(op_input_new.body)
        self.assertEqual('Delete', root_new.tag)
        self.assertEqual('true', root_new.findtext('Quiet'))
        objects_new = root_new.findall('Object')
        self.assertEqual(2, len(objects_new))
        self.assertEqual('key1', objects_new[0].findtext('Key'))
        self.assertEqual('version1', objects_new[0].findtext('VersionId'))
        self.assertEqual('key2', objects_new[1].findtext('Key'))
        self.assertIsNone(objects_new[1].find('VersionId'))
        
        # Test serialization with old parameters
        request_old = model.DeleteMultipleObjectsRequest(
            bucket='bucket_name',
            objects=[
                model.DeleteObject(
                    key='key1',
                    version_id='version1'
                ),
                model.DeleteObject(
                    key='key2'
                )
            ],
            quiet=True,
            request_payer='requester'
        )

        op_input_old = serde.serialize_input(
            request_old,
            OperationInput(
                op_name='DeleteMultipleObjects',
                method='POST',
                bucket=request_old.bucket,
            ),
            custom_serializer=[
                serde_utils.serialize_delete_objects,
                serde_utils.add_content_md5,
            ],
        )
        self.assertEqual('DeleteMultipleObjects', op_input_old.op_name)
        self.assertEqual('POST', op_input_old.method)
        self.assertEqual('bucket_name', op_input_old.bucket)
        self.assertEqual('requester', op_input_old.headers.get('x-oss-request-payer'))
        
        # Check if the body contains the correct XML for old parameters
        root_old = ET.fromstring(op_input_old.body)
        self.assertEqual('Delete', root_old.tag)
        self.assertEqual('true', root_old.findtext('Quiet'))
        objects_old = root_old.findall('Object')
        self.assertEqual(2, len(objects_old))
        self.assertEqual('key1', objects_old[0].findtext('Key'))
        self.assertEqual('version1', objects_old[0].findtext('VersionId'))
        self.assertEqual('key2', objects_old[1].findtext('Key'))
        self.assertIsNone(objects_old[1].find('VersionId'))
        
        # Compare the XML generated by new and old parameters - they should be identical
        self.assertEqual(op_input_new.body, op_input_old.body)

    def test_serialize_delete_multiple_objects_request_error_conditions(self):
        # Test serialization error when neither old nor new parameters are set
        request = model.DeleteMultipleObjectsRequest(
            bucket='bucket_name',
        )
        
        with self.assertRaises(Exception) as context:
            serde.serialize_input(
                request,
                OperationInput(
                    op_name='DeleteMultipleObjects',
                    method='POST',
                    bucket=request.bucket,
                ),
                custom_serializer=[
                    serde_utils.serialize_delete_objects,
                    serde_utils.add_content_md5,
                ],
            )
        self.assertIn('Either old parameters', str(context.exception))
        
        # Test serialization error when both old and new parameters are set
        request = model.DeleteMultipleObjectsRequest(
            bucket='bucket_name',
            delete=model.Delete(
                quiet=True,
                objects=[model.ObjectIdentifier(key='new_key')]
            ),
            objects=[model.DeleteObject(key='old_key')],
        )
        
        with self.assertRaises(Exception) as context:
            serde.serialize_input(
                request,
                OperationInput(
                    op_name='DeleteMultipleObjects',
                    method='POST',
                    bucket=request.bucket,
                ),
                custom_serializer=[
                    serde_utils.serialize_delete_objects,
                    serde_utils.add_content_md5,
                ],
            )
        self.assertIn('Either old parameters', str(context.exception))


    def test_serialize_request(self):
        request = model.DeleteMultipleObjectsRequest(
            bucket='bucket_name',
            objects=[model.DeleteObject(
                    key='key1',
                    version_id='ZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                ),
                model.DeleteObject(
                    key='key2',
                    version_id='CAEQNhiBgMDJgZCA0BYiIDZjhjYmY0****',
                ),
            ],
            encoding_type='url',
            quiet=True,
            request_payer='requester',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteMultipleObjects',
            method='DELETE',
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteMultipleObjects', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)
        self.assertEqual('requester', op_input.headers.get('x-oss-request-payer'))

    def test_constructor_result(self):
        result = model.DeleteMultipleObjectsResult()
        self.assertIsNone(result.deleted_objects)
        self.assertIsNone(result.encoding_type)
        self.assertIsInstance(result, serde.Model)

        result = model.DeleteMultipleObjectsResult(
            deleted_objects=[model.DeletedInfo(
                key='key1',
                version_id='ZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                delete_marker=True,
                delete_marker_version_id='E5NmU5NmFhZjhjYmY0****',
            ),model.DeletedInfo(
                key='key2',
                version_id='jOTRmNTE5NmU5NmFhZjhjYmY0****',
                delete_marker=False,
                delete_marker_version_id='mU5NmFhZjhjYmY0****',
            )],
            encoding_type='url',
        )
        self.assertEqual('key1', result.deleted_objects[0].key)
        self.assertEqual('ZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.deleted_objects[0].version_id)
        self.assertEqual(True, result.deleted_objects[0].delete_marker)
        self.assertEqual('E5NmU5NmFhZjhjYmY0****', result.deleted_objects[0].delete_marker_version_id)
        self.assertEqual('key2', result.deleted_objects[1].key)
        self.assertEqual('jOTRmNTE5NmU5NmFhZjhjYmY0****', result.deleted_objects[1].version_id)
        self.assertEqual(False, result.deleted_objects[1].delete_marker)
        self.assertEqual('mU5NmFhZjhjYmY0****', result.deleted_objects[1].delete_marker_version_id)
        self.assertEqual('url', result.encoding_type)

        result = model.DeleteMultipleObjectsResult(
            encoding_type='url',
            invalid_field='invalid_field',
        )
        self.assertEqual('url', result.encoding_type)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = r'''
<DeleteResult>
    <EncodingType>url</EncodingType>
    <Deleted>
       <Key>multipart.data</Key>
       <VersionId>CAEQNRiBgICEoPiC0BYiIGMxZWJmYmMzYjE0OTQ0ZmZhYjgzNzkzYjc2NjZk****</VersionId>
       <DeleteMarker>true</DeleteMarker>
       <DeleteMarkerVersionId>CAEQMhiBgIDXiaaB0BYiIGQzYmRkZGUxMTM1ZDRjOTZhNjk4YjRjMTAyZjhl****</DeleteMarkerVersionId>
    </Deleted>
    <Deleted>
       <Key>test.jpg</Key>
       <VersionId>0BYiIGMxZWJmYmMzYjE0OTQ0ZmZhYjgzNzkzYjc2NjZk****</VersionId>
       <DeleteMarker>true</DeleteMarker>
       <DeleteMarkerVersionId>CAEQMhiBgIDB3aWB0BYiIGUzYTA3YzliMzVmNzRkZGM5NjllYTVlMjYyYWEy****</DeleteMarkerVersionId>
    </Deleted>
</DeleteResult>'''

        result = model.DeleteMultipleObjectsResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)
        self.assertEqual("url", result.encoding_type)
        self.assertEqual("multipart.data", result.deleted_objects[0].key)
        self.assertEqual("CAEQNRiBgICEoPiC0BYiIGMxZWJmYmMzYjE0OTQ0ZmZhYjgzNzkzYjc2NjZk****", result.deleted_objects[0].version_id)
        self.assertEqual(True, result.deleted_objects[0].delete_marker)
        self.assertEqual("CAEQMhiBgIDXiaaB0BYiIGQzYmRkZGUxMTM1ZDRjOTZhNjk4YjRjMTAyZjhl****", result.deleted_objects[0].delete_marker_version_id)
        self.assertEqual("test.jpg", result.deleted_objects[1].key)
        self.assertEqual("0BYiIGMxZWJmYmMzYjE0OTQ0ZmZhYjgzNzkzYjc2NjZk****", result.deleted_objects[1].version_id)
        self.assertEqual(True, result.deleted_objects[1].delete_marker)
        self.assertEqual("CAEQMhiBgIDB3aWB0BYiIGUzYTA3YzliMzVmNzRkZGM5NjllYTVlMjYyYWEy****", result.deleted_objects[1].delete_marker_version_id)


class TestGetObjectMeta(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetObjectMetaRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsNotNone(request.key)
        self.assertIsNone(request.version_id)
        self.assertIsNone(request.request_payer)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetObjectMetaRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            request_payer='requester',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', request.version_id)
        self.assertEqual('requester', request.request_payer)

        request = model.GetObjectMetaRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            invalid_field='invalid_field',
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('bucket_name', request.bucket)
        self.assertTrue(hasattr(request, 'key'))
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertFalse(hasattr(request, 'invalid_field'))

        request = model.GetObjectMetaRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            headers={'key1': 'value1'},
            parameters={'parm1': 'value1'},
            payload='hello world',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertDictEqual({'key1': 'value1'}, request.headers)
        self.assertDictEqual({'parm1': 'value1'}, request.parameters)
        self.assertEqual('hello world', request.payload)

    def test_serialize_request(self):
        request = model.GetObjectMetaRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            request_payer='requester',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetObjectMeta',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetObjectMeta', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)
        self.assertEqual('requester', op_input.headers.get('x-oss-request-payer'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', op_input.parameters.get('versionId'))

    def test_constructor_result(self):
        result = model.GetObjectMetaResult()
        self.assertIsNone(result.content_length)
        self.assertIsNone(result.etag)
        self.assertIsNone(result.last_modified)
        self.assertIsNone(result.last_access_time)
        self.assertIsNone(result.version_id)
        self.assertIsNone(result.hash_crc64)
        self.assertIsNone(result.transition_time)
        self.assertIsInstance(result, serde.Model)

        result = model.GetObjectMetaResult(
            content_length=101,
            etag='"D41D8CD98F00B204E9800998ECF8****"',
            last_modified=datetime.datetime.fromtimestamp(1702743657, datetime.timezone.utc),
            last_access_time=datetime.datetime.fromtimestamp(1702743657, datetime.timezone.utc),
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            hash_crc64='316181249502703****',
            transition_time='2024-10-12T00:00:00.000Z',
        )
        self.assertEqual(101, result.content_length)
        self.assertEqual('"D41D8CD98F00B204E9800998ECF8****"', result.etag)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657, datetime.timezone.utc), result.last_modified)
        self.assertEqual('2023-12-16T16:20:57.000Z', result.last_modified.strftime("%Y-%m-%dT%H:%M:%S.000Z"))
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657, datetime.timezone.utc), result.last_access_time)
        self.assertEqual('2023-12-16T16:20:57.000Z', result.last_access_time.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.version_id)
        self.assertEqual('316181249502703****', result.hash_crc64)
        self.assertEqual('2024-10-12T00:00:00.000Z', result.transition_time)

    def test_deserialize_result(self):
        xml_data = None
        result = model.GetObjectMetaResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'ETag': '"1CF5A685959CA2ED8DE6E5F8ACC2****"',
                    'x-oss-last-access-time': 'Thu, 14 Oct 2021 11:49:05 GMT',
                    'Last-Modified': 'Tue, 09 Apr 2019 06:24:00 GMT',

                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('"1CF5A685959CA2ED8DE6E5F8ACC2****"', result.headers.get('ETag'))
        self.assertEqual('Thu, 14 Oct 2021 11:49:05 GMT', result.headers.get('x-oss-last-access-time'))
        self.assertEqual('Tue, 09 Apr 2019 06:24:00 GMT', result.headers.get('Last-Modified'))


class TestRestoreObject(unittest.TestCase):
    def test_constructor_request(self):
        request = model.RestoreObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsNotNone(request.key)
        self.assertIsNone(request.version_id)
        self.assertIsNone(request.restore_request)
        self.assertIsNone(request.request_payer)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.RestoreObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            restore_request=model.RestoreRequest(
                days=7,
                tier='Expedited',
            ),
            request_payer='requester',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', request.version_id)
        self.assertEqual(7, request.restore_request.days)
        self.assertEqual('Expedited', request.restore_request.tier)
        self.assertEqual('requester', request.request_payer)

        request = model.RestoreObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            restore_request=model.RestoreRequest(
                days=7,
                job_parameters=model.JobParameters(
                    tier="Expedited"
                )
            ),
            request_payer='requester',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', request.version_id)
        self.assertEqual(7, request.restore_request.days)
        self.assertEqual('Expedited', request.restore_request.job_parameters.tier)
        self.assertEqual('requester', request.request_payer)

        request = model.RestoreObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            invalid_field='invalid_field',
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('bucket_name', request.bucket)
        self.assertTrue(hasattr(request, 'key'))
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertFalse(hasattr(request, 'invalid_field'))

        request = model.RestoreObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            headers={'key1': 'value1'},
            parameters={'parm1': 'value1'},
            payload='hello world',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertDictEqual({'key1': 'value1'}, request.headers)
        self.assertDictEqual({'parm1': 'value1'}, request.parameters)
        self.assertEqual('hello world', request.payload)

    def test_serialize_request(self):
        request = model.RestoreObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            restore_request=model.RestoreRequest(
                days=7,
                tier='Expedited',
            ),
            request_payer='requester',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='RestoreObject',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('RestoreObject', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)
        self.assertEqual('requester', op_input.headers.get('x-oss-request-payer'))

        root = ET.fromstring(op_input.body)
        self.assertEqual('RestoreRequest', root.tag)
        self.assertEqual(7, int(root.findtext('Days')))
        self.assertEqual('Expedited', root.findtext('JobParameters/Tier'))


        request = model.RestoreObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            restore_request=model.RestoreRequest(
                days=7,
                job_parameters=model.JobParameters(
                    tier="Standard"
                )
            ),
            request_payer='requester',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='RestoreObject',
            method='POST',
            bucket=request.bucket,
        ))

        root = ET.fromstring(op_input.body)
        self.assertEqual('RestoreRequest', root.tag)
        self.assertEqual(7, int(root.findtext('Days')))
        self.assertEqual('Standard', root.findtext('JobParameters/Tier'))

    def test_constructor_result(self):
        result = model.RestoreObjectResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.RestoreObjectResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                    'x-oss-version-id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                    'x-oss-object-restore-priority': 'Standard',
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('x-oss-version-id'))
        self.assertEqual('Standard', result.headers.get('x-oss-object-restore-priority'))


class TestPutObjectAcl(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutObjectAclRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            acl='private',
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsNotNone(request.key)
        self.assertIsNotNone(request.acl)
        self.assertIsNone(request.version_id)
        self.assertIsNone(request.request_payer)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutObjectAclRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            acl='private',
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            request_payer='requester',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('private', request.acl)
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', request.version_id)
        self.assertEqual('requester', request.request_payer)

        request = model.PutObjectAclRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            acl='private',
            invalid_field='invalid_field',
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('bucket_name', request.bucket)
        self.assertTrue(hasattr(request, 'key'))
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertTrue(hasattr(request, 'acl'))
        self.assertEqual('private', request.acl)
        self.assertFalse(hasattr(request, 'invalid_field'))

        request = model.PutObjectAclRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            acl='private',
            headers={'key1': 'value1'},
            parameters={'parm1': 'value1'},
            payload='hello world',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('private', request.acl)
        self.assertDictEqual({'key1': 'value1'}, request.headers)
        self.assertDictEqual({'parm1': 'value1'}, request.parameters)
        self.assertEqual('hello world', request.payload)

    def test_serialize_request(self):
        request = model.PutObjectAclRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            acl='private',
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            request_payer='requester',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutObjectAcl',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutObjectAcl', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)
        self.assertEqual('private', op_input.headers.get('x-oss-object-acl'))
        self.assertEqual('requester', op_input.headers.get('x-oss-request-payer'))

    def test_constructor_result(self):
        result = model.PutObjectAclResult()
        self.assertIsNone(result.version_id)
        self.assertIsInstance(result, serde.Model)

        result = model.PutObjectAclResult(
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
        )
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.version_id)

        result = model.PutObjectAclResult(
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            invalid_field='invalid_field',
        )
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.version_id)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutObjectAclResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                    'x-oss-version-id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('x-oss-version-id'))


class TestGetObjectAcl(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetObjectAclRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsNotNone(request.key)
        self.assertIsNone(request.version_id)
        self.assertIsNone(request.request_payer)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetObjectAclRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            request_payer='requester',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', request.version_id)
        self.assertEqual('requester', request.request_payer)

        request = model.GetObjectAclRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            invalid_field='invalid_field',
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('bucket_name', request.bucket)
        self.assertTrue(hasattr(request, 'key'))
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertFalse(hasattr(request, 'invalid_field'))

        request = model.GetObjectAclRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            headers={'key1': 'value1'},
            parameters={'parm1': 'value1'},
            payload='hello world',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertDictEqual({'key1': 'value1'}, request.headers)
        self.assertDictEqual({'parm1': 'value1'}, request.parameters)
        self.assertEqual('hello world', request.payload)

    def test_serialize_request(self):
        request = model.GetObjectAclRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            request_payer='requester',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetObjectAcl',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetObjectAcl', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', op_input.parameters.get('versionId'))
        self.assertEqual('requester', op_input.headers.get('x-oss-request-payer'))

    def test_constructor_result(self):
        result = model.GetObjectAclResult()
        self.assertIsNone(result.acl)
        self.assertIsNone(result.owner)
        self.assertIsNone(result.version_id)
        self.assertIsInstance(result, serde.Model)

        result = model.GetObjectAclResult(
            acl='private',
            owner=model.Owner(
                id='id-test',
                display_name='display_name-test',
            ),
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
        )
        self.assertEqual('private', result.acl)
        self.assertEqual('id-test', result.owner.id)
        self.assertEqual('display_name-test', result.owner.display_name)
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.version_id)

        result = model.GetObjectAclResult(
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            invalid_field='invalid_field',
        )
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.version_id)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = r'''
<AccessControlPolicy>
  <Owner>
    <ID>1234513715092****</ID>
    <DisplayName>1234-****</DisplayName>
  </Owner>
  <AccessControlList>
    <Grant>public-read</Grant>
  </AccessControlList>
</AccessControlPolicy>'''

        result = model.GetObjectAclResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)
        self.assertEqual("1234513715092****", result.owner.id)
        self.assertEqual("1234-****", result.owner.display_name)
        self.assertEqual("public-read", result.acl)


class TestInitiateMultipartUpload(unittest.TestCase):
    def test_constructor_request(self):
        request = model.InitiateMultipartUploadRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsNotNone(request.key)
        self.assertIsNone(request.encoding_type)
        self.assertIsNone(request.storage_class)
        self.assertIsNone(request.metadata)
        self.assertIsNone(request.cache_control)
        self.assertIsNone(request.content_disposition)
        self.assertIsNone(request.content_encoding)
        self.assertIsNone(request.content_length)
        self.assertIsNone(request.content_md5)
        self.assertIsNone(request.content_type)
        self.assertIsNone(request.expires)
        self.assertIsNone(request.server_side_encryption)
        self.assertIsNone(request.server_side_data_encryption)
        self.assertIsNone(request.server_side_encryption_key_id)
        self.assertIsNone(request.tagging)
        self.assertIsNone(request.forbid_overwrite)
        self.assertIsNone(request.request_payer)
        self.assertIsNone(request.cse_data_size)
        self.assertIsNone(request.cse_part_size)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.InitiateMultipartUploadRequest(
            bucket='bucket_name',
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
            server_side_encryption_key_id='9468da86-3509-4f8d-a61e-6eab1eac****',
            tagging='tagging-test',
            forbid_overwrite=True,
            request_payer='requester',
            cse_data_size=94472,
            cse_part_size=24210,
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('url', request.encoding_type)
        self.assertEqual('ColdArchive', request.storage_class)
        self.assertEqual('nyXOp7delQ/MQLjKQMhHLaTHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=', request.metadata.get("client-side-encryption-key"))
        self.assertEqual('De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=', request.metadata.get("client-side-encryption-start"))
        self.assertEqual('AES/CTR/NoPadding', request.metadata.get("client-side-encryption-cek-alg"))
        self.assertEqual('RSA/NONE/PKCS1Padding', request.metadata.get("client-side-encryption-wrap-alg"))
        self.assertEqual('no-cache', request.cache_control)
        self.assertEqual('attachment', request.content_disposition)
        self.assertEqual('utf-8', request.content_encoding)
        self.assertEqual(101, request.content_length)
        self.assertEqual('B5eJF1ptWaXm4bijSPyx', request.content_md5)
        self.assertEqual('application/octet-stream', request.content_type)
        self.assertEqual('2022-10-12T00:00:00.000Z', request.expires)
        self.assertEqual('SM4', request.server_side_encryption)
        self.assertEqual('KMS', request.server_side_data_encryption)
        self.assertEqual('9468da86-3509-4f8d-a61e-6eab1eac****', request.server_side_encryption_key_id)
        self.assertEqual('tagging-test', request.tagging)
        self.assertEqual(True, request.forbid_overwrite)
        self.assertEqual('requester', request.request_payer)
        self.assertEqual(94472, request.cse_data_size)
        self.assertEqual(24210, request.cse_part_size)

        request = model.InitiateMultipartUploadRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            invalid_field='invalid_field',
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('bucket_name', request.bucket)
        self.assertTrue(hasattr(request, 'key'))
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertFalse(hasattr(request, 'invalid_field'))

        request = model.InitiateMultipartUploadRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            headers={'key1': 'value1'},
            parameters={'parm1': 'value1'},
            payload='hello world',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertDictEqual({'key1': 'value1'}, request.headers)
        self.assertDictEqual({'parm1': 'value1'}, request.parameters)
        self.assertEqual('hello world', request.payload)

    def test_serialize_request(self):
        request = model.InitiateMultipartUploadRequest(
            bucket='bucket_name',
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
            server_side_encryption_key_id='9468da86-3509-4f8d-a61e-6eab1eac****',
            tagging='tagging-test',
            forbid_overwrite=True,
            request_payer='requester',
            cse_data_size=26446,
            cse_part_size=6298,
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='InitiateMultipartUpload',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('InitiateMultipartUpload', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)
        self.assertEqual('url', op_input.parameters.get('encoding-type'))
        self.assertEqual('ColdArchive', op_input.headers.get('x-oss-storage-class'))
        self.assertEqual('no-cache', op_input.headers.get('Cache-Control'))
        self.assertEqual('attachment', op_input.headers.get('Content-Disposition'))
        self.assertEqual('utf-8', op_input.headers.get('Content-Encoding'))
        self.assertEqual('101', op_input.headers.get('Content-Length'))
        self.assertEqual('B5eJF1ptWaXm4bijSPyx', op_input.headers.get('Content-MD5'))
        self.assertEqual('application/octet-stream', op_input.headers.get('Content-Type'))
        self.assertEqual('2022-10-12T00:00:00.000Z', op_input.headers.get('Expires'))
        self.assertEqual('SM4', op_input.headers.get('x-oss-server-side-encryption'))
        self.assertEqual('KMS', op_input.headers.get('x-oss-server-side-data-encryption'))
        self.assertEqual('9468da86-3509-4f8d-a61e-6eab1eac****', op_input.headers.get('x-oss-server-side-encryption-key-id'))
        self.assertEqual('tagging-test', op_input.headers.get('x-oss-tagging'))
        self.assertEqual(True, bool(op_input.headers.get('x-oss-forbid-overwrite')))
        self.assertEqual('requester', op_input.headers.get('x-oss-request-payer'))

    def test_constructor_result(self):
        result = model.InitiateMultipartUploadResult()
        self.assertIsNone(result.bucket)
        self.assertIsNone(result.key)
        self.assertIsNone(result.upload_id)
        self.assertIsNone(result.encoding_type)
        self.assertIsNone(result.cse_multipart_context)
        self.assertIsInstance(result, serde.Model)

        result = model.InitiateMultipartUploadResult(
            bucket='bucket_name',
            key='example-object-2.jpg',
            upload_id='result.upload_id',
            encoding_type='url',
            cse_multipart_context='Fu|YR6),Rl',
        )
        self.assertEqual('bucket_name', result.bucket)
        self.assertEqual('example-object-2.jpg', result.key)
        self.assertEqual('result.upload_id', result.upload_id)
        self.assertEqual('url', result.encoding_type)
        self.assertEqual('Fu|YR6),Rl', result.cse_multipart_context)

        result = model.InitiateMultipartUploadResult(
            cse_multipart_context='-LP+w|kLr/',
            invalid_field='invalid_field',
        )
        self.assertEqual('-LP+w|kLr/', result.cse_multipart_context)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = r'''
<InitiateMultipartUploadResult>
    <Bucket>oss-example</Bucket>
    <Key>multipart.data</Key>
    <UploadId>0004B9894A22E5B1888A1E29F823****</UploadId>
</InitiateMultipartUploadResult>'''

        result = model.InitiateMultipartUploadResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)
        self.assertEqual("oss-example", result.bucket)
        self.assertEqual("multipart.data", result.key)
        self.assertEqual("0004B9894A22E5B1888A1E29F823****", result.upload_id)




class TestUploadPart(unittest.TestCase):
    def test_constructor_request(self):
        request = model.UploadPartRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            part_number=1,
            upload_id='0004B9894A22E5B1888A1E29F823****',
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsNotNone(request.key)
        self.assertIsNotNone(request.part_number)
        self.assertIsNotNone(request.upload_id)
        self.assertIsNone(request.content_md5)
        self.assertIsNone(request.content_length)
        self.assertIsNone(request.traffic_limit)
        self.assertIsNone(request.body)
        self.assertIsNone(request.request_payer)
        self.assertIsNone(request.progress_fn)
        self.assertIsNone(request.cse_multipart_context)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.UploadPartRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            part_number=1,
            upload_id='0004B9894A22E5B1888A1E29F823****',
            content_md5='B5eJF1ptWaXm4bijSPyx',
            content_length=101,
            traffic_limit=100*1024*8,
            body='xml_data',
            request_payer='requester',
            progress_fn='progress_fn-test',
            cse_multipart_context='894A22E5B1888A1E29F823**',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual(1, request.part_number)
        self.assertEqual('0004B9894A22E5B1888A1E29F823****', request.upload_id)
        self.assertEqual('B5eJF1ptWaXm4bijSPyx', request.content_md5)
        self.assertEqual(101, request.content_length)
        self.assertEqual(100 * 1024 * 8, request.traffic_limit)
        self.assertEqual('xml_data', request.body)
        self.assertEqual('requester', request.request_payer)
        self.assertEqual('progress_fn-test', request.progress_fn)
        self.assertEqual('894A22E5B1888A1E29F823**', request.cse_multipart_context)


        request = model.UploadPartRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            part_number=1,
            upload_id='0004B9894A22E5B1888A1E29F823****',
            invalid_field='invalid_field',
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('bucket_name', request.bucket)
        self.assertTrue(hasattr(request, 'key'))
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertTrue(hasattr(request, 'part_number'))
        self.assertEqual(1, request.part_number)
        self.assertTrue(hasattr(request, 'upload_id'))
        self.assertEqual('0004B9894A22E5B1888A1E29F823****', request.upload_id)
        self.assertFalse(hasattr(request, 'invalid_field'))

        request = model.UploadPartRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            part_number=1,
            upload_id='0004B9894A22E5B1888A1E29F823****',
            headers={'key1': 'value1'},
            parameters={'parm1': 'value1'},
            payload='hello world',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual(1, request.part_number)
        self.assertEqual('0004B9894A22E5B1888A1E29F823****', request.upload_id)
        self.assertDictEqual({'key1': 'value1'}, request.headers)
        self.assertDictEqual({'parm1': 'value1'}, request.parameters)
        self.assertEqual('hello world', request.payload)

    def test_serialize_request(self):
        request = model.UploadPartRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            part_number=1,
            upload_id='0004B9894A22E5B1888A1E29F823****',
            content_md5='B5eJF1ptWaXm4bijSPyx',
            content_length=101,
            traffic_limit=100*1024*8,
            body='xml_data',
            request_payer='requester',
            progress_fn='progress_fn-test',
            cse_multipart_context='894A22E5B1888A1E29F823**',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='UploadPart',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('UploadPart', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)
        self.assertEqual(1, int(op_input.parameters.get('partNumber')))
        self.assertEqual('0004B9894A22E5B1888A1E29F823****', op_input.parameters.get('uploadId'))
        self.assertEqual('B5eJF1ptWaXm4bijSPyx', op_input.headers.get('Content-MD5'))
        self.assertEqual(101, int(op_input.headers.get('Content-Length')))
        self.assertEqual(100*1024*8, int(op_input.headers.get('x-oss-traffic-limit')))
        self.assertEqual('requester', op_input.headers.get('x-oss-request-payer'))

    def test_constructor_result(self):
        result = model.UploadPartResult()
        self.assertIsNone(result.content_md5)
        self.assertIsNone(result.etag)
        self.assertIsNone(result.hash_crc64)
        self.assertIsInstance(result, serde.Model)

        result = model.UploadPartResult(
            content_md5='B5eJF1ptWaXm4bijSPyx',
            etag='"D41D8CD98F00B204E9800998ECF8****"',
            hash_crc64='316181249502703****',
        )
        self.assertEqual('B5eJF1ptWaXm4bijSPyx', result.content_md5)
        self.assertEqual('"D41D8CD98F00B204E9800998ECF8****"', result.etag)
        self.assertEqual('316181249502703****', result.hash_crc64)

        result = model.UploadPartResult(
            hash_crc64='316181249502703****',
            invalid_field='invalid_field',
        )
        self.assertEqual('316181249502703****', result.hash_crc64)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = None
        result = model.UploadPartResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                    'x-oss-version-id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('x-oss-version-id'))


class TestUploadPartCopy(unittest.TestCase):
    def test_constructor_request(self):
        request = model.UploadPartCopyRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            part_number=1,
            upload_id='0004B9894A22E5B1888A1E29F823****',
            source_key='source-invalid-key',
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsNotNone(request.key)
        self.assertIsNotNone(request.part_number)
        self.assertIsNotNone(request.upload_id)
        self.assertIsNotNone(request.source_key)
        self.assertIsNone(request.source_bucket)
        self.assertIsNone(request.source_version_id)
        self.assertIsNone(request.source_range)
        self.assertIsNone(request.if_match)
        self.assertIsNone(request.if_none_match)
        self.assertIsNone(request.if_modified_since)
        self.assertIsNone(request.if_unmodified_since)
        self.assertIsNone(request.traffic_limit)
        self.assertIsNone(request.request_payer)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.UploadPartCopyRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            part_number=1,
            upload_id='0004B9894A22E5B1888A1E29F823****',
            source_key='source-invalid-key',
            source_bucket='source_bucket',
            source_version_id='8F00B204E9800998ECF9**',
            source_range='bytes 0~9/44',
            if_match='D41D8CD98F00B204E9800998ECF8****',
            if_none_match='D41D8CD98F00B204E9800998ECF9****',
            if_modified_since='Fri, 13 Nov 2023 14:47:53 GMT',
            if_unmodified_since='Fri, 13 Nov 2015 14:47:53 GMT',
            traffic_limit=100 * 1024 * 8,
            request_payer='requester',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual(1, request.part_number)
        self.assertEqual('0004B9894A22E5B1888A1E29F823****', request.upload_id)
        self.assertEqual('source-invalid-key', request.source_key)
        self.assertEqual('source_bucket', request.source_bucket)
        self.assertEqual('8F00B204E9800998ECF9**', request.source_version_id)
        self.assertEqual('bytes 0~9/44', request.source_range)
        self.assertEqual('D41D8CD98F00B204E9800998ECF8****', request.if_match)
        self.assertEqual('D41D8CD98F00B204E9800998ECF9****', request.if_none_match)
        self.assertEqual('Fri, 13 Nov 2023 14:47:53 GMT', request.if_modified_since)
        self.assertEqual('Fri, 13 Nov 2015 14:47:53 GMT', request.if_unmodified_since)
        self.assertEqual(100 * 1024 * 8, request.traffic_limit)
        self.assertEqual('requester', request.request_payer)


        request = model.UploadPartCopyRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            part_number=1,
            upload_id='0004B9894A22E5B1888A1E29F823****',
            source_key='source-invalid-key',
            invalid_field='invalid_field',
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('bucket_name', request.bucket)
        self.assertTrue(hasattr(request, 'key'))
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertTrue(hasattr(request, 'part_number'))
        self.assertEqual(1, request.part_number)
        self.assertTrue(hasattr(request, 'upload_id'))
        self.assertEqual('0004B9894A22E5B1888A1E29F823****', request.upload_id)
        self.assertTrue(hasattr(request, 'source_key'))
        self.assertEqual('source-invalid-key', request.source_key)
        self.assertFalse(hasattr(request, 'invalid_field'))

        request = model.UploadPartCopyRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            part_number=1,
            upload_id='0004B9894A22E5B1888A1E29F823****',
            source_key='source-invalid-key',
            headers={'key1': 'value1'},
            parameters={'parm1': 'value1'},
            payload='hello world',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual(1, request.part_number)
        self.assertEqual('0004B9894A22E5B1888A1E29F823****', request.upload_id)
        self.assertEqual('source-invalid-key', request.source_key)
        self.assertDictEqual({'key1': 'value1'}, request.headers)
        self.assertDictEqual({'parm1': 'value1'}, request.parameters)
        self.assertEqual('hello world', request.payload)

    def test_serialize_request(self):
        request = model.UploadPartCopyRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            part_number=1,
            upload_id='0004B9894A22E5B1888A1E29F823****',
            source_key='source-invalid-key',
            source_bucket='source_bucket',
            source_version_id='8F00B204E9800998ECF9**',
            source_range='bytes 0~9/44',
            if_match='D41D8CD98F00B204E9800998ECF8****',
            if_none_match='D41D8CD98F00B204E9800998ECF9****',
            if_modified_since='Fri, 13 Nov 2023 14:47:53 GMT',
            if_unmodified_since='Fri, 13 Nov 2015 14:47:53 GMT',
            traffic_limit=100 * 1024 * 8,
            request_payer='requester',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='UploadPartCopy',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('UploadPartCopy', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)
        self.assertEqual(1, int(op_input.parameters.get('partNumber')))
        self.assertEqual('0004B9894A22E5B1888A1E29F823****', op_input.parameters.get('uploadId'))
        self.assertEqual('bytes 0~9/44', op_input.headers.get('x-oss-copy-source-range'))
        self.assertEqual('D41D8CD98F00B204E9800998ECF8****', op_input.headers.get('x-oss-copy-source-if-match'))
        self.assertEqual('D41D8CD98F00B204E9800998ECF9****', op_input.headers.get('x-oss-copy-source-if-none-match'))
        self.assertEqual('Fri, 13 Nov 2023 14:47:53 GMT', op_input.headers.get('x-oss-copy-source-if-modified-since'))
        self.assertEqual('Fri, 13 Nov 2015 14:47:53 GMT', op_input.headers.get('x-oss-copy-source-if-unmodified-since'))
        self.assertEqual(100 * 1024 * 8, int(op_input.headers.get('x-oss-traffic-limit')))
        self.assertEqual('requester', op_input.headers.get('x-oss-request-payer'))

    def test_constructor_result(self):
        result = model.UploadPartCopyResult()
        self.assertIsNone(result.last_modified)
        self.assertIsNone(result.etag)
        self.assertIsNone(result.source_version_id)
        self.assertIsInstance(result, serde.Model)

        result = model.UploadPartCopyResult(
            last_modified=datetime.datetime.fromtimestamp(1702743657, datetime.timezone.utc),
            etag='"D41D8CD98F00B204E9800998ECF8****"',
            source_version_id='D8CD98F00B204E9800998ECF8**',
        )
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657, datetime.timezone.utc), result.last_modified)
        self.assertEqual('2023-12-16T16:20:57.000Z', result.last_modified.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('"D41D8CD98F00B204E9800998ECF8****"', result.etag)
        self.assertEqual('D8CD98F00B204E9800998ECF8**', result.source_version_id)

        result = model.UploadPartCopyResult(
            source_version_id='D8CD98F00B204E9800998ECF8**',
            invalid_field='invalid_field',
        )
        self.assertEqual('D8CD98F00B204E9800998ECF8**', result.source_version_id)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = r'''
        <CopyObjectResult>
            <ETag>"C4CA4238A0B923820DCC509A6F75****"</ETag>
            <LastModified>2019-04-09T03:45:32.000Z</LastModified>
        </CopyObjectResult>'''

        result = model.UploadPartCopyResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)
        self.assertEqual('"C4CA4238A0B923820DCC509A6F75****"', result.etag)
        self.assertEqual("2019-04-09T03:45:32.000Z", result.last_modified.strftime('%Y-%m-%dT%H:%M:%S.000Z'))


class TestCompleteMultipartUpload(unittest.TestCase):
    def test_constructor_request(self):
        request = model.CompleteMultipartUploadRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            upload_id='0004B9894A22E5B1888A1E29F823****',
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsNotNone(request.key)
        self.assertIsNotNone(request.upload_id)
        self.assertIsNone(request.acl)
        self.assertIsNone(request.complete_multipart_upload)
        self.assertIsNone(request.complete_all)
        self.assertIsNone(request.callback)
        self.assertIsNone(request.callback_var)
        self.assertIsNone(request.forbid_overwrite)
        self.assertIsNone(request.encoding_type)
        self.assertIsNone(request.request_payer)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.CompleteMultipartUploadRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            upload_id='0004B9894A22E5B1888A1E29F823****',
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
            complete_all='false',
            callback='{\"callbackUrl\":\"www.abc.com/callback\",\"callbackBody\":\"${etag}\"}',
            callback_var='{\"x:var1\":\"value1\",\"x:var2\":\"value2\"}',
            forbid_overwrite=True,
            encoding_type='url',
            request_payer='requester',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('0004B9894A22E5B1888A1E29F823****', request.upload_id)
        self.assertEqual('private', request.acl)
        self.assertEqual(1, request.complete_multipart_upload.parts[0].part_number)
        self.assertEqual('ZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', request.complete_multipart_upload.parts[0].etag)
        self.assertEqual(2, request.complete_multipart_upload.parts[1].part_number)
        self.assertEqual('jOTRmNTE5NmU5NmFhZjhjYmY0****', request.complete_multipart_upload.parts[1].etag)
        self.assertEqual('false', request.complete_all)
        self.assertEqual('{\"callbackUrl\":\"www.abc.com/callback\",\"callbackBody\":\"${etag}\"}', request.callback)
        self.assertEqual('{\"x:var1\":\"value1\",\"x:var2\":\"value2\"}', request.callback_var)
        self.assertEqual(True, request.forbid_overwrite)
        self.assertEqual('url', request.encoding_type)
        self.assertEqual('requester', request.request_payer)

        request = model.CompleteMultipartUploadRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            upload_id='0004B9894A22E5B1888A1E29F823****',
            invalid_field='invalid_field',
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('bucket_name', request.bucket)
        self.assertTrue(hasattr(request, 'key'))
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertTrue(hasattr(request, 'upload_id'))
        self.assertEqual('0004B9894A22E5B1888A1E29F823****', request.upload_id)
        self.assertFalse(hasattr(request, 'invalid_field'))

        request = model.CompleteMultipartUploadRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            upload_id='0004B9894A22E5B1888A1E29F823****',
            headers={'key1': 'value1'},
            parameters={'parm1': 'value1'},
            payload='hello world',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('0004B9894A22E5B1888A1E29F823****', request.upload_id)
        self.assertDictEqual({'key1': 'value1'}, request.headers)
        self.assertDictEqual({'parm1': 'value1'}, request.parameters)
        self.assertEqual('hello world', request.payload)

    def test_serialize_request(self):
        request = model.CompleteMultipartUploadRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            upload_id='0004B9894A22E5B1888A1E29F823****',
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
            complete_all='true',
            callback='{\"callbackUrl\":\"www.abc.com/callback\",\"callbackBody\":\"${etag}\"}',
            callback_var='{\"x:var1\":\"value1\",\"x:var2\":\"value2\"}',
            forbid_overwrite=True,
            encoding_type='url',
            request_payer='requester',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='CompleteMultipartUpload',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('CompleteMultipartUpload', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)
        self.assertEqual('0004B9894A22E5B1888A1E29F823****', op_input.parameters.get('uploadId'))
        self.assertEqual('url', op_input.parameters.get('encoding-type'))
        self.assertEqual('private', op_input.headers.get('x-oss-object-acl'))
        self.assertEqual('true', op_input.headers.get('x-oss-complete-all'))
        self.assertEqual('{\"callbackUrl\":\"www.abc.com/callback\",\"callbackBody\":\"${etag}\"}', op_input.headers.get('x-oss-callback'))
        self.assertEqual('{\"x:var1\":\"value1\",\"x:var2\":\"value2\"}', op_input.headers.get('x-oss-callback-var'))
        self.assertEqual(True, bool(op_input.headers.get('x-oss-forbid-overwrite')))
        self.assertEqual('requester', op_input.headers.get('x-oss-request-payer'))

        root = ET.fromstring(op_input.body)
        self.assertEqual('CompleteMultipartUpload', root.tag)
        self.assertEqual(1, int(root.findall('Part')[0].findtext('PartNumber')))
        self.assertEqual('ZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', root.findall('Part')[0].findtext('ETag'))
        self.assertEqual(2, int(root.findall('Part')[1].findtext('PartNumber')))
        self.assertEqual('jOTRmNTE5NmU5NmFhZjhjYmY0****', root.findall('Part')[1].findtext('ETag'))

    def test_constructor_result(self):
        result = model.CompleteMultipartUploadResult()
        self.assertIsNone(result.bucket)
        self.assertIsNone(result.key)
        self.assertIsNone(result.location)
        self.assertIsNone(result.etag)
        self.assertIsNone(result.encoding_type)
        self.assertIsNone(result.hash_crc64)
        self.assertIsNone(result.version_id)
        self.assertIsNone(result.callback_result)
        self.assertIsInstance(result, serde.Model)

        result = model.CompleteMultipartUploadResult(
            bucket='bucket_name',
            key='example-object-2.jpg',
            location='oss-cn-hangzhou',
            etag='"D41D8CD98F00B204E9800998ECF8****"',
            encoding_type='url',
            hash_crc64='316181249502703****',
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            callback_result={
                "callbackUrl": "172.16.XX.XX/test.php",
                "callbackHost": "oss-cn-hangzhou.aliyuncs.com",
                "callbackBody": "{\"mimeType\":${mimeType},\"size\":${size}}",
                "callbackBodyType": "application/json",
                "callbackSNI": False,
            },
        )
        self.assertEqual('bucket_name', result.bucket)
        self.assertEqual('example-object-2.jpg', result.key)
        self.assertEqual('oss-cn-hangzhou', result.location)
        self.assertEqual('"D41D8CD98F00B204E9800998ECF8****"', result.etag)
        self.assertEqual('url', result.encoding_type)
        self.assertEqual('316181249502703****', result.hash_crc64)
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.version_id)
        self.assertEqual("172.16.XX.XX/test.php", result.callback_result.get("callbackUrl"))
        self.assertEqual("oss-cn-hangzhou.aliyuncs.com", result.callback_result.get("callbackHost"))
        self.assertEqual("{\"mimeType\":${mimeType},\"size\":${size}}", result.callback_result.get("callbackBody"))
        self.assertEqual("application/json", result.callback_result.get("callbackBodyType"))
        self.assertEqual(False, result.callback_result.get("callbackSNI"))


        result = model.CompleteMultipartUploadResult(
            key='example-object-2.jpg',
            invalid_field='invalid_field',
        )
        self.assertEqual('example-object-2.jpg', result.key)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = r'''
<CompleteMultipartUploadResult>
    <EncodingType>url</EncodingType>
    <Location>http://oss-example.oss-cn-hangzhou.aliyuncs.com /multipart.data</Location>
    <Bucket>oss-example</Bucket>
    <Key>multipart.data</Key>
    <ETag>"B864DB6A936D376F9F8D3ED3BBE540****"</ETag>
</CompleteMultipartUploadResult>'''

        result = model.CompleteMultipartUploadResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)
        self.assertEqual("url", result.encoding_type)
        self.assertEqual("http://oss-example.oss-cn-hangzhou.aliyuncs.com /multipart.data", result.location)
        self.assertEqual("oss-example", result.bucket)
        self.assertEqual("multipart.data", result.key)
        self.assertEqual('"B864DB6A936D376F9F8D3ED3BBE540****"', result.etag)


class TestAbortMultipartUpload(unittest.TestCase):
    def test_constructor_request(self):
        request = model.AbortMultipartUploadRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            upload_id='0004B9894A22E5B1888A1E29F823****',
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsNotNone(request.key)
        self.assertIsNotNone(request.upload_id)
        self.assertIsNone(request.request_payer)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.AbortMultipartUploadRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            upload_id='0004B9894A22E5B1888A1E29F823****',
            request_payer='requester',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('0004B9894A22E5B1888A1E29F823****', request.upload_id)
        self.assertEqual('requester', request.request_payer)

        request = model.AbortMultipartUploadRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            upload_id='0004B9894A22E5B1888A1E29F823****',
            invalid_field='invalid_field',
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('bucket_name', request.bucket)
        self.assertTrue(hasattr(request, 'key'))
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertTrue(hasattr(request, 'upload_id'))
        self.assertEqual('0004B9894A22E5B1888A1E29F823****', request.upload_id)
        self.assertFalse(hasattr(request, 'invalid_field'))

        request = model.AbortMultipartUploadRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            upload_id='0004B9894A22E5B1888A1E29F823****',
            headers={'key1': 'value1'},
            parameters={'parm1': 'value1'},
            payload='hello world',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('0004B9894A22E5B1888A1E29F823****', request.upload_id)
        self.assertDictEqual({'key1': 'value1'}, request.headers)
        self.assertDictEqual({'parm1': 'value1'}, request.parameters)
        self.assertEqual('hello world', request.payload)

    def test_serialize_request(self):
        request = model.AbortMultipartUploadRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            upload_id='0004B9894A22E5B1888A1E29F823****',
            request_payer='requester',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='AbortMultipartUpload',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('AbortMultipartUpload', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)
        self.assertEqual('0004B9894A22E5B1888A1E29F823****', op_input.parameters.get('uploadId'))
        self.assertEqual('requester', op_input.headers.get('x-oss-request-payer'))

    def test_constructor_result(self):
        result = model.AbortMultipartUploadResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.AbortMultipartUploadResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                    'x-oss-version-id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('x-oss-version-id'))


class TestListMultipartUploads(unittest.TestCase):
    def test_constructor_request(self):
        request = model.ListMultipartUploadsRequest(
            bucket='bucket_name',
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsNone(request.delimiter)
        self.assertIsNone(request.encoding_type)
        self.assertIsNone(request.key_marker)
        self.assertIsNone(request.max_uploads)
        self.assertIsNone(request.prefix)
        self.assertIsNone(request.upload_id_marker)
        self.assertIsNone(request.request_payer)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.ListMultipartUploadsRequest(
            bucket='bucket_name',
            delimiter='/',
            encoding_type='url',
            key_marker='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            max_uploads=90009,
            prefix='aaa',
            upload_id_marker='VyL2VyaWMvZGVtbzMuanNvbhAA',
            request_payer='requester',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('/', request.delimiter)
        self.assertEqual('url', request.encoding_type)
        self.assertEqual('ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', request.key_marker)
        self.assertEqual(90009, request.max_uploads)
        self.assertEqual('aaa', request.prefix)
        self.assertEqual('VyL2VyaWMvZGVtbzMuanNvbhAA', request.upload_id_marker)
        self.assertEqual('requester', request.request_payer)

        request = model.ListMultipartUploadsRequest(
            bucket='bucket_name',
            invalid_field='invalid_field',
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('bucket_name', request.bucket)
        self.assertFalse(hasattr(request, 'invalid_field'))

        request = model.ListMultipartUploadsRequest(
            bucket='bucket_name',
            headers={'key1': 'value1'},
            parameters={'parm1': 'value1'},
            payload='hello world',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertDictEqual({'key1': 'value1'}, request.headers)
        self.assertDictEqual({'parm1': 'value1'}, request.parameters)
        self.assertEqual('hello world', request.payload)

    def test_serialize_request(self):
        request = model.ListMultipartUploadsRequest(
            bucket='bucket_name',
            delimiter='/',
            encoding_type='url',
            key_marker='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            max_uploads=90009,
            prefix='aaa',
            upload_id_marker='VyL2VyaWMvZGVtbzMuanNvbhAA',
            request_payer='requester',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='ListMultipartUploads',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('ListMultipartUploads', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)
        self.assertEqual('/', op_input.parameters.get('delimiter'))
        self.assertEqual('url', op_input.parameters.get('encoding-type'))
        self.assertEqual('ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', op_input.parameters.get('key-marker'))
        self.assertEqual(90009, int(op_input.parameters.get('max-uploads')))
        self.assertEqual('aaa', op_input.parameters.get('prefix'))
        self.assertEqual('VyL2VyaWMvZGVtbzMuanNvbhAA', op_input.parameters.get('upload-id-marker'))
        self.assertEqual('requester', op_input.headers.get('x-oss-request-payer'))

    def test_constructor_result(self):
        result = model.ListMultipartUploadsResult()
        self.assertIsNone(result.encoding_type)
        self.assertIsNone(result.bucket)
        self.assertIsNone(result.key_marker)
        self.assertIsNone(result.upload_id_marker)
        self.assertIsNone(result.next_key_marker)
        self.assertIsNone(result.next_upload_id_marker)
        self.assertIsNone(result.delimiter)
        self.assertIsNone(result.prefix)
        self.assertIsNone(result.max_uploads)
        self.assertIsNone(result.is_truncated)
        self.assertIsNone(result.uploads)

        result = model.ListMultipartUploadsResult(
            encoding_type='url',
            bucket='bucket_name',
            key_marker='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            upload_id_marker='VyL2VyaWMvZGVtbzMuanNvbhAA',
            next_key_marker='demo%2FREADME-CN.md',
            next_upload_id_marker='VyL2VzMuanNvbhAA',
            delimiter='/',
            prefix='aaa',
            max_uploads=90009,
            is_truncated=True,
            uploads=[model.Upload(
                key='example-object-1.jpg',
                upload_id='0004B9894A22E5B1888A1E29F823****',
                initiated=datetime.datetime.fromtimestamp(1702743657, datetime.timezone.utc),
            ), model.Upload(
                key='example-object-2.jpg',
                upload_id='4B9894A22E5B1888A1E29F823****',
                initiated=datetime.datetime.fromtimestamp(1702743657, datetime.timezone.utc),
            )],
        )
        self.assertEqual('url', result.encoding_type)
        self.assertEqual('bucket_name', result.bucket)
        self.assertEqual('ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', result.key_marker)
        self.assertEqual('VyL2VyaWMvZGVtbzMuanNvbhAA', result.upload_id_marker)
        self.assertEqual('demo%2FREADME-CN.md', result.next_key_marker)
        self.assertEqual('VyL2VzMuanNvbhAA', result.next_upload_id_marker)
        self.assertEqual('/', result.delimiter)
        self.assertEqual('aaa', result.prefix)
        self.assertEqual(90009, result.max_uploads)
        self.assertEqual(True, result.is_truncated)
        self.assertEqual('example-object-1.jpg', result.uploads[0].key)
        self.assertEqual('0004B9894A22E5B1888A1E29F823****', result.uploads[0].upload_id)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657, datetime.timezone.utc), result.uploads[0].initiated)
        self.assertEqual('2023-12-16T16:20:57.000Z', result.uploads[0].initiated.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('example-object-2.jpg', result.uploads[1].key)
        self.assertEqual('4B9894A22E5B1888A1E29F823****', result.uploads[1].upload_id)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657, datetime.timezone.utc), result.uploads[1].initiated)
        self.assertEqual('2023-12-16T16:20:57.000Z', result.uploads[0].initiated.strftime('%Y-%m-%dT%H:%M:%S.000Z'))


        result = model.ListMultipartUploadsResult(
            bucket='bucket',
            key_marker='example-object-2.jpg',
            invalid_field='invalid_field',
        )
        self.assertEqual('bucket', result.bucket)
        self.assertEqual('example-object-2.jpg', result.key_marker)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = r'''
<ListMultipartUploadsResult>
    <Bucket>oss-example</Bucket>
    <KeyMarker>sadagfsd</KeyMarker>
    <UploadIdMarker>eeev34536dd</UploadIdMarker>
    <NextKeyMarker>oss.avi</NextKeyMarker>
    <NextUploadIdMarker>0004B99B8E707874FC2D692FA5D77D3F</NextUploadIdMarker>
    <Delimiter>/</Delimiter>
    <Prefix>11waa/</Prefix>
    <MaxUploads>1000</MaxUploads>
    <IsTruncated>false</IsTruncated>
    <Upload>
        <Key>multipart1.data</Key>
        <UploadId>0004B999EF518A1FE585B0C9360DC4C8</UploadId>
        <Initiated>2011-02-23T04:18:23.000Z</Initiated>
    </Upload>
    <Upload>
        <Key>multipart2.data</Key>
        <UploadId>F5A239BB9138C6227D6****</UploadId>
        <Initiated>2012-02-23T04:18:23.000Z</Initiated>
    </Upload>
    <Upload>
        <Key>oss.avi</Key>
        <UploadId>0004B99B8E707874FC2D692FA5D7****</UploadId>
        <Initiated>2012-02-23T06:14:27.000Z</Initiated>
    </Upload>
</ListMultipartUploadsResult>'''

        result = model.ListMultipartUploadsResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)
        self.assertEqual("oss-example", result.bucket)
        self.assertEqual("sadagfsd", result.key_marker)
        self.assertEqual("eeev34536dd", result.upload_id_marker)
        self.assertEqual("oss.avi", result.next_key_marker)
        self.assertEqual("0004B99B8E707874FC2D692FA5D77D3F", result.next_upload_id_marker)
        self.assertEqual("/", result.delimiter)
        self.assertEqual("11waa/", result.prefix)
        self.assertEqual(1000, result.max_uploads)
        self.assertEqual(False, result.is_truncated)
        self.assertEqual("multipart1.data", result.uploads[0].key)
        self.assertEqual("0004B999EF518A1FE585B0C9360DC4C8", result.uploads[0].upload_id)
        self.assertEqual("2011-02-23T04:18:23.000Z", result.uploads[0].initiated.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual("multipart2.data", result.uploads[1].key)
        self.assertEqual("F5A239BB9138C6227D6****", result.uploads[1].upload_id)
        self.assertEqual("2012-02-23T04:18:23.000Z", result.uploads[1].initiated.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual("oss.avi", result.uploads[2].key)
        self.assertEqual("0004B99B8E707874FC2D692FA5D7****", result.uploads[2].upload_id)
        self.assertEqual("2012-02-23T06:14:27.000Z", result.uploads[2].initiated.strftime('%Y-%m-%dT%H:%M:%S.000Z'))


class TestListParts(unittest.TestCase):
    def test_constructor_request(self):
        request = model.ListPartsRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            upload_id='0004B9894A22E5B1888A1E29F823****',
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsNotNone(request.key)
        self.assertIsNotNone(request.upload_id)
        self.assertIsNone(request.encoding_type)
        self.assertIsNone(request.max_parts)
        self.assertIsNone(request.part_number_marker)
        self.assertIsNone(request.request_payer)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.ListPartsRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            upload_id='0004B9894A22E5B1888A1E29F823****',
            encoding_type='url',
            max_parts=30971,
            part_number_marker='1',
            request_payer='requester',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('0004B9894A22E5B1888A1E29F823****', request.upload_id)
        self.assertEqual('url', request.encoding_type)
        self.assertEqual(30971, request.max_parts)
        self.assertEqual('1', request.part_number_marker)
        self.assertEqual('requester', request.request_payer)

        request = model.ListPartsRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            upload_id='0004B9894A22E5B1888A1E29F823****',
            invalid_field='invalid_field',
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('bucket_name', request.bucket)
        self.assertTrue(hasattr(request, 'key'))
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertTrue(hasattr(request, 'upload_id'))
        self.assertEqual('0004B9894A22E5B1888A1E29F823****', request.upload_id)
        self.assertFalse(hasattr(request, 'invalid_field'))

        request = model.ListPartsRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            upload_id='0004B9894A22E5B1888A1E29F823****',
            headers={'key1': 'value1'},
            parameters={'parm1': 'value1'},
            payload='hello world',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('0004B9894A22E5B1888A1E29F823****', request.upload_id)
        self.assertDictEqual({'key1': 'value1'}, request.headers)
        self.assertDictEqual({'parm1': 'value1'}, request.parameters)
        self.assertEqual('hello world', request.payload)

    def test_serialize_request(self):
        request = model.ListPartsRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            upload_id='0004B9894A22E5B1888A1E29F823****',
            encoding_type='url',
            max_parts=30971,
            part_number_marker='2',
            request_payer='requester',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='ListParts',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('ListParts', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)
        self.assertEqual('0004B9894A22E5B1888A1E29F823****', op_input.parameters.get('uploadId'))
        self.assertEqual('url', op_input.parameters.get('encoding-type'))
        self.assertEqual(30971, int(op_input.parameters.get('max-parts')))
        self.assertEqual('2', op_input.parameters.get('part-number-marker'))
        self.assertEqual('requester', op_input.headers.get('x-oss-request-payer'))

    def test_constructor_result(self):
        result = model.ListPartsResult()
        self.assertIsNone(result.encoding_type)
        self.assertIsNone(result.bucket)
        self.assertIsNone(result.key)
        self.assertIsNone(result.upload_id)
        self.assertIsNone(result.part_number_marker)
        self.assertIsNone(result.next_part_number_marker)
        self.assertIsNone(result.max_parts)
        self.assertIsNone(result.is_truncated)
        self.assertIsNone(result.storage_class)
        self.assertIsNone(result.client_encryption_key)
        self.assertIsNone(result.client_encryption_start)
        self.assertIsNone(result.client_encryption_cek_alg)
        self.assertIsNone(result.client_encryption_wrap_alg)
        self.assertIsNone(result.client_encryption_data_size)
        self.assertIsNone(result.client_encryption_part_size)
        self.assertIsNone(result.parts)
        self.assertIsInstance(result, serde.Model)

        result = model.ListPartsResult(
            encoding_type='url',
            bucket='bucket_name',
            key='example-object-2.jpg',
            upload_id='0004B9894A22E5B1888A1E29F823****',
            part_number_marker=30987,
            next_part_number_marker=24619,
            max_parts=30971,
            is_truncated=True,
            storage_class='ColdArchive',
            client_encryption_key='client_encryption_key',
            client_encryption_start='client_encryption_start',
            client_encryption_cek_alg='client_encryption_cek_alg',
            client_encryption_wrap_alg='client_encryption_wrap_alg',
            client_encryption_data_size=28827,
            client_encryption_part_size=94474,
            parts=[model.Part(
                part_number=1,
                etag='"D41D8CD98F00B204E9800998ECF8****"',
                last_modified=datetime.datetime.fromtimestamp(1702743657, datetime.timezone.utc),
                size=344606,
                hash_crc64='316181249502703****',
            ), model.Part(
                part_number=2,
                etag='"4E9800998ECF8****"',
                last_modified=datetime.datetime.fromtimestamp(1702743657, datetime.timezone.utc),
                size=606,
                hash_crc64='32703****',
            )],
        )
        self.assertEqual('url', result.encoding_type)
        self.assertEqual('bucket_name', result.bucket)
        self.assertEqual('example-object-2.jpg', result.key)
        self.assertEqual('0004B9894A22E5B1888A1E29F823****', result.upload_id)
        self.assertEqual(30987, result.part_number_marker)
        self.assertEqual(24619, result.next_part_number_marker)
        self.assertEqual(30971, result.max_parts)
        self.assertEqual(True, result.is_truncated)
        self.assertEqual('ColdArchive', result.storage_class)
        self.assertEqual('client_encryption_key', result.client_encryption_key)
        self.assertEqual('client_encryption_start', result.client_encryption_start)
        self.assertEqual('client_encryption_cek_alg', result.client_encryption_cek_alg)
        self.assertEqual('client_encryption_wrap_alg', result.client_encryption_wrap_alg)
        self.assertEqual(28827, result.client_encryption_data_size)
        self.assertEqual(94474, result.client_encryption_part_size)
        self.assertEqual(1, result.parts[0].part_number)
        self.assertEqual('"D41D8CD98F00B204E9800998ECF8****"', result.parts[0].etag)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657, datetime.timezone.utc), result.parts[0].last_modified)
        self.assertEqual('2023-12-16T16:20:57.000Z', result.parts[1].last_modified.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual(344606, result.parts[0].size)
        self.assertEqual('316181249502703****', result.parts[0].hash_crc64)
        self.assertEqual(2, result.parts[1].part_number)
        self.assertEqual('"4E9800998ECF8****"', result.parts[1].etag)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657, datetime.timezone.utc), result.parts[1].last_modified)
        self.assertEqual('2023-12-16T16:20:57.000Z', result.parts[1].last_modified.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual(606, result.parts[1].size)
        self.assertEqual('32703****', result.parts[1].hash_crc64)

        result = model.ListPartsResult(
            bucket='bucket',
            invalid_field='invalid_field',
        )

        self.assertEqual('bucket', result.bucket)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = r'''
<ListPartsResult>
    <Bucket>multipart_upload</Bucket>
    <Key>multipart.data</Key>
    <UploadId>0004B999EF5A239BB9138C6227D6****</UploadId>
    <NextPartNumberMarker>5</NextPartNumberMarker>
    <MaxParts>1000</MaxParts>
    <IsTruncated>false</IsTruncated>
    <Part>
        <PartNumber>1</PartNumber>
        <LastModified>2012-02-23T07:01:34.000Z</LastModified>
        <ETag>"3349DC700140D7F86A0784842780****"</ETag>
        <Size>6291456</Size>
    </Part>
    <Part>
        <PartNumber>2</PartNumber>
        <LastModified>2012-02-23T07:01:12.000Z</LastModified>
        <ETag>"3349DC700140D7F86A0784842780****"</ETag>
        <Size>6291456</Size>
    </Part>
    <Part>
        <PartNumber>5</PartNumber>
        <LastModified>2012-02-23T07:02:03.000Z</LastModified>
        <ETag>"7265F4D211B56873A381D321F586****"</ETag>
        <Size>1024</Size>
    </Part>
</ListPartsResult>'''

        result = model.ListPartsResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)
        self.assertEqual("multipart_upload", result.bucket)
        self.assertEqual("multipart.data", result.key)
        self.assertEqual("0004B999EF5A239BB9138C6227D6****", result.upload_id)
        self.assertEqual(5, result.next_part_number_marker)
        self.assertEqual(1000, result.max_parts)
        self.assertEqual(False, result.is_truncated)
        self.assertEqual(1, result.parts[0].part_number)
        self.assertEqual("2012-02-23T07:01:34.000Z", result.parts[0].last_modified.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('"3349DC700140D7F86A0784842780****"', result.parts[0].etag)
        self.assertEqual(6291456, result.parts[0].size)
        self.assertEqual(2, result.parts[1].part_number)
        self.assertEqual("2012-02-23T07:01:12.000Z", result.parts[1].last_modified.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('"3349DC700140D7F86A0784842780****"', result.parts[1].etag)
        self.assertEqual(6291456, result.parts[1].size)
        self.assertEqual(5, result.parts[2].part_number)
        self.assertEqual("2012-02-23T07:02:03.000Z", result.parts[2].last_modified.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('"7265F4D211B56873A381D321F586****"', result.parts[2].etag)
        self.assertEqual(1024, result.parts[2].size)


class TestPutSymlink(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutSymlinkRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            target='KbGMxddWss',
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsNotNone(request.key)
        self.assertIsNotNone(request.target)
        self.assertIsNone(request.acl)
        self.assertIsNone(request.storage_class)
        self.assertIsNone(request.metadata)
        self.assertIsNone(request.forbid_overwrite)
        self.assertIsNone(request.request_payer)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutSymlinkRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            target='KbGMxddWss',
            acl='private',
            storage_class='ColdArchive',
            metadata={
                "client-side-encryption-key": "nyXOp7delQ/MQLjKQMhHLaTHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=",
                "client-side-encryption-start": "De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=",
                "client-side-encryption-cek-alg": "AES/CTR/NoPadding",
                "client-side-encryption-wrap-alg": "RSA/NONE/PKCS1Padding",
            },
            forbid_overwrite=True,
            request_payer='requester',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('KbGMxddWss', request.target)
        self.assertEqual('private', request.acl)
        self.assertEqual('ColdArchive', request.storage_class)
        self.assertEqual("nyXOp7delQ/MQLjKQMhHLaTHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=", request.metadata.get("client-side-encryption-key"))
        self.assertEqual("De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=", request.metadata.get("client-side-encryption-start"))
        self.assertEqual("AES/CTR/NoPadding", request.metadata.get("client-side-encryption-cek-alg"))
        self.assertEqual("RSA/NONE/PKCS1Padding", request.metadata.get("client-side-encryption-wrap-alg"))
        self.assertEqual(True, request.forbid_overwrite)
        self.assertEqual('requester', request.request_payer)

        request = model.PutSymlinkRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            target='KbGMxddWss',
            invalid_field='invalid_field',
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('bucket_name', request.bucket)
        self.assertTrue(hasattr(request, 'key'))
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertTrue(hasattr(request, 'target'))
        self.assertEqual('KbGMxddWss', request.target)
        self.assertFalse(hasattr(request, 'invalid_field'))

        request = model.PutSymlinkRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            target='KbGMxddWss',
            headers={'key1': 'value1'},
            parameters={'parm1': 'value1'},
            payload='hello world',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('KbGMxddWss', request.target)
        self.assertDictEqual({'key1': 'value1'}, request.headers)
        self.assertDictEqual({'parm1': 'value1'}, request.parameters)
        self.assertEqual('hello world', request.payload)

    def test_serialize_request(self):
        request = model.PutSymlinkRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            target='KbGMxddWss',
            acl='private',
            storage_class='ColdArchive',
            metadata={
                "client-side-encryption-key": "nyXOp7delQ/MQLjKQMhHLaTHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=",
                "client-side-encryption-start": "De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=",
                "client-side-encryption-cek-alg": "AES/CTR/NoPadding",
                "client-side-encryption-wrap-alg": "RSA/NONE/PKCS1Padding",
            },
            forbid_overwrite=True,
            request_payer='requester',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutSymlink',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutSymlink', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)
        self.assertEqual('KbGMxddWss', op_input.headers.get('x-oss-symlink-target'))
        self.assertEqual('private', op_input.headers.get('x-oss-object-acl'))
        self.assertEqual('ColdArchive', op_input.headers.get('x-oss-storage-class'))
        self.assertEqual('nyXOp7delQ/MQLjKQMhHLaTHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=', request.metadata.get('client-side-encryption-key'))
        self.assertEqual('De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=', request.metadata.get('client-side-encryption-start'))
        self.assertEqual('AES/CTR/NoPadding', request.metadata.get('client-side-encryption-cek-alg'))
        self.assertEqual('RSA/NONE/PKCS1Padding', request.metadata.get('client-side-encryption-wrap-alg'))
        self.assertEqual(True, bool(op_input.headers.get('x-oss-forbid-overwrite')))
        self.assertEqual('requester', op_input.headers.get('x-oss-request-payer'))

    def test_constructor_result(self):
        result = model.PutSymlinkResult()
        self.assertIsNone(result.version_id)
        self.assertIsInstance(result, serde.Model)

        result = model.PutSymlinkResult(
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
        )
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.version_id)

        result = model.PutSymlinkResult(
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            invalid_field='invalid_field',
        )
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.version_id)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutSymlinkResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                    'x-oss-version-id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('x-oss-version-id'))


class TestGetSymlink(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetSymlinkRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsNotNone(request.key)
        self.assertIsNone(request.version_id)
        self.assertIsNone(request.request_payer)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetSymlinkRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            request_payer='requester',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', request.version_id)
        self.assertEqual('requester', request.request_payer)

        request = model.GetSymlinkRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            invalid_field='invalid_field',
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('bucket_name', request.bucket)
        self.assertTrue(hasattr(request, 'key'))
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertFalse(hasattr(request, 'invalid_field'))

        request = model.GetSymlinkRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            headers={'key1': 'value1'},
            parameters={'parm1': 'value1'},
            payload='hello world',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertDictEqual({'key1': 'value1'}, request.headers)
        self.assertDictEqual({'parm1': 'value1'}, request.parameters)
        self.assertEqual('hello world', request.payload)

    def test_serialize_request(self):
        request = model.GetSymlinkRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            request_payer='requester',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetSymlink',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetSymlink', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', op_input.parameters.get('versionId'))
        self.assertEqual('requester', op_input.headers.get('x-oss-request-payer'))

    def test_constructor_result(self):
        result = model.GetSymlinkResult()
        self.assertIsNone(result.version_id)
        self.assertIsNone(result.target)
        self.assertIsNone(result.etag)
        self.assertIsNone(result.metadata)
        self.assertIsInstance(result, serde.Model)

        result = model.GetSymlinkResult(
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            target='gZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0***',
            etag='"D41D8CD98F00B204E9800998ECF8****"',
            metadata={
                "client-side-encryption-key": "nyXOp7delQ/MQLjKQMhHLaTHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=",
                "client-side-encryption-start": "De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=",
                "client-side-encryption-cek-alg": "AES/CTR/NoPadding",
                "client-side-encryption-wrap-alg": "RSA/NONE/PKCS1Padding",
            },
        )
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.version_id)
        self.assertEqual('gZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0***', result.target)
        self.assertEqual('"D41D8CD98F00B204E9800998ECF8****"', result.etag)
        self.assertEqual("nyXOp7delQ/MQLjKQMhHLaTHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=", result.metadata.get("client-side-encryption-key"))
        self.assertEqual("De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=", result.metadata.get("client-side-encryption-start"))
        self.assertEqual("AES/CTR/NoPadding", result.metadata.get("client-side-encryption-cek-alg"))
        self.assertEqual("RSA/NONE/PKCS1Padding", result.metadata.get("client-side-encryption-wrap-alg"))

        result = model.GetSymlinkResult(
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            invalid_field='invalid_field',
        )
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.version_id)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = None
        result = model.GetSymlinkResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                    'x-oss-version-id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('x-oss-version-id'))


class TestPutObjectTagging(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutObjectTaggingRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            tagging=model.Tagging(
                tag_set=model.TagSet(
                    tags=[model.Tag(
                        key='tag-key1',
                        value='tag-value1',
                    ),model.Tag(
                        key='tag-key2',
                        value='tag-value2',
                    )]
                ),
            ),
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsNotNone(request.key)
        self.assertIsNotNone(request.tagging)
        self.assertIsNone(request.version_id)
        self.assertIsNone(request.request_payer)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutObjectTaggingRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            tagging=model.Tagging(
                tag_set=model.TagSet(
                    tags=[model.Tag(
                        key='tag-key1',
                        value='tag-value1',
                    ),model.Tag(
                        key='tag-key2',
                        value='tag-value2',
                    )]
                ),
            ),
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            request_payer='requester',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('tag-key1', request.tagging.tag_set.tags[0].key)
        self.assertEqual('tag-value1', request.tagging.tag_set.tags[0].value)
        self.assertEqual('tag-key2', request.tagging.tag_set.tags[1].key)
        self.assertEqual('tag-value2', request.tagging.tag_set.tags[1].value)
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', request.version_id)
        self.assertEqual('requester', request.request_payer)

        request = model.PutObjectTaggingRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            tagging=model.Tagging(
                tag_set=model.TagSet(
                    tags=[model.Tag(
                        key='tag-key1',
                        value='tag-value1',
                    ),model.Tag(
                        key='tag-key2',
                        value='tag-value2',
                    )]
                ),
            ),
            invalid_field='invalid_field',
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('bucket_name', request.bucket)
        self.assertTrue(hasattr(request, 'key'))
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertTrue(hasattr(request, 'tagging'))
        self.assertEqual('tag-key1', request.tagging.tag_set.tags[0].key)
        self.assertEqual('tag-value1', request.tagging.tag_set.tags[0].value)
        self.assertEqual('tag-key2', request.tagging.tag_set.tags[1].key)
        self.assertEqual('tag-value2', request.tagging.tag_set.tags[1].value)
        self.assertFalse(hasattr(request, 'invalid_field'))

        request = model.PutObjectTaggingRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            tagging=model.Tagging(
                tag_set=model.TagSet(
                    tags=[model.Tag(
                        key='tag-key1',
                        value='tag-value1',
                    )]
                ),
            ),
            headers={'key1': 'value1'},
            parameters={'parm1': 'value1'},
            payload='hello world',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('tag-key1', request.tagging.tag_set.tags[0].key)
        self.assertEqual('tag-value1', request.tagging.tag_set.tags[0].value)
        self.assertDictEqual({'key1': 'value1'}, request.headers)
        self.assertDictEqual({'parm1': 'value1'}, request.parameters)
        self.assertEqual('hello world', request.payload)

    def test_serialize_request(self):
        request = model.PutObjectTaggingRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            tagging=model.Tagging(
                tag_set=model.TagSet(
                    tags=[model.Tag(
                        key='tag-key1',
                        value='tag-value1',
                    ),model.Tag(
                        key='tag-key2',
                        value='tag-value2',
                    )]
                ),
            ),
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            request_payer='requester',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutObjectTagging',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutObjectTagging', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', op_input.parameters.get('versionId'))
        self.assertEqual('requester', op_input.headers.get('x-oss-request-payer'))

        root = ET.fromstring(op_input.body)
        self.assertEqual('Tagging', root.tag)
        self.assertEqual('tag-key1', root.find('TagSet').findall('Tag')[0].findtext('Key'))
        self.assertEqual('tag-value1', root.find('TagSet').findall('Tag')[0].findtext('Value'))
        self.assertEqual('tag-key2', root.find('TagSet').findall('Tag')[1].findtext('Key'))
        self.assertEqual('tag-value2', root.find('TagSet').findall('Tag')[1].findtext('Value'))

    def test_constructor_result(self):
        result = model.PutObjectTaggingResult()
        self.assertIsNone(result.version_id)
        self.assertIsInstance(result, serde.Model)

        result = model.PutObjectTaggingResult(
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
        )
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.version_id)

        result = model.PutObjectTaggingResult(
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            invalid_field='invalid_field',
        )
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.version_id)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutObjectTaggingResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                    'x-oss-version-id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('x-oss-version-id'))


class TestGetObjectTagging(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetObjectTaggingRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsNotNone(request.key)
        self.assertIsNone(request.version_id)
        self.assertIsNone(request.request_payer)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetObjectTaggingRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            request_payer='requester',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', request.version_id)
        self.assertEqual('requester', request.request_payer)

        request = model.GetObjectTaggingRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            invalid_field='invalid_field',
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('bucket_name', request.bucket)
        self.assertTrue(hasattr(request, 'key'))
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertFalse(hasattr(request, 'invalid_field'))

        request = model.GetObjectTaggingRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            headers={'key1': 'value1'},
            parameters={'parm1': 'value1'},
            payload='hello world',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertDictEqual({'key1': 'value1'}, request.headers)
        self.assertDictEqual({'parm1': 'value1'}, request.parameters)
        self.assertEqual('hello world', request.payload)

    def test_serialize_request(self):
        request = model.GetObjectTaggingRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            request_payer='requester',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetObjectTagging',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetObjectTagging', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', op_input.parameters.get('versionId'))
        self.assertEqual('requester', op_input.headers.get('x-oss-request-payer'))

    def test_constructor_result(self):
        result = model.GetObjectTaggingResult()
        self.assertIsNone(result.version_id)
        self.assertIsNone(result.tag_set)
        self.assertIsInstance(result, serde.Model)

        result = model.GetObjectTaggingResult(
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            tag_set=model.TagSet(
                tags=[model.Tag(
                    key='tag-key1',
                    value='tag-value1',
                ), model.Tag(
                    key='tag-key2',
                    value='tag-value2',
                )]
            ),
        )
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.version_id)
        self.assertEqual('tag-key1', result.tag_set.tags[0].key)
        self.assertEqual('tag-value1', result.tag_set.tags[0].value)
        self.assertEqual('tag-key2', result.tag_set.tags[1].key)
        self.assertEqual('tag-value2', result.tag_set.tags[1].value)

        result = model.GetObjectTaggingResult(
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            invalid_field = 'invalid_field',
        )
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.version_id)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = r'''
<Tagging>
  <TagSet>
    <Tag>
      <Key>a</Key>
      <Value>1</Value>
    </Tag>
    <Tag>
      <Key>b</Key>
      <Value>2</Value>
    </Tag>
  </TagSet>
</Tagging>'''

        result = model.GetObjectTaggingResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)
        self.assertEqual("a", result.tag_set.tags[0].key)
        self.assertEqual("1", result.tag_set.tags[0].value)
        self.assertEqual("b", result.tag_set.tags[1].key)
        self.assertEqual("2", result.tag_set.tags[1].value)


class DeleteObjectTagging(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DeleteObjectTaggingRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsNotNone(request.key)
        self.assertIsNone(request.version_id)
        self.assertIsNone(request.request_payer)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DeleteObjectTaggingRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            request_payer='requester',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', request.version_id)
        self.assertEqual('requester', request.request_payer)

        request = model.DeleteObjectTaggingRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            invalid_field='invalid_field',
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('bucket_name', request.bucket)
        self.assertTrue(hasattr(request, 'key'))
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertFalse(hasattr(request, 'invalid_field'))

        request = model.DeleteObjectTaggingRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            headers={'key1': 'value1'},
            parameters={'parm1': 'value1'},
            payload='hello world',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertDictEqual({'key1': 'value1'}, request.headers)
        self.assertDictEqual({'parm1': 'value1'}, request.parameters)
        self.assertEqual('hello world', request.payload)

    def test_serialize_request(self):
        request = model.DeleteObjectTaggingRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            request_payer='requester',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='serde.',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('serde.', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', op_input.parameters.get('versionId'))
        self.assertEqual('requester', op_input.headers.get('x-oss-request-payer'))

    def test_constructor_result(self):
        result = model.DeleteObjectTaggingResult()
        self.assertIsNone(result.version_id)
        self.assertIsInstance(result, serde.Model)

        result = model.DeleteObjectTaggingResult(
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
        )
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.version_id)

        result = model.DeleteObjectTaggingResult(
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            invalid_field='invalid_field',
        )
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.version_id)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = None
        result = model.DeleteObjectTaggingResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                    'x-oss-version-id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('x-oss-version-id'))


class TestProcessObject(unittest.TestCase):
    def test_constructor_request(self):
        request = model.ProcessObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            process='process-test',
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsNotNone(request.key)
        self.assertIsNotNone(request.process)
        self.assertIsNone(request.request_payer)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.ProcessObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            process='process-test',
            request_payer='requester',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('process-test', request.process)
        self.assertEqual('requester', request.request_payer)

        request = model.ProcessObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            process='process-test',
            invalid_field='invalid_field',
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('bucket_name', request.bucket)
        self.assertTrue(hasattr(request, 'key'))
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertTrue(hasattr(request, 'process'))
        self.assertEqual('process-test', request.process)
        self.assertFalse(hasattr(request, 'invalid_field'))

        request = model.ProcessObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            process='process-test',
            headers={'key1': 'value1'},
            parameters={'parm1': 'value1'},
            payload='hello world',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('process-test', request.process)
        self.assertDictEqual({'key1': 'value1'}, request.headers)
        self.assertDictEqual({'parm1': 'value1'}, request.parameters)
        self.assertEqual('hello world', request.payload)

    def test_serialize_request(self):
        request = model.ProcessObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            process='process-test',
            request_payer='requester',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='ProcessObject',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('ProcessObject', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)
        self.assertEqual('requester', op_input.headers.get('x-oss-request-payer'))

    def test_constructor_result(self):
        result = model.ProcessObjectResult()
        self.assertIsNone(result.bucket)
        self.assertIsNone(result.file_size)
        self.assertIsNone(result.key)
        self.assertIsNone(result.process_status)
        self.assertIsInstance(result, serde.Model)

        result = model.ProcessObjectResult(
            bucket='bucket_name',
            file_size=30197,
            key='example-object-2.jpg',
            process_status='process_status-test',
        )
        self.assertEqual('bucket_name', result.bucket)
        self.assertEqual(30197, result.file_size)
        self.assertEqual('example-object-2.jpg', result.key)
        self.assertEqual('process_status-test', result.process_status)

        result = model.ProcessObjectResult(
            process_status='process_status-test',
            invalid_field='invalid_field',
        )
        self.assertEqual('process_status-test', result.process_status)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = None
        result = model.ProcessObjectResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                    'x-oss-version-id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('x-oss-version-id'))


class TestAsyncProcessObject(unittest.TestCase):
    def test_constructor_request(self):
        request = model.AsyncProcessObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            process='process-test',
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsNotNone(request.key)
        self.assertIsNotNone(request.process)
        self.assertIsNone(request.request_payer)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.AsyncProcessObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            process='process-test',
            request_payer='requester',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('process-test', request.process)
        self.assertEqual('requester', request.request_payer)

        request = model.AsyncProcessObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            process='process-test',
            invalid_field='invalid_field',
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('bucket_name', request.bucket)
        self.assertTrue(hasattr(request, 'key'))
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertTrue(hasattr(request, 'process'))
        self.assertEqual('process-test', request.process)
        self.assertFalse(hasattr(request, 'invalid_field'))

        request = model.AsyncProcessObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            process='process-test',
            headers={'key1': 'value1'},
            parameters={'parm1': 'value1'},
            payload='hello world',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('process-test', request.process)
        self.assertDictEqual({'key1': 'value1'}, request.headers)
        self.assertDictEqual({'parm1': 'value1'}, request.parameters)
        self.assertEqual('hello world', request.payload)

    def test_serialize_request(self):
        request = model.AsyncProcessObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            process='process-test',
            request_payer='requester',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='AsyncProcessObject',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('AsyncProcessObject', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)
        self.assertEqual('requester', op_input.headers.get('x-oss-request-payer'))

    def test_constructor_result(self):
        result = model.AsyncProcessObjectResult()
        self.assertIsNone(result.event_id)
        self.assertIsNone(result.task_id)
        self.assertIsNone(result.process_request_id)
        self.assertIsInstance(result, serde.Model)

        result = model.AsyncProcessObjectResult(
            event_id='gMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0***',
            task_id=123,
            process_request_id='gMDJgZCA0mFhZjhjYmY0***',
        )
        self.assertEqual('gMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0***', result.event_id)
        self.assertEqual(123, result.task_id)
        self.assertEqual('gMDJgZCA0mFhZjhjYmY0***', result.process_request_id)

        result = model.AsyncProcessObjectResult(
            process_request_id='RgMDJgZCA0BYiIDYmY0***',
            invalid_field='invalid_field',
        )
        self.assertEqual('RgMDJgZCA0BYiIDYmY0***', result.process_request_id)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = None
        result = model.AsyncProcessObjectResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                    'x-oss-version-id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('x-oss-version-id'))


