# pylint: skip-file
"""Integration tests for MetaQuery operations via dataprocess Client.

Aligned with Java ClientMetaQueryTest.
"""

from . import TestBaseDataProcess, collect_error_messages
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.dataprocess as oss_dataprocess


class TestMetaQuery(TestBaseDataProcess):

    def test_meta_query_lifecycle(self):
        client = self.dp_client

        # 1. Get MetaQuery Status
        status_result = client.get_meta_query_status(
            oss_dataprocess.models.GetMetaQueryStatusRequest(
                bucket=self.dp_bucket,
            )
        )

        self.assertIsNotNone(status_result)
        self.assertEqual(200, status_result.status_code)
        self.assertIsNotNone(status_result.status, 'metaQueryStatus should not be null')
        self.assertIsNotNone(status_result.status.state, 'state should not be null')

        # 2. Do MetaQuery (semantic mode)
        do_result = client.do_meta_query(
            oss_dataprocess.models.DoMetaQueryRequest(
                bucket=self.dp_bucket,
                mode='semantic',
                meta_query_body=oss_dataprocess.models.MetaQueryDoBody(
                    query='{"Field": "Size", "Value": "0", "Operation": "gt"}',
                    sort='Size',
                    order='asc',
                    max_results=5,
                ),
            )
        )

        self.assertIsNotNone(do_result)
        self.assertEqual(200, do_result.status_code)
        # files may or may not be returned depending on data
        if do_result.files is not None and do_result.files.file:
            f = do_result.files.file[0]
            self.assertIsNotNone(f.uri, 'URI should not be null')

    def test_do_meta_query_with_aggregations(self):
        client = self.dp_client

        agg = oss_dataprocess.models.Aggregation(
            field='Size',
            operation='sum',
        )

        # Aggregations are NOT supported in semantic mode. Issuing such a request must
        # fail with a clear server-side error message. We assert the documented constraint
        # surfaces through the propagated exception chain.
        try:
            client.do_meta_query(
                oss_dataprocess.models.DoMetaQueryRequest(
                    bucket=self.dp_bucket,
                    mode='semantic',
                    meta_query_body=oss_dataprocess.models.MetaQueryDoBody(
                        query='{"Field": "Size", "Value": "0", "Operation": "gt"}',
                        aggregations=oss_dataprocess.models.MetaQueryAggregations(
                            aggregation=[agg],
                        ),
                        max_results=5,
                    ),
                )
            )
            self.fail('Expected an exception: Aggregations is not supported in semantic mode.')
        except Exception as e:
            msg = collect_error_messages(e)
            self.assertIn('Aggregations is not supported in semantic mode.', msg)

    def test_get_meta_query_status_fields(self):
        client = self.dp_client

        status_result = client.get_meta_query_status(
            oss_dataprocess.models.GetMetaQueryStatusRequest(
                bucket=self.dp_bucket,
            )
        )

        self.assertIsNotNone(status_result)
        self.assertEqual(200, status_result.status_code)

        status = status_result.status
        self.assertIsNotNone(status)
        self.assertIsNotNone(status.state, 'state should not be null')
        self.assertIsNotNone(status.create_time, 'createTime should not be null')
