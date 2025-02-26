# pylint: skip-file
import os
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


    def test_eclient_upload_object(self):
        mc = oss.crypto.MasterRsaCipher(
            mat_desc={"tag": "value"},
            public_key=RSA_PUBLIC_KEY,
            private_key=RSA_PRIVATE_KEY
        )
        eclient = oss.EncryptionClient(self.client, mc)

        data_lenth = 1 * 1024 * 1024
        data = random_str(data_lenth)
        temp = tempfile.NamedTemporaryFile(delete=False)
        try:
            temp.write(data.encode())
            temp.close()

            # upload file
            key = 'object-upload-file.bin'
            result = eclient.new_uploader(
                part_size=100 * 1024,
                parallel_num=5,
                leave_parts_on_error=True,
                enable_checkpoint=True,
                checkpoint_dir=temp.name
            ).upload_file(oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=key,
            ), filepath=temp.name)
            self.assertIsNotNone(result)
            self.assertIsInstance(result, oss.UploadResult)
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
            self.assertEqual(1024 * 1024, len(egresult.body.content))


            # upload from
            example_data = b''
            key = 'object-upload-from.bin'
            with open(temp.name, 'rb') as f:
                result = eclient.new_uploader(
                    part_size=100 * 1024,
                    # parallel_num=5,
                    # leave_parts_on_error=True,
                    enable_checkpoint=True,
                    # checkpoint_dir=args.file_path
                ).upload_from(oss.PutObjectRequest(
                    bucket=self.bucket_name,
                    key=key,
                ), reader=f)
                self.assertIsNotNone(result)
                self.assertIsInstance(result, oss.UploadResult)
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
            self.assertEqual(1024 * 1024, len(example_data))
            self.assertEqual(example_data, egresult.body.content)

        finally:
            os.remove(temp.name)


    def test_eclient_upload_object_check_point(self):
        mc = oss.crypto.MasterRsaCipher(
            mat_desc={"tag": "value"},
            public_key=RSA_PUBLIC_KEY,
            private_key=RSA_PRIVATE_KEY
        )
        eclient = oss.EncryptionClient(self.client, mc)

        data_lenth = 1 * 1024 * 1024
        data = random_str(data_lenth)
        temp = tempfile.NamedTemporaryFile(delete=False)
        try:
            temp.write(data.encode())
            temp.close()

            # upload file
            key = 'object-upload-file.bin'
            result = eclient.new_uploader(
                part_size=100 * 1024,
                parallel_num=5,
                leave_parts_on_error=True,
                enable_checkpoint=True,
                checkpoint_dir=temp.name
            ).upload_file(oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=key,
            ), filepath=temp.name)
            self.assertIsNotNone(result)
            self.assertIsInstance(result, oss.UploadResult)
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
            self.assertEqual(1024 * 1024, len(egresult.body.content))


            # upload from
            key = 'object-upload-from.bin'
            with open(temp.name, 'rb') as f:
                result = eclient.new_uploader(
                    part_size=100 * 1024,
                    parallel_num=5,
                    leave_parts_on_error=True,
                    enable_checkpoint=True,
                ).upload_from(oss.PutObjectRequest(
                    bucket=self.bucket_name,
                    key=key,
                ), reader=f)
                self.assertIsNotNone(result)
                self.assertIsInstance(result, oss.UploadResult)
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
            self.assertEqual(1024 * 1024, len(example_data))
            self.assertEqual(example_data, egresult.body.content)

        finally:
            os.remove(temp.name)