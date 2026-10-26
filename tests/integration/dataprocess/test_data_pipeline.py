# pylint: skip-file
"""Integration tests for Data Pipeline CRUD operations via dataprocess Client.

Aligned with Java ClientDataPipelineTest.
"""

import time
import xml.etree.ElementTree as ET
from unittest import mock

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
from .. import API_KEY, MODEL_TYPE, DIMENSION, ROLE_NAME, RAM_ROLE_ARN
from .. import random_vector_bucket_name, clean_objects


class TestDataPipeline(TestBaseDataProcess):
    # Data pipeline does not depend on meta query, skip opening it.
    open_meta_query_on_setup = False

    def _assert_phase_element_present(self, xml_data, pipeline_name):
        root = ET.fromstring(xml_data)
        if root.tag == 'DataPipelineConfiguration':
            configurations = [root]
        else:
            configurations = root.findall(
                './DataPipelineConfigurations/DataPipelineConfiguration',
            )
        configuration = next(
            (item for item in configurations
             if item.findtext('DataPipelineName') == pipeline_name),
            None,
        )
        self.assertIsNotNone(configuration, '响应中未找到目标 pipeline 配置')
        self.assertIsNotNone(configuration.find('Phase'), '响应中缺少 Phase 元素')

    def _invoke_with_phase_check(self, client, pipeline_name, operation, *args):
        invoke_operation = client._client.invoke_operation

        def invoke_and_check(op_input, **kwargs):
            op_output = invoke_operation(op_input, **kwargs)
            self._assert_phase_element_present(
                op_output.http_response.content, pipeline_name,
            )
            return op_output

        with mock.patch.object(client._client, 'invoke_operation',
                               side_effect=invoke_and_check):
            return operation(*args)

    def _delete_error_bucket(self, oss_client, bucket_name):
        # The pipeline may record errors into this bucket, so empty it first.
        try:
            clean_objects(oss_client, bucket_name)
            oss_client.delete_bucket(
                oss.models.DeleteBucketRequest(
                    bucket=bucket_name,
                )
            )
        except Exception:
            pass

    def _assert_v2_configuration(self, configuration, pipeline_name,
                                 vector_bucket_name, index_name):
        self.assertIsNotNone(configuration)
        self.assertEqual(pipeline_name, configuration.data_pipeline_name)
        self.assertEqual('standard', configuration.model_tier)
        self.assertIsNotNone(configuration.status)
        self.assertEqual(1, len(configuration.sources))
        self.assertFalse(configuration.sources[0].ignore_delete)

        process_configuration = configuration.data_pipeline_data_process_configuration
        self.assertIsNotNone(process_configuration)
        self.assertEqual('fast', process_configuration.search_mode)
        snapshot = process_configuration.insights.video.frame_embedding.snapshot
        self.assertEqual('interval', snapshot.mode)
        self.assertEqual(1.0, snapshot.interval)

        self.assertIsNotNone(configuration.data_pipeline_error)
        self.assertEqual('ignoreAndRecord', configuration.data_pipeline_error.error_mode)

        destination = configuration.destination
        self.assertIsNotNone(destination)
        video_frame = destination.video_frame_embedding
        self.assertIsNotNone(video_frame)
        self.assertEqual(vector_bucket_name, video_frame.bucket)
        self.assertEqual(index_name, video_frame.index_name)
        self.assertEqual('v2', video_frame.prefix)
        self.assertIsNone(destination.image_embedding)
        self.assertIsNone(destination.image_text_embedding)
        self.assertIsNone(destination.video_text_embedding)
        self.assertIsNone(destination.document_chunk_embedding)

    def _assert_v2_list_result(self, result, pipeline_name,
                               vector_bucket_name, index_name):
        self.assertIsNotNone(result.data_pipeline_configurations)
        configurations = result.data_pipeline_configurations.data_pipeline_configuration
        self.assertIsNotNone(configurations)
        configuration = next(
            (item for item in configurations
             if item.data_pipeline_name == pipeline_name),
            None,
        )
        self.assertIsNotNone(configuration)
        self._assert_v2_configuration(
            configuration,
            pipeline_name,
            vector_bucket_name,
            index_name,
        )

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
        vector_bucket_name = random_vector_bucket_name()
        index_name = 'testIndexForIntegration'
        error_bucket_name = random_bucket_name() + '-error-test'
        oss_client = get_default_client()
        # Only resources created by this test are cleaned up.
        vector_bucket_created = False
        vector_index_created = False
        error_bucket_created = False

        try:
            # Put vector bucket
            put_vector_result = vectors_client.put_vector_bucket(
                oss_vectors.models.PutVectorBucketRequest(
                    bucket=vector_bucket_name,
                )
            )
            vector_bucket_created = True
            self.assertIsNotNone(put_vector_result)
            self.assertEqual(200, put_vector_result.status_code)

            # 2. Put a vector index
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
            vector_index_created = True

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

            # Create an error bucket
            put_bucket_result = oss_client.put_bucket(
                oss.models.PutBucketRequest(
                    bucket=error_bucket_name,
                    create_bucket_configuration=oss.models.CreateBucketConfiguration(
                        storage_class='Standard',
                    ),
                )
            )
            error_bucket_created = True
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
                    role=RAM_ROLE_ARN,
                    configuration=config,
                )
            )

            self.assertIsNotNone(put_result)
            self.assertEqual(200, put_result.status_code)

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

            # 7. Delete the vector index
            delete_index_result = vectors_client.delete_vector_index(
                oss_vectors.models.DeleteVectorIndexRequest(
                    bucket=vector_bucket_name,
                    index_name=index_name,
                )
            )
            vector_index_created = False

            # Assert successful deletion (Delete operations often return 204 No Content)
            self.assertIsNotNone(delete_index_result)
            self.assertEqual(204, delete_index_result.status_code)

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

            if vector_index_created:
                try:
                    vectors_client.delete_vector_index(
                        oss_vectors.models.DeleteVectorIndexRequest(
                            bucket=vector_bucket_name,
                            index_name=index_name,
                        )
                    )
                except Exception:
                    pass

            if vector_bucket_created:
                try:
                    vectors_client.delete_vector_bucket(
                        oss_vectors.models.DeleteVectorBucketRequest(
                            bucket=vector_bucket_name,
                        )
                    )
                except Exception:
                    pass

            if error_bucket_created:
                self._delete_error_bucket(oss_client, error_bucket_name)

    def test_v2_data_pipeline_lifecycle_and_validation(self):
        client = self.dp_client
        vectors_client = get_vectors_client()
        suffix = str(int(time.time() * 10))
        pipeline_name = 'v2' + suffix
        invalid_pipeline_name = 'v2Invalid' + suffix
        vector_bucket_name = random_vector_bucket_name()
        index_name = 'videoFrame' + suffix
        # DataPipelineError and its ErrorMode are mandatory.
        error_bucket_name = random_bucket_name() + '-error-test'
        oss_client = get_default_client()
        # Only resources created by this test are cleaned up.
        vector_bucket_created = False
        vector_index_created = False
        error_bucket_created = False

        # Align with Java: use the freshly created test bucket as the source.
        source = oss_dataprocess.models.DataPipelineSource(
            input_bucket=self.bucket_name,
            input_data_scope='All',
            filter_configuration=oss_dataprocess.models.DataPipelineSourceFilterConfiguration(
                object_media_types=['video'],
            ),
        )
        insights = oss_dataprocess.models.DataPipelineInsights(
            video=oss_dataprocess.models.InsightsVideo(
                frame_embedding=oss_dataprocess.models.InsightsFrameEmbedding(
                    snapshot=oss_dataprocess.models.InsightsSnapshot(
                        mode='interval',
                        interval=1.0,
                    ),
                ),
            ),
        )
        destination = oss_dataprocess.models.DataPipelineDestination(
            video_frame_embedding=(
                oss_dataprocess.models.VideoFrameEmbedding(
                    bucket=vector_bucket_name,
                    index_name=index_name,
                    prefix='v2',
                )
            ),
        )
        process_configuration = (
            oss_dataprocess.models.DataPipelineDataProcessConfiguration(
                search_mode='fast',
                insights=insights,
            )
        )
        error_config = oss_dataprocess.models.DataPipelineError(
            error_mode='ignoreAndRecord',
            error_bucket=error_bucket_name,
            error_prefix='error-output/',
        )
        configuration = (
            oss_dataprocess.models.PutDataPipelineConfigurationConfiguration(
                data_pipeline_description='V2 fast video pipeline',
                sources=[source],
                model_tier='standard',
                data_pipeline_data_process_configuration=process_configuration,
                destination=destination,
                data_pipeline_error=error_config,
            )
        )

        try:
            put_bucket_result = vectors_client.put_vector_bucket(
                oss_vectors.models.PutVectorBucketRequest(
                    bucket=vector_bucket_name,
                )
            )
            vector_bucket_created = True
            self.assertEqual(200, put_bucket_result.status_code)

            put_index_result = vectors_client.put_vector_index(
                oss_vectors.models.PutVectorIndexRequest(
                    bucket=vector_bucket_name,
                    index_name=index_name,
                    data_type='float32',
                    dimension=768,
                    distance_metric='cosine',
                    metadata={
                        'nonFilterableMetadataKeys': ['VideoStreams'],
                    },
                )
            )
            vector_index_created = True
            self.assertEqual(200, put_index_result.status_code)

            put_error_bucket_result = oss_client.put_bucket(
                oss.models.PutBucketRequest(
                    bucket=error_bucket_name,
                    create_bucket_configuration=oss.models.CreateBucketConfiguration(
                        storage_class='Standard',
                    ),
                )
            )
            error_bucket_created = True
            self.assertEqual(200, put_error_bucket_result.status_code)
            wait_for_cache_expiration(1)

            invalid_configuration = (
                oss_dataprocess.models.PutDataPipelineConfigurationConfiguration(
                    data_pipeline_description=configuration.data_pipeline_description,
                    sources=[source, source],
                    model_tier=configuration.model_tier,
                    data_pipeline_data_process_configuration=(
                        configuration.data_pipeline_data_process_configuration
                    ),
                    destination=configuration.destination,
                    data_pipeline_error=error_config,
                )
            )
            with self.assertRaises(Exception) as context:
                client.put_data_pipeline_configuration(
                    oss_dataprocess.models.PutDataPipelineConfigurationRequest(
                        data_pipeline_name=invalid_pipeline_name,
                        role=RAM_ROLE_ARN,
                        configuration=invalid_configuration,
                    )
                )
            service_error = find_service_error(context.exception)
            self.assertIsNotNone(service_error, 'Expected ServiceException')
            self.assertEqual(400, service_error.status_code)

            put_result = client.put_data_pipeline_configuration(
                oss_dataprocess.models.PutDataPipelineConfigurationRequest(
                    data_pipeline_name=pipeline_name,
                    role=RAM_ROLE_ARN,
                    configuration=configuration,
                )
            )
            self.assertEqual(200, put_result.status_code)

            get_request = oss_dataprocess.models.GetDataPipelineConfigurationRequest(
                data_pipeline_name=pipeline_name,
            )
            get_result = self._invoke_with_phase_check(
                client, pipeline_name,
                client.get_data_pipeline_configuration, get_request,
            )
            self.assertEqual(200, get_result.status_code)
            self._assert_v2_configuration(
                get_result.configuration,
                pipeline_name,
                vector_bucket_name,
                index_name,
            )

            list_request = oss_dataprocess.models.ListDataPipelineConfigurationsRequest(
                max_results=0,
                prefix=pipeline_name,
                input_bucket=self.bucket_name,
            )
            list_result = self._invoke_with_phase_check(
                client, pipeline_name,
                client.list_data_pipeline_configurations, list_request,
            )
            self.assertEqual(200, list_result.status_code)
            self._assert_v2_list_result(
                list_result,
                pipeline_name,
                vector_bucket_name,
                index_name,
            )

        finally:
            for name in (pipeline_name, invalid_pipeline_name):
                try:
                    client.delete_data_pipeline_configuration(
                        oss_dataprocess.models.DeleteDataPipelineConfigurationRequest(
                            data_pipeline_name=name,
                        )
                    )
                except Exception:
                    pass
            if vector_index_created:
                try:
                    vectors_client.delete_vector_index(
                        oss_vectors.models.DeleteVectorIndexRequest(
                            bucket=vector_bucket_name,
                            index_name=index_name,
                        )
                    )
                except Exception:
                    pass
            if vector_bucket_created:
                try:
                    vectors_client.delete_vector_bucket(
                        oss_vectors.models.DeleteVectorBucketRequest(
                            bucket=vector_bucket_name,
                        )
                    )
                except Exception:
                    pass
            if error_bucket_created:
                self._delete_error_bucket(oss_client, error_bucket_name)

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
