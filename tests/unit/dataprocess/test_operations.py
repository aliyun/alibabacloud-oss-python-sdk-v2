# -*- coding: utf-8 -*-
"""Unit tests for dataprocess operations."""

import unittest
from alibabacloud_oss_v2.dataprocess import models, operations
from alibabacloud_oss_v2.types import CaseInsensitiveDict
from tests.unit import MockHttpResponse, mock_client


def _make_client():
    """Create a mock client for testing."""
    return mock_client(
        request_fn=None,
        response_fn=lambda: MockHttpResponse(
            status_code=200,
            headers={
                'x-oss-request-id': 'test-request-id',
                'x-oss-hash-crc64ecma': '316181249502703****',
            },
            body=b'<?xml version="1.0" encoding="UTF-8"?><CreateDatasetResponse><Dataset><DatasetName>test-ds</DatasetName></Dataset></CreateDatasetResponse>',
        ),
    )


def _make_client_with_body(xml_body):
    """Create a mock client that returns the given XML body."""
    return mock_client(
        request_fn=None,
        response_fn=lambda: MockHttpResponse(
            status_code=200,
            headers={
                'x-oss-request-id': 'test-request-id',
            },
            body=xml_body,
        ),
    )


def _make_empty_client():
    """Create a mock client with no body."""
    return mock_client(
        request_fn=None,
        response_fn=lambda: MockHttpResponse(
            status_code=200,
            headers={
                'x-oss-request-id': 'test-request-id',
            },
            body=None,
        ),
    )


class TestDatasetOperations(unittest.TestCase):

    def test_create_dataset(self):
        client = _make_client()
        request = models.CreateDatasetRequest(
            bucket='test-bucket',
            dataset_name='test-ds',
        )
        result = operations.create_dataset(client, request)
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.dataset)
        self.assertEqual('test-ds', result.dataset.dataset_name)

    def test_get_dataset(self):
        xml = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<GetDatasetResponse><Dataset><DatasetName>ds1</DatasetName>'
            b'<Description>desc</Description></Dataset></GetDatasetResponse>'
        )
        client = _make_client_with_body(xml)
        result = operations.get_dataset(client, models.GetDatasetRequest(
            bucket='test-bucket', dataset_name='ds1',
        ))
        self.assertEqual('ds1', result.dataset.dataset_name)
        self.assertEqual('desc', result.dataset.description)

    def test_update_dataset(self):
        xml = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<UpdateDatasetResponse><Dataset><DatasetName>ds1</DatasetName></Dataset></UpdateDatasetResponse>'
        )
        client = _make_client_with_body(xml)
        result = operations.update_dataset(client, models.UpdateDatasetRequest(
            bucket='test-bucket', dataset_name='ds1', description='updated',
        ))
        self.assertIsNotNone(result.dataset)

    def test_delete_dataset(self):
        client = _make_empty_client()
        result = operations.delete_dataset(client, models.DeleteDatasetRequest(
            bucket='test-bucket', dataset_name='ds1',
        ))
        self.assertEqual(200, result.status_code)

    def test_list_datasets(self):
        xml = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<ListDatasetsResponse>'
            b'<Datasets><Dataset><DatasetName>ds1</DatasetName></Dataset></Datasets>'
            b'<NextToken>tok</NextToken>'
            b'</ListDatasetsResponse>'
        )
        client = _make_client_with_body(xml)
        result = operations.list_datasets(client, models.ListDatasetsRequest(bucket='test-bucket'))
        self.assertEqual(1, len(result.datasets.dataset))
        self.assertEqual('tok', result.next_token)

    def test_delete_file_meta(self):
        client = _make_empty_client()
        result = operations.delete_file_meta(client, models.DeleteFileMetaRequest(
            bucket='test-bucket', dataset_name='ds1', uri='oss://test-bucket/file.jpg',
        ))
        self.assertEqual(200, result.status_code)


class TestQueryOperations(unittest.TestCase):

    def test_simple_query(self):
        xml = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<MetaQuery><NextToken>n1</NextToken></MetaQuery>'
        )
        client = _make_client_with_body(xml)
        result = operations.simple_query(client, models.SimpleQueryRequest(
            bucket='test-bucket', dataset_name='ds1',
        ))
        self.assertEqual('n1', result.next_token)

    def test_semantic_query(self):
        xml = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<MetaQuery><Files><File><Filename>f.mp4</Filename></File></Files></MetaQuery>'
        )
        client = _make_client_with_body(xml)
        result = operations.semantic_query(client, models.SemanticQueryRequest(
            bucket='test-bucket', dataset_name='ds1', query='search text',
        ))
        self.assertEqual(1, len(result.files.file))
        self.assertEqual('f.mp4', result.files.file[0].filename)


class TestMetaQueryOperations(unittest.TestCase):

    def test_open_meta_query(self):
        client = _make_empty_client()
        body = models.MetaQueryOpenBody()
        result = operations.open_meta_query(client, models.OpenMetaQueryRequest(
            bucket='test-bucket', meta_query_body=body,
        ))
        self.assertEqual(200, result.status_code)

    def test_get_meta_query_status(self):
        xml = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<MetaQueryStatus><State>Running</State><Phase>FullIndexing</Phase><MetaQueryMode>query</MetaQueryMode></MetaQueryStatus>'
        )
        client = _make_client_with_body(xml)
        result = operations.get_meta_query_status(client, models.GetMetaQueryStatusRequest(bucket='test-bucket'))
        self.assertEqual('Running', result.status.state)
        self.assertEqual('FullIndexing', result.status.phase)
        self.assertEqual('query', result.status.meta_query_mode)

    def test_close_meta_query(self):
        client = _make_empty_client()
        result = operations.close_meta_query(client, models.CloseMetaQueryRequest(bucket='test-bucket'))
        self.assertEqual(200, result.status_code)

    def test_do_meta_query(self):
        xml = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<MetaQuery><NextToken>n1</NextToken><TotalHits>10</TotalHits></MetaQuery>'
        )
        client = _make_client_with_body(xml)
        body = models.MetaQueryDoBody(query='test')
        result = operations.do_meta_query(client, models.DoMetaQueryRequest(
            bucket='test-bucket', meta_query_body=body,
        ))
        self.assertEqual('n1', result.next_token)
        self.assertEqual(10, result.total_hits)


class TestSmartClusterOperations(unittest.TestCase):

    def test_create_smart_cluster(self):
        xml = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<CreateSmartClusterResponse>'
            b'<ObjectId>sc-1</ObjectId>'
            b'</CreateSmartClusterResponse>'
        )
        client = _make_client_with_body(xml)
        result = operations.create_smart_cluster(client, models.CreateSmartClusterRequest(
            bucket='test-bucket', dataset_name='ds1', name='c1', cluster_type='face',
        ))
        self.assertEqual('sc-1', result.object_id)

    def test_get_smart_cluster(self):
        xml = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<GetSmartClusterResponse><SmartCluster>'
            b'<ObjectId>sc-1</ObjectId>'
            b'<Name>c1</Name>'
            b'</SmartCluster></GetSmartClusterResponse>'
        )
        client = _make_client_with_body(xml)
        result = operations.get_smart_cluster(client, models.GetSmartClusterRequest(
            bucket='test-bucket', dataset_name='ds1', object_id='sc-1',
        ))
        self.assertIsNotNone(result.smart_cluster)

    def test_update_smart_cluster(self):
        xml = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<UpdateSmartClusterResponse>'
            b'<ObjectId>sc-1</ObjectId>'
            b'</UpdateSmartClusterResponse>'
        )
        client = _make_client_with_body(xml)
        result = operations.update_smart_cluster(client, models.UpdateSmartClusterRequest(
            bucket='test-bucket', dataset_name='ds1', object_id='sc-1',
        ))
        self.assertEqual('sc-1', result.object_id)

    def test_delete_smart_cluster(self):
        client = _make_empty_client()
        result = operations.delete_smart_cluster(client, models.DeleteSmartClusterRequest(
            bucket='test-bucket', dataset_name='ds1', object_id='sc-1',
        ))
        self.assertEqual(200, result.status_code)

    def test_list_smart_clusters(self):
        xml = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<ListSmartClustersResponse>'
            b'<SmartClusters><SmartCluster><ObjectId>sc-1</ObjectId></SmartCluster></SmartClusters>'
            b'<NextToken>tok</NextToken>'
            b'</ListSmartClustersResponse>'
        )
        client = _make_client_with_body(xml)
        result = operations.list_smart_clusters(client, models.ListSmartClustersRequest(
            bucket='test-bucket', dataset_name='ds1',
        ))
        self.assertEqual(1, len(result.smart_clusters.smart_cluster))
        self.assertEqual('tok', result.next_token)


class TestDataPipelineOperations(unittest.TestCase):

    def test_put_data_pipeline_configuration(self):
        client = _make_empty_client()
        config = models.PutDataPipelineConfigurationConfiguration(
            data_pipeline_description='test',
        )
        result = operations.put_data_pipeline_configuration(client, models.PutDataPipelineConfigurationRequest(
            data_pipeline_name='p1', configuration=config,
        ))
        self.assertEqual(200, result.status_code)

    def test_get_data_pipeline_configuration(self):
        xml = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<DataPipelineConfiguration><DataPipelineName>p1</DataPipelineName><Status>Running</Status></DataPipelineConfiguration>'
        )
        client = _make_client_with_body(xml)
        result = operations.get_data_pipeline_configuration(client, models.GetDataPipelineConfigurationRequest(
            data_pipeline_name='p1',
        ))
        self.assertEqual('p1', result.configuration.data_pipeline_name)

    def test_put_data_pipeline_configuration_v2(self):
        requests = []
        client = mock_client(
            request_fn=lambda request: requests.append(request),
            response_fn=lambda: MockHttpResponse(
                status_code=200,
                headers={'x-oss-request-id': 'test-request-id'},
                body=None,
            ),
        )
        config = models.PutDataPipelineConfigurationConfiguration(
            model_tier='standard',
            data_pipeline_data_process_configuration=models.DataPipelineDataProcessConfiguration(
                search_mode='fast',
            ),
            destination=models.DataPipelineDestination(
                image_embedding=models.ImageEmbedding(
                    bucket='vector-bucket',
                    index_name='image-index',
                ),
            ),
        )

        result = operations.put_data_pipeline_configuration(
            client,
            models.PutDataPipelineConfigurationRequest(
                data_pipeline_name='p1',
                configuration=config,
            ),
        )

        self.assertEqual(200, result.status_code)
        self.assertEqual(1, len(requests))
        self.assertEqual('POST', requests[0].method)
        self.assertEqual('application/xml', requests[0].headers.get('Content-Type'))
        self.assertIsNotNone(requests[0].headers.get('Content-MD5'))
        self.assertIn('dataPipelineName=p1', requests[0].url)
        self.assertIn('action=putDataPipelineConfiguration', requests[0].url)
        self.assertIn(b'<ModelTier>standard</ModelTier>', requests[0].body)
        self.assertIn(b'<SearchMode>fast</SearchMode>', requests[0].body)
        self.assertIn(b'<ImageEmbedding>', requests[0].body)

    def test_get_data_pipeline_configuration_v2(self):
        xml = (
            b'<DataPipelineConfiguration>'
            b'<DataPipelineName>p1</DataPipelineName>'
            b'<Status>Running</Status><Phase>IncrementalScanning</Phase>'
            b'<Sources><InputBucket>source-bucket</InputBucket>'
            b'<IgnoreDelete>false</IgnoreDelete></Sources>'
            b'<ModelTier>standard</ModelTier>'
            b'<DataPipelineDataProcessConfiguration><SearchMode>fast</SearchMode>'
            b'<Insights><Video><FrameEmbedding><Snapshot><Mode>dhash</Mode>'
            b'<Number>20</Number></Snapshot></FrameEmbedding></Video></Insights>'
            b'</DataPipelineDataProcessConfiguration>'
            b'<Destination><ImageEmbedding><Bucket>vector-bucket</Bucket>'
            b'<IndexName>image-index</IndexName><Prefix>v2</Prefix>'
            b'</ImageEmbedding></Destination>'
            b'</DataPipelineConfiguration>'
        )
        client = _make_client_with_body(xml)

        result = operations.get_data_pipeline_configuration(
            client,
            models.GetDataPipelineConfigurationRequest(data_pipeline_name='p1'),
        )

        self.assertEqual('standard', result.configuration.model_tier)
        self.assertEqual('Running', result.configuration.status)
        self.assertEqual('IncrementalScanning', result.configuration.phase)
        self.assertFalse(result.configuration.sources[0].ignore_delete)
        process_config = result.configuration.data_pipeline_data_process_configuration
        self.assertEqual('fast', process_config.search_mode)
        snapshot = process_config.insights.video.frame_embedding.snapshot
        self.assertEqual('dhash', snapshot.mode)
        self.assertEqual(20, snapshot.number)
        self.assertEqual('image-index', result.configuration.destination.image_embedding.index_name)
        self.assertEqual('v2', result.configuration.destination.image_embedding.prefix)

    def test_delete_data_pipeline_configuration(self):
        client = _make_empty_client()
        result = operations.delete_data_pipeline_configuration(client, models.DeleteDataPipelineConfigurationRequest(
            data_pipeline_name='p1',
        ))
        self.assertEqual(200, result.status_code)

    def test_list_data_pipeline_configurations(self):
        requests = []
        xml = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<ListDataPipelineConfigurationsResult>'
            b'<DataPipelineConfigurations><DataPipelineConfiguration><DataPipelineName>p1</DataPipelineName></DataPipelineConfiguration></DataPipelineConfigurations>'
            b'<NextToken>tok</NextToken>'
            b'</ListDataPipelineConfigurationsResult>'
        )
        client = mock_client(
            request_fn=lambda request: requests.append(request),
            response_fn=lambda: MockHttpResponse(
                status_code=200,
                headers={'x-oss-request-id': 'test-request-id'},
                body=xml,
            ),
        )
        result = operations.list_data_pipeline_configurations(
            client,
            models.ListDataPipelineConfigurationsRequest(input_bucket='source-bucket'),
        )
        self.assertEqual(1, len(result.data_pipeline_configurations.data_pipeline_configuration))
        self.assertEqual('tok', result.next_token)
        self.assertEqual(1, len(requests))
        self.assertIn('inputBucket=source-bucket', requests[0].url)

    def test_list_data_pipeline_configurations_v2(self):
        xml = (
            b'<ListDataPipelineConfigurationsResult>'
            b'<DataPipelineConfigurations><DataPipelineConfiguration>'
            b'<DataPipelineName>p1</DataPipelineName>'
            b'<Status>Running</Status><Phase>IncrementalScanning</Phase>'
            b'<Sources><InputBucket>source-bucket</InputBucket>'
            b'<IgnoreDelete>false</IgnoreDelete></Sources>'
            b'<ModelTier>standard</ModelTier>'
            b'<DataPipelineDataProcessConfiguration><SearchMode>balanced</SearchMode>'
            b'<Insights><Image><Caption><Prompt>Describe the image.</Prompt>'
            b'</Caption></Image></Insights></DataPipelineDataProcessConfiguration>'
            b'<Destination><ImageEmbedding><Bucket>vector-bucket</Bucket>'
            b'<IndexName>image-index</IndexName><Prefix>v2</Prefix>'
            b'</ImageEmbedding></Destination>'
            b'</DataPipelineConfiguration></DataPipelineConfigurations>'
            b'<NextToken>next</NextToken>'
            b'</ListDataPipelineConfigurationsResult>'
        )
        client = _make_client_with_body(xml)

        result = operations.list_data_pipeline_configurations(
            client,
            models.ListDataPipelineConfigurationsRequest(input_bucket='source-bucket'),
        )

        self.assertEqual('next', result.next_token)
        configurations = result.data_pipeline_configurations.data_pipeline_configuration
        self.assertEqual(1, len(configurations))
        config = configurations[0]
        self.assertEqual('p1', config.data_pipeline_name)
        self.assertEqual('standard', config.model_tier)
        self.assertFalse(config.sources[0].ignore_delete)
        self.assertEqual(
            'Describe the image.',
            config.data_pipeline_data_process_configuration.insights.image.caption.prompt,
        )
        self.assertEqual('image-index', config.destination.image_embedding.index_name)
        self.assertIsNone(config.destination.image_text_embedding)
        self.assertIsNone(config.destination.video_frame_embedding)
        self.assertIsNone(config.destination.video_text_embedding)
        self.assertIsNone(config.destination.document_chunk_embedding)

    def test_pause_data_pipeline(self):
        client = _make_empty_client()
        result = operations.pause_data_pipeline(client, models.PauseDataPipelineRequest(
            data_pipeline_name='p1',
        ))
        self.assertEqual(200, result.status_code)

    def test_restart_data_pipeline(self):
        client = _make_empty_client()
        result = operations.restart_data_pipeline(client, models.RestartDataPipelineRequest(
            data_pipeline_name='p1',
        ))
        self.assertEqual(200, result.status_code)


if __name__ == '__main__':
    unittest.main()
