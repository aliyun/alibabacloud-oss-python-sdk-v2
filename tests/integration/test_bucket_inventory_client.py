# pylint: skip-file

from typing import cast
import alibabacloud_oss_v2 as oss
from . import TestIntegration, random_bucket_name, USER_ID, RAM_ROLE_ARN, random_lowstr


class TestBucketInventory(TestIntegration):

    def test_bucket_inventory(self):
        # create bucket
        bucket_name = random_bucket_name()
        result = self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        inventory_id = 'test-oss-' + random_lowstr(6)
        # put bucket inventory
        result = self.client.put_bucket_inventory(oss.PutBucketInventoryRequest(
            bucket=bucket_name,
            inventory_id=inventory_id,
            inventory_configuration=oss.InventoryConfiguration(
                included_object_versions='All',
                optional_fields=oss.OptionalFields(
                    fields=[oss.InventoryOptionalFieldType.IS_MULTIPART_UPLOADED, oss.InventoryOptionalFieldType.ENCRYPTION_STATUS],
                ),
                id=inventory_id,
                is_enabled=True,
                destination=oss.InventoryDestination(
                    oss_bucket_destination=oss.InventoryOSSBucketDestination(
                        format=oss.InventoryFormatType.CSV,
                        account_id=USER_ID,
                        role_arn=RAM_ROLE_ARN,
                        bucket='acs:oss:::'+bucket_name,
                        prefix='aaa',
                        encryption=oss.InventoryEncryption(
                            sse_kms=oss.SSEKMS(
                                key_id='GGUIFHBKJNFkjghug',
                            ),
                        ),
                    ),
                ),
                schedule=oss.InventorySchedule(
                    frequency=oss.InventoryFrequencyType.DAILY,
                ),
                filter=oss.InventoryFilter(
                    lower_size_bound=1024,
                    upper_size_bound=1048576,
                    storage_class='ColdArchive',
                    prefix='aaa',
                    last_modify_begin_time_stamp=1637883649,
                    last_modify_end_time_stamp=1638347592,
                ),
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket inventory
        result = self.client.get_bucket_inventory(oss.GetBucketInventoryRequest(
            bucket=bucket_name,
            inventory_id=inventory_id,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('All', result.inventory_configuration.included_object_versions)
        self.assertEqual([oss.InventoryOptionalFieldType.IS_MULTIPART_UPLOADED, oss.InventoryOptionalFieldType.ENCRYPTION_STATUS], result.inventory_configuration.optional_fields.fields)
        self.assertEqual(inventory_id, result.inventory_configuration.id)
        self.assertEqual(True, result.inventory_configuration.is_enabled)
        self.assertEqual(oss.InventoryFormatType.CSV, result.inventory_configuration.destination.oss_bucket_destination.format)
        self.assertEqual(USER_ID, result.inventory_configuration.destination.oss_bucket_destination.account_id)
        self.assertEqual(RAM_ROLE_ARN, result.inventory_configuration.destination.oss_bucket_destination.role_arn)
        self.assertEqual('acs:oss:::' + bucket_name, result.inventory_configuration.destination.oss_bucket_destination.bucket)
        self.assertEqual('aaa', result.inventory_configuration.destination.oss_bucket_destination.prefix)
        self.assertEqual(oss.InventoryFrequencyType.DAILY, result.inventory_configuration.schedule.frequency)
        self.assertEqual(1024, result.inventory_configuration.filter.lower_size_bound)
        self.assertEqual(1048576, result.inventory_configuration.filter.upper_size_bound)
        self.assertEqual('ColdArchive', result.inventory_configuration.filter.storage_class)
        self.assertEqual('aaa', result.inventory_configuration.filter.prefix)
        self.assertEqual(1637883649, result.inventory_configuration.filter.last_modify_begin_time_stamp)
        self.assertEqual(1638347592, result.inventory_configuration.filter.last_modify_end_time_stamp)

        # list bucket inventory
        result = self.client.list_bucket_inventory(oss.ListBucketInventoryRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('All', result.list_inventory_configurations_result.inventory_configurations[0].included_object_versions)
        self.assertEqual([oss.InventoryOptionalFieldType.IS_MULTIPART_UPLOADED, oss.InventoryOptionalFieldType.ENCRYPTION_STATUS], result.list_inventory_configurations_result.inventory_configurations[0].optional_fields.fields)
        self.assertEqual(inventory_id, result.list_inventory_configurations_result.inventory_configurations[0].id)
        self.assertEqual(True, result.list_inventory_configurations_result.inventory_configurations[0].is_enabled)
        self.assertEqual(oss.InventoryFormatType.CSV, result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.format)
        self.assertEqual(USER_ID, result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.account_id)
        self.assertEqual(RAM_ROLE_ARN, result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.role_arn)
        self.assertEqual('acs:oss:::' + bucket_name, result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.bucket)
        self.assertEqual('aaa', result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.prefix)
        self.assertEqual(oss.InventoryFrequencyType.DAILY, result.list_inventory_configurations_result.inventory_configurations[0].schedule.frequency)
        self.assertEqual(1024, result.list_inventory_configurations_result.inventory_configurations[0].filter.lower_size_bound)
        self.assertEqual(1048576, result.list_inventory_configurations_result.inventory_configurations[0].filter.upper_size_bound)
        self.assertEqual('ColdArchive', result.list_inventory_configurations_result.inventory_configurations[0].filter.storage_class)
        self.assertEqual('aaa', result.list_inventory_configurations_result.inventory_configurations[0].filter.prefix)
        self.assertEqual(1637883649, result.list_inventory_configurations_result.inventory_configurations[0].filter.last_modify_begin_time_stamp)
        self.assertEqual(1638347592, result.list_inventory_configurations_result.inventory_configurations[0].filter.last_modify_end_time_stamp)

        # delete bucket inventory
        result = self.client.delete_bucket_inventory(oss.DeleteBucketInventoryRequest(
            bucket=bucket_name,
            inventory_id=inventory_id,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

    def test_bucket_inventory_v1(self):
        # create bucket
        bucket_name = random_bucket_name()
        result = self.signv1_client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        inventory_id = 'test-oss-' + random_lowstr(6)
        # put bucket inventory
        result = self.signv1_client.put_bucket_inventory(oss.PutBucketInventoryRequest(
            bucket=bucket_name,
            inventory_id=inventory_id,
            inventory_configuration=oss.InventoryConfiguration(
                included_object_versions='All',
                optional_fields=oss.OptionalFields(
                    fields=[oss.InventoryOptionalFieldType.IS_MULTIPART_UPLOADED, oss.InventoryOptionalFieldType.ENCRYPTION_STATUS],
                ),
                id=inventory_id,
                is_enabled=True,
                destination=oss.InventoryDestination(
                    oss_bucket_destination=oss.InventoryOSSBucketDestination(
                        format=oss.InventoryFormatType.CSV,
                        account_id=USER_ID,
                        role_arn=RAM_ROLE_ARN,
                        bucket='acs:oss:::'+bucket_name,
                        prefix='aaa',
                        encryption=oss.InventoryEncryption(
                            sse_kms=oss.SSEKMS(
                                key_id='GGUIFHBKJNFkjghug',
                            ),
                        ),
                    ),
                ),
                schedule=oss.InventorySchedule(
                    frequency=oss.InventoryFrequencyType.DAILY,
                ),
                filter=oss.InventoryFilter(
                    lower_size_bound=1024,
                    upper_size_bound=1048576,
                    storage_class='ColdArchive',
                    prefix='aaa',
                    last_modify_begin_time_stamp=1637883649,
                    last_modify_end_time_stamp=1638347592,
                ),
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))


        # get bucket inventory
        result = self.signv1_client.get_bucket_inventory(oss.GetBucketInventoryRequest(
            bucket=bucket_name,
            inventory_id=inventory_id,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('All', result.inventory_configuration.included_object_versions)
        self.assertEqual([oss.InventoryOptionalFieldType.IS_MULTIPART_UPLOADED, oss.InventoryOptionalFieldType.ENCRYPTION_STATUS], result.inventory_configuration.optional_fields.fields)
        self.assertEqual(inventory_id, result.inventory_configuration.id)
        self.assertEqual(True, result.inventory_configuration.is_enabled)
        self.assertEqual(oss.InventoryFormatType.CSV, result.inventory_configuration.destination.oss_bucket_destination.format)
        self.assertEqual(USER_ID, result.inventory_configuration.destination.oss_bucket_destination.account_id)
        self.assertEqual(RAM_ROLE_ARN, result.inventory_configuration.destination.oss_bucket_destination.role_arn)
        self.assertEqual('acs:oss:::' + bucket_name, result.inventory_configuration.destination.oss_bucket_destination.bucket)
        self.assertEqual('aaa', result.inventory_configuration.destination.oss_bucket_destination.prefix)
        self.assertEqual(oss.InventoryFrequencyType.DAILY, result.inventory_configuration.schedule.frequency)
        self.assertEqual(1024, result.inventory_configuration.filter.lower_size_bound)
        self.assertEqual(1048576, result.inventory_configuration.filter.upper_size_bound)
        self.assertEqual('ColdArchive', result.inventory_configuration.filter.storage_class)
        self.assertEqual('aaa', result.inventory_configuration.filter.prefix)
        self.assertEqual(1637883649, result.inventory_configuration.filter.last_modify_begin_time_stamp)
        self.assertEqual(1638347592, result.inventory_configuration.filter.last_modify_end_time_stamp)

        # list bucket inventory
        result = self.signv1_client.list_bucket_inventory(oss.ListBucketInventoryRequest(
            bucket=bucket_name,
            continuation_token='',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('All', result.list_inventory_configurations_result.inventory_configurations[0].included_object_versions)
        self.assertEqual([oss.InventoryOptionalFieldType.IS_MULTIPART_UPLOADED, oss.InventoryOptionalFieldType.ENCRYPTION_STATUS], result.list_inventory_configurations_result.inventory_configurations[0].optional_fields.fields)
        self.assertEqual(inventory_id, result.list_inventory_configurations_result.inventory_configurations[0].id)
        self.assertEqual(True, result.list_inventory_configurations_result.inventory_configurations[0].is_enabled)
        self.assertEqual(oss.InventoryFormatType.CSV, result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.format)
        self.assertEqual(USER_ID, result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.account_id)
        self.assertEqual(RAM_ROLE_ARN, result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.role_arn)
        self.assertEqual('acs:oss:::' + bucket_name, result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.bucket)
        self.assertEqual('aaa', result.list_inventory_configurations_result.inventory_configurations[0].destination.oss_bucket_destination.prefix)
        self.assertEqual(oss.InventoryFrequencyType.DAILY, result.list_inventory_configurations_result.inventory_configurations[0].schedule.frequency)
        self.assertEqual(1024, result.list_inventory_configurations_result.inventory_configurations[0].filter.lower_size_bound)
        self.assertEqual(1048576, result.list_inventory_configurations_result.inventory_configurations[0].filter.upper_size_bound)
        self.assertEqual('ColdArchive', result.list_inventory_configurations_result.inventory_configurations[0].filter.storage_class)
        self.assertEqual('aaa', result.list_inventory_configurations_result.inventory_configurations[0].filter.prefix)
        self.assertEqual(1637883649, result.list_inventory_configurations_result.inventory_configurations[0].filter.last_modify_begin_time_stamp)
        self.assertEqual(1638347592, result.list_inventory_configurations_result.inventory_configurations[0].filter.last_modify_end_time_stamp)

        # delete bucket inventory
        result = self.signv1_client.delete_bucket_inventory(oss.DeleteBucketInventoryRequest(
            bucket=bucket_name,
            inventory_id=inventory_id,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

    def test_bucket_inventory_fail(self):
        # create bucket
        bucket_name = random_bucket_name()
        self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))

        # put bucket inventory
        try:
            self.invalid_client.put_bucket_inventory(oss.PutBucketInventoryRequest(
                bucket=bucket_name,
                inventory_id='inventory_id',
                inventory_configuration=oss.InventoryConfiguration(
                    included_object_versions='All',
                    optional_fields=oss.OptionalFields(
                        fields=[oss.InventoryOptionalFieldType.IS_MULTIPART_UPLOADED, oss.InventoryOptionalFieldType.ENCRYPTION_STATUS],
                    ),
                    id='inventory_id',
                    is_enabled=True,
                    destination=oss.InventoryDestination(
                        oss_bucket_destination=oss.InventoryOSSBucketDestination(
                            format=oss.InventoryFormatType.CSV,
                            account_id=USER_ID,
                            role_arn=RAM_ROLE_ARN,
                            bucket='acs:oss:::' + bucket_name,
                            prefix='aaa',
                            encryption=oss.InventoryEncryption(
                                sse_kms=oss.SSEKMS(
                                    key_id='GGUIFHBKJNFkjghug',
                                ),
                            ),
                        ),
                    ),
                    schedule=oss.InventorySchedule(
                        frequency=oss.InventoryFrequencyType.DAILY,
                    ),
                    filter=oss.InventoryFilter(
                        lower_size_bound=1024,
                        upper_size_bound=1048576,
                        storage_class='ColdArchive',
                        prefix='aaa',
                        last_modify_begin_time_stamp=1637883649,
                        last_modify_end_time_stamp=1638347592,
                    ),
                ),
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        # get bucket inventory
        try:
            self.invalid_client.get_bucket_inventory(oss.GetBucketInventoryRequest(
                bucket=bucket_name,
                inventory_id='D3<y2N_Kx)',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        # delete bucket inventory
        try:
            self.invalid_client.delete_bucket_inventory(oss.DeleteBucketInventoryRequest(
                bucket=bucket_name,
                inventory_id='+Mv>oah@L-',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        # list bucket inventory
        try:
            self.invalid_client.list_bucket_inventory(oss.ListBucketInventoryRequest(
                bucket=bucket_name,
                continuation_token='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)
