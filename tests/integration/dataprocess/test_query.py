# pylint: skip-file
"""Integration tests for SimpleQuery and SemanticQuery operations via dataprocess Client.

Aligned with Java ClientQueryTest.
"""

import base64
import time

from . import TestBaseDataProcess, USER_ID
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.dataprocess as oss_dataprocess

# A tiny valid 1x1 JPEG, avoids checking binary fixtures into the repo.
_TINY_JPEG_B64 = (
    '/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0a'
    'HBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/wAALCAABAAEBAREA/8QAFAABAAAAAAAA'
    'AAAAAAAAAAAAAv/EABQQAQAAAAAAAAAAAAAAAAAAAAD/2gAIAQEAAD8AVN//2Q=='
)


class TestQuery(TestBaseDataProcess):

    def test_simple_query_basic(self):
        client = self.dp_client

        query = oss_dataprocess.models.SimpleQuery(
            field='Filename',
            value='test-media',
            operation='prefix',
        )

        result = client.simple_query(
            oss_dataprocess.models.SimpleQueryRequest(
                bucket=self.dp_bucket,
                dataset_name=self.query_dataset_name,
                query=query.to_parameter_value(),
                max_results=10,
            )
        )

        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        # Verify files are returned
        self.assertIsNotNone(result.files, 'files should not be null')
        self.assertIsNotNone(result.files.file)
        self.assertTrue(len(result.files.file) > 0, 'files should not be empty')

        f = result.files.file[0]
        self.assertIsNotNone(f.uri, 'URI should not be null')
        self.assertIsNotNone(f.filename, 'Filename should not be null')
        self.assertIsNotNone(f.media_type, 'MediaType should not be null')
        self.assertIsNotNone(f.content_type, 'ContentType should not be null')
        self.assertIsNotNone(f.size, 'Size should not be null')
        self.assertGreater(f.size, 0, 'Size should be > 0')

        # Verify labels parsing (wrapper: Labels -> Label).
        # Labels come from IMM AI analysis on real image content, so a fresh
        # test bucket may have none; validate the structure only when present.
        for file in result.files.file:
            if file.labels is not None and file.labels.label:
                label = file.labels.label[0]
                self.assertIsNotNone(label.label_name, 'Label.labelName should not be null')
                break

    def test_simple_query_with_aggregations(self):
        client = self.dp_client

        query = oss_dataprocess.models.SimpleQuery(
            field='Filename',
            value='test-media',
            operation='prefix',
        )

        aggregation = oss_dataprocess.models.Aggregation(
            field='Size',
            operation='sum',
        )

        result = client.simple_query(
            oss_dataprocess.models.SimpleQueryRequest(
                bucket=self.dp_bucket,
                dataset_name=self.query_dataset_name,
                query=query.to_parameter_value(),
                aggregations=oss_dataprocess.models.MetaQueryAggregations(
                    aggregation=[aggregation],
                ).to_parameter_value(),
                max_results=10,
            )
        )

        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        # Verify aggregations
        self.assertIsNotNone(result.aggregations, 'aggregations should not be null')
        self.assertIsNotNone(result.aggregations.aggregation)
        self.assertTrue(len(result.aggregations.aggregation) > 0,
                        'aggregations should not be empty')

        agg = result.aggregations.aggregation[0]
        self.assertEqual('Size', agg.field)
        self.assertEqual('sum', agg.operation)
        self.assertIsNotNone(agg.value, 'aggregation value should not be null')

    def test_simple_query_with_sort_and_order(self):
        client = self.dp_client

        query = oss_dataprocess.models.SimpleQuery(
            field='Filename',
            value='test-media',
            operation='prefix',
        )

        result = client.simple_query(
            oss_dataprocess.models.SimpleQueryRequest(
                bucket=self.dp_bucket,
                dataset_name=self.query_dataset_name,
                query=query.to_parameter_value(),
                sort='Filename',
                order='asc',
                max_results=10,
                without_total_hits=False,
            )
        )

        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        self.assertIsNotNone(result.files, 'files should not be null')
        self.assertIsNotNone(result.files.file)
        self.assertTrue(len(result.files.file) > 0, 'files should not be empty')

        # Verify sorted by Filename ascending
        files = result.files.file
        for i in range(1, len(files)):
            prev = files[i - 1].filename
            curr = files[i].filename
            self.assertLessEqual(prev, curr,
                                 'files should be sorted by Filename asc: ' + prev + ' <= ' + curr)

    def test_simple_query_with_fields(self):
        client = self.dp_client

        query = oss_dataprocess.models.SimpleQuery(
            field='Filename',
            value='test-media',
            operation='prefix',
        )

        result = client.simple_query(
            oss_dataprocess.models.SimpleQueryRequest(
                bucket=self.dp_bucket,
                dataset_name=self.query_dataset_name,
                query=query.to_parameter_value(),
                with_fields=oss_dataprocess.models.WithFields(
                    with_field=['Filename', 'Size', 'ContentType'],
                ).to_parameter_value(),
                max_results=10,
            )
        )

        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        self.assertIsNotNone(result.files, 'files should not be null')
        self.assertIsNotNone(result.files.file)
        self.assertTrue(len(result.files.file) > 0, 'files should not be empty')

        # Verify requested fields are populated
        f = result.files.file[0]
        self.assertIsNotNone(f.filename, 'Filename should not be null')
        self.assertIsNotNone(f.size, 'Size should not be null')
        self.assertIsNotNone(f.content_type, 'ContentType should not be null')

    # Semantic query matches against image content analyzed by the multimodal
    # embedding model. The uploaded placeholder JPEG has no real content, so
    # these cases are disabled by default. If TEST_DATAPROCESS_BUCKET already
    # contains snow-scene images, uncomment them to enable the cases.
    # def test_semantic_query_basic(self):
    #     client = self.dp_client
    #
    #     result = client.semantic_query(
    #         oss_dataprocess.models.SemanticQueryRequest(
    #             bucket=self.dp_bucket,
    #             dataset_name=self.query_dataset_name,
    #             query='雪景',
    #             max_results=10,
    #         )
    #     )
    #
    #     self.assertIsNotNone(result)
    #     self.assertEqual(200, result.status_code)
    #
    #     self.assertIsNotNone(result.files, 'files should not be null')
    #     self.assertIsNotNone(result.files.file)
    #     self.assertTrue(len(result.files.file) > 0, 'files should not be empty')
    #
    #     f = result.files.file[0]
    #     self.assertIsNotNone(f.uri, 'URI should not be null')
    #     self.assertIsNotNone(f.filename, 'Filename should not be null')
    #     self.assertIsNotNone(f.media_type, 'MediaType should not be null')
    #     self.assertIsNotNone(f.size, 'Size should not be null')
    #
    # def test_semantic_query_with_media_types(self):
    #     client = self.dp_client
    #
    #     result = client.semantic_query(
    #         oss_dataprocess.models.SemanticQueryRequest(
    #             bucket=self.dp_bucket,
    #             dataset_name=self.query_dataset_name,
    #             query='雪景',
    #             media_types=oss_dataprocess.models.MediaTypes(
    #                 media_type=['image'],
    #             ).to_parameter_value(),
    #             with_fields=oss_dataprocess.models.WithFields(
    #                 with_field=['Filename', 'Size', 'MediaType'],
    #             ).to_parameter_value(),
    #             max_results=10,
    #         )
    #     )
    #
    #     self.assertIsNotNone(result)
    #     self.assertEqual(200, result.status_code)
    #
    #     self.assertIsNotNone(result.files, 'files should not be null')
    #     self.assertIsNotNone(result.files.file)
    #     self.assertTrue(len(result.files.file) > 0, 'files should not be empty')
    #
    #     # Verify all returned files are images
    #     for f in result.files.file:
    #         self.assertEqual('image', f.media_type, 'MediaType should be image')

    # ====================================================================================

    ROUTING_TAG_KEY = 'routing-dataset'
    OBJECT_KEY_PREFIX = 'test-query-obj-'
    SAMPLE_KEYS = [
        OBJECT_KEY_PREFIX + '1.jpg',
        OBJECT_KEY_PREFIX + '2.jpg',
        OBJECT_KEY_PREFIX + '3.jpg',
    ]
    # Objects for the test-media prefix simple-query cases.
    MEDIA_KEY_PREFIX = 'test-media-'
    MEDIA_KEYS = [
        MEDIA_KEY_PREFIX + '1.jpg',
        MEDIA_KEY_PREFIX + '2.jpg',
        MEDIA_KEY_PREFIX + '3.jpg',
    ]
    INDEX_WAIT_SECONDS = 20

    @classmethod
    def setUpClass(cls):
        """Uploads all objects the query cases depend on, so the tests are
        self-contained instead of relying on pre-existing bucket data.

        MetaQuery is already opened in semantic mode by TestBaseDataProcess.setUpClass
        so we do NOT re-open it here. No createDataset is called either: the default
        dataset oss_<uid>_<bucket> is implicitly maintained by OSS.
        """
        super().setUpClass()

        cls.query_dataset_name = 'oss_' + USER_ID + '_' + cls.dp_bucket

        # Upload sample JPEG objects carrying the routing tag so that they are routed
        # into the default dataset.
        body = base64.b64decode(_TINY_JPEG_B64)
        for key in cls.SAMPLE_KEYS:
            cls.client.put_object(oss.models.PutObjectRequest(
                bucket=cls.dp_bucket,
                key=key,
                tagging=cls.ROUTING_TAG_KEY + '=' + cls.query_dataset_name,
                body=body,
            ))

        # Upload objects with the test-media prefix for the simple-query cases.
        for key in cls.MEDIA_KEYS:
            cls.client.put_object(oss.models.PutObjectRequest(
                bucket=cls.dp_bucket,
                key=key,
                body=body,
            ))

        # Wait briefly for indexing to take effect.
        time.sleep(cls.INDEX_WAIT_SECONDS)

    @classmethod
    def tearDownClass(cls):
        # Delete all uploaded sample objects. The default dataset is OSS-managed
        # and intentionally preserved across test runs.
        for key in list(cls.SAMPLE_KEYS) + list(cls.MEDIA_KEYS):
            try:
                cls.client.delete_object(oss.models.DeleteObjectRequest(
                    bucket=cls.dp_bucket,
                    key=key,
                ))
            except Exception:
                pass
        super().tearDownClass()

    def test_simple_query_by_prefix(self):
        """Simple-query the locally-uploaded JPEG samples by Filename prefix
        against the default dataset oss_<uid>_<bucket>."""
        client = self.dp_client

        query = oss_dataprocess.models.SimpleQuery(
            field='Filename',
            value=self.OBJECT_KEY_PREFIX,
            operation='prefix',
        )

        result = client.simple_query(
            oss_dataprocess.models.SimpleQueryRequest(
                bucket=self.dp_bucket,
                dataset_name=self.query_dataset_name,
                query=query.to_parameter_value(),
                max_results=10,
            )
        )

        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        self.assertIsNotNone(result.files, 'files should not be null')
        self.assertIsNotNone(result.files.file)
        self.assertTrue(len(result.files.file) > 0,
                        'expected uploaded objects to be queryable')

        # Every uploaded key should be present among the returned files.
        filenames = []
        for f in result.files.file:
            self.assertIsNotNone(f.uri, 'URI should not be null')
            self.assertIsNotNone(f.filename, 'Filename should not be null')
            self.assertIsNotNone(f.size, 'Size should not be null')
            filenames.append(f.filename)
        for key in self.SAMPLE_KEYS:
            self.assertIn(key, filenames,
                          'uploaded key should appear in query results: ' + key)

    def test_simple_query_compound_with_raw_json(self):
        """Exercise the raw-JSON form of SimpleQueryRequest.query with a
        compound (Operation=and) condition."""
        client = self.dp_client

        raw_json = ('{"Operation":"and","SubQueries":['
                    '{"Field":"Filename","Operation":"prefix","Value":"' + self.OBJECT_KEY_PREFIX + '"},'
                    '{"Field":"Size","Operation":"gt","Value":"0"}'
                    ']}')

        result = client.simple_query(
            oss_dataprocess.models.SimpleQueryRequest(
                bucket=self.dp_bucket,
                dataset_name=self.query_dataset_name,
                query=raw_json,
                max_results=10,
            )
        )

        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.files, 'files should not be null')
        self.assertIsNotNone(result.files.file)
        self.assertTrue(len(result.files.file) > 0,
                        'compound query should match uploaded objects (size > 0 with given prefix)')
