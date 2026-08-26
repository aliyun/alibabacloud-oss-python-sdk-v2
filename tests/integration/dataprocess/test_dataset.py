# pylint: skip-file
"""Integration tests for Dataset CRUD operations via dataprocess Client.

Aligned with Java ClientDatasetTest.
"""

import time

from . import TestBaseDataProcess, gen_dataset_name, find_service_error
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.dataprocess as oss_dataprocess


class TestDataset(TestBaseDataProcess):

    def test_dataset_lifecycle(self):
        client = self.dp_client
        ds_name = gen_dataset_name()

        # 1. Create dataset
        create_result = client.create_dataset(
            oss_dataprocess.models.CreateDatasetRequest(
                bucket=self.dp_bucket,
                dataset_name=ds_name,
                workflow_parameters=[
                    oss_dataprocess.models.WorkflowParameter(
                        name='ImageInsightEnable',
                        value='True',
                    ),
                ],
                description='integration test dataset',
            )
        )

        self.assertIsNotNone(create_result)
        self.assertEqual(200, create_result.status_code)
        self.assertIsNotNone(create_result.dataset)
        self.assertEqual(ds_name, create_result.dataset.dataset_name)
        self.assertEqual(1, len(create_result.dataset.workflow_parameters.workflow_parameters))
        self.assertEqual('ImageInsightEnable',
                         create_result.dataset.workflow_parameters.workflow_parameters[0].name)
        self.assertEqual('True',
                         create_result.dataset.workflow_parameters.workflow_parameters[0].value)

        try:
            # 2. Get dataset
            get_result = client.get_dataset(
                oss_dataprocess.models.GetDatasetRequest(
                    bucket=self.dp_bucket,
                    dataset_name=ds_name,
                )
            )

            self.assertIsNotNone(get_result)
            self.assertEqual(200, get_result.status_code)
            self.assertIsNotNone(get_result.dataset)
            self.assertEqual(ds_name, get_result.dataset.dataset_name)
            self.assertEqual('integration test dataset', get_result.dataset.description)
            self.assertEqual(1, len(get_result.dataset.workflow_parameters.workflow_parameters))
            self.assertEqual('ImageInsightEnable',
                             get_result.dataset.workflow_parameters.workflow_parameters[0].name)
            self.assertEqual('True',
                             get_result.dataset.workflow_parameters.workflow_parameters[0].value)

            # 3. Get dataset with statistics
            get_with_stats_result = client.get_dataset(
                oss_dataprocess.models.GetDatasetRequest(
                    bucket=self.dp_bucket,
                    dataset_name=ds_name,
                    with_statistics=True,
                )
            )

            self.assertIsNotNone(get_with_stats_result)
            self.assertEqual(200, get_with_stats_result.status_code)
            self.assertIsNotNone(get_with_stats_result.dataset)

            # 4. Update dataset
            update_result = client.update_dataset(
                oss_dataprocess.models.UpdateDatasetRequest(
                    bucket=self.dp_bucket,
                    dataset_name=ds_name,
                    description='updated description 1',
                )
            )

            self.assertIsNotNone(update_result)
            self.assertEqual(200, update_result.status_code)
            self.assertIsNotNone(update_result.dataset)

            # 5. Verify update by getting again
            get_after_update = client.get_dataset(
                oss_dataprocess.models.GetDatasetRequest(
                    bucket=self.dp_bucket,
                    dataset_name=ds_name,
                )
            )

            self.assertIsNotNone(get_after_update)
            self.assertEqual(200, get_after_update.status_code)
            self.assertEqual('updated description 1', get_after_update.dataset.description)

            # 6. Delete dataset
            delete_result = client.delete_dataset(
                oss_dataprocess.models.DeleteDatasetRequest(
                    bucket=self.dp_bucket,
                    dataset_name=ds_name,
                )
            )

            self.assertIsNotNone(delete_result)
            self.assertIn(delete_result.status_code, (200, 204),
                          'Expected 200 or 204 for delete')

        finally:
            # Ensure cleanup
            try:
                client.delete_dataset(
                    oss_dataprocess.models.DeleteDatasetRequest(
                        bucket=self.dp_bucket,
                        dataset_name=ds_name,
                    )
                )
            except Exception:
                pass

    def test_create_and_delete_dataset(self):
        client = self.dp_client
        ds_name = gen_dataset_name()

        # Create
        create_result = client.create_dataset(
            oss_dataprocess.models.CreateDatasetRequest(
                bucket=self.dp_bucket,
                dataset_name=ds_name,
            )
        )

        self.assertIsNotNone(create_result)
        self.assertEqual(200, create_result.status_code)

        # Delete
        delete_result = client.delete_dataset(
            oss_dataprocess.models.DeleteDatasetRequest(
                bucket=self.dp_bucket,
                dataset_name=ds_name,
            )
        )

        self.assertIsNotNone(delete_result)
        self.assertIn(delete_result.status_code, (200, 204),
                      'Expected 200 or 204 for delete')

    def test_get_non_existent_dataset(self):
        client = self.dp_client

        try:
            client.get_dataset(
                oss_dataprocess.models.GetDatasetRequest(
                    bucket=self.dp_bucket,
                    dataset_name='non-existent-dataset-' + str(int(time.time() * 1000)),
                )
            )
            self.fail('Expected ServiceException for non-existent dataset')
        except Exception as e:
            service_error = find_service_error(e)
            self.assertIsNotNone(service_error, 'Expected ServiceException')
            self.assertIn(service_error.status_code, (404, 400),
                          'Expected 404 or 400 status')

    def test_update_dataset_with_config(self):
        client = self.dp_client
        ds_name = gen_dataset_name()

        # Create dataset first
        create_result = client.create_dataset(
            oss_dataprocess.models.CreateDatasetRequest(
                bucket=self.dp_bucket,
                dataset_name=ds_name,
            )
        )

        self.assertIsNotNone(create_result)
        self.assertEqual(200, create_result.status_code)

        try:
            # Update with DatasetConfig (Language = "en")
            config = oss_dataprocess.models.DatasetConfig(
                insights=oss_dataprocess.models.InsightsConfig(
                    language='en',
                ),
            )

            update_result = client.update_dataset(
                oss_dataprocess.models.UpdateDatasetRequest(
                    bucket=self.dp_bucket,
                    dataset_name=ds_name,
                    dataset_config=config,
                )
            )

            self.assertIsNotNone(update_result)
            self.assertEqual(200, update_result.status_code)

            # Verify DatasetConfig is returned correctly
            get_result = client.get_dataset(
                oss_dataprocess.models.GetDatasetRequest(
                    bucket=self.dp_bucket,
                    dataset_name=ds_name,
                )
            )

            self.assertIsNotNone(get_result)
            self.assertEqual(200, get_result.status_code)
            self.assertIsNotNone(get_result.dataset.dataset_config)
            self.assertIsNotNone(get_result.dataset.dataset_config.insights)
            self.assertEqual('en', get_result.dataset.dataset_config.insights.language)
        finally:
            try:
                client.delete_dataset(
                    oss_dataprocess.models.DeleteDatasetRequest(
                        bucket=self.dp_bucket,
                        dataset_name=ds_name,
                    )
                )
            except Exception:
                pass

    def test_create_dataset_with_dataset_config(self):
        client = self.dp_client
        ds_name = gen_dataset_name()

        config = oss_dataprocess.models.DatasetConfig(
            insights=oss_dataprocess.models.InsightsConfig(
                language='ch',
            ),
        )

        create_result = client.create_dataset(
            oss_dataprocess.models.CreateDatasetRequest(
                bucket=self.dp_bucket,
                dataset_name=ds_name,
                dataset_config=config,
            )
        )

        self.assertIsNotNone(create_result)
        self.assertEqual(200, create_result.status_code)

        try:
            # Verify DatasetConfig is returned in get
            get_result = client.get_dataset(
                oss_dataprocess.models.GetDatasetRequest(
                    bucket=self.dp_bucket,
                    dataset_name=ds_name,
                )
            )

            self.assertIsNotNone(get_result)
            self.assertEqual(200, get_result.status_code)
            self.assertIsNotNone(get_result.dataset.dataset_config)
            self.assertIsNotNone(get_result.dataset.dataset_config.insights)
            self.assertEqual('ch', get_result.dataset.dataset_config.insights.language)
        finally:
            try:
                client.delete_dataset(
                    oss_dataprocess.models.DeleteDatasetRequest(
                        bucket=self.dp_bucket,
                        dataset_name=ds_name,
                    )
                )
            except Exception:
                pass

    def test_create_dataset_with_workflow_parameters(self):
        client = self.dp_client
        ds_name = gen_dataset_name()

        workflow_params = [
            oss_dataprocess.models.WorkflowParameter(
                name='VideoInsightEnable',
                value='true',
            ),
        ]

        create_result = client.create_dataset(
            oss_dataprocess.models.CreateDatasetRequest(
                bucket=self.dp_bucket,
                dataset_name=ds_name,
                description='test with workflow parameters',
                workflow_parameters=workflow_params,
            )
        )

        self.assertIsNotNone(create_result)
        self.assertEqual(200, create_result.status_code)
        self.assertIsNotNone(create_result.dataset)
        self.assertEqual(ds_name, create_result.dataset.dataset_name)

        try:
            # Verify workflow parameters are returned in get
            get_result = client.get_dataset(
                oss_dataprocess.models.GetDatasetRequest(
                    bucket=self.dp_bucket,
                    dataset_name=ds_name,
                )
            )

            self.assertIsNotNone(get_result)
            self.assertEqual(200, get_result.status_code)
            self.assertIsNotNone(get_result.dataset)
            self.assertIsNotNone(get_result.dataset.workflow_parameters,
                                 'WorkflowParameters should be returned')

            returned_params = get_result.dataset.workflow_parameters.workflow_parameters
            self.assertIsNotNone(returned_params, 'WorkflowParameter list should be returned')
            self.assertEqual(1, len(returned_params))
            self.assertEqual('VideoInsightEnable', returned_params[0].name)
            self.assertEqual('true', returned_params[0].value)
        finally:
            try:
                client.delete_dataset(
                    oss_dataprocess.models.DeleteDatasetRequest(
                        bucket=self.dp_bucket,
                        dataset_name=ds_name,
                    )
                )
            except Exception:
                pass

    def test_update_dataset_with_workflow_parameters(self):
        client = self.dp_client
        ds_name = gen_dataset_name()

        # Create dataset without workflow parameters
        create_result = client.create_dataset(
            oss_dataprocess.models.CreateDatasetRequest(
                bucket=self.dp_bucket,
                dataset_name=ds_name,
            )
        )

        self.assertIsNotNone(create_result)
        self.assertEqual(200, create_result.status_code)

        try:
            # Update with workflow parameters
            workflow_params = [
                oss_dataprocess.models.WorkflowParameter(
                    name='VideoInsightEnable',
                    value='true',
                ),
            ]

            update_result = client.update_dataset(
                oss_dataprocess.models.UpdateDatasetRequest(
                    bucket=self.dp_bucket,
                    dataset_name=ds_name,
                    workflow_parameters=workflow_params,
                )
            )

            self.assertIsNotNone(update_result)
            self.assertEqual(200, update_result.status_code)

            # Verify update by getting the dataset
            get_result = client.get_dataset(
                oss_dataprocess.models.GetDatasetRequest(
                    bucket=self.dp_bucket,
                    dataset_name=ds_name,
                )
            )

            self.assertIsNotNone(get_result)
            self.assertEqual(200, get_result.status_code)
            self.assertIsNotNone(get_result.dataset.workflow_parameters,
                                 'WorkflowParameters should be returned after update')

            returned_params = get_result.dataset.workflow_parameters.workflow_parameters
            self.assertIsNotNone(returned_params,
                                 'WorkflowParameter list should be returned after update')
            self.assertEqual(1, len(returned_params))
            self.assertEqual('VideoInsightEnable', returned_params[0].name)
            self.assertEqual('true', returned_params[0].value)
        finally:
            try:
                client.delete_dataset(
                    oss_dataprocess.models.DeleteDatasetRequest(
                        bucket=self.dp_bucket,
                        dataset_name=ds_name,
                    )
                )
            except Exception:
                pass

    def test_list_datasets(self):
        client = self.dp_client

        # Use a unique prefix for this test to isolate from other datasets
        test_prefix = 'list-test-' + str(int(time.time() * 1000)) + '-'
        ds_name1 = test_prefix + 'a'
        ds_name2 = test_prefix + 'b'
        ds_name3 = test_prefix + 'c'

        # Create 3 datasets
        for name in (ds_name1, ds_name2, ds_name3):
            cr = client.create_dataset(
                oss_dataprocess.models.CreateDatasetRequest(
                    bucket=self.dp_bucket,
                    dataset_name=name,
                )
            )
            self.assertIsNotNone(cr)
            self.assertEqual(200, cr.status_code,
                             'create ' + name + ' should return 200')

        try:
            # 1. List with prefix, verify all 3 datasets are returned
            list_all = client.list_datasets(
                oss_dataprocess.models.ListDatasetsRequest(
                    bucket=self.dp_bucket,
                    prefix=test_prefix,
                )
            )

            self.assertIsNotNone(list_all)
            self.assertEqual(200, list_all.status_code)
            self.assertIsNotNone(list_all.datasets, 'datasets should not be null')
            self.assertIsNotNone(list_all.datasets.dataset)
            self.assertEqual(3, len(list_all.datasets.dataset),
                             'should list exactly 3 datasets with prefix')

            # Collect listed dataset names and verify each one
            listed_names = set()
            for ds in list_all.datasets.dataset:
                self.assertIsNotNone(ds.dataset_name, 'dataset name should not be null')
                listed_names.add(ds.dataset_name)
            self.assertIn(ds_name1, listed_names, 'dsName1 should be in list')
            self.assertIn(ds_name2, listed_names, 'dsName2 should be in list')
            self.assertIn(ds_name3, listed_names, 'dsName3 should be in list')

            # 2. Paginate with maxResults=1, walk through all pages using nextToken
            paginated_names = set()
            next_token = None
            page_count = 0

            while True:
                page_result = client.list_datasets(
                    oss_dataprocess.models.ListDatasetsRequest(
                        bucket=self.dp_bucket,
                        prefix=test_prefix,
                        max_results=1,
                        next_token=next_token,
                    )
                )
                self.assertIsNotNone(page_result)
                self.assertEqual(200, page_result.status_code)
                self.assertIsNotNone(page_result.datasets)
                self.assertIsNotNone(page_result.datasets.dataset)
                self.assertEqual(1, len(page_result.datasets.dataset),
                                 'each page should have exactly 1 dataset')

                paginated_names.add(page_result.datasets.dataset[0].dataset_name)
                next_token = page_result.next_token
                page_count += 1

                # Safety guard against infinite loop
                self.assertLessEqual(page_count, 10, 'pagination should not exceed 10 pages')

                if not next_token:
                    break

            # Verify pagination walked through all 3 datasets
            self.assertEqual(3, page_count, 'should have paginated through 3 pages')
            self.assertIn(ds_name1, paginated_names, 'paginated dsName1 should be found')
            self.assertIn(ds_name2, paginated_names, 'paginated dsName2 should be found')
            self.assertIn(ds_name3, paginated_names, 'paginated dsName3 should be found')

            # 3. Do one more call with maxResults large enough to get all,
            # nextToken should be null/empty
            full_page = client.list_datasets(
                oss_dataprocess.models.ListDatasetsRequest(
                    bucket=self.dp_bucket,
                    prefix=test_prefix,
                    max_results=100,
                )
            )
            self.assertEqual(200, full_page.status_code)
            self.assertEqual(3, len(full_page.datasets.dataset))
            self.assertFalse(full_page.next_token,
                             'nextToken should be null or empty when all results returned')

        finally:
            # Cleanup all 3 datasets
            for name in (ds_name1, ds_name2, ds_name3):
                try:
                    client.delete_dataset(
                        oss_dataprocess.models.DeleteDatasetRequest(
                            bucket=self.dp_bucket,
                            dataset_name=name,
                        )
                    )
                except Exception:
                    pass
