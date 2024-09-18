# pylint: skip-file
import datetime
import unittest
import xml.etree.ElementTree as ET
from alibabacloud_oss_v2 import serde
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
        self.assertIsNone(request.sse_kms_key_id)
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
            sse_kms_key_id='9468da86-3509-4f8d-a61e-6eab1eac****',
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
        self.assertEqual('9468da86-3509-4f8d-a61e-6eab1eac****', request.sse_kms_key_id)
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
        self.assertIsNone(result.sse_kms_key_id)
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
        self.assertIsInstance(result, serde.Model)

        result = model.HeadObjectResult(
            content_length=1024,
            content_type='text/xml',
            etag='"A082B659EF78733A5A042FA253B1****"',
            last_modified=datetime.datetime.fromtimestamp(1702743657),
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
            hash_crc64='GHH^%$#^&INOU(',
            storage_class='Archive',
            object_type='public-read-write',
            version_id='version_id-test',
            tagging_count=111,
            server_side_encryption='SM4',
            server_side_data_encryption='AES256',
            sse_kms_key_id='9468da86-3509-4f8d-a61e-6eab1eac****',
            next_append_position='222',
            expiration='2022-10-12T00:00:00.000Z',
            restore='ongoing-request=\"false\", expiry-date=\"Sun, 16 Apr 2017 08:12:33 GMT\"',
            process_status='process_status-test',
            request_charged='request_charged-test',
            allow_origin='*',
            allow_methods='PUT,GET',
            allow_age='%#@$#@&^%&(*HIHJ',
            allow_headers='{a:a1, b:b2}',
            expose_headers='{a:a1, b:b2}',
        )
        self.assertEqual(1024, result.content_length)
        self.assertEqual('text/xml', result.content_type)
        self.assertEqual('"A082B659EF78733A5A042FA253B1****"', result.etag)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657), result.last_modified)
        self.assertEqual('2023-12-17T00:20:57.000Z', result.last_modified.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('B5eJF1ptWaXm4bijSPyxw==',result.content_md5)
        self.assertEqual('no-cache', result.cache_control)
        self.assertEqual('attachment; filename=testing.txt',result.content_disposition)
        self.assertEqual('utf-8', result.content_encoding)
        self.assertEqual('2023-10-12T00:00:00.000Z', result.expires)
        self.assertEqual('GHH^%$#^&INOU(', result.hash_crc64)
        self.assertEqual('Archive', result.storage_class)
        self.assertEqual('public-read-write', result.object_type)
        self.assertEqual('version_id-test', result.version_id)
        self.assertEqual(111, result.tagging_count)
        self.assertEqual('SM4', result.server_side_encryption)
        self.assertEqual('AES256', result.server_side_data_encryption)
        self.assertEqual('9468da86-3509-4f8d-a61e-6eab1eac****', result.sse_kms_key_id)
        self.assertEqual('222', result.next_append_position)
        self.assertEqual('2022-10-12T00:00:00.000Z', result.expiration)
        self.assertEqual('ongoing-request=\"false\", expiry-date=\"Sun, 16 Apr 2017 08:12:33 GMT\"',result.restore)
        self.assertEqual('process_status-test', result.process_status)
        self.assertEqual('request_charged-test', result.request_charged)
        self.assertEqual('*', result.allow_origin)
        self.assertEqual('PUT,GET', result.allow_methods)
        self.assertEqual('%#@$#@&^%&(*HIHJ', result.allow_age)
        self.assertEqual('{a:a1, b:b2}', result.allow_headers)
        self.assertEqual('{a:a1, b:b2}', result.expose_headers)

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
        self.assertIsNone(result.sse_kms_key_id)
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
            last_modified=datetime.datetime.fromtimestamp(1702743657),
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
            sse_kms_key_id='9468da86-3509-4f8d-a61e-6eab1eac****',
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
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657), result.last_modified)
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
        self.assertEqual('9468da86-3509-4f8d-a61e-6eab1eac****', result.sse_kms_key_id)
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
        self.assertIsNone(request.sse_kms_key_id)
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
            sse_kms_key_id='9468da86-3509-4f8d-a61e-6eab1eac****',
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
        self.assertEqual('9468da86-3509-4f8d-a61e-6eab1eac****', request.sse_kms_key_id)
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
            sse_kms_key_id='9468da86-3509-4f8d-a61e-6eab1eac****',
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
        self.assertIsNone(request.sse_kms_key_id)
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
            sse_kms_key_id='9468da86-3509-4f8d-a61e-6eab1eac****',
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
        self.assertEqual('9468da86-3509-4f8d-a61e-6eab1eac****', request.sse_kms_key_id)
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
            sse_kms_key_id='9468da86-3509-4f8d-a61e-6eab1eac****',
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
        self.assertIsNone(result.sse_kms_key_id)
        self.assertIsNone(result.last_modified)
        self.assertIsNone(result.etag)
        self.assertIsInstance(result, serde.Model)

        result = model.CopyObjectResult(
            version_id='CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
            hash_crc64='316181249502703****',
            source_version_id='source_version_id-test',
            server_side_encryption='SM4',
            server_side_data_encryption='KMS',
            sse_kms_key_id='9468da86-3509-4f8d-a61e-6eab1eac****',
            last_modified=datetime.datetime.fromtimestamp(1702743657),
            etag='"D41D8CD98F00B204E9800998ECF8****"',
        )
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.version_id)
        self.assertEqual('316181249502703****', result.hash_crc64)
        self.assertEqual('source_version_id-test', result.source_version_id)
        self.assertEqual('SM4', result.server_side_encryption)
        self.assertEqual('KMS', result.server_side_data_encryption)
        self.assertEqual('9468da86-3509-4f8d-a61e-6eab1eac****', result.sse_kms_key_id)
        self.assertEqual(datetime.datetime.fromtimestamp(1702743657), result.last_modified)
        self.assertEqual('2023-12-17T00:20:57.000Z', result.last_modified.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
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
        self.assertIsInstance(result, serde.ResultModel)

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
        self.assertIsNone(request.content_length)
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
        self.assertEqual(101, request.content_length)
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
            content_length=101,
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
        self.assertEqual(101, int(op_input.headers.get('Content-Length')))
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
        self.assertEqual("true", result.deleted_objects[0].delete_marker)
        self.assertEqual("CAEQMhiBgIDXiaaB0BYiIGQzYmRkZGUxMTM1ZDRjOTZhNjk4YjRjMTAyZjhl****", result.deleted_objects[0].delete_marker_version_id)
        self.assertEqual("test.jpg", result.deleted_objects[1].key)
        self.assertEqual("0BYiIGMxZWJmYmMzYjE0OTQ0ZmZhYjgzNzkzYjc2NjZk****", result.deleted_objects[1].version_id)
        self.assertEqual("true", result.deleted_objects[1].delete_marker)
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

    def test_constructor_result(self):
        result = model.GetObjectMetaResult()
        self.assertIsInstance(result, serde.ResultModel)

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
        self.assertEqual('Expedited', root.findtext('JobParameters.Tier'))

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