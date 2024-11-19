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
                            sse_oss='+-HnP#AGMt',
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
        # self.assertEqual(bucket_name, result.bucket)
        # self.assertEqual(inventory_id, result.inventory_id)
        # self.assertEqual('All', result.inventory_configuration.included_object_versions)
        # self.assertEqual([oss.InventoryOptionalFieldType.IS_MULTIPART_UPLOADED, oss.InventoryOptionalFieldType.ENCRYPTION_STATUS], result.inventory_configuration.optional_fields.fields)
        # self.assertEqual(inventory_id, result.inventory_configuration.id)
        # self.assertEqual(True, result.inventory_configuration.is_enabled)
        # self.assertEqual(oss.InventoryFormatType.CSV, result.inventory_configuration.destination.oss_bucket_destination.format)
        # self.assertEqual(USER_ID, result.inventory_configuration.destination.oss_bucket_destination.account_id)
        # self.assertEqual(RAM_ROLE_ARN, result.inventory_configuration.destination.oss_bucket_destination.role_arn)
        # self.assertEqual('acs:oss:::' + bucket_name, result.inventory_configuration.destination.oss_bucket_destination.bucket)
        # self.assertEqual('aaa', result.inventory_configuration.destination.oss_bucket_destination.prefix)
        # self.assertEqual('GGUIFHBKJNFkjghug', result.inventory_configuration.destination.oss_bucket_destination.encryption.sse_kms.key_id)
        # self.assertEqual('+-HnP#AGMt', result.inventory_configuration.destination.oss_bucket_destination.encryption.sse_oss)
        # self.assertEqual(oss.InventoryFrequencyType.DAILY, result.inventory_configuration.schedule.frequency)
        # self.assertEqual(1024, result.inventory_configuration.filter.lower_size_bound)
        # self.assertEqual(1048576, result.inventory_configuration.filter.upper_size_bound)
        # self.assertEqual('ColdArchive', result.inventory_configuration.filter.storage_class)
        # self.assertEqual('aaa', result.inventory_configuration.filter.prefix)
        # self.assertEqual(1637883649, result.inventory_configuration.filter.last_modify_begin_time_stamp)
        # self.assertEqual(1638347592, result.inventory_configuration.filter.last_modify_end_time_stamp)



        # get bucket inventory

        # delete bucket inventory

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
                        bucket='acs:oss:::' + bucket_name,
                        prefix='aaa',
                        encryption=oss.InventoryEncryption(
                            sse_kms=oss.SSEKMS(
                                key_id='GGUIFHBKJNFkjghug',
                            ),
                            sse_oss='+-HnP#AGMt',
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

        # delete bucket inventory

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
                inventory_id='SNKsc:Wj|s',
                inventory_configuration=oss.InventoryConfiguration(
                    included_object_versions='a-8|zg/5q*',
                    optional_fields=oss.OptionalFields(
                        fields=[oss.InventoryOptionalFieldType.E_TAG, oss.InventoryOptionalFieldType.E_TAG],
                    ),
                    id='0022012****',
                    is_enabled=True,
                    destination=oss.InventoryDestination(
                        oss_bucket_destination=oss.InventoryOSSBucketDestination(
                            format=oss.InventoryFormatType.CSV,
                            account_id='PMCl7H&U&T',
                            role_arn='k.G_(r\$ZR',
                            bucket=bucket_name,
                            prefix='aaa',
                            encryption=oss.InventoryEncryption(
                                sse_kms=oss.SSEKMS(
                                    key_id=':qb\KdTDlu',
                                ),
                                sse_oss='+-HnP#AGMt',
                            ),
                        ),
                    ),
                    schedule=oss.InventorySchedule(
                        frequency=oss.InventoryFrequencyType.DAILY,
                    ),
                    filter=oss.InventoryFilter(
                        lower_size_bound=53305,
                        upper_size_bound=8328,
                        storage_class='ColdArchive',
                        prefix='aaa',
                        last_modify_begin_time_stamp=19696,
                        last_modify_end_time_stamp=44727,
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
