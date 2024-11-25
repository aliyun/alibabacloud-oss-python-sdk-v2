# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde, InventoryOptionalFieldType
from alibabacloud_oss_v2.models import bucket_inventory as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse


class TestPutBucketInventory(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutBucketInventoryRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.inventory_id)
        self.assertIsNone(request.inventory_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutBucketInventoryRequest(
            bucket='bucketexampletest',
            inventory_id='SNKsc:Wj|s',
            inventory_configuration=model.InventoryConfiguration(
                included_object_versions='a-8|zg/5q*',
                optional_fields=model.OptionalFields(
                    fields=[model.InventoryOptionalFieldType.ENCRYPTION_STATUS, model.InventoryOptionalFieldType.STORAGE_CLASS],
                ),
                id='0022012****',
                is_enabled=False,
                destination=model.InventoryDestination(
                    oss_bucket_destination=model.InventoryOSSBucketDestination(
                        format=model.InventoryFormatType.CSV,
                        account_id='PMCl7H&U&T',
                        role_arn='k.G_(r\$ZR',
                        bucket='bucketexampletest',
                        prefix='aaa',
                        encryption=model.InventoryEncryption(
                            sse_kms=model.SSEKMS(
                                key_id=':qb\KdTDlu',
                            ),
                            sse_oss='+-HnP#AGMt',
                        ),
                    ),
                ),
                schedule=model.InventorySchedule(
                    frequency=model.InventoryFrequencyType.WEEKLY,
                ),
                filter=model.InventoryFilter(
                    lower_size_bound=53305,
                    upper_size_bound=8328,
                    storage_class='ColdArchive',
                    prefix='aaa',
                    last_modify_begin_time_stamp=19696,
                    last_modify_end_time_stamp=44727,
                ),
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('SNKsc:Wj|s', request.inventory_id)
        self.assertEqual('a-8|zg/5q*', request.inventory_configuration.included_object_versions)
        self.assertEqual([model.InventoryOptionalFieldType.ENCRYPTION_STATUS, model.InventoryOptionalFieldType.STORAGE_CLASS], request.inventory_configuration.optional_fields.fields)
        self.assertEqual('0022012****', request.inventory_configuration.id)
        self.assertEqual(False, request.inventory_configuration.is_enabled)
        self.assertEqual(model.InventoryFormatType.CSV, request.inventory_configuration.destination.oss_bucket_destination.format)
        self.assertEqual('PMCl7H&U&T', request.inventory_configuration.destination.oss_bucket_destination.account_id)
        self.assertEqual('k.G_(r\$ZR', request.inventory_configuration.destination.oss_bucket_destination.role_arn)
        self.assertEqual('bucketexampletest', request.inventory_configuration.destination.oss_bucket_destination.bucket)
        self.assertEqual('aaa', request.inventory_configuration.destination.oss_bucket_destination.prefix)
        self.assertEqual(':qb\KdTDlu', request.inventory_configuration.destination.oss_bucket_destination.encryption.sse_kms.key_id)
        self.assertEqual('+-HnP#AGMt', request.inventory_configuration.destination.oss_bucket_destination.encryption.sse_oss)
        self.assertEqual(model.InventoryFrequencyType.WEEKLY, request.inventory_configuration.schedule.frequency)
        self.assertEqual(53305, request.inventory_configuration.filter.lower_size_bound)
        self.assertEqual(8328, request.inventory_configuration.filter.upper_size_bound)
        self.assertEqual('ColdArchive', request.inventory_configuration.filter.storage_class)
        self.assertEqual('aaa', request.inventory_configuration.filter.prefix)
        self.assertEqual(19696, request.inventory_configuration.filter.last_modify_begin_time_stamp)
        self.assertEqual(44727, request.inventory_configuration.filter.last_modify_end_time_stamp)

    def test_serialize_request(self):
        request = model.PutBucketInventoryRequest(
            bucket='bucketexampletest',
            inventory_id='SNKsc:Wj|s',
            inventory_configuration=model.InventoryConfiguration(
                included_object_versions='a-8|zg/5q*',
                optional_fields=model.OptionalFields(
                    fields=[model.InventoryOptionalFieldType.SIZE, model.InventoryOptionalFieldType.STORAGE_CLASS],
                ),
                id='0022012****',
                is_enabled=True,
                destination=model.InventoryDestination(
                    oss_bucket_destination=model.InventoryOSSBucketDestination(
                        format=model.InventoryFormatType.CSV,
                        account_id='PMCl7H&U&T',
                        role_arn='k.G_(r\$ZR',
                        bucket='bucketexampletest',
                        prefix='aaa',
                        encryption=model.InventoryEncryption(
                            sse_kms=model.SSEKMS(
                                key_id=':qb\KdTDlu',
                            ),
                            sse_oss='+-HnP#AGMt',
                        ),
                    ),
                ),
                schedule=model.InventorySchedule(
                    frequency=model.InventoryFrequencyType.WEEKLY,
                ),
                filter=model.InventoryFilter(
                    lower_size_bound=53305,
                    upper_size_bound=8328,
                    storage_class='ColdArchive',
                    prefix='aaa',
                    last_modify_begin_time_stamp=19696,
                    last_modify_end_time_stamp=44727,
                ),
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutBucketInventory',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutBucketInventory', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)
        self.assertEqual('SNKsc:Wj|s', op_input.parameters.get('inventoryId'))

    def test_constructor_result(self):
        result = model.PutBucketInventoryResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutBucketInventoryResult()
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


class TestGetBucketInventory(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketInventoryRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.inventory_id)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetBucketInventoryRequest(
            bucket='bucketexampletest',
            inventory_id='F^voQQ4Dq#',
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('F^voQQ4Dq#', request.inventory_id)

    def test_serialize_request(self):
        request = model.GetBucketInventoryRequest(
            bucket='bucketexampletest',
            inventory_id='F^voQQ4Dq#',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketInventory',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetBucketInventory', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)
        self.assertEqual('F^voQQ4Dq#', op_input.parameters.get('inventoryId'))

    def test_constructor_result(self):
        result = model.GetBucketInventoryResult()
        self.assertIsNone(result.inventory_configuration)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketInventoryResult(
            inventory_configuration=model.InventoryConfiguration(
                included_object_versions='B?Q|%?(8m3',
                optional_fields=model.OptionalFields(
                    fields=[model.InventoryOptionalFieldType.STORAGE_CLASS, model.InventoryOptionalFieldType.SIZE],
                ),
                id='0022012****',
                is_enabled=False,
                destination=model.InventoryDestination(
                    oss_bucket_destination=model.InventoryOSSBucketDestination(
                        format=model.InventoryFormatType.CSV,
                        account_id='e(ri@MofKd',
                        role_arn='r_R4bA5xpY',
                        bucket='bucketexampletest',
                        prefix='aaa',
                        encryption=model.InventoryEncryption(
                            sse_kms=model.SSEKMS(
                                key_id='v7$8bSN&z9',
                            ),
                            sse_oss='uVT920D9h)',
                        ),
                    ),
                ),
                schedule=model.InventorySchedule(
                    frequency=model.InventoryFrequencyType.DAILY,
                ),
                filter=model.InventoryFilter(
                    lower_size_bound=33642,
                    upper_size_bound=67408,
                    storage_class='ColdArchive',
                    prefix='aaa',
                    last_modify_begin_time_stamp=97612,
                    last_modify_end_time_stamp=34441,
                ),
            ),
        )
        self.assertEqual('B?Q|%?(8m3', result.inventory_configuration.included_object_versions)
        self.assertEqual([model.InventoryOptionalFieldType.STORAGE_CLASS, model.InventoryOptionalFieldType.SIZE], result.inventory_configuration.optional_fields.fields)
        self.assertEqual('0022012****', result.inventory_configuration.id)
        self.assertEqual(False, result.inventory_configuration.is_enabled)
        self.assertEqual(model.InventoryFormatType.CSV, result.inventory_configuration.destination.oss_bucket_destination.format)
        self.assertEqual('e(ri@MofKd', result.inventory_configuration.destination.oss_bucket_destination.account_id)
        self.assertEqual('r_R4bA5xpY', result.inventory_configuration.destination.oss_bucket_destination.role_arn)
        self.assertEqual('bucketexampletest', result.inventory_configuration.destination.oss_bucket_destination.bucket)
        self.assertEqual('aaa', result.inventory_configuration.destination.oss_bucket_destination.prefix)
        self.assertEqual('v7$8bSN&z9', result.inventory_configuration.destination.oss_bucket_destination.encryption.sse_kms.key_id)
        self.assertEqual('uVT920D9h)', result.inventory_configuration.destination.oss_bucket_destination.encryption.sse_oss)
        self.assertEqual(model.InventoryFrequencyType.DAILY, result.inventory_configuration.schedule.frequency)
        self.assertEqual(33642, result.inventory_configuration.filter.lower_size_bound)
        self.assertEqual(67408, result.inventory_configuration.filter.upper_size_bound)
        self.assertEqual('ColdArchive', result.inventory_configuration.filter.storage_class)
        self.assertEqual('aaa', result.inventory_configuration.filter.prefix)
        self.assertEqual(97612, result.inventory_configuration.filter.last_modify_begin_time_stamp)
        self.assertEqual(34441, result.inventory_configuration.filter.last_modify_end_time_stamp)


    def test_deserialize_result(self):
        xml_data = r'''
        <InventoryConfiguration>
        </InventoryConfiguration>'''

        result = model.GetBucketInventoryResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
          <InventoryConfiguration>
             <Id>report1</Id>
             <IsEnabled>true</IsEnabled>
             <Destination>
                <OSSBucketDestination>
                   <Format>CSV</Format>
                   <AccountId>1000000000000000</AccountId>
                   <RoleArn>acs:ram::1000000000000000:role/AliyunOSSRole</RoleArn>
                   <Bucket>acs:oss:::bucket_0001</Bucket>
                   <Prefix>prefix1</Prefix>
                   <Encryption>
                    <SSE-KMS>
                        <KeyId>GGUIHBKJNFkjghug</KeyId>
                    </SSE-KMS>
                      <SSE-OSS>+-HnP#AGMt</SSE-OSS>
                   </Encryption>
                </OSSBucketDestination>
             </Destination>
             <Schedule>
                <Frequency>Daily</Frequency>
             </Schedule>
             <Filter>
               <Prefix>myprefix/</Prefix>
             </Filter>
             <IncludedObjectVersions>All</IncludedObjectVersions>
             <OptionalFields>
                <Field>Size</Field>
                <Field>LastModifiedDate</Field>
                <Field>ETag</Field>
                <Field>StorageClass</Field>
                <Field>IsMultipartUploaded</Field>
                <Field>EncryptionStatus</Field>
             </OptionalFields>
          </InventoryConfiguration>
        '''

        result = model.GetBucketInventoryResult()
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=xml_data,
            )
        )
        deserializer = [serde.deserialize_output_xmlbody]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertEqual('report1', result.inventory_configuration.id)
        self.assertEqual(True, result.inventory_configuration.is_enabled)
        self.assertEqual('CSV', result.inventory_configuration.destination.oss_bucket_destination.format)
        self.assertEqual('1000000000000000', result.inventory_configuration.destination.oss_bucket_destination.account_id)
        self.assertEqual('acs:ram::1000000000000000:role/AliyunOSSRole', result.inventory_configuration.destination.oss_bucket_destination.role_arn)
        self.assertEqual('acs:oss:::bucket_0001', result.inventory_configuration.destination.oss_bucket_destination.bucket)
        self.assertEqual('prefix1', result.inventory_configuration.destination.oss_bucket_destination.prefix)
        self.assertEqual('GGUIHBKJNFkjghug', result.inventory_configuration.destination.oss_bucket_destination.encryption.sse_kms.key_id)
        self.assertEqual('+-HnP#AGMt', result.inventory_configuration.destination.oss_bucket_destination.encryption.sse_oss)
        self.assertEqual('Daily', result.inventory_configuration.schedule.frequency)
        self.assertEqual('myprefix/', result.inventory_configuration.filter.prefix)
        self.assertEqual('All', result.inventory_configuration.included_object_versions)
        self.assertEqual(InventoryOptionalFieldType.SIZE, result.inventory_configuration.optional_fields.fields[0])
        self.assertEqual(InventoryOptionalFieldType.LAST_MODIFIED_DATE, result.inventory_configuration.optional_fields.fields[1])
        self.assertEqual(InventoryOptionalFieldType.E_TAG, result.inventory_configuration.optional_fields.fields[2])
        self.assertEqual(InventoryOptionalFieldType.STORAGE_CLASS, result.inventory_configuration.optional_fields.fields[3])
        self.assertEqual(InventoryOptionalFieldType.IS_MULTIPART_UPLOADED, result.inventory_configuration.optional_fields.fields[4])
        self.assertEqual(InventoryOptionalFieldType.ENCRYPTION_STATUS, result.inventory_configuration.optional_fields.fields[5])


class TestListBucketInventory(unittest.TestCase):
    def test_constructor_request(self):
        request = model.ListBucketInventoryRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.continuation_token)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.ListBucketInventoryRequest(
            bucket='bucketexampletest',
            continuation_token='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', request.continuation_token)

    def test_serialize_request(self):
        request = model.ListBucketInventoryRequest(
            bucket='bucketexampletest',
            continuation_token='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='ListBucketInventory',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('ListBucketInventory', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)
        self.assertEqual('ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', op_input.parameters.get('continuation-token'))

    def test_constructor_result(self):
        result = model.ListBucketInventoryResult()
        self.assertIsNone(result.list_inventory_configurations_result)
        self.assertIsInstance(result, serde.Model)

        result = model.ListBucketInventoryResult(
            list_inventory_configurations_result=model.ListInventoryConfigurationsResult(
                inventory_configurations=[model.InventoryConfiguration(
                    included_object_versions='@p2nBjWrD ',
                    optional_fields=model.OptionalFields(
                        fields=[model.InventoryOptionalFieldType.LAST_MODIFIED_DATE, model.InventoryOptionalFieldType.IS_MULTIPART_UPLOADED],
                    ),
                    id='0022012****',
                    is_enabled=False,
                    destination=model.InventoryDestination(
                        oss_bucket_destination=model.InventoryOSSBucketDestination(
                            format=model.InventoryFormatType.CSV,
                            account_id='NEGtM%x5:P',
                            role_arn='aY(i k>HZU',
                            bucket='bucketexampletest',
                            prefix='aaa',
                            encryption=model.InventoryEncryption(
                                sse_kms=model.SSEKMS(
                                    key_id='u2w5O6vlJU',
                                ),
                                sse_oss='iC\9Q$6gtP',
                            ),
                        ),
                    ),
                    schedule=model.InventorySchedule(
                        frequency=model.InventoryFrequencyType.DAILY,
                    ),
                    filter=model.InventoryFilter(
                        lower_size_bound=29522,
                        upper_size_bound=23178,
                        storage_class='ColdArchive',
                        prefix='aaa',
                        last_modify_begin_time_stamp=12789,
                        last_modify_end_time_stamp=2209,
                    ),
                ), model.InventoryConfiguration(
                    included_object_versions='@p2nBjWrD ',
                    optional_fields=model.OptionalFields(
                        fields=[model.InventoryOptionalFieldType.E_TAG, model.InventoryOptionalFieldType.ENCRYPTION_STATUS],
                    ),
                    id='0022012****',
                    is_enabled=True,
                    destination=model.InventoryDestination(
                        oss_bucket_destination=model.InventoryOSSBucketDestination(
                            format=model.InventoryFormatType.CSV,
                            account_id='NEGtM%x5:P',
                            role_arn='aY(i k>HZU',
                            bucket='bucketexampletest',
                            prefix='aaa',
                            encryption=model.InventoryEncryption(
                                sse_kms=model.SSEKMS(
                                    key_id='u2w5O6vlJU',
                                ),
                                sse_oss='iC\9Q$6gtP',
                            ),
                        ),
                    ),
                    schedule=model.InventorySchedule(
                        frequency=model.InventoryFrequencyType.WEEKLY,
                    ),
                    filter=model.InventoryFilter(
                        lower_size_bound=29522,
                        upper_size_bound=23178,
                        storage_class='ColdArchive',
                        prefix='aaa',
                        last_modify_begin_time_stamp=12789,
                        last_modify_end_time_stamp=2209,
                    ),
                )],
                is_truncated=True,
                next_continuation_token='NextChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            ),
        )
        self.assertEqual('@p2nBjWrD ', result.list_inventory_configurations_result.inventory_configurations[0].included_object_versions)
        self.assertEqual([model.InventoryOptionalFieldType.LAST_MODIFIED_DATE, model.InventoryOptionalFieldType.IS_MULTIPART_UPLOADED], result.list_inventory_configurations_result.inventory_configurations[0].optional_fields.fields)
        self.assertEqual('0022012****', result.list_inventory_configurations_result.inventory_configurations[0].id)
        self.assertEqual(False, result.list_inventory_configurations_result.inventory_configurations[0].is_enabled)
        self.assertEqual(model.InventoryFormatType.CSV, result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.format)
        self.assertEqual('NEGtM%x5:P', result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.account_id)
        self.assertEqual('aY(i k>HZU', result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.role_arn)
        self.assertEqual('bucketexampletest', result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.bucket)
        self.assertEqual('aaa', result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.prefix)
        self.assertEqual('u2w5O6vlJU', result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.encryption.sse_kms.key_id)
        self.assertEqual('iC\9Q$6gtP', result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.encryption.sse_oss)
        self.assertEqual(model.InventoryFrequencyType.DAILY, result.list_inventory_configurations_result.inventory_configurations[0].schedule.frequency)
        self.assertEqual(29522, result.list_inventory_configurations_result.inventory_configurations[0].filter.lower_size_bound)
        self.assertEqual(23178, result.list_inventory_configurations_result.inventory_configurations[0].filter.upper_size_bound)
        self.assertEqual('ColdArchive', result.list_inventory_configurations_result.inventory_configurations[0].filter.storage_class)
        self.assertEqual('aaa', result.list_inventory_configurations_result.inventory_configurations[0].filter.prefix)
        self.assertEqual(12789, result.list_inventory_configurations_result.inventory_configurations[0].filter.last_modify_begin_time_stamp)
        self.assertEqual(2209, result.list_inventory_configurations_result.inventory_configurations[0].filter.last_modify_end_time_stamp)
        self.assertEqual('@p2nBjWrD ', result.list_inventory_configurations_result.inventory_configurations[1].included_object_versions)
        self.assertEqual([model.InventoryOptionalFieldType.E_TAG, model.InventoryOptionalFieldType.ENCRYPTION_STATUS], result.list_inventory_configurations_result.inventory_configurations[1].optional_fields.fields)
        self.assertEqual('0022012****', result.list_inventory_configurations_result.inventory_configurations[1].id)
        self.assertEqual(True, result.list_inventory_configurations_result.inventory_configurations[1].is_enabled)
        self.assertEqual(model.InventoryFormatType.CSV, result.list_inventory_configurations_result.inventory_configurations[1].destination.oss_bucket_destination.format)
        self.assertEqual('NEGtM%x5:P', result.list_inventory_configurations_result.inventory_configurations[1].destination.oss_bucket_destination.account_id)
        self.assertEqual('aY(i k>HZU', result.list_inventory_configurations_result.inventory_configurations[1].destination.oss_bucket_destination.role_arn)
        self.assertEqual('bucketexampletest', result.list_inventory_configurations_result.inventory_configurations[1].destination.oss_bucket_destination.bucket)
        self.assertEqual('aaa', result.list_inventory_configurations_result.inventory_configurations[1].destination.oss_bucket_destination.prefix)
        self.assertEqual('u2w5O6vlJU', result.list_inventory_configurations_result.inventory_configurations[1].destination.oss_bucket_destination.encryption.sse_kms.key_id)
        self.assertEqual('iC\9Q$6gtP', result.list_inventory_configurations_result.inventory_configurations[1].destination.oss_bucket_destination.encryption.sse_oss)
        self.assertEqual(model.InventoryFrequencyType.WEEKLY, result.list_inventory_configurations_result.inventory_configurations[1].schedule.frequency)
        self.assertEqual(29522, result.list_inventory_configurations_result.inventory_configurations[1].filter.lower_size_bound)
        self.assertEqual(23178, result.list_inventory_configurations_result.inventory_configurations[1].filter.upper_size_bound)
        self.assertEqual('ColdArchive', result.list_inventory_configurations_result.inventory_configurations[1].filter.storage_class)
        self.assertEqual('aaa', result.list_inventory_configurations_result.inventory_configurations[1].filter.prefix)
        self.assertEqual(12789, result.list_inventory_configurations_result.inventory_configurations[1].filter.last_modify_begin_time_stamp)
        self.assertEqual(2209, result.list_inventory_configurations_result.inventory_configurations[1].filter.last_modify_end_time_stamp)
        self.assertEqual(True, result.list_inventory_configurations_result.is_truncated)
        self.assertEqual('NextChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', result.list_inventory_configurations_result.next_continuation_token)


        result = model.ListBucketInventoryResult(
            list_inventory_configurations_result=model.ListInventoryConfigurationsResult(
                inventory_configurations=[model.InventoryConfiguration(
                    included_object_versions='@p2nBjWrD ',
                    optional_fields=model.OptionalFields(
                        fields=['ETag', 'ETag'],
                    ),
                    id='0022012****',
                    is_enabled=True,
                    destination=model.InventoryDestination(
                        oss_bucket_destination=model.InventoryOSSBucketDestination(
                            format='CSV',
                            account_id='NEGtM%x5:P',
                            role_arn='aY(i k>HZU',
                            bucket='bucketexampletest',
                            prefix='aaa',
                            encryption=model.InventoryEncryption(
                                sse_kms=model.SSEKMS(
                                    key_id='u2w5O6vlJU',
                                ),
                                sse_oss='iC\9Q$6gtP',
                            ),
                        ),
                    ),
                    schedule=model.InventorySchedule(
                        frequency='Daily',
                    ),
                    filter=model.InventoryFilter(
                        lower_size_bound=29522,
                        upper_size_bound=23178,
                        storage_class='ColdArchive',
                        prefix='aaa',
                        last_modify_begin_time_stamp=12789,
                        last_modify_end_time_stamp=2209,
                    ),
                ), model.InventoryConfiguration(
                    included_object_versions='@p2nBjWrD ',
                    optional_fields=model.OptionalFields(
                        fields=['LastModifiedDate', 'IsMultipartUploaded'],
                    ),
                    id='0022012****',
                    is_enabled=True,
                    destination=model.InventoryDestination(
                        oss_bucket_destination=model.InventoryOSSBucketDestination(
                            format='CSV',
                            account_id='NEGtM%x5:P',
                            role_arn='aY(i k>HZU',
                            bucket='bucketexampletest',
                            prefix='aaa',
                            encryption=model.InventoryEncryption(
                                sse_kms=model.SSEKMS(
                                    key_id='u2w5O6vlJU',
                                ),
                                sse_oss='iC\9Q$6gtP',
                            ),
                        ),
                    ),
                    schedule=model.InventorySchedule(
                        frequency='Weekly',
                    ),
                    filter=model.InventoryFilter(
                        lower_size_bound=29522,
                        upper_size_bound=23178,
                        storage_class='ColdArchive',
                        prefix='aaa',
                        last_modify_begin_time_stamp=12789,
                        last_modify_end_time_stamp=2209,
                    ),
                )],
                is_truncated=True,
                next_continuation_token='NextChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            ),
        )
        self.assertEqual('@p2nBjWrD ', result.list_inventory_configurations_result.inventory_configurations[0].included_object_versions)
        self.assertEqual(['ETag', 'ETag'], result.list_inventory_configurations_result.inventory_configurations[0].optional_fields.fields)
        self.assertEqual('0022012****', result.list_inventory_configurations_result.inventory_configurations[0].id)
        self.assertEqual(True, result.list_inventory_configurations_result.inventory_configurations[0].is_enabled)
        self.assertEqual('CSV', result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.format)
        self.assertEqual('NEGtM%x5:P', result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.account_id)
        self.assertEqual('aY(i k>HZU', result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.role_arn)
        self.assertEqual('bucketexampletest', result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.bucket)
        self.assertEqual('aaa', result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.prefix)
        self.assertEqual('u2w5O6vlJU', result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.encryption.sse_kms.key_id)
        self.assertEqual('iC\9Q$6gtP', result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.encryption.sse_oss)
        self.assertEqual('Daily', result.list_inventory_configurations_result.inventory_configurations[0].schedule.frequency)
        self.assertEqual(29522, result.list_inventory_configurations_result.inventory_configurations[0].filter.lower_size_bound)
        self.assertEqual(23178, result.list_inventory_configurations_result.inventory_configurations[0].filter.upper_size_bound)
        self.assertEqual('ColdArchive', result.list_inventory_configurations_result.inventory_configurations[0].filter.storage_class)
        self.assertEqual('aaa', result.list_inventory_configurations_result.inventory_configurations[0].filter.prefix)
        self.assertEqual(12789, result.list_inventory_configurations_result.inventory_configurations[0].filter.last_modify_begin_time_stamp)
        self.assertEqual(2209, result.list_inventory_configurations_result.inventory_configurations[0].filter.last_modify_end_time_stamp)
        self.assertEqual('@p2nBjWrD ', result.list_inventory_configurations_result.inventory_configurations[1].included_object_versions)
        self.assertEqual(['LastModifiedDate', 'IsMultipartUploaded'], result.list_inventory_configurations_result.inventory_configurations[1].optional_fields.fields)
        self.assertEqual('0022012****', result.list_inventory_configurations_result.inventory_configurations[1].id)
        self.assertEqual(True, result.list_inventory_configurations_result.inventory_configurations[1].is_enabled)
        self.assertEqual('CSV', result.list_inventory_configurations_result.inventory_configurations[1].destination.oss_bucket_destination.format)
        self.assertEqual('NEGtM%x5:P', result.list_inventory_configurations_result.inventory_configurations[1].destination.oss_bucket_destination.account_id)
        self.assertEqual('aY(i k>HZU', result.list_inventory_configurations_result.inventory_configurations[1].destination.oss_bucket_destination.role_arn)
        self.assertEqual('bucketexampletest', result.list_inventory_configurations_result.inventory_configurations[1].destination.oss_bucket_destination.bucket)
        self.assertEqual('aaa', result.list_inventory_configurations_result.inventory_configurations[1].destination.oss_bucket_destination.prefix)
        self.assertEqual('u2w5O6vlJU', result.list_inventory_configurations_result.inventory_configurations[1].destination.oss_bucket_destination.encryption.sse_kms.key_id)
        self.assertEqual('iC\9Q$6gtP', result.list_inventory_configurations_result.inventory_configurations[1].destination.oss_bucket_destination.encryption.sse_oss)
        self.assertEqual('Weekly', result.list_inventory_configurations_result.inventory_configurations[1].schedule.frequency)
        self.assertEqual(29522, result.list_inventory_configurations_result.inventory_configurations[1].filter.lower_size_bound)
        self.assertEqual(23178, result.list_inventory_configurations_result.inventory_configurations[1].filter.upper_size_bound)
        self.assertEqual('ColdArchive', result.list_inventory_configurations_result.inventory_configurations[1].filter.storage_class)
        self.assertEqual('aaa', result.list_inventory_configurations_result.inventory_configurations[1].filter.prefix)
        self.assertEqual(12789, result.list_inventory_configurations_result.inventory_configurations[1].filter.last_modify_begin_time_stamp)
        self.assertEqual(2209, result.list_inventory_configurations_result.inventory_configurations[1].filter.last_modify_end_time_stamp)
        self.assertEqual(True, result.list_inventory_configurations_result.is_truncated)
        self.assertEqual('NextChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', result.list_inventory_configurations_result.next_continuation_token)


    def test_deserialize_result(self):
        xml_data = r'''
        <ListInventoryConfigurationsResult>
        </ListInventoryConfigurationsResult>'''

        result = model.ListBucketInventoryResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
                   <ListInventoryConfigurationsResult>
                      <InventoryConfiguration>
                         <Id>report1</Id>
                         <IsEnabled>true</IsEnabled>
                         <Destination>
                            <OSSBucketDestination>
                               <Format>CSV</Format>
                               <AccountId>1000000000000000</AccountId>
                               <RoleArn>acs:ram::1000000000000000:role/AliyunOSSRole</RoleArn>
                               <Bucket>acs:oss:::destination-bucket</Bucket>
                               <Prefix>prefix1</Prefix>
                            </OSSBucketDestination>
                         </Destination>
                         <Schedule>
                            <Frequency>Daily</Frequency>
                         </Schedule>
                         <Filter>
                            <Prefix>prefix/One</Prefix>
                         </Filter>
                         <IncludedObjectVersions>All</IncludedObjectVersions>
                         <OptionalFields>
                            <Field>Size</Field>
                            <Field>LastModifiedDate</Field>
                            <Field>ETag</Field>
                            <Field>StorageClass</Field>
                            <Field>IsMultipartUploaded</Field>
                            <Field>EncryptionStatus</Field>
                         </OptionalFields>
                      </InventoryConfiguration>
                      <InventoryConfiguration>
                         <Id>report2</Id>
                         <IsEnabled>true</IsEnabled>
                         <Destination>
                            <OSSBucketDestination>
                               <Format>CSV</Format>
                               <AccountId>1000000000000000</AccountId>
                               <RoleArn>acs:ram::1000000000000000:role/AliyunOSSRole</RoleArn>
                               <Bucket>acs:oss:::destination-bucket</Bucket>
                               <Prefix>prefix2</Prefix>
                            </OSSBucketDestination>
                         </Destination>
                         <Schedule>
                            <Frequency>Daily</Frequency>
                         </Schedule>
                         <Filter>
                            <Prefix>prefix/Two</Prefix>
                         </Filter>
                         <IncludedObjectVersions>All</IncludedObjectVersions>
                         <OptionalFields>
                            <Field>Size</Field>
                            <Field>LastModifiedDate</Field>
                            <Field>ETag</Field>
                            <Field>StorageClass</Field>
                            <Field>IsMultipartUploaded</Field>
                            <Field>EncryptionStatus</Field>
                         </OptionalFields>
                      </InventoryConfiguration>
                      <InventoryConfiguration>
                         <Id>report3</Id>
                         <IsEnabled>true</IsEnabled>
                         <Destination>
                            <OSSBucketDestination>
                               <Format>CSV</Format>
                               <AccountId>1000000000000000</AccountId>
                               <RoleArn>acs:ram::1000000000000000:role/AliyunOSSRole</RoleArn>
                               <Bucket>acs:oss:::destination-bucket</Bucket>
                               <Prefix>prefix3</Prefix>
                            </OSSBucketDestination>
                         </Destination>
                         <Schedule>
                            <Frequency>Daily</Frequency>
                         </Schedule>
                         <Filter>
                            <Prefix>prefix/Three</Prefix>
                         </Filter>
                         <IncludedObjectVersions>All</IncludedObjectVersions>
                         <OptionalFields>
                            <Field>Size</Field>
                            <Field>LastModifiedDate</Field>
                            <Field>ETag</Field>
                            <Field>StorageClass</Field>
                            <Field>IsMultipartUploaded</Field>
                            <Field>EncryptionStatus</Field>
                         </OptionalFields>
                      </InventoryConfiguration>
                      <IsTruncated>true</IsTruncated>
                      <NextContinuationToken>aaa...</NextContinuationToken>
                   </ListInventoryConfigurationsResult>
        '''

        result = model.ListBucketInventoryResult()
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=xml_data,
            )
        )
        deserializer = [serde.deserialize_output_xmlbody]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertEqual('report1', result.list_inventory_configurations_result.inventory_configurations[0].id)
        self.assertEqual(True, result.list_inventory_configurations_result.inventory_configurations[0].is_enabled)
        self.assertEqual('CSV', result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.format)
        self.assertEqual('1000000000000000', result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.account_id)
        self.assertEqual('acs:ram::1000000000000000:role/AliyunOSSRole', result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.role_arn)
        self.assertEqual('acs:oss:::destination-bucket', result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.bucket)
        self.assertEqual('prefix1', result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.prefix)
        self.assertEqual('Daily', result.list_inventory_configurations_result.inventory_configurations[0].schedule.frequency)
        self.assertEqual('prefix/One', result.list_inventory_configurations_result.inventory_configurations[0].filter.prefix)
        self.assertEqual('All', result.list_inventory_configurations_result.inventory_configurations[0].included_object_versions)
        self.assertEqual('Size', result.list_inventory_configurations_result.inventory_configurations[0].optional_fields.fields[0])
        self.assertEqual('LastModifiedDate', result.list_inventory_configurations_result.inventory_configurations[0].optional_fields.fields[1])
        self.assertEqual('ETag', result.list_inventory_configurations_result.inventory_configurations[0].optional_fields.fields[2])
        self.assertEqual('StorageClass', result.list_inventory_configurations_result.inventory_configurations[0].optional_fields.fields[3])
        self.assertEqual('IsMultipartUploaded', result.list_inventory_configurations_result.inventory_configurations[0].optional_fields.fields[4])
        self.assertEqual('EncryptionStatus', result.list_inventory_configurations_result.inventory_configurations[0].optional_fields.fields[5])
        self.assertEqual('report2', result.list_inventory_configurations_result.inventory_configurations[1].id)
        self.assertEqual(True, result.list_inventory_configurations_result.inventory_configurations[1].is_enabled)
        self.assertEqual('CSV', result.list_inventory_configurations_result.inventory_configurations[1].destination.oss_bucket_destination.format)
        self.assertEqual('1000000000000000', result.list_inventory_configurations_result.inventory_configurations[1].destination.oss_bucket_destination.account_id)
        self.assertEqual('acs:ram::1000000000000000:role/AliyunOSSRole', result.list_inventory_configurations_result.inventory_configurations[1].destination.oss_bucket_destination.role_arn)
        self.assertEqual('acs:oss:::destination-bucket', result.list_inventory_configurations_result.inventory_configurations[1].destination.oss_bucket_destination.bucket)
        self.assertEqual('prefix2', result.list_inventory_configurations_result.inventory_configurations[1].destination.oss_bucket_destination.prefix)
        self.assertEqual('Daily', result.list_inventory_configurations_result.inventory_configurations[1].schedule.frequency)
        self.assertEqual('prefix/Two', result.list_inventory_configurations_result.inventory_configurations[1].filter.prefix)
        self.assertEqual('All', result.list_inventory_configurations_result.inventory_configurations[1].included_object_versions)
        self.assertEqual('Size', result.list_inventory_configurations_result.inventory_configurations[1].optional_fields.fields[0])
        self.assertEqual('LastModifiedDate', result.list_inventory_configurations_result.inventory_configurations[1].optional_fields.fields[1])
        self.assertEqual('ETag', result.list_inventory_configurations_result.inventory_configurations[1].optional_fields.fields[2])
        self.assertEqual('StorageClass', result.list_inventory_configurations_result.inventory_configurations[1].optional_fields.fields[3])
        self.assertEqual('IsMultipartUploaded', result.list_inventory_configurations_result.inventory_configurations[1].optional_fields.fields[4])
        self.assertEqual('EncryptionStatus', result.list_inventory_configurations_result.inventory_configurations[1].optional_fields.fields[5])
        self.assertEqual('report3', result.list_inventory_configurations_result.inventory_configurations[2].id)
        self.assertEqual(True, result.list_inventory_configurations_result.inventory_configurations[2].is_enabled)
        self.assertEqual('CSV', result.list_inventory_configurations_result.inventory_configurations[2].destination.oss_bucket_destination.format)
        self.assertEqual('1000000000000000', result.list_inventory_configurations_result.inventory_configurations[2].destination.oss_bucket_destination.account_id)
        self.assertEqual('acs:ram::1000000000000000:role/AliyunOSSRole', result.list_inventory_configurations_result.inventory_configurations[2].destination.oss_bucket_destination.role_arn)
        self.assertEqual('acs:oss:::destination-bucket', result.list_inventory_configurations_result.inventory_configurations[2].destination.oss_bucket_destination.bucket)
        self.assertEqual('prefix3', result.list_inventory_configurations_result.inventory_configurations[2].destination.oss_bucket_destination.prefix)
        self.assertEqual('Daily', result.list_inventory_configurations_result.inventory_configurations[2].schedule.frequency)
        self.assertEqual('prefix/Three', result.list_inventory_configurations_result.inventory_configurations[2].filter.prefix)
        self.assertEqual('All', result.list_inventory_configurations_result.inventory_configurations[2].included_object_versions)
        self.assertEqual('Size', result.list_inventory_configurations_result.inventory_configurations[2].optional_fields.fields[0])
        self.assertEqual('LastModifiedDate', result.list_inventory_configurations_result.inventory_configurations[2].optional_fields.fields[1])
        self.assertEqual('ETag', result.list_inventory_configurations_result.inventory_configurations[2].optional_fields.fields[2])
        self.assertEqual('StorageClass', result.list_inventory_configurations_result.inventory_configurations[2].optional_fields.fields[3])
        self.assertEqual('IsMultipartUploaded', result.list_inventory_configurations_result.inventory_configurations[2].optional_fields.fields[4])
        self.assertEqual('EncryptionStatus', result.list_inventory_configurations_result.inventory_configurations[2].optional_fields.fields[5])
        self.assertEqual(True, result.list_inventory_configurations_result.is_truncated)
        self.assertEqual('aaa...', result.list_inventory_configurations_result.next_continuation_token)


class TestDeleteBucketInventory(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DeleteBucketInventoryRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.inventory_id)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DeleteBucketInventoryRequest(
            bucket='bucketexampletest',
            inventory_id='+Mv>oah@L-',
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('+Mv>oah@L-', request.inventory_id)

    def test_serialize_request(self):
        request = model.DeleteBucketInventoryRequest(
            bucket='bucketexampletest',
            inventory_id='+Mv>oah@L-',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteBucketInventory',
            method='DELETE',
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteBucketInventory', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)
        self.assertEqual('+Mv>oah@L-', op_input.parameters.get('inventoryId'))

    def test_constructor_result(self):
        result = model.DeleteBucketInventoryResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.DeleteBucketInventoryResult()
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
