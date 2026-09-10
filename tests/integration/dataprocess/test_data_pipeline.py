# pylint: skip-file
"""Integration tests for Data Pipeline CRUD operations via dataprocess Client.

Aligned with Java ClientDataPipelineTest.
"""

import time
import random

from . import (
    TestBaseDataProcess,
    get_default_client,
    get_vectors_client,
    random_bucket_name,
    wait_for_cache_expiration,
    find_service_error,
)
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.vectors as oss_vectors
import alibabacloud_oss_v2.dataprocess as oss_dataprocess
from .. import API_KEY, MODEL_TYPE, DIMENSION, ROLE_NAME


class TestDataPipeline(TestBaseDataProcess):
    # Data pipeline does not depend on meta query, skip opening it.
    open_meta_query_on_setup = False

    def test_data_pipeline_lifecycle(self):
        client = self.dp_client
        pipeline_name = 'test-pipeline-' + str(int(time.time() * 1000))

        # 1. Put Data Pipeline Configuration
        filter_config = oss_dataprocess.models.DataPipelineSourceFilterConfiguration(
            prefix_set=['prefix1/', 'prefix2/prefix3/'],
            object_media_types=['text', 'image', 'video'],
        )

        source = oss_dataprocess.models.DataPipelineSource(
            input_bucket=self.dp_bucket,
            input_data_scope='All',
            ignore_delete=True,
            filter_configuration=filter_config,
        )

        embedding_config = oss_dataprocess.models.DataPipelineEmbeddingConfiguration(
            embedding_provider='bailian',
            api_key=API_KEY,
            model=MODEL_TYPE,
            fps=1.0,
        )

        vectors_client = get_vectors_client()
        vector_bucket_name = 'sdk-oss-python-test-' + str(int(time.time() * 1000)) + '-' + str(random.randint(0, 9999))

        # Put vector bucket
        put_vector_result = vectors_client.put_vector_bucket(
            oss_vectors.models.PutVectorBucketRequest(
                bucket=vector_bucket_name,
            )
        )
        self.assertIsNotNone(put_vector_result)
        self.assertEqual(200, put_vector_result.status_code)

        # 2. Put a vector index
        index_name = 'testIndexForIntegration'
        dimension = int(DIMENSION)

        metadata = {
            'nonFilterableMetadataKeys': ['key1', 'key2'],
        }

        put_vector_index_result = vectors_client.put_vector_index(
            oss_vectors.models.PutVectorIndexRequest(
                bucket=vector_bucket_name,
                data_type='float32',
                dimension=dimension,
                distance_metric='cosine',
                index_name=index_name,
                metadata=metadata,
            )
        )

        # Assert successful creation
        self.assertIsNotNone(put_vector_index_result)
        self.assertEqual(200, put_vector_index_result.status_code)

        destination = oss_dataprocess.models.DataPipelineDestination(
            vector_bucket_name=vector_bucket_name,
            vector_key_prefix='',
            vector_index_names=[index_name],
            object_tag_to_metadata=['key1', 'key2'],
            usermeta_to_metadata=['x-oss-meta-key1'],
        )

        error_bucket_name = random_bucket_name() + '-error-test'

        # Create an error bucket
        oss_client = get_default_client()
        put_bucket_result = oss_client.put_bucket(
            oss.models.PutBucketRequest(
                bucket=error_bucket_name,
                create_bucket_configuration=oss.models.CreateBucketConfiguration(
                    storage_class='Standard',
                ),
            )
        )
        self.assertIsNotNone(put_bucket_result)
        self.assertEqual(200, put_bucket_result.status_code)
        wait_for_cache_expiration(1)

        error_config = oss_dataprocess.models.DataPipelineError(
            error_mode='ignoreAndRecord',
            error_bucket=error_bucket_name,
            error_prefix='error-output/',
        )

        config = oss_dataprocess.models.PutDataPipelineConfigurationConfiguration(
            data_pipeline_description='使用百炼多模态模型为业务数据向量化',
            sources=[source],
            data_pipeline_embedding_configuration=embedding_config,
            destination=destination,
            data_pipeline_error=error_config,
        )

        put_result = client.put_data_pipeline_configuration(
            oss_dataprocess.models.PutDataPipelineConfigurationRequest(
                data_pipeline_name=pipeline_name,
                role=ROLE_NAME,
                configuration=config,
            )
        )

        self.assertIsNotNone(put_result)
        self.assertEqual(200, put_result.status_code)

        try:
            # 2. Get Data Pipeline Configuration
            get_result = client.get_data_pipeline_configuration(
                oss_dataprocess.models.GetDataPipelineConfigurationRequest(
                    data_pipeline_name=pipeline_name,
                )
            )

            self.assertIsNotNone(get_result)
            self.assertEqual(200, get_result.status_code)
            self.assertIsNotNone(get_result.configuration)

            # 3. List Data Pipeline Configurations
            list_result = client.list_data_pipeline_configurations(
                oss_dataprocess.models.ListDataPipelineConfigurationsRequest()
            )

            self.assertIsNotNone(list_result)
            self.assertEqual(200, list_result.status_code)
            self.assertIsNotNone(list_result.data_pipeline_configurations)

            # 4. Pause Data Pipeline
            pause_result = client.pause_data_pipeline(
                oss_dataprocess.models.PauseDataPipelineRequest(
                    data_pipeline_name=pipeline_name,
                )
            )

            self.assertIsNotNone(pause_result)
            self.assertEqual(200, pause_result.status_code)

            # 5. Restart Data Pipeline
            restart_result = client.restart_data_pipeline(
                oss_dataprocess.models.RestartDataPipelineRequest(
                    data_pipeline_name=pipeline_name,
                )
            )

            self.assertIsNotNone(restart_result)
            self.assertEqual(200, restart_result.status_code)

            # 6. Delete Data Pipeline Configuration
            delete_result = client.delete_data_pipeline_configuration(
                oss_dataprocess.models.DeleteDataPipelineConfigurationRequest(
                    data_pipeline_name=pipeline_name,
                )
            )

            self.assertIsNotNone(delete_result)
            self.assertIn(delete_result.status_code, (200, 204),
                          'Expected 200 or 204 for delete')

        finally:
            # Ensure cleanup
            try:
                client.delete_data_pipeline_configuration(
                    oss_dataprocess.models.DeleteDataPipelineConfigurationRequest(
                        data_pipeline_name=pipeline_name,
                    )
                )
            except Exception:
                pass

            delete_index_result = vectors_client.delete_vector_index(
                oss_vectors.models.DeleteVectorIndexRequest(
                    bucket=vector_bucket_name,
                    index_name=index_name,
                )
            )

            # Assert successful deletion (Delete operations often return 204 No Content)
            self.assertIsNotNone(delete_index_result)
            self.assertEqual(204, delete_index_result.status_code)

            try:
                vectors_client.delete_vector_bucket(
                    oss_vectors.models.DeleteVectorBucketRequest(
                        bucket=vector_bucket_name,
                    )
                )
            except Exception:
                pass

            try:
                oss_client.delete_bucket(
                    oss.models.DeleteBucketRequest(
                        bucket=error_bucket_name,
                    )
                )
            except Exception:
                pass

    def test_get_non_existent_pipeline_configuration(self):
        client = self.dp_client

        try:
            client.get_data_pipeline_configuration(
                oss_dataprocess.models.GetDataPipelineConfigurationRequest(
                    data_pipeline_name='non-existent-pipeline-' + str(int(time.time() * 1000)),
                )
            )
            self.fail('Expected ServiceException for non-existent pipeline')
        except Exception as e:
            service_error = find_service_error(e)
            self.assertIsNotNone(service_error, 'Expected ServiceException')
            self.assertIn(service_error.status_code, (404, 400),
                          'Expected 404 or 400 status')

    def test_delete_non_existent_pipeline_configuration(self):
        client = self.dp_client

        try:
            delete_result = client.delete_data_pipeline_configuration(
                oss_dataprocess.models.DeleteDataPipelineConfigurationRequest(
                    data_pipeline_name='non-existent-pipeline-' + str(int(time.time() * 1000)),
                )
            )
            # Delete might return 204 even if not exists
            self.assertIsNotNone(delete_result)
            self.assertIn(delete_result.status_code, (200, 204, 404),
                          'Expected 200, 204 or 404')
        except Exception as e:
            # Or throw 404
            service_error = find_service_error(e)
            self.assertIsNotNone(service_error, 'Expected ServiceException')
            self.assertEqual(404, service_error.status_code, 'Expected 404 status')
