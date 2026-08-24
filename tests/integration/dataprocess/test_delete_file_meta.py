# pylint: skip-file
"""Integration tests for DeleteFileMeta operation via DataProcess client.

Aligned with Java ClientDeleteFileMetaTest:
- setUp creates a dataset, tearDown deletes it.
- testDeleteFileMeta: list the first object in the bucket, delete its file meta.
- testDeleteFileMetaWithInvalidUri: invalid URI, success or error both acceptable.
"""

from . import TestBaseDataProcess, gen_dataset_name
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.dataprocess as oss_dataprocess


class TestDeleteFileMeta(TestBaseDataProcess):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        setup_assert = cls.setup_assertions()
        cls.dfm_ds_name = gen_dataset_name()
        result = cls.dp_client.create_dataset(
            oss_dataprocess.models.CreateDatasetRequest(
                bucket=cls.dp_bucket,
                dataset_name=cls.dfm_ds_name,
            )
        )
        setup_assert.assertIsNotNone(result)
        setup_assert.assertEqual(200, result.status_code)

        # The test bucket is newly created and empty, upload a test object
        # so that listObjectsV2 can return at least one object.
        cls.first_object_key = 'test-delete-file-meta-object.jpg'
        put_result = cls.client.put_object(oss.models.PutObjectRequest(
            bucket=cls.dp_bucket,
            key=cls.first_object_key,
            body=b'hello delete file meta',
        ))
        setup_assert.assertIsNotNone(put_result)
        setup_assert.assertIn(put_result.status_code, [200, 201])

    @classmethod
    def tearDownClass(cls):
        if getattr(cls, 'dp_client', None) is not None and getattr(cls, 'dfm_ds_name', None) is not None:
            try:
                cls.dp_client.delete_dataset(
                    oss_dataprocess.models.DeleteDatasetRequest(
                        bucket=cls.dp_bucket,
                        dataset_name=cls.dfm_ds_name,
                    )
                )
            except Exception:
                pass
        super().tearDownClass()

    def test_delete_file_meta(self):
        """List the first object in the test bucket and delete its file meta."""
        # List the first object in the test bucket and use its key as the target URI
        list_result = self.client.list_objects_v2(oss.models.ListObjectsV2Request(
            bucket=self.dp_bucket,
            max_keys=1,
        ))
        self.assertIsNotNone(list_result)
        self.assertEqual(200, list_result.status_code)
        self.assertIsNotNone(list_result.contents, "bucket should contain at least one object")
        self.assertGreater(len(list_result.contents), 0, "bucket should contain at least one object")

        first_object_key = list_result.contents[0].key
        self.assertIsNotNone(first_object_key, "first object key should not be null")

        # Delete file meta for the first object
        result = self.dp_client.delete_file_meta(
            oss_dataprocess.models.DeleteFileMetaRequest(
                bucket=self.dp_bucket,
                dataset_name=self.dfm_ds_name,
                uri='oss://' + self.dp_bucket + '/' + first_object_key,
            )
        )
        self.assertIsNotNone(result)
        # Either 200 or 204 is acceptable
        self.assertIn(result.status_code, [200, 204],
                      "Expected 200 or 204 for delete_file_meta")

    def test_delete_file_meta_with_invalid_uri(self):
        """Delete file meta with invalid URI - success or error both acceptable."""
        try:
            self.dp_client.delete_file_meta(
                oss_dataprocess.models.DeleteFileMetaRequest(
                    bucket=self.dp_bucket,
                    dataset_name=self.dfm_ds_name,
                    uri='invalid-uri',
                )
            )
            # May succeed depending on server validation
        except Exception as e:
            # Expected - server may reject invalid URI format
            self.assertTrue(str(e), "Exception should have a message")
