# pylint: skip-file
import os
import random
import tempfile
from typing import cast
import alibabacloud_oss_v2 as oss
from . import TestIntegration, random_bucket_name, random_str, REGION, OBJECTNAME_PREFIX

RSA_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCokfiAVXXf5ImFzKDw+XO/UByW
6mse2QsIgz3ZwBtMNu59fR5zttSx+8fB7vR4CN3bTztrP9A6bjoN0FFnhlQ3vNJC
5MFO1PByrE/MNd5AAfSVba93I6sx8NSk5MzUCA4NJzAUqYOEWGtGBcom6kEF6MmR
1EKib1Id8hpooY5xaQIDAQAB
-----END PUBLIC KEY-----"""

RSA_PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAKiR+IBVdd/kiYXM
oPD5c79QHJbqax7ZCwiDPdnAG0w27n19HnO21LH7x8Hu9HgI3dtPO2s/0DpuOg3Q
UWeGVDe80kLkwU7U8HKsT8w13kAB9JVtr3cjqzHw1KTkzNQIDg0nMBSpg4RYa0YF
yibqQQXoyZHUQqJvUh3yGmihjnFpAgMBAAECgYA49RmCQ14QyKevDfVTdvYlLmx6
kbqgMbYIqk+7w611kxoCTMR9VMmJWgmk/Zic9mIAOEVbd7RkCdqT0E+xKzJJFpI2
ZHjrlwb21uqlcUqH1Gn+wI+jgmrafrnKih0kGucavr/GFi81rXixDrGON9KBE0FJ
cPVdc0XiQAvCBnIIAQJBANXu3htPH0VsSznfqcDE+w8zpoAJdo6S/p30tcjsDQnx
l/jYV4FXpErSrtAbmI013VYkdJcghNSLNUXppfk2e8UCQQDJt5c07BS9i2SDEXiz
byzqCfXVzkdnDj9ry9mba1dcr9B9NCslVelXDGZKvQUBqNYCVxg398aRfWlYDTjU
IoVVAkAbTyjPN6R4SkC4HJMg5oReBmvkwFCAFsemBk0GXwuzD0IlJAjXnAZ+/rIO
ItewfwXIL1Mqz53lO/gK+q6TR585AkB304KUIoWzjyF3JqLP3IQOxzns92u9EV6l
V2P+CkbMPXiZV6sls6I4XppJXX2i3bu7iidN3/dqJ9izQK94fMU9AkBZvgsIPCot
y1/POIbv9LtnviDKrmpkXgVQSU4BmTPvXwTJm8APC7P/horSh3SVf1zgmnsyjm9D
hO92gGc+4ajL
-----END PRIVATE KEY-----"""
class TestEncryptionCLient(TestIntegration):

    def test_put_object(self):
        mc = oss.crypto.MasterRsaCipher(
            mat_desc={"tag": "value"},
            public_key=RSA_PUBLIC_KEY,
            private_key=RSA_PRIVATE_KEY
        )
        eclient = oss.EncryptionClient(self.client, mc)

        # str
        body = 'hello world'
        key = 'object-str.bin'
        result = eclient.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=body
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.PutObjectResult)
        self.assertEqual(200, result.status_code)

        gresult = eclient.unwrap().get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(gresult)
        self.assertIsInstance(gresult, oss.GetObjectResult)
        self.assertEqual(200, gresult.status_code)        
        self.assertIsNotNone(gresult.headers.get('x-oss-meta-client-side-encryption-start', None))
        self.assertIsNotNone(gresult.headers.get('x-oss-meta-client-side-encryption-key', None))
        self.assertEqual('{"tag": "value"}', gresult.headers.get('x-oss-meta-client-side-encryption-matdesc', None))
        self.assertEqual('AES/CTR/NoPadding', gresult.headers.get('x-oss-meta-client-side-encryption-cek-alg', None))
        self.assertEqual('RSA/NONE/PKCS1Padding', gresult.headers.get('x-oss-meta-client-side-encryption-wrap-alg', None))
        self.assertIsNone(gresult.headers.get('x-oss-meta-client-side-encryption-unencrypted-content-md5', None))
        self.assertIsNone(gresult.headers.get('x-oss-meta-client-side-encryption-unencrypted-content-length', None))
        
        self.assertEqual(len(body), len(gresult.body.content))
        self.assertNotEqual(body.encode(), gresult.body.content)

        egresult = eclient.get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(egresult)
        self.assertIsInstance(egresult, oss.GetObjectResult)
        self.assertEqual(200, egresult.status_code)        
        self.assertIsNotNone(egresult.headers.get('x-oss-meta-client-side-encryption-start', None))
        self.assertIsNotNone(egresult.headers.get('x-oss-meta-client-side-encryption-key', None))
        self.assertEqual('{"tag": "value"}', egresult.headers.get('x-oss-meta-client-side-encryption-matdesc', None))
        self.assertEqual('AES/CTR/NoPadding', egresult.headers.get('x-oss-meta-client-side-encryption-cek-alg', None))
        self.assertEqual('RSA/NONE/PKCS1Padding', egresult.headers.get('x-oss-meta-client-side-encryption-wrap-alg', None))
        self.assertIsNone(egresult.headers.get('x-oss-meta-client-side-encryption-unencrypted-content-md5', None))
        self.assertIsNone(egresult.headers.get('x-oss-meta-client-side-encryption-unencrypted-content-length', None))
        
        self.assertEqual(len(body), len(egresult.body.content))
        self.assertEqual(body.encode(), egresult.body.content)

        # bytes
        body = b'hello world 123'
        key = 'object-bytes.bin'
        result = eclient.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            content_length=str(len(body)),
            body=body
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.PutObjectResult)
        self.assertEqual(200, result.status_code)

        egresult = eclient.get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(egresult)
        self.assertIsInstance(egresult, oss.GetObjectResult)
        self.assertEqual(200, egresult.status_code)        
        self.assertIsNotNone(egresult.headers.get('x-oss-meta-client-side-encryption-start', None))
        self.assertIsNotNone(egresult.headers.get('x-oss-meta-client-side-encryption-key', None))
        self.assertEqual('{"tag": "value"}', egresult.headers.get('x-oss-meta-client-side-encryption-matdesc', None))
        self.assertEqual('AES/CTR/NoPadding', egresult.headers.get('x-oss-meta-client-side-encryption-cek-alg', None))
        self.assertEqual('RSA/NONE/PKCS1Padding', egresult.headers.get('x-oss-meta-client-side-encryption-wrap-alg', None))
        self.assertIsNone(egresult.headers.get('x-oss-meta-client-side-encryption-unencrypted-content-md5', None))
        self.assertEqual(str(len(body)), egresult.headers.get('x-oss-meta-client-side-encryption-unencrypted-content-length', None))
        
        self.assertEqual(len(body), len(egresult.body.content))
        self.assertEqual(b'hello world 123', egresult.body.content)

        # file
        example_data = b''
        key = 'object-file.bin'        
        with open("./tests/data/example.jpg", 'rb') as f:
            result = eclient.put_object(oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=key,
                body=f
            ))
            self.assertIsNotNone(result)
            self.assertIsInstance(result, oss.PutObjectResult)
            self.assertEqual(200, result.status_code)

            f.seek(0, os.SEEK_SET)
            example_data = f.read()

        egresult = eclient.get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(egresult)
        self.assertIsInstance(egresult, oss.GetObjectResult)
        self.assertEqual(200, egresult.status_code)        
        self.assertEqual(21839, len(example_data))
        self.assertEqual(example_data, egresult.body.content)

        #iterable
        key = 'object-iterable.bin'        
        result = eclient.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=iter(example_data)
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.PutObjectResult)
        self.assertEqual(200, result.status_code)

        egresult = eclient.get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(egresult)
        self.assertIsInstance(egresult, oss.GetObjectResult)
        self.assertEqual(200, egresult.status_code)        
        self.assertEqual(21839, len(example_data))
        self.assertEqual(example_data, egresult.body.content)

    def test_multipart_from_bytes(self):
        part_size = 100 * 1024
        data_size = 3 * part_size + 1245
        data = random_str(data_size).encode()

        key = 'multipart-bytes.bin'
        mc = oss.crypto.MasterRsaCipher(
            mat_desc={"tag": "value"},
            public_key=RSA_PUBLIC_KEY,
            private_key=RSA_PRIVATE_KEY
        )
        eclient = oss.EncryptionClient(self.client, mc)

        #init
        initresult = eclient.initiate_multipart_upload(oss.InitiateMultipartUploadRequest(
            bucket=self.bucket_name,
            key=key,
            cse_part_size=part_size,
            cse_data_size=data_size
        ))
        self.assertIsNotNone(initresult)
        self.assertIsInstance(initresult, oss.InitiateMultipartUploadResult)
        self.assertEqual(200, initresult.status_code)
        self.assertIsNotNone(initresult.cse_multipart_context)
        self.assertIsInstance(initresult.cse_multipart_context, oss.EncryptionMultiPartContext)
        cse_context = cast(oss.EncryptionMultiPartContext, initresult.cse_multipart_context)
        self.assertEqual(part_size, cse_context.part_size)
        self.assertEqual(data_size, cse_context.data_size)
        self.assertIsInstance(cse_context.content_cipher, oss.crypto.ContentCipher)

        #upload part
        part_number = 1
        upload_parts = []
        for start in range(0, data_size, part_size):
            end = start + part_size
            if end > data_size:
               end =  data_size
            upresult = eclient.upload_part(oss.UploadPartRequest(
                bucket=self.bucket_name,
                key=key,
                upload_id=initresult.upload_id,
                part_number=part_number,
                cse_multipart_context=cse_context,
                body=data[start:end]
            ))
            self.assertIsNotNone(upresult)
            self.assertIsInstance(upresult, oss.UploadPartResult)
            self.assertEqual(200, upresult.status_code)
            upload_parts.append(oss.UploadPart(part_number=part_number, etag=upresult.etag))
            part_number += 1

        self.assertEqual(4, len(upload_parts))

        #listpart
        lpresult = eclient.list_parts(oss.ListPartsRequest(
            bucket=self.bucket_name,
            key=key,
            upload_id=initresult.upload_id
        ))
        self.assertIsNotNone(lpresult)
        self.assertIsInstance(lpresult, oss.ListPartsResult)
        self.assertEqual(200, lpresult.status_code)
        self.assertIsNotNone(lpresult.client_encryption_key)
        self.assertIsNotNone(lpresult.client_encryption_start)
        self.assertEqual(part_size, lpresult.client_encryption_part_size)
        self.assertEqual(data_size, lpresult.client_encryption_data_size)
        self.assertEqual("RSA/NONE/PKCS1Padding", lpresult.client_encryption_wrap_alg)
        self.assertEqual("AES/CTR/NoPadding", lpresult.client_encryption_cek_alg)

        #complete
        parts = sorted(upload_parts, key=lambda p: p.part_number)
        cmresult = eclient.complete_multipart_upload(oss.CompleteMultipartUploadRequest(
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
        rawresult = eclient.unwrap().get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key
        ))
        self.assertIsNotNone(rawresult)
        self.assertIsInstance(rawresult, oss.GetObjectResult)
        self.assertEqual(200, rawresult.status_code)
        self.assertIsNotNone(rawresult.headers.get('x-oss-meta-client-side-encryption-start', None))
        self.assertIsNotNone(rawresult.headers.get('x-oss-meta-client-side-encryption-key', None))
        self.assertEqual('{"tag": "value"}', rawresult.headers.get('x-oss-meta-client-side-encryption-matdesc', None))
        self.assertEqual('AES/CTR/NoPadding', rawresult.headers.get('x-oss-meta-client-side-encryption-cek-alg', None))
        self.assertEqual('RSA/NONE/PKCS1Padding', rawresult.headers.get('x-oss-meta-client-side-encryption-wrap-alg', None))
        self.assertIsNone(rawresult.headers.get('x-oss-meta-client-side-encryption-unencrypted-content-md5', None))
        self.assertEqual(data_size, len(rawresult.body.content))
        self.assertNotEqual(data, rawresult.body.content)

        goresult = eclient.get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key
        ))
        self.assertIsNotNone(goresult)
        self.assertIsInstance(goresult, oss.GetObjectResult)
        self.assertEqual(200, goresult.status_code)
        self.assertIsNotNone(goresult.headers.get('x-oss-meta-client-side-encryption-start', None))
        self.assertIsNotNone(goresult.headers.get('x-oss-meta-client-side-encryption-key', None))
        self.assertEqual('{"tag": "value"}', goresult.headers.get('x-oss-meta-client-side-encryption-matdesc', None))
        self.assertEqual('AES/CTR/NoPadding', goresult.headers.get('x-oss-meta-client-side-encryption-cek-alg', None))
        self.assertEqual('RSA/NONE/PKCS1Padding', goresult.headers.get('x-oss-meta-client-side-encryption-wrap-alg', None))
        self.assertIsNone(goresult.headers.get('x-oss-meta-client-side-encryption-unencrypted-content-md5', None))
        self.assertEqual(data_size, len(goresult.body.content))
        self.assertEqual(data, goresult.body.content)


    def test_multipart_from_file(self):
        part_size = 100 * 1024
        data_size = 3 * part_size + 1245
        data = random_str(data_size).encode()
        key = 'multipart-file.bin'
        mc = oss.crypto.MasterRsaCipher(
            mat_desc={"tag": "value"},
            public_key=RSA_PUBLIC_KEY,
            private_key=RSA_PRIVATE_KEY
        )
        eclient = oss.EncryptionClient(self.client, mc)

        #init
        initresult = eclient.initiate_multipart_upload(oss.InitiateMultipartUploadRequest(
            bucket=self.bucket_name,
            key=key,
            cse_part_size=part_size,
            cse_data_size=data_size
        ))
        self.assertIsNotNone(initresult)
        self.assertIsInstance(initresult, oss.InitiateMultipartUploadResult)
        self.assertEqual(200, initresult.status_code)
        self.assertIsNotNone(initresult.cse_multipart_context)
        self.assertIsInstance(initresult.cse_multipart_context, oss.EncryptionMultiPartContext)
        cse_context = cast(oss.EncryptionMultiPartContext, initresult.cse_multipart_context)
        self.assertEqual(part_size, cse_context.part_size)
        self.assertEqual(data_size, cse_context.data_size)
        self.assertIsInstance(cse_context.content_cipher, oss.crypto.ContentCipher)

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
                upresult = eclient.upload_part(oss.UploadPartRequest(
                    bucket=self.bucket_name,
                    key=key,
                    upload_id=initresult.upload_id,
                    part_number=part_number,
                    cse_multipart_context=cse_context,
                    body=reader
                ))
                self.assertIsNotNone(upresult)
                self.assertIsInstance(upresult, oss.UploadPartResult)
                self.assertEqual(200, upresult.status_code)
                upload_parts.append(oss.UploadPart(part_number=part_number, etag=upresult.etag))
                part_number += 1

            self.assertEqual(4, len(upload_parts))

        #listpart
        lpresult = eclient.list_parts(oss.ListPartsRequest(
            bucket=self.bucket_name,
            key=key,
            upload_id=initresult.upload_id
        ))
        self.assertIsNotNone(lpresult)
        self.assertIsInstance(lpresult, oss.ListPartsResult)
        self.assertEqual(200, lpresult.status_code)
        self.assertIsNotNone(lpresult.client_encryption_key)
        self.assertIsNotNone(lpresult.client_encryption_start)
        self.assertEqual(part_size, lpresult.client_encryption_part_size)
        self.assertEqual(data_size, lpresult.client_encryption_data_size)
        self.assertEqual("RSA/NONE/PKCS1Padding", lpresult.client_encryption_wrap_alg)
        self.assertEqual("AES/CTR/NoPadding", lpresult.client_encryption_cek_alg)

        #complete
        parts = sorted(upload_parts, key=lambda p: p.part_number)
        cmresult = eclient.complete_multipart_upload(oss.CompleteMultipartUploadRequest(
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
        rawresult = eclient.unwrap().get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key
        ))
        self.assertIsNotNone(rawresult)
        self.assertIsInstance(rawresult, oss.GetObjectResult)
        self.assertEqual(200, rawresult.status_code)
        self.assertIsNotNone(rawresult.headers.get('x-oss-meta-client-side-encryption-start', None))
        self.assertIsNotNone(rawresult.headers.get('x-oss-meta-client-side-encryption-key', None))
        self.assertEqual('{"tag": "value"}', rawresult.headers.get('x-oss-meta-client-side-encryption-matdesc', None))
        self.assertEqual('AES/CTR/NoPadding', rawresult.headers.get('x-oss-meta-client-side-encryption-cek-alg', None))
        self.assertEqual('RSA/NONE/PKCS1Padding', rawresult.headers.get('x-oss-meta-client-side-encryption-wrap-alg', None))
        self.assertIsNone(rawresult.headers.get('x-oss-meta-client-side-encryption-unencrypted-content-md5', None))
        self.assertEqual(data_size, len(rawresult.body.content))
        self.assertNotEqual(data, rawresult.body.content)

        goresult = eclient.get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key
        ))
        self.assertIsNotNone(goresult)
        self.assertIsInstance(goresult, oss.GetObjectResult)
        self.assertEqual(200, goresult.status_code)
        self.assertIsNotNone(goresult.headers.get('x-oss-meta-client-side-encryption-start', None))
        self.assertIsNotNone(goresult.headers.get('x-oss-meta-client-side-encryption-key', None))
        self.assertEqual('{"tag": "value"}', goresult.headers.get('x-oss-meta-client-side-encryption-matdesc', None))
        self.assertEqual('AES/CTR/NoPadding', goresult.headers.get('x-oss-meta-client-side-encryption-cek-alg', None))
        self.assertEqual('RSA/NONE/PKCS1Padding', goresult.headers.get('x-oss-meta-client-side-encryption-wrap-alg', None))
        self.assertIsNone(goresult.headers.get('x-oss-meta-client-side-encryption-unencrypted-content-md5', None))
        self.assertEqual(data_size, len(goresult.body.content))
        self.assertEqual(data, goresult.body.content)


    def test_compatibility(self):

        rsa_private = """-----BEGIN RSA PRIVATE KEY-----
        MIICWwIBAAKBgQCokfiAVXXf5ImFzKDw+XO/UByW6mse2QsIgz3ZwBtMNu59fR5z
        ttSx+8fB7vR4CN3bTztrP9A6bjoN0FFnhlQ3vNJC5MFO1PByrE/MNd5AAfSVba93
        I6sx8NSk5MzUCA4NJzAUqYOEWGtGBcom6kEF6MmR1EKib1Id8hpooY5xaQIDAQAB
        AoGAOPUZgkNeEMinrw31U3b2JS5sepG6oDG2CKpPu8OtdZMaAkzEfVTJiVoJpP2Y
        nPZiADhFW3e0ZAnak9BPsSsySRaSNmR465cG9tbqpXFKh9Rp/sCPo4Jq2n65yood
        JBrnGr6/xhYvNa14sQ6xjjfSgRNBSXD1XXNF4kALwgZyCAECQQDV7t4bTx9FbEs5
        36nAxPsPM6aACXaOkv6d9LXI7A0J8Zf42FeBV6RK0q7QG5iNNd1WJHSXIITUizVF
        6aX5NnvFAkEAybeXNOwUvYtkgxF4s28s6gn11c5HZw4/a8vZm2tXXK/QfTQrJVXp
        VwxmSr0FAajWAlcYN/fGkX1pWA041CKFVQJAG08ozzekeEpAuByTIOaEXgZr5MBQ
        gBbHpgZNBl8Lsw9CJSQI15wGfv6yDiLXsH8FyC9TKs+d5Tv4Cvquk0efOQJAd9OC
        lCKFs48hdyaiz9yEDsc57PdrvRFepVdj/gpGzD14mVerJbOiOF6aSV19ot27u4on
        Td/3aifYs0CveHzFPQJAWb4LCDwqLctfzziG7/S7Z74gyq5qZF4FUElOAZkz718E
        yZvADwuz/4aK0od0lX9c4Jp7Mo5vQ4TvdoBnPuGoyw==
        -----END RSA PRIVATE KEY-----"""

        objectname = 'enc-example.jpg'
        example_data = b''
        with open("./tests/data/example.jpg", 'rb') as f:
            example_data = f.read()
        self.assertTrue(len(example_data) > 0)

        with open("./tests/data/enc-example.jpg", 'rb') as f:
            result = self.client.put_object(oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=objectname,
                body=f,
                metadata= {
                    "client-side-encryption-key": "nyXOp7delQ/MQLjKQMhHLaT0w7u2yQoDLkSnK8MFg/MwYdh4na4/LS8LLbLcM18m8I/ObWUHU775I50sJCpdv+f4e0jLeVRRiDFWe+uo7Puc9j4xHj8YB3QlcIOFQiTxHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=",
                    "client-side-encryption-start":    "De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwox4WhLGng5DK2vNXxULmulMUUpYkdc9umqmDilgSy5Z3Foafw+v4JJThfw68T/9G2gxZLrQTbAlvFPFfPM9Ehk6cY4+8WpY32uN8w5vrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=",
                    "client-side-encryption-cek-alg":  "AES/CTR/NoPadding",
                    "client-side-encryption-wrap-alg": "RSA/NONE/PKCS1Padding",
                }
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual('OK', result.status)
            self.assertEqual(24, len(result.request_id))
            self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        mc = oss.crypto.MasterRsaCipher(mat_desc={"tag": "value"}, private_key=rsa_private)
        eclient = oss.EncryptionClient(self.client, mc)

        # read all
        result = eclient.get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=objectname
        ))
        self.assertEqual(example_data, result.body.content)
        result.body.close()

        #range read and iter_bytes
        for i in range(0, 33):
            result = eclient.get_object(oss.GetObjectRequest(
                bucket=self.bucket_name,
                key=objectname,
                range_header=f'bytes={i}-12345'
            ))
            size = 12345 - i + 1
            with result.body as f:
                data = b''
                for d in f.iter_bytes(block_size=8*1024):
                    self.assertTrue(len(d) <= 8 *1024)
                    data += d
                self.assertEqual(example_data[i:12346], data)
                self.assertEqual(size, len(data))

    def test_eclient_open_file_baisc(self):

        mc = oss.crypto.MasterRsaCipher(
            mat_desc={"tag": "value"},
            public_key=RSA_PUBLIC_KEY,
            private_key=RSA_PRIVATE_KEY
        )
        eclient = oss.EncryptionClient(self.client, mc)

        data_size = 1234
        key = 'check_member-' + random_str(6)
        data = random_str(data_size).encode()
        result = eclient.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        rf: oss.ReadOnlyFile = None
        with eclient.open_file(self.bucket_name, key) as f:
            self.assertIsNotNone(f)
            rf = f
            self.assertEqual(0, f.tell())
            self.assertEqual(True, f.seekable())
            self.assertEqual(True, f.readable())
            self.assertEqual(False, f.closed)
            self.assertEqual(f'oss://{self.bucket_name}/{key}', f.name)
            self.assertEqual('rb', f.mode)

            # seek, tell
            f.seek(0, os.SEEK_SET)
            self.assertEqual(0, f.tell())
            offset = f.tell()
            b = f.read(2)
            self.assertEqual(data[offset:offset + 2], b)

            f.seek(1, os.SEEK_SET)
            self.assertEqual(1, f.tell())
            offset = f.tell()
            b = f.read(2)
            self.assertEqual(data[offset:offset + 2], b)

            f.seek(data_size, os.SEEK_SET)
            self.assertEqual(data_size, f.tell())
            offset = f.tell()
            b = f.read(2)
            self.assertEqual(data[offset:offset + 2], b)

            f.seek(-data_size, os.SEEK_END)
            self.assertEqual(0, f.tell())
            offset = f.tell()
            b = f.read(2)
            self.assertEqual(data[offset:offset + 2], b)

            f.seek(-1, os.SEEK_END)
            self.assertEqual(data_size - 1, f.tell())
            offset = f.tell()
            b = f.read(2)
            self.assertEqual(data[data_size - 1:], b)

            f.seek(0, os.SEEK_END)
            self.assertEqual(data_size, f.tell())
            offset = f.tell()
            b = f.read(2)
            self.assertEqual(b'', b)

            f.seek(123, os.SEEK_SET)
            self.assertEqual(123, f.tell())
            offset = f.tell()
            b = f.read(2)
            self.assertEqual(data[offset:offset + 2], b)

            f.seek(123, os.SEEK_CUR)
            self.assertEqual(248, f.tell())
            offset = f.tell()
            b = f.read(2)
            self.assertEqual(data[offset:offset + 2], b)

        self.assertEqual(True, rf.closed)
        self.assertEqual(None, rf._read_buf)
        self.assertEqual(None, rf._stream_reader)
        self.assertEqual(None, rf._stream_iter)

        # call close many times
        rf.close()
        rf.close()

        rf = eclient.open_file(self.bucket_name, key)
        self.assertIsNotNone(rf)
        self.assertEqual(False, rf.closed)
        with rf as f:
            self.assertEqual(False, f.closed)
        self.assertEqual(True, rf.closed)

    def test_eclient_open_file_read_size(self):
        mc = oss.crypto.MasterRsaCipher(
            mat_desc={"tag": "value"},
            public_key=RSA_PUBLIC_KEY,
            private_key=RSA_PRIVATE_KEY
        )
        eclient = oss.EncryptionClient(self.client, mc)

        key = 'read_size-' + random_str(6)
        data = random_str(100 * 1024 * 5 + 1234).encode()

        result = eclient.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        # read with size
        rf: oss.ReadOnlyFile = None
        with eclient.open_file(self.bucket_name, key) as f:
            self.assertIsNotNone(f)
            rf = f
            end = 129
            for i in range(0, end):
                size = 200 * 1024 + 12345 - i
                f.seek(i, 0)
                self.assertEqual(i, f.tell())
                got = f.read(size)
                self.assertEqual(size, len(got))
                self.assertEqual(data[i:i + size], got)
                self.assertEqual(i + size, f.tell())

        self.assertEqual(True, rf.closed)

    def test_eclient_open_file_readall(self):
        mc = oss.crypto.MasterRsaCipher(
            mat_desc={"tag": "value"},
            public_key=RSA_PUBLIC_KEY,
            private_key=RSA_PRIVATE_KEY
        )
        eclient = oss.EncryptionClient(self.client, mc)

        key = 'readall-' + random_str(6)
        data = random_str(100 * 1024 * 5 + 1234).encode()

        result = eclient.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        # read all
        with eclient.open_file(self.bucket_name, key) as f:
            self.assertIsNotNone(f)
            f.seek(123)
            self.assertEqual(123, f.tell())
            got = f.readall()
            self.assertEqual(data[123:], got)
            self.assertEqual(len(data), f.tell())

            f.seek(1234)
            got1 = f.read(17)
            self.assertEqual(1234 + 17, f.tell())
            self.assertEqual(data[1234:1234 + 17], got1)
            got2 = f.read()
            self.assertEqual(len(data), f.tell())
            self.assertEqual(data[1234 + 17:], got2)
            self.assertEqual(data[1234:], got1 + got2)

            f.seek(12345)
            got1 = f.read(172)
            self.assertEqual(12345 + 172, f.tell())
            self.assertEqual(data[12345:12345 + 172], got1)
            got2 = f.readall()
            self.assertEqual(len(data), f.tell())
            self.assertEqual(data[12345 + 172:], got2)
            self.assertEqual(data[12345:], got1 + got2)

    def test_eclient_open_file_readinto(self):
        mc = oss.crypto.MasterRsaCipher(
            mat_desc={"tag": "value"},
            public_key=RSA_PUBLIC_KEY,
            private_key=RSA_PRIVATE_KEY
        )
        eclient = oss.EncryptionClient(self.client, mc)

        key = 'readinto-' + random_str(6)
        data = random_str(100 * 1024 * 5 + 1234).encode()

        result = eclient.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        # read into bytearray
        with eclient.open_file(self.bucket_name, key) as f:
            self.assertIsNotNone(f)
            b = bytearray(11)
            self.assertEqual(0, f.tell())
            n = f.readinto(b)
            self.assertEqual(11, n)
            self.assertEqual(data[0:11], b)
            self.assertEqual(11, f.tell())

            b = bytearray(9)
            n = f.readinto(b)
            self.assertEqual(9, n)
            self.assertEqual(data[11:20], b)
            self.assertEqual(20, f.tell())

            b = bytearray(len(data))
            f.seek(12345)
            n = f.readinto(b)
            self.assertEqual(len(data) - 12345, n)
            self.assertEqual(len(data), f.tell())

            b = bytearray(len(data) * 2)
            f.seek(1234)
            n = f.readinto(b)
            self.assertEqual(len(data) - 1234, n)
            self.assertEqual(len(data), f.tell())
            self.assertEqual(data[1234:], b[:len(data) - 1234])

        # read into blob = memoryview(bytearray(size))
        with eclient.open_file(self.bucket_name, key) as f:
            self.assertIsNotNone(f)
            blob = memoryview(bytearray(len(data)))
            self.assertEqual(0, f.tell())
            n = f.readinto(blob[0:11])
            self.assertEqual(11, n)
            self.assertEqual(data[0:11], blob[0:11])
            self.assertEqual(11, f.tell())

            n = f.readinto(blob[11:20])
            self.assertEqual(9, n)
            self.assertEqual(data[11:20], blob[11:20])
            self.assertEqual(20, f.tell())

            # remains
            n = f.readinto(blob)
            self.assertEqual(len(data) - 20, n)
            self.assertEqual(data[20:], blob[0:n])
            self.assertEqual(len(data), f.tell())

    def test_eclient_open_file_fail(self):
        mc = oss.crypto.MasterRsaCipher(
            mat_desc={"tag": "value"},
            public_key=RSA_PUBLIC_KEY,
            private_key=RSA_PRIVATE_KEY
        )
        eclient = oss.EncryptionClient(self.client, mc)

        key = 'fail-test-' + random_str(6)
        nokey = key + 'no-key'
        data = random_str(1234).encode()

        result = eclient.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        # open fail
        try:
            with eclient.open_file(self.bucket_name, nokey) as f:
                self.assertIsNotNone(f)
            self.fail('should not here')
        except oss.PathError as err:
            self.assertIn('stat_object', str(err))
            self.assertIn(f'oss://{self.bucket_name}/{nokey}', str(err))

        # seek fail
        try:
            with eclient.open_file(self.bucket_name, key) as f:
                f.seek(len(data) + 1, os.SEEK_SET)
            self.fail('should not here')
        except oss.PathError as err:
            self.assertIn('seek', str(err))
            self.assertIn('offset is unavailable', str(err))

        try:
            with eclient.open_file(self.bucket_name, key) as f:
                f.seek(-1, os.SEEK_SET)
            self.fail('should not here')
        except oss.PathError as err:
            self.assertIn('seek', str(err))
            self.assertIn('negative seek position', str(err))

        try:
            with eclient.open_file(self.bucket_name, key) as f:
                f.seek(0, 3)
            self.fail('should not here')
        except oss.PathError as err:
            self.assertIn('seek', str(err))
            self.assertIn('unsupported whence value', str(err))

        try:
            with eclient.open_file(self.bucket_name, key) as f:
                f.seek('123', 3)
            self.fail('should not here')
        except oss.PathError as err:
            self.assertIn('seek', str(err))
            self.assertIn('is not an integer', str(err))

        # call after close
        rf: oss.ReadOnlyFile = None
        with eclient.open_file(self.bucket_name, key) as f:
            self.assertIsNotNone(f)
            rf = f

        try:
            rf.read()
        except oss.PathError as err:
            self.assertIn('read', str(err))
            self.assertIn('I/O operation on closed file.', str(err))

        try:
            rf.readall()
        except oss.PathError as err:
            self.assertIn('read', str(err))
            self.assertIn('I/O operation on closed file.', str(err))

        try:
            rf.readinto(bytearray(123))
        except oss.PathError as err:
            self.assertIn('read', str(err))
            self.assertIn('I/O operation on closed file.', str(err))

        try:
            rf.seek(0, os.SEEK_CUR)
        except oss.PathError as err:
            self.assertIn('seek', str(err))
            self.assertIn('I/O operation on closed file.', str(err))

        try:
            rf.tell()
        except oss.PathError as err:
            self.assertIn('tell', str(err))
            self.assertIn('I/O operation on closed file.', str(err))

        try:
            rf.readable()
        except oss.PathError as err:
            self.assertIn('readable', str(err))
            self.assertIn('I/O operation on closed file.', str(err))

        try:
            rf.seekable()
        except oss.PathError as err:
            self.assertIn('seekable', str(err))
            self.assertIn('I/O operation on closed file.', str(err))

        try:
            with rf as f:
                pass
        except oss.PathError as err:
            self.assertIn('enter', str(err))
            self.assertIn('I/O operation on closed file.', str(err))

    def tes_eclient_open_file_resume_read(self):
        mc = oss.crypto.MasterRsaCipher(
            mat_desc={"tag": "value"},
            public_key=RSA_PUBLIC_KEY,
            private_key=RSA_PRIVATE_KEY
        )
        eclient = oss.EncryptionClient(self.client, mc)

        key = 'resume_read-' + random_str(6)
        data = random_str(200 * 1024 + 1234).encode()

        result = eclient.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        with eclient.open_file(self.bucket_name, key) as f:
            b1 = f.read(1234)
            # wait stream close
            f._stream_iter = None
            # time.sleep(120)
            b2 = f.read()
            self.assertEqual(data, b1 + b2)

    def test_eclient_open_file_source_changed(self):
        mc = oss.crypto.MasterRsaCipher(
            mat_desc={"tag": "value"},
            public_key=RSA_PUBLIC_KEY,
            private_key=RSA_PRIVATE_KEY
        )
        eclient = oss.EncryptionClient(self.client, mc)

        key = 'source_changed-' + random_str(6)
        data1 = random_str(200 * 1024 + 1234).encode()
        data2 = random_str(201 * 1024 + 1234).encode()
        result = eclient.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data1
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        with eclient.open_file(self.bucket_name, key) as f:
            b1 = f.read(1234)
            self.assertEqual(data1[0:len(b1)], b1)

            # change file
            result = eclient.put_object(oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=key,
                body=data2
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual('OK', result.status)

            try:
                f.seek(0)
                f.readall()
            except oss.PathError as err:
                self.assertIn('get_object', str(err))
                self.assertIn('Source file is changed, origin info', str(err))

    def test_eclient_open_file_prefetch_read(self):
        mc = oss.crypto.MasterRsaCipher(
            mat_desc={"tag": "value"},
            public_key=RSA_PUBLIC_KEY,
            private_key=RSA_PRIVATE_KEY
        )
        eclient = oss.EncryptionClient(self.client, mc)

        key = 'prefetch-' + random_str(6)
        data_len = 11 * 200 * 1024 + 1234
        data = random_str(data_len).encode()
        result = eclient.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        rf: oss.ReadOnlyFile = None
        with eclient.open_file(
                self.bucket_name, key,
                enable_prefetch=True,
                prefetch_num=3,
                chunk_size=2 * 200 * 1024,
                prefetch_threshold=0) as f:

            rf = f
            self.assertEqual(True, f._enable_prefetch)
            self.assertEqual(3, f._prefetch_num)
            self.assertEqual(2 * 200 * 1024, f._chunk_size)
            self.assertEqual(0, f._prefetch_threshold)

            # size
            start = f.seek(0, os.SEEK_SET)
            end = f.seek(0, os.SEEK_END)
            self.assertEqual(data_len, end - start)

            # print('\nreadall')
            # readall
            f.seek(0, os.SEEK_SET)
            b = f.readall()
            self.assertEqual(data, b)
            self.assertIsNone(f._stream_reader)
            self.assertIsNone(f._stream_iter)
            self.assertIsNotNone(f._generator)
            self.assertIsNotNone(f._executor)
            self.assertEqual(3, f._executor._max_workers)

            b = f.readall()
            self.assertEqual(b'', b)

            # print('seek readN')
            # seek readN
            for _ in range(0, 64):
                offset = random.randint(0, data_len // 5)
                n = random.randint(0, data_len // 4) + 3 * 200 * 1024
                begin = f.seek(offset, os.SEEK_SET)
                f._num_ooo_read = 0
                self.assertEqual(offset, begin)
                # print(f'seek readN {offset} {n}')
                b = f.read(n)
                self.assertEqual(n, len(b))
                self.assertEqual(data[offset:offset + n], b)
                if n % f._chunk_size > 0:
                    self.assertGreater(len(f._prefetch_readers), 1)
                self.assertIsNone(f._stream_reader)
                self.assertIsNone(f._stream_iter)
                self.assertIsNotNone(f._generator)

            # print('seek read from offset to end')
            # seek read from offset to end
            for _ in range(0, 64):
                offset = random.randint(0, data_len // 5)
                begin = f.seek(offset, os.SEEK_SET)
                f._num_ooo_read = 0
                self.assertEqual(offset, begin)
                b = f.read()
                self.assertEqual(data_len - offset, len(b))
                self.assertEqual(data[offset:], b)
                self.assertEqual(0, len(f._prefetch_readers))
                self.assertIsNone(f._stream_reader)
                self.assertIsNone(f._stream_iter)
                self.assertIsNotNone(f._generator)

            # print('seek readInto N')
            # seek readInto N
            for _ in range(0, 64):
                offset = random.randint(0, data_len // 5)
                n = random.randint(0, data_len // 4) + 3 * 200 * 1024
                begin = f.seek(offset, os.SEEK_SET)
                f._num_ooo_read = 0
                self.assertEqual(offset, begin)
                blob = memoryview(bytearray(n))
                got = f.readinto(blob)
                self.assertEqual(n, got)
                self.assertEqual(data[offset:offset + n], blob[0:])
                if n % f._chunk_size > 0:
                    self.assertGreater(len(f._prefetch_readers), 1)
                self.assertIsNotNone(f._generator)
                self.assertIsNone(f._stream_reader)
                self.assertIsNone(f._stream_iter)

            # print('seek readInto from offset to end')
            # seek readInto from offset to end
            bloball = memoryview(bytearray(data_len))
            for _ in range(0, 64):
                offset = random.randint(0, data_len // 5)
                begin = f.seek(offset, os.SEEK_SET)
                f._num_ooo_read = 0
                self.assertEqual(offset, begin)
                got = f.readinto(bloball)
                self.assertEqual(data_len - offset, got)
                self.assertEqual(data[offset:], bloball[0:got])
                self.assertEqual(0, len(f._prefetch_readers))
                self.assertIsNone(f._stream_reader)
                self.assertIsNone(f._stream_iter)
                self.assertIsNotNone(f._generator)

        self.assertEqual(None, rf._read_buf)
        self.assertEqual(None, rf._stream_reader)
        self.assertEqual(None, rf._prefetch_readers)
        self.assertEqual(None, rf._generator)
        self.assertEqual(None, rf._executor)

        # call close many times
        rf.close()
        rf.close()

    def test_eclient_open_file_mix_read(self):
        mc = oss.crypto.MasterRsaCipher(
            mat_desc={"tag": "value"},
            public_key=RSA_PUBLIC_KEY,
            private_key=RSA_PRIVATE_KEY
        )
        eclient = oss.EncryptionClient(self.client, mc)

        key = 'mix-' + random_str(6)
        data_len = 11 * 200 * 1024 + 12345
        data = random_str(data_len).encode()
        result = eclient.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        rf: oss.ReadOnlyFile = None
        with eclient.open_file(
                self.bucket_name, key,
                enable_prefetch=True,
                prefetch_num=3,
                chunk_size=1 * 200 * 1024,
                prefetch_threshold=5 * 200 * 1024) as f:
            rf = f
            self.assertEqual(True, f._enable_prefetch)
            self.assertEqual(3, f._prefetch_num)
            self.assertEqual(1 * 200 * 1024, f._chunk_size)
            self.assertEqual(5 * 200 * 1024, f._prefetch_threshold)

            # read some
            some1 = 3 * 100 * 1024 + 123
            f.seek(0, os.SEEK_SET)
            b1 = f.read(some1)
            self.assertEqual(data[0:some1], b1)
            self.assertIsNotNone(f._stream_reader)
            self.assertIsNotNone(f._stream_iter)
            self.assertIsNone(f._generator)
            self.assertIsNone(f._executor)

            # read some
            some2 = 8 * 100 * 1024 + 123
            self.assertGreater(some1 + some2, f._prefetch_threshold)
            b2 = f.read(some2)
            self.assertEqual(data[some1:some1 + some2], b2)
            self.assertIsNone(f._stream_reader)
            self.assertIsNone(f._stream_iter)
            self.assertIsNotNone(f._generator)
            self.assertIsNotNone(f._executor)
            self.assertEqual(3, f._executor._max_workers)

            # read last
            b3 = f.readall()
            self.assertEqual(data, b1 + b2 + b3)

        self.assertEqual(None, rf._read_buf)
        self.assertEqual(None, rf._stream_reader)
        self.assertEqual(None, rf._prefetch_readers)
        self.assertEqual(None, rf._generator)
        self.assertEqual(None, rf._executor)

        # seq read, seek, read all
        with eclient.open_file(
                self.bucket_name, key,
                enable_prefetch=True,
                prefetch_num=3,
                chunk_size=1 * 200 * 1024,
                prefetch_threshold=5 * 200 * 1024) as f:
            self.assertEqual(True, f._enable_prefetch)
            self.assertEqual(3, f._prefetch_num)
            self.assertEqual(1 * 200 * 1024, f._chunk_size)
            self.assertEqual(5 * 200 * 1024, f._prefetch_threshold)

            # read some
            off1 = 1
            some1 = 3 * 100 * 1024 + 123
            f.seek(off1, os.SEEK_SET)
            b1 = f.read(some1)
            self.assertEqual(data[off1:off1 + some1], b1)
            self.assertIsNotNone(f._stream_reader)
            self.assertIsNotNone(f._stream_iter)
            self.assertIsNone(f._generator)
            self.assertIsNone(f._executor)

            # read some
            off2 = 100
            some2 = 15 * 100 * 1024 + 123
            self.assertGreater(some2, f._prefetch_threshold)
            f.seek(off2, os.SEEK_SET)
            b2 = f.read(some2)
            self.assertEqual(data[off2:off2 + some2], b2)
            self.assertIsNone(f._stream_reader)
            self.assertIsNone(f._stream_iter)
            self.assertIsNotNone(f._generator)
            self.assertIsNotNone(f._executor)
            self.assertEqual(3, f._executor._max_workers)

    def test_eclient_open_file_prefetch_source_changed(self):
        mc = oss.crypto.MasterRsaCipher(
            mat_desc={"tag": "value"},
            public_key=RSA_PUBLIC_KEY,
            private_key=RSA_PRIVATE_KEY
        )
        eclient = oss.EncryptionClient(self.client, mc)

        key = 'prefetch_source_changed-' + random_str(6)
        data1 = random_str(11 * 200 * 1024 + 12345).encode()
        data2 = random_str(11 * 200 * 1024 + 12345).encode()
        result = eclient.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data1
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        with eclient.open_file(
                self.bucket_name, key,
                enable_prefetch=True,
                prefetch_num=3,
                chunk_size=2 * 200 * 1024,
                prefetch_threshold=0) as f:

            len1 = 3 * 200 * 1024 + 12
            b1 = f.read(len1)
            self.assertIsNone(f._stream_reader)
            self.assertIsNone(f._stream_iter)
            self.assertIsNotNone(f._generator)
            self.assertIsNotNone(f._executor)
            self.assertEqual(data1[0:len1], b1)

            # change file
            result = eclient.put_object(oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=key,
                body=data2
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual('OK', result.status)

            # read data saved in the buffer
            len2 = 1 * 200 * 1024
            b2 = f.read(len2)
            self.assertEqual(data1[len1:len1 + len2], b2)

            # read remains
            try:
                f.readall()
            except oss.PathError as err:
                self.assertIn('get_object', str(err))
                self.assertIn('Source file is changed, origin info', str(err))

    def test_eclient_open_file_mix_read2(self):
        mc = oss.crypto.MasterRsaCipher(
            mat_desc={"tag": "value"},
            public_key=RSA_PUBLIC_KEY,
            private_key=RSA_PRIVATE_KEY
        )
        eclient = oss.EncryptionClient(self.client, mc)

        key = 'prefetch-' + random_str(6)
        data_len = 6 * 100 * 1024 + 1234
        data = random_str(data_len).encode()
        result = eclient.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        with eclient.open_file(
                self.bucket_name, key,
                enable_prefetch=True,
                prefetch_num=2,
                chunk_size=1 * 200 * 1024,
                prefetch_threshold=1 * 200 * 1024) as f:
            self.assertEqual(True, f._enable_prefetch)
            self.assertEqual(2, f._prefetch_num)
            self.assertEqual(1 * 200 * 1024, f._chunk_size)
            self.assertEqual(1 * 200 * 1024, f._prefetch_threshold)

            len1 = 12345
            b1 = f.read(len1)
            self.assertEqual(data[0:len1], b1)
            self.assertIsNotNone(f._stream_reader)
            self.assertIsNotNone(f._stream_iter)
            self.assertIsNone(f._generator)
            self.assertIsNone(f._executor)

            len2 = 1 * 200 * 1024
            b2 = f.read(len2)
            self.assertEqual(data[len1:len1 + len2], b2)
            self.assertIsNone(f._stream_reader)
            self.assertIsNone(f._stream_iter)
            self.assertIsNotNone(f._generator)
            self.assertIsNotNone(f._executor)

            # set reader fail
            f._prefetch_readers[0]._failed = True
            len3 = 1 * 100 * 1024
            b3 = f.read(len3)
            self.assertEqual(data[:len1 + len2 + len3], b1 + b2 + b3)
            self.assertIsNotNone(f._stream_reader)
            self.assertIsNotNone(f._stream_iter)
            self.assertIsNone(f._generator)
            self.assertIsNotNone(f._executor)