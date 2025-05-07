# pylint: skip-file

from typing import cast
import alibabacloud_oss_v2 as oss
from . import TestIntegration, random_bucket_name


class TestOpenMetaQuery(TestIntegration):

    def test_open_meta_query(self):
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

        # open meta query
        result = self.client.open_meta_query(oss.OpenMetaQueryRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get meta query status
        result = self.client.get_meta_query_status(oss.GetMetaQueryStatusRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('Ready', result.meta_query_status.state)
        self.assertIsNotNone('2024-09-11T10:49:17.289372919+08:00')
        self.assertIsNotNone('2024-09-11T10:49:17.289372919+08:00')
        self.assertEqual('basic', result.meta_query_status.meta_query_mode)

        # do meta query
        result = self.client.do_meta_query(oss.DoMetaQueryRequest(
            bucket=bucket_name,
            meta_query=oss.MetaQuery(
                aggregations=oss.MetaQueryAggregations(
                    aggregations=[oss.MetaQueryAggregation(
                        field='Size',
                        operation='sum',
                    ), oss.MetaQueryAggregation(
                        field='Size',
                        operation='max',
                    )],
                ),
                next_token='',
                max_results=80369,
                query='{"Field": "Size","Value": "1048576","Operation": "gt"}',
                sort='Size',
                order=oss.MetaQueryOrderType.DESC,
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('Size', result.aggregations.aggregations[0].field)
        self.assertEqual('sum', result.aggregations.aggregations[0].operation)
        self.assertEqual('Size', result.aggregations.aggregations[1].field)
        self.assertEqual('max', result.aggregations.aggregations[1].operation)


        # close meta query
        result = self.client.close_meta_query(oss.CloseMetaQueryRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

    def test_meta_query_semantic(self):
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

        # open meta query
        result = self.client.open_meta_query(oss.OpenMetaQueryRequest(
            bucket=bucket_name,
            mode='semantic',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get meta query status
        result = self.client.get_meta_query_status(oss.GetMetaQueryStatusRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('Ready', result.meta_query_status.state)
        self.assertIsNotNone(result.meta_query_status.create_time)
        self.assertIsNotNone(result.meta_query_status.update_time)
        self.assertEqual('semantic', result.meta_query_status.meta_query_mode)

        # do meta query
        result = self.client.do_meta_query(oss.DoMetaQueryRequest(
            bucket=bucket_name,
            mode='semantic',
            meta_query=oss.MetaQuery(
                max_results=1000,
                query='俯瞰白雪覆盖的森林',
                order='desc',
                media_types=['image'],
                simple_query='{"Operation":"gt", "Field": "Size", "Value": "30"}',
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # close meta query
        result = self.client.close_meta_query(oss.CloseMetaQueryRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

    def test_open_meta_query_v1(self):
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

        # open meta query
        result = self.signv1_client.open_meta_query(oss.OpenMetaQueryRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get meta query status
        result = self.signv1_client.get_meta_query_status(oss.GetMetaQueryStatusRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('Ready', result.meta_query_status.state)
        self.assertIsNotNone('2024-09-11T10:49:17.289372919+08:00')
        self.assertIsNotNone('2024-09-11T10:49:17.289372919+08:00')
        self.assertEqual('basic', result.meta_query_status.meta_query_mode)

        # do meta query
        result = self.signv1_client.do_meta_query(oss.DoMetaQueryRequest(
            bucket=bucket_name,
            meta_query=oss.MetaQuery(
                aggregations=oss.MetaQueryAggregations(
                    aggregations=[oss.MetaQueryAggregation(
                        field='Size',
                        operation='sum',
                    ), oss.MetaQueryAggregation(
                        field='Size',
                        operation='max',
                    )],
                ),
                next_token='',
                max_results=80369,
                query='{"Field": "Size","Value": "1048576","Operation": "gt"}',
                sort='Size',
                order=oss.MetaQueryOrderType.DESC,
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('Size', result.aggregations.aggregations[0].field)
        self.assertEqual('sum', result.aggregations.aggregations[0].operation)
        self.assertEqual('Size', result.aggregations.aggregations[1].field)
        self.assertEqual('max', result.aggregations.aggregations[1].operation)

        # close meta query
        result = self.signv1_client.close_meta_query(oss.CloseMetaQueryRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

    def test_meta_query_semantic_v1(self):
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

        # open meta query
        result = self.signv1_client.open_meta_query(oss.OpenMetaQueryRequest(
            bucket=bucket_name,
            mode='semantic',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get meta query status
        result = self.signv1_client.get_meta_query_status(oss.GetMetaQueryStatusRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('Ready', result.meta_query_status.state)
        self.assertIsNotNone(result.meta_query_status.create_time)
        self.assertIsNotNone(result.meta_query_status.update_time)
        self.assertEqual('semantic', result.meta_query_status.meta_query_mode)

        # do meta query
        result = self.signv1_client.do_meta_query(oss.DoMetaQueryRequest(
            bucket=bucket_name,
            mode='semantic',
            meta_query=oss.MetaQuery(
                max_results=1000,
                query='俯瞰白雪覆盖的森林',
                order='desc',
                media_types=['image'],
                simple_query='{"Operation":"gt", "Field": "Size", "Value": "30"}',
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # close meta query
        result = self.signv1_client.close_meta_query(oss.CloseMetaQueryRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

    def test_open_meta_query_fail(self):
        # create bucket
        bucket_name = random_bucket_name()
        self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))

        # open meta query
        try:
            self.invalid_client.open_meta_query(oss.OpenMetaQueryRequest(
                bucket=bucket_name,
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)


        # get meta query status
        try:
            self.invalid_client.get_meta_query_status(oss.GetMetaQueryStatusRequest(
                bucket=bucket_name,
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        # do meta query
        try:
            self.invalid_client.do_meta_query(oss.DoMetaQueryRequest(
                bucket=bucket_name,
                meta_query=oss.MetaQuery(
                    aggregations=oss.MetaQueryAggregations(
                        aggregations=[oss.MetaQueryAggregation(
                            field='test_field',
                            operation='test_operation',
                        ), oss.MetaQueryAggregation(
                            field='test_field',
                            operation='test_operation',
                        )],
                    ),
                    next_token='test_next_token',
                    max_results=22044,
                    query='test_query',
                    sort='test_sort',
                    order=oss.MetaQueryOrderType.ASC,
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


        # close meta query
        try:
            self.invalid_client.close_meta_query(oss.CloseMetaQueryRequest(
                bucket=bucket_name,
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)


    def test_open_meta_query_semantic_fail(self):
        # create bucket
        bucket_name = random_bucket_name()
        self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))

        # open meta query
        try:
            self.invalid_client.open_meta_query(oss.OpenMetaQueryRequest(
                bucket=bucket_name,
                mode='semantic',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)


        # get meta query status
        try:
            self.invalid_client.get_meta_query_status(oss.GetMetaQueryStatusRequest(
                bucket=bucket_name,
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        # do meta query
        try:
            self.invalid_client.do_meta_query(oss.DoMetaQueryRequest(
                bucket=bucket_name,
                mode='semantic',
                meta_query=oss.MetaQuery(
                    max_results=1000,
                    query='俯瞰白雪覆盖的森林',
                    order='desc',
                    media_types=['image'],
                    simple_query='{"Operation":"gt", "Field": "Size", "Value": "30"}',
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


        # close meta query
        try:
            self.invalid_client.close_meta_query(oss.CloseMetaQueryRequest(
                bucket=bucket_name,
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)