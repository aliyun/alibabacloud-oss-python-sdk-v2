# pylint: skip-file
"""Unit tests for dataprocess dataset models."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))
import json
import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.dataprocess.models import dataset_basic as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict
from tests.unit import MockHttpResponse


# ==================== Sub-model tests ====================

class TestWorkflowParameter(unittest.TestCase):
    def test_empty_constructor(self):
        param = model.WorkflowParameter()
        self.assertIsNone(param.name)
        self.assertIsNone(param.value)

    def test_full_constructor(self):
        param = model.WorkflowParameter(name='ImageInsightEnable', value='True')
        self.assertEqual('ImageInsightEnable', param.name)
        self.assertEqual('True', param.value)


class TestWorkflowParameters(unittest.TestCase):
    def test_empty_constructor(self):
        wps = model.WorkflowParameters()
        self.assertIsNone(wps.workflow_parameters)

    def test_full_constructor(self):
        params = [
            model.WorkflowParameter(name='k1', value='v1'),
            model.WorkflowParameter(name='k2', value='v2'),
        ]
        wps = model.WorkflowParameters(workflow_parameters=params)
        self.assertEqual(2, len(wps.workflow_parameters))
        self.assertEqual('k1', wps.workflow_parameters[0].name)
        self.assertEqual('v1', wps.workflow_parameters[0].value)


class TestEnableConfig(unittest.TestCase):
    def test_empty_constructor(self):
        cfg = model.EnableConfig()
        self.assertIsNone(cfg.enable)

    def test_full_constructor(self):
        cfg = model.EnableConfig(enable='true')
        self.assertEqual('true', cfg.enable)


class TestInsightsLabelItem(unittest.TestCase):
    def test_empty_constructor(self):
        item = model.InsightsLabelItem()
        self.assertIsNone(item.name)
        self.assertIsNone(item.description)

    def test_full_constructor(self):
        item = model.InsightsLabelItem(name='cat', description='cat label')
        self.assertEqual('cat', item.name)
        self.assertEqual('cat label', item.description)


class TestInsightsLabels(unittest.TestCase):
    def test_empty_constructor(self):
        labels = model.InsightsLabels()
        self.assertIsNone(labels.label)

    def test_full_constructor(self):
        labels = model.InsightsLabels(label=[
            model.InsightsLabelItem(name='cat', description='cat label'),
            model.InsightsLabelItem(name='dog', description='dog label'),
        ])
        self.assertEqual(2, len(labels.label))
        self.assertEqual('cat', labels.label[0].name)
        self.assertEqual('dog', labels.label[1].name)


class TestInsightsCaptionConfig(unittest.TestCase):
    def test_empty_constructor(self):
        cfg = model.InsightsCaptionConfig()
        self.assertIsNone(cfg.enable)
        self.assertIsNone(cfg.prompt)

    def test_full_constructor(self):
        cfg = model.InsightsCaptionConfig(enable='true', prompt='describe the image')
        self.assertEqual('true', cfg.enable)
        self.assertEqual('describe the image', cfg.prompt)


class TestInsightsImageConfig(unittest.TestCase):
    def test_empty_constructor(self):
        cfg = model.InsightsImageConfig()
        self.assertIsNone(cfg.caption)

    def test_full_constructor(self):
        cfg = model.InsightsImageConfig(
            caption=model.InsightsCaptionConfig(enable='true', prompt='describe')
        )
        self.assertIsNotNone(cfg.caption)
        self.assertEqual('true', cfg.caption.enable)
        self.assertEqual('describe', cfg.caption.prompt)


class TestInsightsVideoCaptionConfig(unittest.TestCase):
    def test_empty_constructor(self):
        cfg = model.InsightsVideoCaptionConfig()
        self.assertIsNone(cfg.enable)
        self.assertIsNone(cfg.prompt)
        self.assertIsNone(cfg.person_reference)

    def test_full_constructor(self):
        cfg = model.InsightsVideoCaptionConfig(
            enable='true',
            prompt='describe video',
            person_reference=model.EnableConfig(enable='true'),
        )
        self.assertEqual('true', cfg.enable)
        self.assertEqual('describe video', cfg.prompt)
        self.assertEqual('true', cfg.person_reference.enable)


class TestInsightsLabelUserDefinedConfig(unittest.TestCase):
    def test_empty_constructor(self):
        cfg = model.InsightsLabelUserDefinedConfig()
        self.assertIsNone(cfg.enable)
        self.assertIsNone(cfg.mode)
        self.assertIsNone(cfg.labels)

    def test_full_constructor(self):
        cfg = model.InsightsLabelUserDefinedConfig(
            enable='true',
            mode='tagging',
            labels=model.InsightsLabels(
                label=[model.InsightsLabelItem(name='dog', description='dog label')],
            ),
        )
        self.assertEqual('true', cfg.enable)
        self.assertEqual('tagging', cfg.mode)
        self.assertEqual(1, len(cfg.labels.label))
        self.assertEqual('dog', cfg.labels.label[0].name)

    def test_xml_builder(self):
        xml_data = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<UserDefined>'
            b'<Enable>true</Enable>'
            b'<Mode>tagging</Mode>'
            b'<Labels><Label><Name>dog</Name><Description>dog label</Description></Label></Labels>'
            b'</UserDefined>'
        )
        cfg = model.InsightsLabelUserDefinedConfig()
        serde.deserialize_xml(xml_data=xml_data, obj=cfg)
        self.assertEqual('true', cfg.enable)
        self.assertEqual('tagging', cfg.mode)
        self.assertIsNotNone(cfg.labels)
        self.assertEqual(1, len(cfg.labels.label))
        self.assertEqual('dog', cfg.labels.label[0].name)
        self.assertEqual('dog label', cfg.labels.label[0].description)


class TestInsightsLabelHighlightConfig(unittest.TestCase):
    def test_empty_constructor(self):
        cfg = model.InsightsLabelHighlightConfig()
        self.assertIsNone(cfg.enable)
        self.assertIsNone(cfg.labels)

    def test_full_constructor(self):
        cfg = model.InsightsLabelHighlightConfig(
            enable='true',
            labels=model.InsightsLabels(
                label=[model.InsightsLabelItem(name='dog', description='dog label')],
            ),
        )
        self.assertEqual('true', cfg.enable)
        self.assertEqual(1, len(cfg.labels.label))
        self.assertEqual('dog', cfg.labels.label[0].name)


class TestInsightsVideoLabelConfig(unittest.TestCase):
    def test_empty_constructor(self):
        cfg = model.InsightsVideoLabelConfig()
        self.assertIsNone(cfg.system)
        self.assertIsNone(cfg.user_defined)
        self.assertIsNone(cfg.highlight)

    def test_full_constructor(self):
        cfg = model.InsightsVideoLabelConfig(
            system=model.EnableConfig(enable='true'),
            user_defined=model.InsightsLabelUserDefinedConfig(enable='true', mode='custom'),
            highlight=model.InsightsLabelHighlightConfig(enable='true'),
        )
        self.assertEqual('true', cfg.system.enable)
        self.assertEqual('custom', cfg.user_defined.mode)
        self.assertEqual('true', cfg.highlight.enable)


class TestInsightsVideoConfig(unittest.TestCase):
    def test_empty_constructor(self):
        cfg = model.InsightsVideoConfig()
        self.assertIsNone(cfg.caption)
        self.assertIsNone(cfg.label)
        self.assertIsNone(cfg.multi_stream)

    def test_full_constructor(self):
        cfg = model.InsightsVideoConfig(
            caption=model.InsightsVideoCaptionConfig(enable='true'),
            label=model.InsightsVideoLabelConfig(
                user_defined=model.InsightsLabelUserDefinedConfig(enable='true'),
            ),
            multi_stream=model.EnableConfig(enable='false'),
        )
        self.assertEqual('true', cfg.caption.enable)
        self.assertEqual('true', cfg.label.user_defined.enable)
        self.assertEqual('false', cfg.multi_stream.enable)


class TestReverseImageConfig(unittest.TestCase):
    def test_empty_constructor(self):
        cfg = model.ReverseImageConfig()
        self.assertIsNone(cfg.image)
        self.assertIsNone(cfg.video)

    def test_full_constructor(self):
        cfg = model.ReverseImageConfig(
            image=model.EnableConfig(enable='true'),
            video=model.EnableConfig(enable='false'),
        )
        self.assertEqual('true', cfg.image.enable)
        self.assertEqual('false', cfg.video.enable)


class TestInsightsConfig(unittest.TestCase):
    def test_empty_constructor(self):
        cfg = model.InsightsConfig()
        self.assertIsNone(cfg.language)
        self.assertIsNone(cfg.image)
        self.assertIsNone(cfg.video)

    def test_full_constructor(self):
        cfg = model.InsightsConfig(
            language='en',
            image=model.InsightsImageConfig(
                caption=model.InsightsCaptionConfig(enable='true', prompt='describe'),
            ),
            video=model.InsightsVideoConfig(
                caption=model.InsightsVideoCaptionConfig(enable='true'),
                label=model.InsightsVideoLabelConfig(
                    user_defined=model.InsightsLabelUserDefinedConfig(enable='true'),
                ),
                multi_stream=model.EnableConfig(enable='false'),
            ),
        )
        self.assertEqual('en', cfg.language)
        self.assertEqual('true', cfg.image.caption.enable)
        self.assertEqual('describe', cfg.image.caption.prompt)
        self.assertEqual('true', cfg.video.caption.enable)
        self.assertEqual('true', cfg.video.label.user_defined.enable)
        self.assertEqual('false', cfg.video.multi_stream.enable)


class TestSmartClusterFigureConfig(unittest.TestCase):
    def test_empty_constructor(self):
        cfg = model.SmartClusterFigureConfig()
        self.assertIsNone(cfg.auto_generate)
        self.assertIsNone(cfg.auto_clustering)
        self.assertIsNone(cfg.min_entity_count)
        self.assertIsNone(cfg.enabled_features)

    def test_full_constructor(self):
        cfg = model.SmartClusterFigureConfig(
            auto_generate='true',
            auto_clustering='false',
            min_entity_count=5,
            enabled_features=['face', 'object'],
        )
        self.assertEqual('true', cfg.auto_generate)
        self.assertEqual('false', cfg.auto_clustering)
        self.assertEqual(5, cfg.min_entity_count)
        self.assertEqual(2, len(cfg.enabled_features))


class TestSmartClusterConfig(unittest.TestCase):
    def test_empty_constructor(self):
        cfg = model.SmartClusterConfig()
        self.assertIsNone(cfg.figure)

    def test_full_constructor(self):
        cfg = model.SmartClusterConfig(
            figure=model.SmartClusterFigureConfig(
                auto_generate='true',
                min_entity_count=10,
            ),
        )
        self.assertEqual('true', cfg.figure.auto_generate)
        self.assertEqual(10, cfg.figure.min_entity_count)


class TestDatasetConfig(unittest.TestCase):
    def test_empty_constructor(self):
        cfg = model.DatasetConfig()
        self.assertIsNone(cfg.reverse_image)
        self.assertIsNone(cfg.insights)
        self.assertIsNone(cfg.smart_cluster)

    def test_full_constructor(self):
        cfg = model.DatasetConfig(
            reverse_image=model.ReverseImageConfig(
                image=model.EnableConfig(enable='true'),
                video=model.EnableConfig(enable='false'),
            ),
            insights=model.InsightsConfig(
                language='en',
                image=model.InsightsImageConfig(
                    caption=model.InsightsCaptionConfig(enable='true', prompt='describe'),
                ),
                video=model.InsightsVideoConfig(
                    caption=model.InsightsVideoCaptionConfig(enable='true'),
                    label=model.InsightsVideoLabelConfig(
                        user_defined=model.InsightsLabelUserDefinedConfig(enable='true'),
                    ),
                    multi_stream=model.EnableConfig(enable='false'),
                ),
            ),
            smart_cluster=model.SmartClusterConfig(
                figure=model.SmartClusterFigureConfig(
                    auto_generate='true',
                    auto_clustering='false',
                    min_entity_count=5,
                    enabled_features=['face'],
                ),
            ),
        )
        self.assertEqual('true', cfg.reverse_image.image.enable)
        self.assertEqual('false', cfg.reverse_image.video.enable)
        self.assertEqual('en', cfg.insights.language)
        self.assertEqual('describe', cfg.insights.image.caption.prompt)
        self.assertEqual('true', cfg.insights.video.caption.enable)
        self.assertEqual('true', cfg.insights.video.label.user_defined.enable)
        self.assertEqual('true', cfg.smart_cluster.figure.auto_generate)
        self.assertEqual(5, cfg.smart_cluster.figure.min_entity_count)


class TestDataset(unittest.TestCase):
    def test_empty_constructor(self):
        ds = model.Dataset()
        self.assertIsNone(ds.dataset_name)
        self.assertIsNone(ds.description)
        self.assertIsNone(ds.create_time)
        self.assertIsNone(ds.update_time)
        self.assertIsNone(ds.dataset_max_bind_count)
        self.assertIsNone(ds.dataset_max_file_count)
        self.assertIsNone(ds.dataset_max_entity_count)
        self.assertIsNone(ds.dataset_max_relation_count)
        self.assertIsNone(ds.dataset_max_total_file_size)
        self.assertIsNone(ds.file_count)
        self.assertIsNone(ds.total_file_size)
        self.assertIsNone(ds.workflow_parameters)
        self.assertIsNone(ds.dataset_config)

    def test_full_constructor(self):
        ds = model.Dataset(
            dataset_name='photos-2026',
            description='Photo collection for year 2026',
            create_time='2026-05-20T08:00:00.000+08:00',
            update_time='2026-05-20T08:30:00.000+08:00',
            dataset_max_bind_count=10,
            dataset_max_file_count=100000000,
            dataset_max_entity_count=10000000000,
            dataset_max_relation_count=100000000000,
            dataset_max_total_file_size=90000000000000000,
            file_count=3456,
            total_file_size=10737418240,
            workflow_parameters=model.WorkflowParameters(
                workflow_parameters=[
                    model.WorkflowParameter(name='ImageInsightEnable', value='True'),
                ],
            ),
            dataset_config=model.DatasetConfig(
                insights=model.InsightsConfig(language='en'),
            ),
        )
        self.assertEqual('photos-2026', ds.dataset_name)
        self.assertEqual('Photo collection for year 2026', ds.description)
        self.assertEqual(10, ds.dataset_max_bind_count)
        self.assertEqual(3456, ds.file_count)
        self.assertEqual(10737418240, ds.total_file_size)
        self.assertEqual(1, len(ds.workflow_parameters.workflow_parameters))
        self.assertEqual('en', ds.dataset_config.insights.language)


class TestDatasets(unittest.TestCase):
    def test_empty_constructor(self):
        datasets = model.Datasets()
        self.assertIsNone(datasets.dataset)

    def test_full_constructor(self):
        datasets = model.Datasets(dataset=[
            model.Dataset(dataset_name='ds1'),
            model.Dataset(dataset_name='ds2'),
        ])
        self.assertEqual(2, len(datasets.dataset))
        self.assertEqual('ds1', datasets.dataset[0].dataset_name)
        self.assertEqual('ds2', datasets.dataset[1].dataset_name)


# ==================== CreateDataset ====================

class TestCreateDatasetRequest(unittest.TestCase):
    def test_empty_constructor(self):
        request = model.CreateDatasetRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.dataset_name)
        self.assertIsNone(request.description)
        self.assertIsNone(request.workflow_parameters)
        self.assertIsNone(request.dataset_config)
        self.assertIsInstance(request, serde.RequestModel)

    def test_full_constructor(self):
        wp = model.WorkflowParameter(name='ImageInsightEnable', value='True')
        config = model.DatasetConfig(
            insights=model.InsightsConfig(language='en'),
        )
        request = model.CreateDatasetRequest(
            bucket='examplebucket',
            dataset_name='photos-2026',
            description='Photo collection for year 2026',
            workflow_parameters=[wp],
            dataset_config=config,
        )
        self.assertEqual('examplebucket', request.bucket)
        self.assertEqual('photos-2026', request.dataset_name)
        self.assertEqual('Photo collection for year 2026', request.description)
        self.assertIsNotNone(request.workflow_parameters)
        self.assertIsNotNone(request.dataset_config)

    def test_constructor_with_string_parameters(self):
        request = model.CreateDatasetRequest(
            bucket='test-bucket',
            dataset_name='test-dataset',
            workflow_parameters='[{"Name":"ImageInsightEnable","Value":"True"}]',
            dataset_config='{"Insights":{"Language":"ch"}}',
        )
        self.assertEqual('test-bucket', request.bucket)
        self.assertEqual('[{"Name":"ImageInsightEnable","Value":"True"}]', request.workflow_parameters)
        self.assertEqual('{"Insights":{"Language":"ch"}}', request.dataset_config)

    def test_xml_builder(self):
        # Reference: Java CreateDatasetRequestTest.xmlBuilder
        wp = model.WorkflowParameter(name='ImageInsightEnable', value='True')
        insights_config = model.InsightsConfig(language='en')
        config = model.DatasetConfig(insights=insights_config)

        request = model.CreateDatasetRequest(
            bucket='examplebucket',
            dataset_name='photos-2026',
            description='Photo collection for year 2026',
            workflow_parameters=[wp],
            dataset_config=config,
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='CreateDataset',
            method='POST',
            parameters={'metaQuery': '', 'action': 'createDataset'},
            bucket=request.bucket,
        ))

        self.assertEqual('examplebucket', op_input.bucket)
        self.assertEqual('photos-2026', op_input.parameters.get('datasetName'))
        self.assertEqual('Photo collection for year 2026', op_input.parameters.get('description'))
        self.assertEqual('POST', op_input.method)


class TestCreateDatasetResult(unittest.TestCase):
    def test_empty_constructor(self):
        result = model.CreateDatasetResult()
        self.assertIsInstance(result, serde.ResultModel)
        self.assertIsNone(result.dataset)

    def test_full_constructor(self):
        ds = model.Dataset(dataset_name='ds1', file_count=10)
        result = model.CreateDatasetResult(dataset=ds)
        self.assertEqual('ds1', result.dataset.dataset_name)
        self.assertEqual(10, result.dataset.file_count)

    def test_xml_builder(self):
        # Reference: Java CreateDatasetResultTest.xmlBuilder - HTTP 200, no body
        result = model.CreateDatasetResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({'x-oss-request-id': 'req-create-dataset'}),
                http_response=MockHttpResponse(
                    status_code=200,
                    headers={'x-oss-request-id': 'req-create-dataset'},
                    body=None,
                ),
            ),
        )
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertIsNone(result.dataset)


# ==================== GetDataset ====================

class TestGetDatasetRequest(unittest.TestCase):
    def test_empty_constructor(self):
        request = model.GetDatasetRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.dataset_name)
        self.assertIsNone(request.with_statistics)

    def test_full_constructor(self):
        request = model.GetDatasetRequest(
            bucket='examplebucket',
            dataset_name='photos-2026',
            with_statistics=True,
        )
        self.assertEqual('examplebucket', request.bucket)
        self.assertEqual('photos-2026', request.dataset_name)
        self.assertTrue(request.with_statistics)

    def test_xml_builder(self):
        # Reference: Java GetDatasetRequestTest.xmlBuilder
        request = model.GetDatasetRequest(
            bucket='examplebucket',
            dataset_name='photos-2026',
            with_statistics=True,
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetDataset',
            method='POST',
            parameters={'metaQuery': '', 'action': 'getDataset'},
            bucket=request.bucket,
        ))

        self.assertEqual('examplebucket', op_input.bucket)
        self.assertEqual('photos-2026', op_input.parameters.get('datasetName'))
        self.assertEqual('true', op_input.parameters.get('withStatistics'))
        self.assertEqual('POST', op_input.method)


class TestGetDatasetResult(unittest.TestCase):
    def test_empty_constructor(self):
        result = model.GetDatasetResult()
        self.assertIsNone(result.dataset)

    def test_full_constructor(self):
        ds = model.Dataset(dataset_name='ds1', file_count=100)
        result = model.GetDatasetResult(dataset=ds)
        self.assertEqual('ds1', result.dataset.dataset_name)

    def test_xml_builder(self):
        # Reference: Java GetDatasetResultTest.xmlBuilder (withStatistics=true)
        xml_data = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<GetDatasetResponse>'
            b'  <Dataset>'
            b'    <DatasetName>photos-2026</DatasetName>'
            b'    <Description>Photo collection for year 2026</Description>'
            b'    <CreateTime>2026-05-20T08:00:00.000+08:00</CreateTime>'
            b'    <UpdateTime>2026-05-20T08:30:00.000+08:00</UpdateTime>'
            b'    <WorkflowParameters>'
            b'      <WorkflowParameter><Name>ImageInsightEnable</Name><Value>True</Value></WorkflowParameter>'
            b'    </WorkflowParameters>'
            b'    <DatasetMaxBindCount>10</DatasetMaxBindCount>'
            b'    <DatasetMaxFileCount>100000000</DatasetMaxFileCount>'
            b'    <DatasetMaxEntityCount>10000000000</DatasetMaxEntityCount>'
            b'    <DatasetMaxRelationCount>100000000000</DatasetMaxRelationCount>'
            b'    <DatasetMaxTotalFileSize>90000000000000000</DatasetMaxTotalFileSize>'
            b'    <DatasetConfig>'
            b'      <Insights><Language>en</Language></Insights>'
            b'    </DatasetConfig>'
            b'    <FileCount>3456</FileCount>'
            b'    <TotalFileSize>10737418240</TotalFileSize>'
            b'  </Dataset>'
            b'</GetDatasetResponse>'
        )

        result = model.GetDatasetResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({'x-oss-request-id': 'req-get-dataset'}),
                http_response=MockHttpResponse(
                    status_code=200,
                    headers={'x-oss-request-id': 'req-get-dataset'},
                    body=xml_data,
                ),
            ),
            custom_deserializer=[serde.deserialize_output_xmlbody],
        )

        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.dataset)

        ds = result.dataset
        self.assertEqual('photos-2026', ds.dataset_name)
        self.assertEqual('Photo collection for year 2026', ds.description)
        self.assertEqual('2026-05-20T08:00:00.000+08:00', ds.create_time)
        self.assertEqual('2026-05-20T08:30:00.000+08:00', ds.update_time)

        # WorkflowParameters
        self.assertIsNotNone(ds.workflow_parameters)
        self.assertEqual(1, len(ds.workflow_parameters.workflow_parameters))
        self.assertEqual('ImageInsightEnable', ds.workflow_parameters.workflow_parameters[0].name)
        self.assertEqual('True', ds.workflow_parameters.workflow_parameters[0].value)

        # Quota fields
        self.assertEqual(10, ds.dataset_max_bind_count)
        self.assertEqual(100000000, ds.dataset_max_file_count)
        self.assertEqual(10000000000, ds.dataset_max_entity_count)
        self.assertEqual(100000000000, ds.dataset_max_relation_count)
        self.assertEqual(90000000000000000, ds.dataset_max_total_file_size)

        # DatasetConfig
        self.assertIsNotNone(ds.dataset_config)
        self.assertIsNotNone(ds.dataset_config.insights)
        self.assertEqual('en', ds.dataset_config.insights.language)

        # withStatistics fields
        self.assertEqual(3456, ds.file_count)
        self.assertEqual(10737418240, ds.total_file_size)

    def test_xml_builder_without_statistics(self):
        # Reference: Java GetDatasetResultTest.xmlBuilderWithoutStatistics
        xml_data = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<GetDatasetResponse>'
            b'  <Dataset>'
            b'    <DatasetName>oss_1023210024677934_examplebucket</DatasetName>'
            b'    <CreateTime>2026-05-20T08:00:00.000+08:00</CreateTime>'
            b'    <UpdateTime>2026-05-20T08:00:00.000+08:00</UpdateTime>'
            b'  </Dataset>'
            b'</GetDatasetResponse>'
        )

        result = model.GetDatasetResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({}),
                http_response=MockHttpResponse(
                    status_code=200,
                    headers={},
                    body=xml_data,
                ),
            ),
            custom_deserializer=[serde.deserialize_output_xmlbody],
        )

        self.assertIsNotNone(result.dataset)
        self.assertEqual('oss_1023210024677934_examplebucket', result.dataset.dataset_name)
        self.assertIsNone(result.dataset.description)
        self.assertIsNone(result.dataset.file_count)
        self.assertIsNone(result.dataset.total_file_size)
        self.assertIsNone(result.dataset.workflow_parameters)
        self.assertIsNone(result.dataset.dataset_config)


# ==================== UpdateDataset ====================

class TestUpdateDatasetRequest(unittest.TestCase):
    def test_empty_constructor(self):
        request = model.UpdateDatasetRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.dataset_name)
        self.assertIsNone(request.description)
        self.assertIsNone(request.workflow_parameters)
        self.assertIsNone(request.dataset_config)

    def test_full_constructor(self):
        config = model.DatasetConfig(
            insights=model.InsightsConfig(language='en'),
        )
        request = model.UpdateDatasetRequest(
            bucket='examplebucket',
            dataset_name='photos-2026',
            description='Updated photo collection for year 2026',
            dataset_config=config,
        )
        self.assertEqual('examplebucket', request.bucket)
        self.assertEqual('photos-2026', request.dataset_name)
        self.assertEqual('Updated photo collection for year 2026', request.description)
        self.assertIsNotNone(request.dataset_config)

    def test_xml_builder(self):
        # Reference: Java UpdateDatasetRequestTest.xmlBuilder
        request = model.UpdateDatasetRequest(
            bucket='examplebucket',
            dataset_name='photos-2026',
            description='Updated photo collection for year 2026',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='UpdateDataset',
            method='POST',
            parameters={'metaQuery': '', 'action': 'updateDataset'},
            bucket=request.bucket,
        ))

        self.assertEqual('examplebucket', op_input.bucket)
        self.assertEqual('photos-2026', op_input.parameters.get('datasetName'))
        self.assertEqual('Updated photo collection for year 2026', op_input.parameters.get('description'))
        self.assertEqual('POST', op_input.method)


class TestUpdateDatasetResult(unittest.TestCase):
    def test_empty_constructor(self):
        result = model.UpdateDatasetResult()
        self.assertIsNone(result.dataset)

    def test_full_constructor(self):
        ds = model.Dataset(dataset_name='ds1')
        result = model.UpdateDatasetResult(dataset=ds)
        self.assertEqual('ds1', result.dataset.dataset_name)

    def test_xml_builder(self):
        # Reference: Java UpdateDatasetResultTest.xmlBuilder - HTTP 200, no body
        result = model.UpdateDatasetResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({'x-oss-request-id': 'req-update-dataset'}),
                http_response=MockHttpResponse(
                    status_code=200,
                    headers={'x-oss-request-id': 'req-update-dataset'},
                    body=None,
                ),
            ),
        )
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertIsNone(result.dataset)


# ==================== DeleteDataset ====================

class TestDeleteDatasetRequest(unittest.TestCase):
    def test_empty_constructor(self):
        request = model.DeleteDatasetRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.dataset_name)

    def test_full_constructor(self):
        request = model.DeleteDatasetRequest(
            bucket='examplebucket',
            dataset_name='photos-2026',
        )
        self.assertEqual('examplebucket', request.bucket)
        self.assertEqual('photos-2026', request.dataset_name)

    def test_xml_builder(self):
        # Reference: Java DeleteDatasetRequestTest.xmlBuilder
        request = model.DeleteDatasetRequest(
            bucket='examplebucket',
            dataset_name='photos-2026',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteDataset',
            method='POST',
            parameters={'metaQuery': '', 'action': 'deleteDataset'},
            bucket=request.bucket,
        ))

        self.assertEqual('examplebucket', op_input.bucket)
        self.assertEqual('photos-2026', op_input.parameters.get('datasetName'))
        self.assertEqual('POST', op_input.method)


class TestDeleteDatasetResult(unittest.TestCase):
    def test_empty_constructor(self):
        result = model.DeleteDatasetResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_xml_builder(self):
        # Reference: Java DeleteDatasetResultTest.xmlBuilder - HTTP 200, no body (async)
        result = model.DeleteDatasetResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({'x-oss-request-id': 'req-delete-dataset'}),
                http_response=MockHttpResponse(
                    status_code=200,
                    headers={'x-oss-request-id': 'req-delete-dataset'},
                    body=None,
                ),
            ),
        )
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)


# ==================== ListDatasets ====================

class TestListDatasetsRequest(unittest.TestCase):
    def test_empty_constructor(self):
        request = model.ListDatasetsRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.prefix)
        self.assertIsNone(request.max_results)
        self.assertIsNone(request.next_token)

    def test_full_constructor(self):
        request = model.ListDatasetsRequest(
            bucket='examplebucket',
            prefix='oss_1023210024677934_',
            max_results=50,
            next_token='token-abc123',
        )
        self.assertEqual('examplebucket', request.bucket)
        self.assertEqual('oss_1023210024677934_', request.prefix)
        self.assertEqual(50, request.max_results)
        self.assertEqual('token-abc123', request.next_token)

    def test_xml_builder(self):
        # Reference: Java ListDatasetsRequestTest.xmlBuilder
        request = model.ListDatasetsRequest(
            bucket='examplebucket',
            prefix='oss_1023210024677934_',
            max_results=50,
            next_token='token-abc123',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='ListDatasets',
            method='POST',
            parameters={'metaQuery': '', 'action': 'listDatasets'},
            bucket=request.bucket,
        ))

        self.assertEqual('examplebucket', op_input.bucket)
        self.assertEqual('oss_1023210024677934_', op_input.parameters.get('prefix'))
        self.assertEqual('50', op_input.parameters.get('maxResults'))
        self.assertEqual('token-abc123', op_input.parameters.get('nextToken'))
        self.assertEqual('POST', op_input.method)


class TestListDatasetsResult(unittest.TestCase):
    def test_empty_constructor(self):
        result = model.ListDatasetsResult()
        self.assertIsNone(result.datasets)
        self.assertIsNone(result.next_token)

    def test_full_constructor(self):
        result = model.ListDatasetsResult(
            datasets=model.Datasets(dataset=[
                model.Dataset(dataset_name='ds1'),
                model.Dataset(dataset_name='ds2'),
            ]),
            next_token='tok',
        )
        self.assertEqual(2, len(result.datasets.dataset))
        self.assertEqual('tok', result.next_token)

    def test_xml_builder(self):
        # Reference: Java ListDatasetsResultTest.xmlBuilder
        xml_data = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<ListDatasetsResponse>'
            b'  <NextToken>page-2-token-abc</NextToken>'
            b'  <Datasets>'
            b'    <Dataset>'
            b'      <DatasetName>oss_1023210024677934_examplebucket</DatasetName>'
            b'      <CreateTime>2026-05-20T08:00:00.000+08:00</CreateTime>'
            b'      <UpdateTime>2026-05-20T08:00:00.000+08:00</UpdateTime>'
            b'    </Dataset>'
            b'    <Dataset>'
            b'      <DatasetName>photos-2026</DatasetName>'
            b'      <CreateTime>2026-05-21T09:00:00.000+08:00</CreateTime>'
            b'      <UpdateTime>2026-05-22T10:30:00.000+08:00</UpdateTime>'
            b'    </Dataset>'
            b'  </Datasets>'
            b'</ListDatasetsResponse>'
        )

        result = model.ListDatasetsResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({'x-oss-request-id': 'req-list-datasets'}),
                http_response=MockHttpResponse(
                    status_code=200,
                    headers={'x-oss-request-id': 'req-list-datasets'},
                    body=xml_data,
                ),
            ),
            custom_deserializer=[serde.deserialize_output_xmlbody],
        )

        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual('page-2-token-abc', result.next_token)

        # Verify datasets
        self.assertIsNotNone(result.datasets)
        self.assertEqual(2, len(result.datasets.dataset))
        self.assertEqual('oss_1023210024677934_examplebucket', result.datasets.dataset[0].dataset_name)
        self.assertEqual('2026-05-20T08:00:00.000+08:00', result.datasets.dataset[0].create_time)
        self.assertEqual('2026-05-20T08:00:00.000+08:00', result.datasets.dataset[0].update_time)
        self.assertEqual('photos-2026', result.datasets.dataset[1].dataset_name)

    def test_xml_builder_empty(self):
        # Reference: Java ListDatasetsResultTest.xmlBuilderEmpty
        xml_data = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<ListDatasetsResponse>'
            b'  <Datasets/>'
            b'</ListDatasetsResponse>'
        )

        result = model.ListDatasetsResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({}),
                http_response=MockHttpResponse(
                    status_code=200,
                    headers={},
                    body=xml_data,
                ),
            ),
            custom_deserializer=[serde.deserialize_output_xmlbody],
        )

        self.assertIsNone(result.next_token)


# ==================== DeleteFileMeta ====================


class TestDeleteFileMetaRequest(unittest.TestCase):
    def test_empty_constructor(self):
        """Reference: Java DeleteFileMetaRequestTest.testEmptyBuilder()"""
        request = model.DeleteFileMetaRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.dataset_name)
        self.assertIsNone(request.uri)

    def test_full_constructor(self):
        """Reference: Java DeleteFileMetaRequestTest.testFullBuilder()"""
        request = model.DeleteFileMetaRequest(
            bucket='examplebucket',
            dataset_name='my-dataset',
            uri='oss://examplebucket/prefix/test.jpg',
        )
        self.assertEqual('examplebucket', request.bucket)
        self.assertEqual('my-dataset', request.dataset_name)
        self.assertEqual('oss://examplebucket/prefix/test.jpg', request.uri)

    def test_xml_builder(self):
        """Reference: Java DeleteFileMetaRequestTest.xmlBuilder()"""
        request = model.DeleteFileMetaRequest(
            bucket='examplebucket',
            dataset_name='photos-2026',
            uri='oss://examplebucket/photos/sunset.jpg',
        )
        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteFileMeta',
            method='POST',
            parameters={'metaQuery': '', 'action': 'deleteFileMeta'},
            bucket=request.bucket,
        ))
        self.assertEqual('examplebucket', op_input.bucket)
        self.assertEqual('deleteFileMeta', op_input.parameters.get('action'))
        self.assertEqual('', op_input.parameters.get('metaQuery'))
        self.assertEqual('photos-2026', op_input.parameters.get('datasetName'))
        self.assertEqual('oss://examplebucket/photos/sunset.jpg', op_input.parameters.get('uri'))
        self.assertEqual('POST', op_input.method)
        self.assertIsNone(op_input.body)


class TestDeleteFileMetaResult(unittest.TestCase):
    def test_empty_constructor(self):
        """Reference: Java DeleteFileMetaResultTest.testEmptyBuilder()"""
        result = model.DeleteFileMetaResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_xml_builder(self):
        """Reference: Java DeleteFileMetaResultTest.xmlBuilder()"""
        result = model.DeleteFileMetaResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({'x-oss-request-id': 'req-delete-file-meta'}),
                http_response=MockHttpResponse(
                    status_code=200,
                    headers={'x-oss-request-id': 'req-delete-file-meta'},
                    body=None,
                ),
            ),
        )
        self.assertEqual(200, result.status_code)
        self.assertEqual('req-delete-file-meta', result.headers.get('x-oss-request-id'))


if __name__ == '__main__':
    unittest.main()
