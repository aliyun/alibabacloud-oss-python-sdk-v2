# pylint: skip-file

import unittest

from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_metadata_configuration as model
from alibabacloud_oss_v2.types import CaseInsensitiveDict, OperationInput, OperationOutput
from .. import MockHttpResponse


class TestCreateBucketMetadataConfiguration(unittest.TestCase):

    def test_empty_constructor(self):
        request = model.CreateBucketMetadataConfigurationRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.metadata_configuration)
        self.assertIsInstance(request, serde.RequestModel)

    def test_full_constructor(self):
        request = model.CreateBucketMetadataConfigurationRequest(
            bucket='bucketexampletest',
            metadata_configuration=model.MetadataConfiguration(
                journal_table_configuration=model.JournalTableConfiguration(
                    record_expiration=model.RecordExpiration(
                        expiration=model.RecordExpirationType.ENABLED,
                        days=30,
                    ),
                    encryption_configuration=model.MetadataTableEncryptionConfiguration(
                        sse_algorithm=model.SseAlgorithmType.AES256,
                    ),
                ),
                inventory_table_configuration=model.InventoryTableConfiguration(
                    configuration_state=model.ConfigurationStateType.DISABLED,
                ),
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual(model.RecordExpirationType.ENABLED,
                         request.metadata_configuration.journal_table_configuration.record_expiration.expiration)
        self.assertEqual(30, request.metadata_configuration.journal_table_configuration.record_expiration.days)
        self.assertEqual(model.SseAlgorithmType.AES256,
                         request.metadata_configuration.journal_table_configuration.encryption_configuration.sse_algorithm)
        self.assertEqual(model.ConfigurationStateType.DISABLED,
                         request.metadata_configuration.inventory_table_configuration.configuration_state)

    def test_xml_builder(self):
        # Build the canonical expected XML.
        expected_xml = (
            '<MetadataConfiguration>'
            '  <JournalTableConfiguration>'
            '    <RecordExpiration>'
            '      <Expiration>ENABLED</Expiration>'
            '      <Days>30</Days>'
            '    </RecordExpiration>'
            '    <EncryptionConfiguration>'
            '      <SseAlgorithm>AES256</SseAlgorithm>'
            '    </EncryptionConfiguration>'
            '  </JournalTableConfiguration>'
            '  <InventoryTableConfiguration>'
            '    <ConfigurationState>DISABLED</ConfigurationState>'
            '  </InventoryTableConfiguration>'
            '</MetadataConfiguration>'
        )
        expected_configuration = model.MetadataConfiguration()
        serde.deserialize_xml(
            expected_xml.encode('utf-8'),
            expected_configuration,
            expect_tag='MetadataConfiguration',
        )
        expected_xml_bytes = serde.serialize_xml(expected_configuration, root='MetadataConfiguration')

        # Build and serialize the request.
        configuration = model.MetadataConfiguration(
            journal_table_configuration=model.JournalTableConfiguration(
                record_expiration=model.RecordExpiration(
                    expiration=model.RecordExpirationType.ENABLED,
                    days=30,
                ),
                encryption_configuration=model.MetadataTableEncryptionConfiguration(
                    sse_algorithm=model.SseAlgorithmType.AES256,
                ),
            ),
            inventory_table_configuration=model.InventoryTableConfiguration(
                configuration_state=model.ConfigurationStateType.DISABLED,
            ),
        )
        request = model.CreateBucketMetadataConfigurationRequest(
            bucket='bucketexampletest',
            metadata_configuration=configuration,
        )
        op_input = serde.serialize_input(request, OperationInput(
            op_name='CreateBucketMetadataConfiguration',
            method='POST',
            bucket=request.bucket,
        ))
        xml_bytes = serde.serialize_xml(configuration, root='MetadataConfiguration')

        # Verify the operation input and exact XML body.
        self.assertEqual('CreateBucketMetadataConfiguration', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)
        self.assertEqual(xml_bytes, expected_xml_bytes)
        self.assertEqual(op_input.body, expected_xml_bytes)

    def test_empty_result_constructor(self):
        result = model.CreateBucketMetadataConfigurationResult()
        self.assertIsInstance(result, serde.ResultModel)


class TestGetBucketMetadataConfiguration(unittest.TestCase):

    def test_constructor_request(self):
        request = model.GetBucketMetadataConfigurationRequest()
        self.assertIsNone(request.bucket)
        self.assertIsInstance(request, serde.RequestModel)
        request = model.GetBucketMetadataConfigurationRequest(bucket='bucketexampletest')
        self.assertEqual('bucketexampletest', request.bucket)

    def test_deserialize_result(self):
        xml_data = b'''<GetBucketMetadataConfigurationResult>
          <MetadataConfigurationResult>
            <DestinationResult>
              <TableBucketType>oss</TableBucketType>
              <TableBucketArn>acs:oss:cn-hangzhou:1234567890123456:bucket/table-bucket</TableBucketArn>
              <TableNamespace>b_bucketexampletest</TableNamespace>
            </DestinationResult>
            <JournalTableConfigurationResult>
              <TableStatus>ACTIVE</TableStatus>
              <TableName>journal</TableName>
              <TableArn>acs:ots:cn-hangzhou:1234567890123456:instance/table/journal</TableArn>
              <RecordExpiration>
                <Expiration>ENABLED</Expiration>
                <Days>30</Days>
              </RecordExpiration>
              <EncryptionConfiguration>
                <SseAlgorithm>AES256</SseAlgorithm>
              </EncryptionConfiguration>
            </JournalTableConfigurationResult>
            <InventoryTableConfigurationResult>
              <ConfigurationState>ENABLED</ConfigurationState>
              <TableStatus>BACKFILLING</TableStatus>
              <TableName>inventory</TableName>
              <TableArn>acs:ots:cn-hangzhou:1234567890123456:instance/table/inventory</TableArn>
              <EncryptionConfiguration>
                <SseAlgorithm>oss:kms</SseAlgorithm>
                <KmsKeyArn>acs:kms:cn-hangzhou:1234567890123456:key/example-key</KmsKeyArn>
              </EncryptionConfiguration>
              <Error>
                <ErrorCode>ExampleError</ErrorCode>
                <ErrorMessage>example error</ErrorMessage>
              </Error>
            </InventoryTableConfigurationResult>
          </MetadataConfigurationResult>
        </GetBucketMetadataConfigurationResult>'''
        result = serde.deserialize_output(
            model.GetBucketMetadataConfigurationResult(),
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({'x-oss-request-id': 'request-id'}),
                http_response=MockHttpResponse(body=xml_data),
            ),
            custom_deserializer=[serde.deserialize_output_xmlbody],
        )
        self.assertEqual('request-id', result.request_id)
        metadata = result.metadata_configuration_result
        # DestinationResult
        self.assertEqual('oss', metadata.destination_result.table_bucket_type)
        self.assertEqual('acs:oss:cn-hangzhou:1234567890123456:bucket/table-bucket',
                         metadata.destination_result.table_bucket_arn)
        self.assertEqual('b_bucketexampletest', metadata.destination_result.table_namespace)
        # JournalTableConfigurationResult
        self.assertEqual('ACTIVE', metadata.journal_table_configuration_result.table_status)
        self.assertEqual(model.TableStatusType.ACTIVE, metadata.journal_table_configuration_result.table_status)
        self.assertEqual('journal', metadata.journal_table_configuration_result.table_name)
        self.assertEqual('acs:ots:cn-hangzhou:1234567890123456:instance/table/journal',
                         metadata.journal_table_configuration_result.table_arn)
        self.assertEqual('ENABLED', metadata.journal_table_configuration_result.record_expiration.expiration)
        self.assertEqual(30, metadata.journal_table_configuration_result.record_expiration.days)
        self.assertEqual('AES256', metadata.journal_table_configuration_result.encryption_configuration.sse_algorithm)
        # InventoryTableConfigurationResult
        self.assertEqual('ENABLED', metadata.inventory_table_configuration_result.configuration_state)
        self.assertEqual('BACKFILLING', metadata.inventory_table_configuration_result.table_status)
        self.assertEqual(model.TableStatusType.BACKFILLING, metadata.inventory_table_configuration_result.table_status)
        self.assertEqual('inventory', metadata.inventory_table_configuration_result.table_name)
        self.assertEqual('acs:ots:cn-hangzhou:1234567890123456:instance/table/inventory',
                         metadata.inventory_table_configuration_result.table_arn)
        self.assertEqual('oss:kms', metadata.inventory_table_configuration_result.encryption_configuration.sse_algorithm)
        self.assertEqual(model.SseAlgorithmType.OSS_KMS,
                         metadata.inventory_table_configuration_result.encryption_configuration.sse_algorithm)
        self.assertEqual('acs:kms:cn-hangzhou:1234567890123456:key/example-key',
                         metadata.inventory_table_configuration_result.encryption_configuration.kms_key_arn)
        self.assertEqual('ExampleError', metadata.inventory_table_configuration_result.error.error_code)
        self.assertEqual('example error', metadata.inventory_table_configuration_result.error.error_message)

    def test_empty_result_constructor(self):
        result = model.GetBucketMetadataConfigurationResult()
        self.assertIsNone(result.metadata_configuration_result)
        self.assertIsInstance(result, serde.ResultModel)


class TestDeleteBucketMetadataConfiguration(unittest.TestCase):

    def test_empty_constructor(self):
        request = model.DeleteBucketMetadataConfigurationRequest()
        self.assertIsNone(request.bucket)
        self.assertIsInstance(request, serde.RequestModel)

    def test_request_and_result(self):
        request = model.DeleteBucketMetadataConfigurationRequest(bucket='bucketexampletest')
        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteBucketMetadataConfiguration',
            method='DELETE',
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteBucketMetadataConfiguration', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)
        self.assertIsInstance(model.DeleteBucketMetadataConfigurationResult(), serde.ResultModel)


class TestUpdateBucketMetadataInventoryTableConfiguration(unittest.TestCase):

    def test_empty_constructor(self):
        request = model.UpdateBucketMetadataInventoryTableConfigurationRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.inventory_table_configuration)
        self.assertIsInstance(request, serde.RequestModel)

    def test_full_constructor(self):
        request = model.UpdateBucketMetadataInventoryTableConfigurationRequest(
            bucket='bucketexampletest',
            inventory_table_configuration=model.InventoryTableConfiguration(
                configuration_state=model.ConfigurationStateType.ENABLED,
                encryption_configuration=model.MetadataTableEncryptionConfiguration(
                    sse_algorithm=model.SseAlgorithmType.OSS_KMS,
                    kms_key_arn='acs:kms:cn-hangzhou:1234567890123456:key/example-key',
                ),
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual(model.ConfigurationStateType.ENABLED,
                         request.inventory_table_configuration.configuration_state)
        self.assertEqual(model.SseAlgorithmType.OSS_KMS,
                         request.inventory_table_configuration.encryption_configuration.sse_algorithm)
        self.assertEqual('acs:kms:cn-hangzhou:1234567890123456:key/example-key',
                         request.inventory_table_configuration.encryption_configuration.kms_key_arn)

    def test_xml_builder(self):
        # Build the canonical expected XML.
        expected_xml = (
            '<InventoryTableConfiguration>'
            '  <ConfigurationState>ENABLED</ConfigurationState>'
            '  <EncryptionConfiguration>'
            '    <SseAlgorithm>oss:kms</SseAlgorithm>'
            '    <KmsKeyArn>acs:kms:cn-hangzhou:1234567890123456:key/example-key</KmsKeyArn>'
            '  </EncryptionConfiguration>'
            '</InventoryTableConfiguration>'
        )
        expected_configuration = model.InventoryTableConfiguration()
        serde.deserialize_xml(
            expected_xml.encode('utf-8'),
            expected_configuration,
            expect_tag='InventoryTableConfiguration',
        )
        expected_xml_bytes = serde.serialize_xml(expected_configuration, root='InventoryTableConfiguration')

        # Build and serialize the request.
        configuration = model.InventoryTableConfiguration(
            configuration_state=model.ConfigurationStateType.ENABLED,
            encryption_configuration=model.MetadataTableEncryptionConfiguration(
                sse_algorithm=model.SseAlgorithmType.OSS_KMS,
                kms_key_arn='acs:kms:cn-hangzhou:1234567890123456:key/example-key',
            ),
        )
        request = model.UpdateBucketMetadataInventoryTableConfigurationRequest(
            bucket='bucketexampletest',
            inventory_table_configuration=configuration,
        )
        op_input = serde.serialize_input(request, OperationInput(
            op_name='UpdateBucketMetadataInventoryTableConfiguration',
            method='PUT',
            bucket=request.bucket,
        ))
        xml_bytes = serde.serialize_xml(configuration, root='InventoryTableConfiguration')

        # Verify the operation input and exact XML body.
        self.assertEqual('UpdateBucketMetadataInventoryTableConfiguration', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)
        self.assertEqual(xml_bytes, expected_xml_bytes)
        self.assertEqual(op_input.body, expected_xml_bytes)

    def test_empty_result_constructor(self):
        result = model.UpdateBucketMetadataInventoryTableConfigurationResult()
        self.assertIsInstance(result, serde.ResultModel)


class TestUpdateBucketMetadataJournalTableConfiguration(unittest.TestCase):

    def test_empty_constructor(self):
        request = model.UpdateBucketMetadataJournalTableConfigurationRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.journal_table_configuration)
        self.assertIsInstance(request, serde.RequestModel)

    def test_full_constructor(self):
        request = model.UpdateBucketMetadataJournalTableConfigurationRequest(
            bucket='bucketexampletest',
            journal_table_configuration=model.JournalTableConfiguration(
                record_expiration=model.RecordExpiration(
                    expiration=model.RecordExpirationType.DISABLED,
                ),
                encryption_configuration=model.MetadataTableEncryptionConfiguration(
                    sse_algorithm=model.SseAlgorithmType.OSS_KMS,
                    kms_key_arn='acs:kms:cn-hangzhou:1234567890123456:key/example-key',
                ),
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual(model.RecordExpirationType.DISABLED,
                         request.journal_table_configuration.record_expiration.expiration)
        self.assertIsNone(request.journal_table_configuration.record_expiration.days)
        self.assertEqual(model.SseAlgorithmType.OSS_KMS,
                         request.journal_table_configuration.encryption_configuration.sse_algorithm)
        self.assertEqual('acs:kms:cn-hangzhou:1234567890123456:key/example-key',
                         request.journal_table_configuration.encryption_configuration.kms_key_arn)

    def test_xml_builder(self):
        # Build the canonical expected XML.
        expected_xml = (
            '<JournalTableConfiguration>'
            '  <RecordExpiration>'
            '    <Expiration>DISABLED</Expiration>'
            '  </RecordExpiration>'
            '  <EncryptionConfiguration>'
            '    <SseAlgorithm>oss:kms</SseAlgorithm>'
            '    <KmsKeyArn>acs:kms:cn-hangzhou:1234567890123456:key/example-key</KmsKeyArn>'
            '  </EncryptionConfiguration>'
            '</JournalTableConfiguration>'
        )
        expected_configuration = model.JournalTableConfiguration()
        serde.deserialize_xml(
            expected_xml.encode('utf-8'),
            expected_configuration,
            expect_tag='JournalTableConfiguration',
        )
        expected_xml_bytes = serde.serialize_xml(expected_configuration, root='JournalTableConfiguration')

        # Build and serialize the request.
        configuration = model.JournalTableConfiguration(
            record_expiration=model.RecordExpiration(
                expiration=model.RecordExpirationType.DISABLED,
            ),
            encryption_configuration=model.MetadataTableEncryptionConfiguration(
                sse_algorithm=model.SseAlgorithmType.OSS_KMS,
                kms_key_arn='acs:kms:cn-hangzhou:1234567890123456:key/example-key',
            ),
        )
        request = model.UpdateBucketMetadataJournalTableConfigurationRequest(
            bucket='bucketexampletest',
            journal_table_configuration=configuration,
        )
        op_input = serde.serialize_input(request, OperationInput(
            op_name='UpdateBucketMetadataJournalTableConfiguration',
            method='PUT',
            bucket=request.bucket,
        ))
        xml_bytes = serde.serialize_xml(configuration, root='JournalTableConfiguration')

        # Verify the operation input and exact XML body.
        self.assertEqual('UpdateBucketMetadataJournalTableConfiguration', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)
        self.assertEqual(xml_bytes, expected_xml_bytes)
        self.assertEqual(op_input.body, expected_xml_bytes)

    def test_empty_result_constructor(self):
        result = model.UpdateBucketMetadataJournalTableConfigurationResult()
        self.assertIsInstance(result, serde.ResultModel)


class TestBucketMetadataConfigurationEnums(unittest.TestCase):

    def test_configuration_state_type(self):
        self.assertEqual('ENABLED', model.ConfigurationStateType.ENABLED)
        self.assertEqual('DISABLED', model.ConfigurationStateType.DISABLED)

    def test_record_expiration_type(self):
        self.assertEqual('ENABLED', model.RecordExpirationType.ENABLED)
        self.assertEqual('DISABLED', model.RecordExpirationType.DISABLED)

    def test_table_status_type(self):
        self.assertEqual('CREATING', model.TableStatusType.CREATING)
        self.assertEqual('BACKFILLING', model.TableStatusType.BACKFILLING)
        self.assertEqual('ACTIVE', model.TableStatusType.ACTIVE)
        self.assertEqual('FAILED', model.TableStatusType.FAILED)

    def test_sse_algorithm_type(self):
        self.assertEqual('AES256', model.SseAlgorithmType.AES256)
        self.assertEqual('oss:kms', model.SseAlgorithmType.OSS_KMS)
