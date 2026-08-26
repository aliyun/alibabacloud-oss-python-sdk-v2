# pylint: skip-file
import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.agentic import models
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict
from ... import MockHttpResponse


def _output(body):
    return OperationOutput(
        status='OK',
        status_code=200,
        headers=CaseInsensitiveDict({'x-oss-request-id': 'req-1'}),
        http_response=MockHttpResponse(status_code=200, headers={}, body=body),
    )


class TestCreateAgenticBucket(unittest.TestCase):
    def test_constructor(self):
        request = models.CreateAgenticBucketRequest()
        self.assertIsNone(request.bucket)
        self.assertIsInstance(request, serde.RequestModel)

    def test_serialize_body(self):
        request = models.CreateAgenticBucketRequest(
            bucket='my-agentic',
            create_agentic_bucket_configuration=models.CreateAgenticBucketConfiguration(
                storage_class='IA',
                data_redundancy_type='ZRS',
            ),
        )
        op_input = serde.serialize_input(request, OperationInput(
            op_name='CreateAgenticBucket', method='PUT', bucket=request.bucket))
        self.assertEqual('my-agentic', op_input.bucket)
        self.assertIn(b'<CreateAgenticBucketConfiguration>', op_input.body)
        self.assertIn(b'<StorageClass>IA</StorageClass>', op_input.body)
        self.assertIn(b'<DataRedundancyType>ZRS</DataRedundancyType>', op_input.body)

    def test_deserialize_result(self):
        result = serde.deserialize_output(
            models.CreateAgenticBucketResult(), _output(None),
            custom_deserializer=[serde.deserialize_output_xmlbody])
        self.assertEqual(200, result.status_code)
        self.assertEqual('req-1', result.request_id)


class TestGetAgenticBucket(unittest.TestCase):
    def test_deserialize_result(self):
        xml = (
            b'<AgenticBucketInfo>'
            b'<Name>my-agentic-1234567890123456-cn-hangzhou-ab-apsr</Name>'
            b'<Owner>1234567890123456</Owner>'
            b'<Region>cn-hangzhou</Region>'
            b'<StorageClass>Standard</StorageClass>'
            b'<DataRedundancyType>LRS</DataRedundancyType>'
            b'<Status>Enabled</Status>'
            b'<BucketResourceType>agentic</BucketResourceType>'
            b'<CreateTime>2026-06-13T08:00:00.000Z</CreateTime>'
            b'<ACL>private</ACL>'
            b'<PublicAccessBlock>true</PublicAccessBlock>'
            b'<ServerSideEncryptionRule><ApplyServerSideEncryptionByDefault>'
            b'<SSEAlgorithm>AES256</SSEAlgorithm>'
            b'</ApplyServerSideEncryptionByDefault></ServerSideEncryptionRule>'
            b'<Versioning>Disabled</Versioning>'
            b'<BucketPolicy></BucketPolicy>'
            b'</AgenticBucketInfo>'
        )
        result = serde.deserialize_output(
            models.GetAgenticBucketResult(), _output(xml),
            custom_deserializer=[serde.deserialize_output_xmlbody])
        info = result.agentic_bucket_info
        self.assertEqual('my-agentic-1234567890123456-cn-hangzhou-ab-apsr', info.name)
        self.assertEqual('1234567890123456', info.owner)
        self.assertEqual('cn-hangzhou', info.region)
        self.assertEqual('Standard', info.storage_class)
        self.assertEqual('Enabled', info.status)
        self.assertEqual('agentic', info.bucket_resource_type)
        self.assertEqual('private', info.acl)
        self.assertEqual('true', info.public_access_block)
        self.assertEqual('Disabled', info.versioning)
        self.assertEqual(
            'AES256',
            info.server_side_encryption_rule.apply_server_side_encryption_by_default.sse_algorithm)


class TestListAgenticBuckets(unittest.TestCase):
    def test_serialize_query(self):
        request = models.ListAgenticBucketsRequest(continuation_token='tok', max_keys=50)
        op_input = serde.serialize_input(request, OperationInput(
            op_name='ListAgenticBuckets', method='GET'))
        self.assertEqual('tok', op_input.parameters['continuation-token'])
        self.assertEqual('50', op_input.parameters['max-keys'])
        self.assertIsNone(op_input.bucket)

    def test_deserialize_result(self):
        xml = (
            b'<ListAgenticBucketsResult>'
            b'<Region>cn-hangzhou</Region><Owner>123</Owner>'
            b'<IsTruncated>true</IsTruncated>'
            b'<NextContinuationToken>next</NextContinuationToken>'
            b'<AgenticBuckets>'
            b'<AgenticBucket><Name>a-ab-apsr</Name><StorageClass>Standard</StorageClass>'
            b'<DataRedundancyType>LRS</DataRedundancyType><CreateTime>2026-06-13T08:00:00.000Z</CreateTime></AgenticBucket>'
            b'<AgenticBucket><Name>b-ab-apsr</Name><StorageClass>IA</StorageClass></AgenticBucket>'
            b'</AgenticBuckets>'
            b'</ListAgenticBucketsResult>'
        )
        result = serde.deserialize_output(
            models.ListAgenticBucketsResult(), _output(xml),
            custom_deserializer=[serde.deserialize_output_xmlbody])
        self.assertEqual('cn-hangzhou', result.region)
        self.assertTrue(result.is_truncated)
        self.assertEqual('next', result.next_continuation_token)
        self.assertEqual(2, len(result.agentic_buckets))
        self.assertEqual('a-ab-apsr', result.agentic_buckets[0].name)
        self.assertEqual('IA', result.agentic_buckets[1].storage_class)


class TestPutAgenticBucketStatus(unittest.TestCase):
    def test_serialize_body(self):
        request = models.PutAgenticBucketStatusRequest(
            bucket='b', agentic_bucket_status=models.AgenticBucketStatus(status='Disabled'))
        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutAgenticBucketStatus', method='PUT', bucket=request.bucket))
        self.assertEqual(
            b'<AgenticBucketStatus><Status>Disabled</Status></AgenticBucketStatus>', op_input.body)


class TestListBucketSpaces(unittest.TestCase):
    def test_serialize_query(self):
        request = models.ListBucketSpacesRequest(
            bucket='b', prefix='p', continuation_token='t', start_after='s0', max_keys=10)
        op_input = serde.serialize_input(request, OperationInput(
            op_name='ListBucketSpaces', method='GET', bucket=request.bucket))
        self.assertEqual('p', op_input.parameters['prefix'])
        self.assertEqual('t', op_input.parameters['continuation-token'])
        self.assertEqual('s0', op_input.parameters['start-after'])
        self.assertEqual('10', op_input.parameters['max-keys'])

    def test_deserialize_result(self):
        xml = (
            b'<ListBucketSpacesResult>'
            b'<Owner><ID>1234567890123456</ID><DisplayName>user</DisplayName></Owner>'
            b'<BucketSpaces>'
            b'<BucketSpace><Name>s1-bs-apsr</Name><Location>oss-cn-hangzhou</Location>'
            b'<CreationDate>2026-06-18T08:00:00.000Z</CreationDate><StorageClass>Standard</StorageClass></BucketSpace>'
            b'</BucketSpaces>'
            b'<Prefix>p</Prefix><MaxKeys>100</MaxKeys>'
            b'<IsTruncated>true</IsTruncated><NextContinuationToken>tok</NextContinuationToken>'
            b'<StartAfter>s0</StartAfter>'
            b'</ListBucketSpacesResult>'
        )
        result = serde.deserialize_output(
            models.ListBucketSpacesResult(), _output(xml),
            custom_deserializer=[serde.deserialize_output_xmlbody])
        self.assertEqual('1234567890123456', result.owner.id)
        self.assertEqual('user', result.owner.display_name)
        self.assertEqual(1, len(result.bucket_spaces))
        self.assertEqual('s1-bs-apsr', result.bucket_spaces[0].name)
        self.assertEqual('oss-cn-hangzhou', result.bucket_spaces[0].location)
        self.assertEqual(100, result.max_keys)
        self.assertTrue(result.is_truncated)
        self.assertEqual('tok', result.next_continuation_token)
        self.assertEqual('s0', result.start_after)


class TestAgenticBucketAttributes(unittest.TestCase):
    def test_acl_put_header(self):
        request = models.PutAgenticBucketAclRequest(bucket='b', acl='private')
        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutAgenticBucketAcl', method='PUT', bucket=request.bucket))
        self.assertEqual('private', op_input.headers['x-oss-acl'])

    def test_acl_get_result(self):
        xml = (
            b'<AccessControlPolicy>'
            b'<Owner><ID>123</ID><DisplayName>u</DisplayName></Owner>'
            b'<AccessControlList><Grant>private</Grant></AccessControlList>'
            b'</AccessControlPolicy>'
        )
        result = serde.deserialize_output(
            models.GetAgenticBucketAclResult(), _output(xml),
            custom_deserializer=[serde.deserialize_output_xmlbody])
        self.assertEqual('123', result.owner.id)
        self.assertEqual('private', result.acl)

    def test_encryption_put_body(self):
        from alibabacloud_oss_v2.models.bucket_encryption import (
            ServerSideEncryptionRule, ApplyServerSideEncryptionByDefault)
        request = models.PutAgenticBucketEncryptionRequest(
            bucket='b',
            server_side_encryption_rule=ServerSideEncryptionRule(
                apply_server_side_encryption_by_default=ApplyServerSideEncryptionByDefault(
                    sse_algorithm='AES256')))
        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutAgenticBucketEncryption', method='PUT', bucket=request.bucket))
        self.assertIn(b'<ServerSideEncryptionRule>', op_input.body)
        self.assertIn(b'<SSEAlgorithm>AES256</SSEAlgorithm>', op_input.body)

    def test_encryption_get_result(self):
        xml = (
            b'<ServerSideEncryptionRule><ApplyServerSideEncryptionByDefault>'
            b'<SSEAlgorithm>KMS</SSEAlgorithm></ApplyServerSideEncryptionByDefault>'
            b'</ServerSideEncryptionRule>'
        )
        result = serde.deserialize_output(
            models.GetAgenticBucketEncryptionResult(), _output(xml),
            custom_deserializer=[serde.deserialize_output_xmlbody])
        self.assertEqual(
            'KMS',
            result.server_side_encryption_rule.apply_server_side_encryption_by_default.sse_algorithm)

    def test_versioning_put_body(self):
        from alibabacloud_oss_v2.models.bucket_basic import VersioningConfiguration
        request = models.PutAgenticBucketVersioningRequest(
            bucket='b', versioning_configuration=VersioningConfiguration(status='Enabled'))
        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutAgenticBucketVersioning', method='PUT', bucket=request.bucket))
        self.assertEqual(
            b'<VersioningConfiguration><Status>Enabled</Status></VersioningConfiguration>', op_input.body)

    def test_versioning_get_result(self):
        xml = b'<VersioningConfiguration><Status>Enabled</Status></VersioningConfiguration>'
        result = serde.deserialize_output(
            models.GetAgenticBucketVersioningResult(), _output(xml),
            custom_deserializer=[serde.deserialize_output_xmlbody])
        self.assertEqual('Enabled', result.version_status)

    def test_pab_put_body(self):
        from alibabacloud_oss_v2.models.bucket_public_access_block import PublicAccessBlockConfiguration
        request = models.PutAgenticBucketPublicAccessBlockRequest(
            bucket='b',
            public_access_block_configuration=PublicAccessBlockConfiguration(block_public_access=True))
        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutAgenticBucketPublicAccessBlock', method='PUT', bucket=request.bucket))
        self.assertIn(b'<BlockPublicAccess>true</BlockPublicAccess>', op_input.body)

    def test_pab_get_result(self):
        xml = (
            b'<PublicAccessBlockConfiguration><BlockPublicAccess>true</BlockPublicAccess>'
            b'</PublicAccessBlockConfiguration>'
        )
        result = serde.deserialize_output(
            models.GetAgenticBucketPublicAccessBlockResult(), _output(xml),
            custom_deserializer=[serde.deserialize_output_xmlbody])
        self.assertTrue(result.public_access_block_configuration.block_public_access)

    def test_policy_get_result(self):
        body = b'{"Version":"1","Statement":[]}'
        result = serde.deserialize_output(
            models.GetAgenticBucketPolicyResult(body=body.decode()), _output(body),
            custom_deserializer=[serde.deserialize_output_xmlbody])
        self.assertEqual('{"Version":"1","Statement":[]}', result.body)


if __name__ == '__main__':
    unittest.main()
