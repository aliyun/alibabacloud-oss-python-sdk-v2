# pylint: skip-file
"""Unit tests for dataprocess data pipeline models."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))
import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.dataprocess.models import data_pipeline_basic as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict
from tests.unit import MockHttpResponse


# ==================== Sub-model tests ====================

class TestDataPipelineSourceFilterConfiguration(unittest.TestCase):
    def test_empty_constructor(self):
        f = model.DataPipelineSourceFilterConfiguration()
        self.assertIsNone(f.prefix_set)
        self.assertIsNone(f.object_media_types)

    def test_full_constructor(self):
        f = model.DataPipelineSourceFilterConfiguration(
            prefix_set=['prefix1/', 'prefix2/prefix3/'],
            object_media_types=['text', 'image', 'video'],
        )
        self.assertEqual(2, len(f.prefix_set))
        self.assertEqual(3, len(f.object_media_types))
        self.assertEqual('prefix1/', f.prefix_set[0])
        self.assertEqual('text', f.object_media_types[0])


class TestDataPipelineSource(unittest.TestCase):
    def test_empty_constructor(self):
        src = model.DataPipelineSource()
        self.assertIsNone(src.input_bucket)
        self.assertIsNone(src.input_data_scope)
        self.assertIsNone(src.ignore_delete)
        self.assertIsNone(src.filter_configuration)

    def test_full_constructor(self):
        src = model.DataPipelineSource(
            input_bucket='my-bucket',
            input_data_scope='All',
            ignore_delete=True,
            filter_configuration=model.DataPipelineSourceFilterConfiguration(
                prefix_set=['images/'],
                object_media_types=['image/jpeg'],
            ),
        )
        self.assertEqual('my-bucket', src.input_bucket)
        self.assertEqual('All', src.input_data_scope)
        self.assertTrue(src.ignore_delete)
        self.assertIsNotNone(src.filter_configuration)
        self.assertEqual(1, len(src.filter_configuration.prefix_set))


class TestDataPipelineDestination(unittest.TestCase):
    def test_empty_constructor(self):
        dest = model.DataPipelineDestination()
        self.assertIsNone(dest.vector_bucket_name)
        self.assertIsNone(dest.vector_key_prefix)
        self.assertIsNone(dest.vector_index_names)
        self.assertIsNone(dest.object_tag_to_metadata)
        self.assertIsNone(dest.usermeta_to_metadata)

    def test_full_constructor(self):
        dest = model.DataPipelineDestination(
            vector_bucket_name='my-vector-bucket',
            vector_key_prefix='',
            vector_index_names=['my-index'],
            object_tag_to_metadata=['key1', 'key2'],
            usermeta_to_metadata=['x-oss-meta-key1'],
        )
        self.assertEqual('my-vector-bucket', dest.vector_bucket_name)
        self.assertEqual('', dest.vector_key_prefix)
        self.assertEqual(1, len(dest.vector_index_names))
        self.assertEqual(2, len(dest.object_tag_to_metadata))
        self.assertEqual(1, len(dest.usermeta_to_metadata))


class TestDataPipelineEmbeddingConfiguration(unittest.TestCase):
    def test_empty_constructor(self):
        emb = model.DataPipelineEmbeddingConfiguration()
        self.assertIsNone(emb.embedding_provider)
        self.assertIsNone(emb.api_key)
        self.assertIsNone(emb.model)
        self.assertIsNone(emb.fps)

    def test_full_constructor(self):
        emb = model.DataPipelineEmbeddingConfiguration(
            embedding_provider='bailian',
            api_key='xxxx',
            model='qwen2.5-vl-embedding',
            fps=1.0,
        )
        self.assertEqual('bailian', emb.embedding_provider)
        self.assertEqual('xxxx', emb.api_key)
        self.assertEqual('qwen2.5-vl-embedding', emb.model)
        self.assertEqual(1.0, emb.fps)


class TestDataPipelineError(unittest.TestCase):
    def test_empty_constructor(self):
        err = model.DataPipelineError()
        self.assertIsNone(err.error_mode)
        self.assertIsNone(err.error_bucket)
        self.assertIsNone(err.error_prefix)

    def test_full_constructor(self):
        err = model.DataPipelineError(
            error_mode='ignoreAndRecord',
            error_bucket='my-error-bucket',
            error_prefix='error-output/',
        )
        self.assertEqual('ignoreAndRecord', err.error_mode)
        self.assertEqual('my-error-bucket', err.error_bucket)
        self.assertEqual('error-output/', err.error_prefix)


class TestDataPipelineConfiguration(unittest.TestCase):
    def test_empty_constructor(self):
        config = model.DataPipelineConfiguration()
        self.assertIsNone(config.data_pipeline_name)
        self.assertIsNone(config.data_pipeline_description)
        self.assertIsNone(config.data_pipeline_role)
        self.assertIsNone(config.status)
        self.assertIsNone(config.phase)
        self.assertIsNone(config.data_pipeline_embedding_configuration)
        self.assertIsNone(config.destination)
        self.assertIsNone(config.data_pipeline_error)
        self.assertIsNone(config.create_time)
        self.assertIsNone(config.sources)

    def test_full_constructor(self):
        config = model.DataPipelineConfiguration(
            data_pipeline_name='my-data-pipeline',
            data_pipeline_description='test pipeline',
            data_pipeline_role='my-data-pipeline-role',
            status='Running',
            phase='IncrementalScanning',
            sources=[model.DataPipelineSource(input_bucket='my-bucket')],
            data_pipeline_embedding_configuration=model.DataPipelineEmbeddingConfiguration(
                embedding_provider='bailian',
            ),
            destination=model.DataPipelineDestination(vector_bucket_name='my-vector-bucket'),
            data_pipeline_error=model.DataPipelineError(error_mode='ignoreAndRecord'),
            create_time='2021-06-29T14:50:13.011643661+08:00',
        )
        self.assertEqual('my-data-pipeline', config.data_pipeline_name)
        self.assertEqual('Running', config.status)
        self.assertEqual('IncrementalScanning', config.phase)
        self.assertEqual(1, len(config.sources))
        self.assertIsNotNone(config.destination)
        self.assertIsNotNone(config.data_pipeline_embedding_configuration)
        self.assertIsNotNone(config.data_pipeline_error)


class TestDataPipelineConfigurations(unittest.TestCase):
    def test_empty_constructor(self):
        configs = model.DataPipelineConfigurations()
        self.assertIsNone(configs.data_pipeline_configuration)

    def test_full_constructor(self):
        configs = model.DataPipelineConfigurations(data_pipeline_configuration=[
            model.DataPipelineConfiguration(data_pipeline_name='p1'),
            model.DataPipelineConfiguration(data_pipeline_name='p2'),
        ])
        self.assertEqual(2, len(configs.data_pipeline_configuration))
        self.assertEqual('p1', configs.data_pipeline_configuration[0].data_pipeline_name)
        self.assertEqual('p2', configs.data_pipeline_configuration[1].data_pipeline_name)


class TestPutDataPipelineConfigurationConfiguration(unittest.TestCase):
    def test_empty_constructor(self):
        config = model.PutDataPipelineConfigurationConfiguration()
        self.assertIsNone(config.data_pipeline_description)
        self.assertIsNone(config.sources)
        self.assertIsNone(config.data_pipeline_embedding_configuration)
        self.assertIsNone(config.destination)
        self.assertIsNone(config.data_pipeline_error)

    def test_full_constructor(self):
        config = model.PutDataPipelineConfigurationConfiguration(
            data_pipeline_description='test pipeline',
            sources=[
                model.DataPipelineSource(
                    input_bucket='my-bucket',
                    input_data_scope='All',
                    ignore_delete=True,
                    filter_configuration=model.DataPipelineSourceFilterConfiguration(
                        prefix_set=['prefix1/', 'prefix2/prefix3/'],
                        object_media_types=['text', 'image', 'video'],
                    ),
                ),
            ],
            data_pipeline_embedding_configuration=model.DataPipelineEmbeddingConfiguration(
                embedding_provider='bailian',
                api_key='xxxx',
                model='qwen2.5-vl-embedding',
                fps=1.0,
            ),
            destination=model.DataPipelineDestination(
                vector_bucket_name='my-vector-bucket',
                vector_index_names=['my-index'],
                vector_key_prefix='',
                object_tag_to_metadata=['key1', 'key2'],
                usermeta_to_metadata=['x-oss-meta-key1'],
            ),
            data_pipeline_error=model.DataPipelineError(
                error_mode='ignoreAndRecord',
                error_bucket='my-error-bucket',
                error_prefix='error-output/',
            ),
        )
        self.assertEqual('test pipeline', config.data_pipeline_description)
        self.assertEqual(1, len(config.sources))
        self.assertEqual('bailian', config.data_pipeline_embedding_configuration.embedding_provider)
        self.assertEqual('my-vector-bucket', config.destination.vector_bucket_name)
        self.assertEqual('ignoreAndRecord', config.data_pipeline_error.error_mode)


# ==================== PutDataPipelineConfiguration ====================

class TestPutDataPipelineConfigurationRequest(unittest.TestCase):
    def test_empty_constructor(self):
        request = model.PutDataPipelineConfigurationRequest()
        self.assertIsNone(request.data_pipeline_name)
        self.assertIsNone(request.role)
        self.assertIsNone(request.configuration)

    def test_full_constructor(self):
        config = model.PutDataPipelineConfigurationConfiguration(
            data_pipeline_description='test pipeline',
            sources=[model.DataPipelineSource(input_bucket='my-bucket')],
        )
        request = model.PutDataPipelineConfigurationRequest(
            data_pipeline_name='test-pipeline',
            role='test-role',
            configuration=config,
        )
        self.assertEqual('test-pipeline', request.data_pipeline_name)
        self.assertEqual('test-role', request.role)
        self.assertIsNotNone(request.configuration)

    def test_xml_builder(self):
        # Reference: Java PutDataPipelineConfigurationRequestTest.xmlBuilder
        # Step 1: Define expected XML (same structure as Java test)
        expected_xml = (
            '<DataPipelineConfiguration>'
            '  <DataPipelineDescription>使用百炼多模态模型为业务数据向量化</DataPipelineDescription>'
            '  <Sources>'
            '      <InputBucket>my-bucket</InputBucket>'
            '      <InputDataScope>All</InputDataScope>'
            '      <IgnoreDelete>true</IgnoreDelete>'
            '      <FilterConfiguration>'
            '          <PrefixSet>prefix1/</PrefixSet>'
            '          <PrefixSet>prefix2/prefix3/</PrefixSet>'
            '          <ObjectMediaTypes>text</ObjectMediaTypes>'
            '          <ObjectMediaTypes>image</ObjectMediaTypes>'
            '          <ObjectMediaTypes>video</ObjectMediaTypes>'
            '      </FilterConfiguration>'
            '  </Sources>'
            '  <DataPipelineEmbeddingConfiguration>'
            '      <EmbeddingProvider>bailian</EmbeddingProvider>'
            '      <ApiKey>xxxx</ApiKey>'
            '      <Model>qwen2.5-vl-embedding</Model>'
            '      <FPS>1.0</FPS>'
            '  </DataPipelineEmbeddingConfiguration>'
            '  <Destination>'
            '      <VectorBucketName>my-vector-bucket</VectorBucketName>'
            '      <VectorIndexNames>my-index</VectorIndexNames>'
            '      <VectorKeyPrefix>vector-prefix/</VectorKeyPrefix>'
            '      <ObjectTagToMetadata>key1</ObjectTagToMetadata>'
            '      <ObjectTagToMetadata>key2</ObjectTagToMetadata>'
            '      <UsermetaToMetadata>x-oss-meta-key1</UsermetaToMetadata>'
            '  </Destination>'
            '  <DataPipelineError>'
            '      <ErrorMode>ignoreAndRecord</ErrorMode>'
            '      <ErrorBucket>my-error-bucket</ErrorBucket>'
            '      <ErrorPrefix>error-output/</ErrorPrefix>'
            '  </DataPipelineError>'
            '</DataPipelineConfiguration>'
        )

        # Step 2: Parse expected XML and re-serialize to get canonical form
        # (equivalent to Java: xmlMapper.readValue → xmlMapper.writeValueAsString)
        expected_config = model.PutDataPipelineConfigurationConfiguration()
        serde.deserialize_xml(
            expected_xml.encode('utf-8'),
            expected_config,
            expect_tag='DataPipelineConfiguration',
        )
        expected_xml_bytes = serde.serialize_xml(expected_config, root='DataPipelineConfiguration')

        # Step 3: Manually construct configuration (same as Java testFullBuilder)
        filter_config = model.DataPipelineSourceFilterConfiguration(
            prefix_set=['prefix1/', 'prefix2/prefix3/'],
            object_media_types=['text', 'image', 'video'],
        )
        source = model.DataPipelineSource(
            input_bucket='my-bucket',
            input_data_scope='All',
            ignore_delete=True,
            filter_configuration=filter_config,
        )
        embedding_config = model.DataPipelineEmbeddingConfiguration(
            embedding_provider='bailian',
            api_key='xxxx',
            model='qwen2.5-vl-embedding',
            fps=1.0,
        )
        destination = model.DataPipelineDestination(
            vector_bucket_name='my-vector-bucket',
            vector_index_names=['my-index'],
            vector_key_prefix='vector-prefix/',
            object_tag_to_metadata=['key1', 'key2'],
            usermeta_to_metadata=['x-oss-meta-key1'],
        )
        error_config = model.DataPipelineError(
            error_mode='ignoreAndRecord',
            error_bucket='my-error-bucket',
            error_prefix='error-output/',
        )
        config = model.PutDataPipelineConfigurationConfiguration(
            data_pipeline_description='使用百炼多模态模型为业务数据向量化',
            sources=[source],
            data_pipeline_embedding_configuration=embedding_config,
            destination=destination,
            data_pipeline_error=error_config,
        )

        request = model.PutDataPipelineConfigurationRequest(
            data_pipeline_name='xml-pipeline',
            role='xml-role',
            configuration=config,
        )

        # Step 4: Verify parameters via serialize_input
        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutDataPipelineConfiguration',
            method='POST',
            parameters={'dataPipeline': '', 'action': 'putDataPipelineConfiguration'},
        ))
        self.assertEqual('xml-pipeline', op_input.parameters.get('dataPipelineName'))
        self.assertEqual('xml-role', op_input.parameters.get('role'))

        # Step 5: Serialize configuration to XML
        actual_xml_bytes = serde.serialize_xml(config, root='DataPipelineConfiguration')
        xml_content = actual_xml_bytes.decode('utf-8')

        # Step 6: Contains checks (equivalent to Java assertThat(xmlContent).contains(...))
        self.assertIn('<DataPipelineConfiguration>', xml_content)
        self.assertIn('<DataPipelineDescription>使用百炼多模态模型为业务数据向量化</DataPipelineDescription>', xml_content)
        self.assertIn('<InputBucket>my-bucket</InputBucket>', xml_content)
        self.assertIn('<EmbeddingProvider>bailian</EmbeddingProvider>', xml_content)
        self.assertIn('<VectorBucketName>my-vector-bucket</VectorBucketName>', xml_content)
        self.assertIn('<ErrorMode>ignoreAndRecord</ErrorMode>', xml_content)

        # Step 7: Exact comparison (equivalent to Java assertThat(xmlContent).isEqualTo(expectedXml))
        self.assertEqual(actual_xml_bytes, expected_xml_bytes)


class TestPutDataPipelineConfigurationResult(unittest.TestCase):
    def test_empty_constructor(self):
        result = model.PutDataPipelineConfigurationResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_xml_builder(self):
        # Reference: Java PutDataPipelineConfigurationResultTest.xmlBuilder - no body
        result = model.PutDataPipelineConfigurationResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({'x-oss-request-id': 'req-put-pipeline'}),
                http_response=MockHttpResponse(
                    status_code=200,
                    headers={'x-oss-request-id': 'req-put-pipeline'},
                    body=None,
                ),
            ),
        )
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)


# ==================== GetDataPipelineConfiguration ====================

class TestGetDataPipelineConfigurationRequest(unittest.TestCase):
    def test_empty_constructor(self):
        request = model.GetDataPipelineConfigurationRequest()
        self.assertIsNone(request.data_pipeline_name)

    def test_full_constructor(self):
        request = model.GetDataPipelineConfigurationRequest(data_pipeline_name='my-data-pipeline')
        self.assertEqual('my-data-pipeline', request.data_pipeline_name)

    def test_xml_builder(self):
        # Reference: Java GetDataPipelineConfigurationRequestTest.xmlBuilder
        request = model.GetDataPipelineConfigurationRequest(
            data_pipeline_name='my-data-pipeline',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetDataPipelineConfiguration',
            method='POST',
            parameters={'dataPipeline': '', 'action': 'getDataPipelineConfiguration'},
        ))

        self.assertEqual('my-data-pipeline', op_input.parameters.get('dataPipelineName'))


class TestGetDataPipelineConfigurationResult(unittest.TestCase):
    def test_empty_constructor(self):
        result = model.GetDataPipelineConfigurationResult()
        self.assertIsNone(result.configuration)

    def test_full_constructor(self):
        config = model.DataPipelineConfiguration(data_pipeline_name='p1')
        result = model.GetDataPipelineConfigurationResult(configuration=config)
        self.assertEqual('p1', result.configuration.data_pipeline_name)

    def test_xml_builder(self):
        # Reference: Java GetDataPipelineConfigurationResultTest.xmlBuilder
        xml_data = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<DataPipelineConfiguration>'
            b'  <DataPipelineName>my-data-pipeline</DataPipelineName>'
            b'  <DataPipelineDescription>test pipeline desc</DataPipelineDescription>'
            b'  <DataPipelineRole>my-data-pipeline-role</DataPipelineRole>'
            b'  <Status>Running</Status>'
            b'  <Phase>IncrementalScanning</Phase>'
            b'  <Sources>'
            b'      <InputBucket>my-bucket</InputBucket>'
            b'      <InputDataScope>All</InputDataScope>'
            b'      <IgnoreDelete>true</IgnoreDelete>'
            b'      <FilterConfiguration>'
            b'          <PrefixSet>prefix1/</PrefixSet>'
            b'          <PrefixSet>prefix2/prefix3/</PrefixSet>'
            b'          <ObjectMediaTypes>text</ObjectMediaTypes>'
            b'          <ObjectMediaTypes>image</ObjectMediaTypes>'
            b'          <ObjectMediaTypes>video</ObjectMediaTypes>'
            b'      </FilterConfiguration>'
            b'  </Sources>'
            b'  <DataPipelineEmbeddingConfiguration>'
            b'      <EmbeddingProvider>bailian</EmbeddingProvider>'
            b'      <ApiKey>xxxx</ApiKey>'
            b'      <Model>qwen2.5-vl-embedding</Model>'
            b'      <FPS>1.0</FPS>'
            b'  </DataPipelineEmbeddingConfiguration>'
            b'  <Destination>'
            b'      <VectorBucketName>my-vector-bucket</VectorBucketName>'
            b'      <VectorIndexNames>my-index</VectorIndexNames>'
            b'      <VectorKeyPrefix></VectorKeyPrefix>'
            b'      <ObjectTagToMetadata>key1</ObjectTagToMetadata>'
            b'      <ObjectTagToMetadata>key2</ObjectTagToMetadata>'
            b'      <UsermetaToMetadata>x-oss-meta-key1</UsermetaToMetadata>'
            b'  </Destination>'
            b'  <DataPipelineError>'
            b'      <ErrorMode>ignoreAndRecord</ErrorMode>'
            b'      <ErrorBucket>my-error-bucket</ErrorBucket>'
            b'      <ErrorPrefix>error-output/</ErrorPrefix>'
            b'  </DataPipelineError>'
            b'  <CreateTime>2021-06-29T14:50:13.011643661+08:00</CreateTime>'
            b'</DataPipelineConfiguration>'
        )

        result = model.GetDataPipelineConfigurationResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': 'req-get-pipeline',
                    'Content-Type': 'application/xml',
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    headers={
                        'x-oss-request-id': 'req-get-pipeline',
                        'Content-Type': 'application/xml',
                    },
                    body=xml_data,
                ),
            ),
            custom_deserializer=[serde.deserialize_output_xmlbody],
        )

        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.configuration)

        cfg = result.configuration
        self.assertEqual('my-data-pipeline', cfg.data_pipeline_name)
        self.assertEqual('test pipeline desc', cfg.data_pipeline_description)
        self.assertEqual('my-data-pipeline-role', cfg.data_pipeline_role)
        self.assertEqual('Running', cfg.status)
        self.assertEqual('IncrementalScanning', cfg.phase)
        self.assertEqual('2021-06-29T14:50:13.011643661+08:00', cfg.create_time)

        # Sources
        self.assertIsNotNone(cfg.sources)
        self.assertEqual(1, len(cfg.sources))
        src = cfg.sources[0]
        self.assertEqual('my-bucket', src.input_bucket)
        self.assertEqual('All', src.input_data_scope)
        self.assertTrue(src.ignore_delete)
        self.assertIsNotNone(src.filter_configuration)
        self.assertEqual(['prefix1/', 'prefix2/prefix3/'], src.filter_configuration.prefix_set)
        self.assertEqual(['text', 'image', 'video'], src.filter_configuration.object_media_types)

        # Embedding
        self.assertIsNotNone(cfg.data_pipeline_embedding_configuration)
        emb = cfg.data_pipeline_embedding_configuration
        self.assertEqual('bailian', emb.embedding_provider)
        self.assertEqual('xxxx', emb.api_key)
        self.assertEqual('qwen2.5-vl-embedding', emb.model)
        self.assertEqual(1.0, emb.fps)

        # Destination
        self.assertIsNotNone(cfg.destination)
        dest = cfg.destination
        self.assertEqual('my-vector-bucket', dest.vector_bucket_name)
        self.assertEqual(['my-index'], dest.vector_index_names)
        self.assertIsNone(dest.vector_key_prefix)
        self.assertEqual(['key1', 'key2'], dest.object_tag_to_metadata)
        self.assertEqual(['x-oss-meta-key1'], dest.usermeta_to_metadata)

        # Error
        self.assertIsNotNone(cfg.data_pipeline_error)
        err = cfg.data_pipeline_error
        self.assertEqual('ignoreAndRecord', err.error_mode)
        self.assertEqual('my-error-bucket', err.error_bucket)
        self.assertEqual('error-output/', err.error_prefix)


# ==================== DeleteDataPipelineConfiguration ====================

class TestDeleteDataPipelineConfigurationRequest(unittest.TestCase):
    def test_empty_constructor(self):
        request = model.DeleteDataPipelineConfigurationRequest()
        self.assertIsNone(request.data_pipeline_name)

    def test_full_constructor(self):
        request = model.DeleteDataPipelineConfigurationRequest(data_pipeline_name='my-data-pipeline')
        self.assertEqual('my-data-pipeline', request.data_pipeline_name)

    def test_xml_builder(self):
        # Reference: Java DeleteDataPipelineConfigurationRequestTest.xmlBuilder
        request = model.DeleteDataPipelineConfigurationRequest(
            data_pipeline_name='my-data-pipeline',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteDataPipelineConfiguration',
            method='POST',
            parameters={'dataPipeline': '', 'action': 'deleteDataPipelineConfiguration'},
        ))

        self.assertEqual('my-data-pipeline', op_input.parameters.get('dataPipelineName'))


class TestDeleteDataPipelineConfigurationResult(unittest.TestCase):
    def test_empty_constructor(self):
        result = model.DeleteDataPipelineConfigurationResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_xml_builder(self):
        # Reference: Java DeleteDataPipelineConfigurationResultTest.xmlBuilder - no body
        result = model.DeleteDataPipelineConfigurationResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=204,
                headers=CaseInsensitiveDict({'x-oss-request-id': 'req-delete-pipeline'}),
                http_response=MockHttpResponse(
                    status_code=204,
                    headers={'x-oss-request-id': 'req-delete-pipeline'},
                    body=None,
                ),
            ),
        )
        self.assertIsNotNone(result)
        self.assertEqual(204, result.status_code)


# ==================== ListDataPipelineConfigurations ====================

class TestListDataPipelineConfigurationsRequest(unittest.TestCase):
    def test_empty_constructor(self):
        request = model.ListDataPipelineConfigurationsRequest()
        self.assertIsNone(request.max_results)
        self.assertIsNone(request.prefix)
        self.assertIsNone(request.next_token)

    def test_full_constructor(self):
        request = model.ListDataPipelineConfigurationsRequest(
            max_results=50,
            prefix='xml-prefix',
            next_token='xml-token',
        )
        self.assertEqual(50, request.max_results)
        self.assertEqual('xml-prefix', request.prefix)
        self.assertEqual('xml-token', request.next_token)

    def test_xml_builder(self):
        # Reference: Java ListDataPipelineConfigurationsRequestTest.xmlBuilder
        request = model.ListDataPipelineConfigurationsRequest(
            max_results=50,
            prefix='xml-prefix',
            next_token='xml-token',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='ListDataPipelineConfigurations',
            method='POST',
            parameters={'dataPipeline': '', 'action': 'listDataPipelineConfigurations'},
        ))

        self.assertEqual('50', op_input.parameters.get('maxResults'))
        self.assertEqual('xml-prefix', op_input.parameters.get('prefix'))
        self.assertEqual('xml-token', op_input.parameters.get('nextToken'))


class TestListDataPipelineConfigurationsResult(unittest.TestCase):
    def test_empty_constructor(self):
        result = model.ListDataPipelineConfigurationsResult()
        self.assertIsNone(result.data_pipeline_configurations)
        self.assertIsNone(result.next_token)

    def test_full_constructor(self):
        configs = [
            model.DataPipelineConfiguration(data_pipeline_name='p1', status='Running'),
            model.DataPipelineConfiguration(data_pipeline_name='p2', status='Paused'),
        ]
        result = model.ListDataPipelineConfigurationsResult(
            data_pipeline_configurations=model.DataPipelineConfigurations(data_pipeline_configuration=configs),
            next_token='tok',
        )
        self.assertEqual(2, len(result.data_pipeline_configurations.data_pipeline_configuration))
        self.assertEqual('tok', result.next_token)

    def test_xml_builder(self):
        # Reference: Java ListDataPipelineConfigurationsResultTest.xmlBuilder
        xml_data = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<ListDataPipelineConfigurationsResult>'
            b'  <DataPipelineConfigurations>'
            b'  <DataPipelineConfiguration>'
            b'    <DataPipelineName>my-data-pipeline</DataPipelineName>'
            b'    <DataPipelineDescription>test pipeline desc</DataPipelineDescription>'
            b'    <DataPipelineRole>my-data-pipeline-role</DataPipelineRole>'
            b'    <Status>Running</Status>'
            b'    <Phase>IncrementalScanning</Phase>'
            b'    <Sources>'
            b'        <InputBucket>my-bucket</InputBucket>'
            b'        <InputDataScope>All</InputDataScope>'
            b'        <IgnoreDelete>true</IgnoreDelete>'
            b'        <FilterConfiguration>'
            b'            <PrefixSet>prefix1/</PrefixSet>'
            b'            <PrefixSet>prefix2/prefix3/</PrefixSet>'
            b'            <ObjectMediaTypes>text</ObjectMediaTypes>'
            b'            <ObjectMediaTypes>image</ObjectMediaTypes>'
            b'            <ObjectMediaTypes>video</ObjectMediaTypes>'
            b'        </FilterConfiguration>'
            b'    </Sources>'
            b'    <DataPipelineEmbeddingConfiguration>'
            b'        <EmbeddingProvider>bailian</EmbeddingProvider>'
            b'        <ApiKey>xxxx</ApiKey>'
            b'        <Model>qwen2.5-vl-embedding</Model>'
            b'        <FPS>1.0</FPS>'
            b'    </DataPipelineEmbeddingConfiguration>'
            b'    <Destination>'
            b'        <VectorBucketName>my-vector-bucket</VectorBucketName>'
            b'        <VectorIndexNames>my-index</VectorIndexNames>'
            b'        <VectorKeyPrefix></VectorKeyPrefix>'
            b'        <ObjectTagToMetadata>key1</ObjectTagToMetadata>'
            b'        <ObjectTagToMetadata>key2</ObjectTagToMetadata>'
            b'        <UsermetaToMetadata>x-oss-meta-key1</UsermetaToMetadata>'
            b'    </Destination>'
            b'    <DataPipelineError>'
            b'        <ErrorMode>ignoreAndRecord</ErrorMode>'
            b'        <ErrorBucket>my-error-bucket</ErrorBucket>'
            b'        <ErrorPrefix>error-output/</ErrorPrefix>'
            b'    </DataPipelineError>'
            b'    <CreateTime>2021-06-29T14:50:13.011643661+08:00</CreateTime>'
            b'  </DataPipelineConfiguration>'
            b'  </DataPipelineConfigurations>'
            b'  <NextToken>xxx</NextToken>'
            b'</ListDataPipelineConfigurationsResult>'
        )

        result = model.ListDataPipelineConfigurationsResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': 'req-list-pipelines',
                    'Content-Type': 'application/xml',
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    headers={
                        'x-oss-request-id': 'req-list-pipelines',
                        'Content-Type': 'application/xml',
                    },
                    body=xml_data,
                ),
            ),
            custom_deserializer=[serde.deserialize_output_xmlbody],
        )

        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual('xxx', result.next_token)

        # Verify configurations
        self.assertIsNotNone(result.data_pipeline_configurations)
        self.assertEqual(1, len(result.data_pipeline_configurations.data_pipeline_configuration))

        cfg = result.data_pipeline_configurations.data_pipeline_configuration[0]
        self.assertEqual('my-data-pipeline', cfg.data_pipeline_name)
        self.assertEqual('test pipeline desc', cfg.data_pipeline_description)
        self.assertEqual('my-data-pipeline-role', cfg.data_pipeline_role)
        self.assertEqual('Running', cfg.status)
        self.assertEqual('IncrementalScanning', cfg.phase)
        self.assertEqual('2021-06-29T14:50:13.011643661+08:00', cfg.create_time)

        # Sources
        self.assertIsNotNone(cfg.sources)
        self.assertEqual(1, len(cfg.sources))
        self.assertEqual('my-bucket', cfg.sources[0].input_bucket)
        self.assertEqual('All', cfg.sources[0].input_data_scope)
        self.assertTrue(cfg.sources[0].ignore_delete)
        self.assertIsNotNone(cfg.sources[0].filter_configuration)
        self.assertEqual(['prefix1/', 'prefix2/prefix3/'], cfg.sources[0].filter_configuration.prefix_set)
        self.assertEqual(['text', 'image', 'video'], cfg.sources[0].filter_configuration.object_media_types)

        # Embedding
        self.assertIsNotNone(cfg.data_pipeline_embedding_configuration)
        self.assertEqual('bailian', cfg.data_pipeline_embedding_configuration.embedding_provider)
        self.assertEqual('xxxx', cfg.data_pipeline_embedding_configuration.api_key)
        self.assertEqual('qwen2.5-vl-embedding', cfg.data_pipeline_embedding_configuration.model)
        self.assertEqual(1.0, cfg.data_pipeline_embedding_configuration.fps)

        # Destination
        self.assertIsNotNone(cfg.destination)
        self.assertEqual('my-vector-bucket', cfg.destination.vector_bucket_name)
        self.assertEqual(['my-index'], cfg.destination.vector_index_names)
        self.assertIsNone(cfg.destination.vector_key_prefix)
        self.assertEqual(['key1', 'key2'], cfg.destination.object_tag_to_metadata)
        self.assertEqual(['x-oss-meta-key1'], cfg.destination.usermeta_to_metadata)

        # Error
        self.assertIsNotNone(cfg.data_pipeline_error)
        self.assertEqual('ignoreAndRecord', cfg.data_pipeline_error.error_mode)
        self.assertEqual('my-error-bucket', cfg.data_pipeline_error.error_bucket)
        self.assertEqual('error-output/', cfg.data_pipeline_error.error_prefix)


# ==================== PauseDataPipeline ====================

class TestPauseDataPipelineRequest(unittest.TestCase):
    def test_empty_constructor(self):
        request = model.PauseDataPipelineRequest()
        self.assertIsNone(request.data_pipeline_name)

    def test_full_constructor(self):
        request = model.PauseDataPipelineRequest(data_pipeline_name='my-data-pipeline')
        self.assertEqual('my-data-pipeline', request.data_pipeline_name)

    def test_xml_builder(self):
        # Reference: Java PauseDataPipelineRequestTest.xmlBuilder
        request = model.PauseDataPipelineRequest(data_pipeline_name='my-data-pipeline')

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PauseDataPipeline',
            method='POST',
            parameters={'dataPipeline': '', 'action': 'pauseDataPipeline'},
        ))

        self.assertEqual('my-data-pipeline', op_input.parameters.get('dataPipelineName'))


class TestPauseDataPipelineResult(unittest.TestCase):
    def test_empty_constructor(self):
        result = model.PauseDataPipelineResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_xml_builder(self):
        # Reference: Java PauseDataPipelineResultTest.xmlBuilder - no body
        result = model.PauseDataPipelineResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({'x-oss-request-id': 'req-pause-pipeline'}),
                http_response=MockHttpResponse(
                    status_code=200,
                    headers={'x-oss-request-id': 'req-pause-pipeline'},
                    body=None,
                ),
            ),
        )
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)


# ==================== RestartDataPipeline ====================

class TestRestartDataPipelineRequest(unittest.TestCase):
    def test_empty_constructor(self):
        request = model.RestartDataPipelineRequest()
        self.assertIsNone(request.data_pipeline_name)

    def test_full_constructor(self):
        request = model.RestartDataPipelineRequest(data_pipeline_name='my-data-pipeline')
        self.assertEqual('my-data-pipeline', request.data_pipeline_name)

    def test_xml_builder(self):
        # Reference: Java RestartDataPipelineRequestTest.xmlBuilder
        request = model.RestartDataPipelineRequest(data_pipeline_name='my-data-pipeline')

        op_input = serde.serialize_input(request, OperationInput(
            op_name='RestartDataPipeline',
            method='POST',
            parameters={'dataPipeline': '', 'action': 'restartDataPipeline'},
        ))

        self.assertEqual('my-data-pipeline', op_input.parameters.get('dataPipelineName'))


class TestRestartDataPipelineResult(unittest.TestCase):
    def test_empty_constructor(self):
        result = model.RestartDataPipelineResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_xml_builder(self):
        # Reference: Java RestartDataPipelineResultTest.xmlBuilder - no body
        result = model.RestartDataPipelineResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({'x-oss-request-id': 'req-restart-pipeline'}),
                http_response=MockHttpResponse(
                    status_code=200,
                    headers={'x-oss-request-id': 'req-restart-pipeline'},
                    body=None,
                ),
            ),
        )
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)


if __name__ == '__main__':
    unittest.main()
