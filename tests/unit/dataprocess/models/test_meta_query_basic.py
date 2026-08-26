# pylint: skip-file
"""Unit tests for dataprocess meta query models.

Follows the Java SDK test structure:
- test_empty_constructor: verify all fields default to None (like testEmptyBuilder)
- test_full_constructor: set all fields, verify values (like testFullBuilder)
- test_xml_builder: XML serialization/deserialization end-to-end (like xmlBuilder)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))
import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.dataprocess.models import meta_query_basic as model
from alibabacloud_oss_v2.dataprocess.models import dataset_basic as ds_model
from alibabacloud_oss_v2.dataprocess.models import query_basic as q_model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict
from tests.unit import MockHttpResponse


# ==================== Sub-model tests ====================


class TestIndexOptions(unittest.TestCase):
    def test_empty_constructor(self):
        opts = model.IndexOptions()
        self.assertIsNone(opts.ignore_object_delete)
        self.assertIsNone(opts.ignore_events)

    def test_full_constructor(self):
        opts = model.IndexOptions(
            ignore_object_delete='True',
            ignore_events=model.IgnoreEvents(ignore_event=['ObjectCreated:PutObject', 'ObjectRemoved:DeleteObject']),
        )
        self.assertEqual('True', opts.ignore_object_delete)
        self.assertEqual(2, len(opts.ignore_events.ignore_event))
        self.assertEqual('ObjectCreated:PutObject', opts.ignore_events.ignore_event[0])


class TestRouteRule(unittest.TestCase):
    def test_empty_constructor(self):
        rule = model.RouteRule()
        self.assertIsNone(rule.type)
        self.assertIsNone(rule.auto_create_dataset)
        self.assertIsNone(rule.oss_tag_key)

    def test_full_constructor(self):
        rule = model.RouteRule(
            type='OSSTag',
            auto_create_dataset='True',
            oss_tag_key='routing-dataset',
        )
        self.assertEqual('OSSTag', rule.type)
        self.assertEqual('True', rule.auto_create_dataset)
        self.assertEqual('routing-dataset', rule.oss_tag_key)


class TestMetaQueryNotification(unittest.TestCase):
    def test_empty_constructor(self):
        n = model.MetaQueryNotification()
        self.assertIsNone(n.mns)

    def test_full_constructor(self):
        n = model.MetaQueryNotification(mns='imm-index-notification')
        self.assertEqual('imm-index-notification', n.mns)


class TestNotificationAttributes(unittest.TestCase):
    def test_empty_constructor(self):
        attrs = model.NotificationAttributes()
        self.assertIsNone(attrs.notifications)
        self.assertIsNone(attrs.with_fields)

    def test_full_constructor(self):
        attrs = model.NotificationAttributes(
            notifications=model.MetaQueryNotifications(
                notifications=[model.MetaQueryNotification(mns='imm-index-notification')],
            ),
            with_fields=model.WithFields(with_field=['Insights', 'Labels']),
        )
        self.assertIsNotNone(attrs.notifications)
        self.assertEqual(1, len(attrs.notifications.notifications))
        self.assertEqual('imm-index-notification', attrs.notifications.notifications[0].mns)
        self.assertEqual(2, len(attrs.with_fields.with_field))


class TestMetaQueryStatus(unittest.TestCase):
    def test_empty_constructor(self):
        status = model.MetaQueryStatus()
        self.assertIsNone(status.state)
        self.assertIsNone(status.phase)
        self.assertIsNone(status.create_time)
        self.assertIsNone(status.update_time)
        self.assertIsNone(status.meta_query_mode)
        self.assertIsNone(status.workflow_parameters)
        self.assertIsNone(status.index_options)
        self.assertIsNone(status.route_rule)
        self.assertIsNone(status.notification_attributes)
        self.assertIsNone(status.dataset_config)
        self.assertIsNone(status.filters)

    def test_full_constructor(self):
        status = model.MetaQueryStatus(
            state='Running',
            phase='FullIndexing',
            create_time='2026-05-20T08:00:00.000+08:00',
            update_time='2026-05-20T08:30:00.000+08:00',
            meta_query_mode='semantic',
            filters=model.Filters(filter=['Size > 1024']),
        )
        self.assertEqual('Running', status.state)
        self.assertEqual('FullIndexing', status.phase)
        self.assertEqual('2026-05-20T08:00:00.000+08:00', status.create_time)
        self.assertEqual('semantic', status.meta_query_mode)
        self.assertEqual(1, len(status.filters.filter))


# ==================== OpenMetaQuery ====================


class TestOpenMetaQueryRequest(unittest.TestCase):
    def test_empty_constructor(self):
        request = model.OpenMetaQueryRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.mode)
        self.assertIsNone(request.role)
        self.assertIsNone(request.meta_query_body)

    def test_full_constructor(self):
        body = model.MetaQueryOpenBody(
            dataset_config=ds_model.DatasetConfig(),
        )
        request = model.OpenMetaQueryRequest(
            bucket='examplebucket',
            mode='semantic',
            role='acs:ram::1234567890:role/AliyunMetaQueryDefaultRole',
            meta_query_body=body,
        )
        self.assertEqual('examplebucket', request.bucket)
        self.assertEqual('semantic', request.mode)
        self.assertEqual('acs:ram::1234567890:role/AliyunMetaQueryDefaultRole', request.role)
        self.assertIsNotNone(request.meta_query_body)

    def test_xml_builder(self):
        """Reference: Java OpenMetaQueryRequestTest.xmlBuilder()"""
        # Step 1: Expected XML (equivalent to Java expected xml string)
        expected_xml = (
            '<MetaQuery>'
            '  <WorkflowParameters>'
            '    <WorkflowParameter>'
            '      <Name>ImageInsightEnable</Name>'
            '      <Value>True</Value>'
            '    </WorkflowParameter>'
            '    <WorkflowParameter>'
            '      <Name>VideoInsightEnable</Name>'
            '      <Value>True</Value>'
            '    </WorkflowParameter>'
            '  </WorkflowParameters>'
            '  <NotificationAttributes>'
            '    <Notifications>'
            '      <Notification>'
            '        <MNS>imm-index-notification</MNS>'
            '      </Notification>'
            '    </Notifications>'
            '    <WithFields>'
            '      <WithField>Insights</WithField>'
            '      <WithField>Labels</WithField>'
            '    </WithFields>'
            '  </NotificationAttributes>'
            '  <IndexOptions>'
            '    <IgnoreObjectDelete>True</IgnoreObjectDelete>'
            '  </IndexOptions>'
            '  <RouteRule>'
            '    <Type>OSSTag</Type>'
            '    <AutoCreateDataset>True</AutoCreateDataset>'
            '    <OSSTagKey>routing-dataset</OSSTagKey>'
            '  </RouteRule>'
            '  <DatasetConfig>'
            '    <Insights>'
            '      <Language>en</Language>'
            '    </Insights>'
            '  </DatasetConfig>'
            '</MetaQuery>'
        )

        # Step 2: Parse expected XML and re-serialize to get canonical form
        # (equivalent to Java: xmlMapper.readValue → xmlMapper.writeValueAsString)
        expected_body = model.MetaQueryOpenBody()
        serde.deserialize_xml(
            expected_xml.encode('utf-8'),
            expected_body,
            expect_tag='MetaQuery',
        )
        expected_xml_bytes = serde.serialize_xml(expected_body, root='MetaQuery')

        # Step 3: Build full body
        notification = model.MetaQueryNotification(mns='imm-index-notification')
        notifications = model.MetaQueryNotifications(notifications=[notification])
        notification_attributes = model.NotificationAttributes(
            notifications=notifications,
            with_fields=model.WithFields(with_field=['Insights', 'Labels']),
        )
        route_rule = model.RouteRule(
            type='OSSTag',
            auto_create_dataset='True',
            oss_tag_key='routing-dataset',
        )
        index_options = model.IndexOptions(ignore_object_delete='True')
        insights_config = ds_model.InsightsConfig(language='en')
        dataset_config = ds_model.DatasetConfig(insights=insights_config)
        workflow_params = ds_model.WorkflowParameters(
            workflow_parameters=[
                ds_model.WorkflowParameter(name='ImageInsightEnable', value='True'),
                ds_model.WorkflowParameter(name='VideoInsightEnable', value='True'),
            ],
        )
        body = model.MetaQueryOpenBody(
            workflow_parameters=workflow_params,
            notification_attributes=notification_attributes,
            index_options=index_options,
            route_rule=route_rule,
            dataset_config=dataset_config,
        )
        request = model.OpenMetaQueryRequest(
            bucket='examplebucket',
            mode='semantic',
            role='AliyunMetaQueryDefaultRole',
            meta_query_body=body,
        )

        # Step 4: Verify serialize_input parameters
        op_input = serde.serialize_input(request, OperationInput(
            op_name='OpenMetaQuery',
            method='POST',
            parameters={'metaQuery': '', 'action': 'openMetaQuery'},
            bucket=request.bucket,
        ))
        self.assertEqual('examplebucket', op_input.bucket)
        self.assertEqual('semantic', op_input.parameters.get('mode'))
        self.assertEqual('AliyunMetaQueryDefaultRole', op_input.parameters.get('role'))

        # Step 5: Verify body XML serialization
        _xml_map = getattr(body, '_xml_map', {})
        xml_bytes = serde.serialize_xml(body, root=_xml_map.get('name', None))
        xml_content = xml_bytes.decode('utf-8')
        self.assertIn('<MetaQuery>', xml_content)
        self.assertIn('<WorkflowParameter>', xml_content)
        self.assertIn('<Name>ImageInsightEnable</Name>', xml_content)
        self.assertIn('<Value>True</Value>', xml_content)
        self.assertIn('<MNS>imm-index-notification</MNS>', xml_content)
        self.assertIn('<WithField>Insights</WithField>', xml_content)
        self.assertIn('<IgnoreObjectDelete>True</IgnoreObjectDelete>', xml_content)
        self.assertIn('<Type>OSSTag</Type>', xml_content)
        self.assertIn('<AutoCreateDataset>True</AutoCreateDataset>', xml_content)
        self.assertIn('<OSSTagKey>routing-dataset</OSSTagKey>', xml_content)
        self.assertIn('<Language>en</Language>', xml_content)
        self.assertIn('</MetaQuery>', xml_content)

        # Step 6: Exact comparison (equivalent to Java assertThat(xmlContent).isEqualTo(expectedXml))
        self.assertEqual(xml_bytes, expected_xml_bytes)


class TestOpenMetaQueryResult(unittest.TestCase):
    def test_empty_constructor(self):
        result = model.OpenMetaQueryResult()
        self.assertIsInstance(result, serde.ResultModel)


# ==================== GetMetaQueryStatus ====================


class TestGetMetaQueryStatusRequest(unittest.TestCase):
    def test_empty_constructor(self):
        request = model.GetMetaQueryStatusRequest()
        self.assertIsNone(request.bucket)

    def test_full_constructor(self):
        request = model.GetMetaQueryStatusRequest(bucket='examplebucket')
        self.assertEqual('examplebucket', request.bucket)

    def test_xml_builder(self):
        """Reference: Java GetMetaQueryStatusRequestTest.xmlBuilder()"""
        request = model.GetMetaQueryStatusRequest(bucket='examplebucket')
        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetMetaQueryStatus',
            method='POST',
            parameters={'metaQuery': '', 'action': 'getMetaQueryStatus'},
            bucket=request.bucket,
        ))
        self.assertEqual('examplebucket', op_input.bucket)
        self.assertEqual('getMetaQueryStatus', op_input.parameters.get('action'))
        self.assertEqual('', op_input.parameters.get('metaQuery'))


class TestGetMetaQueryStatusResult(unittest.TestCase):
    def test_empty_constructor(self):
        result = model.GetMetaQueryStatusResult()
        self.assertIsNone(result.status)

    def test_xml_builder(self):
        """Reference: Java GetMetaQueryStatusResultTest.xmlBuilder()"""
        xml_data = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<MetaQueryStatus>'
            b'  <State>Running</State>'
            b'  <Phase>IncrementalScanning</Phase>'
            b'  <CreateTime>2026-05-20T08:00:00.000+08:00</CreateTime>'
            b'  <UpdateTime>2026-05-20T08:30:00.000+08:00</UpdateTime>'
            b'  <MetaQueryMode>semantic</MetaQueryMode>'
            b'  <Filters>'
            b'    <Filter>Size &gt; 1024</Filter>'
            b"    <Filter>ObjectACL = 'default'</Filter>"
            b'  </Filters>'
            b'  <WorkflowParameters>'
            b'    <WorkflowParameter>'
            b'      <Name>ImageInsightEnable</Name>'
            b'      <Value>True</Value>'
            b'    </WorkflowParameter>'
            b'  </WorkflowParameters>'
            b'  <IndexOptions>'
            b'    <IgnoreObjectDelete>True</IgnoreObjectDelete>'
            b'  </IndexOptions>'
            b'  <RouteRule>'
            b'    <Type>OSSTag</Type>'
            b'    <AutoCreateDataset>True</AutoCreateDataset>'
            b'    <OSSTagKey>routing-dataset</OSSTagKey>'
            b'  </RouteRule>'
            b'  <NotificationAttributes>'
            b'    <Notifications>'
            b'      <Notification>'
            b'        <MNS>imm-index-notification</MNS>'
            b'      </Notification>'
            b'    </Notifications>'
            b'    <WithFields>'
            b'      <WithField>Insights</WithField>'
            b'    </WithFields>'
            b'  </NotificationAttributes>'
            b'  <DatasetConfig>'
            b'    <Insights>'
            b'      <Language>en</Language>'
            b'    </Insights>'
            b'  </DatasetConfig>'
            b'</MetaQueryStatus>'
        )
        result = model.GetMetaQueryStatusResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({'x-oss-request-id': 'req-get-metaquery-status'}),
                http_response=MockHttpResponse(
                    status_code=200,
                    headers={'x-oss-request-id': 'req-get-metaquery-status'},
                    body=xml_data,
                ),
            ),
            custom_deserializer=[serde.deserialize_output_xmlbody],
        )
        self.assertEqual(200, result.status_code)
        self.assertEqual('req-get-metaquery-status', result.headers.get('x-oss-request-id'))
        self.assertIsNotNone(result.status)

        status = result.status
        self.assertEqual('Running', status.state)
        self.assertEqual('IncrementalScanning', status.phase)
        self.assertEqual('2026-05-20T08:00:00.000+08:00', status.create_time)
        self.assertEqual('2026-05-20T08:30:00.000+08:00', status.update_time)
        self.assertEqual('semantic', status.meta_query_mode)

        # Filters
        self.assertIsNotNone(status.filters)
        self.assertEqual(2, len(status.filters.filter))
        self.assertEqual('Size > 1024', status.filters.filter[0])
        self.assertEqual("ObjectACL = 'default'", status.filters.filter[1])

        # WorkflowParameters
        self.assertIsNotNone(status.workflow_parameters)
        self.assertEqual(1, len(status.workflow_parameters.workflow_parameters))
        self.assertEqual('ImageInsightEnable', status.workflow_parameters.workflow_parameters[0].name)
        self.assertEqual('True', status.workflow_parameters.workflow_parameters[0].value)

        # IndexOptions
        self.assertIsNotNone(status.index_options)
        self.assertEqual('True', status.index_options.ignore_object_delete)

        # RouteRule
        self.assertIsNotNone(status.route_rule)
        self.assertEqual('OSSTag', status.route_rule.type)
        self.assertEqual('True', status.route_rule.auto_create_dataset)
        self.assertEqual('routing-dataset', status.route_rule.oss_tag_key)

        # NotificationAttributes
        self.assertIsNotNone(status.notification_attributes)
        self.assertIsNotNone(status.notification_attributes.notifications)
        self.assertEqual(1, len(status.notification_attributes.notifications.notifications))
        self.assertEqual('imm-index-notification', status.notification_attributes.notifications.notifications[0].mns)
        self.assertEqual(['Insights'], status.notification_attributes.with_fields.with_field)

        # DatasetConfig
        self.assertIsNotNone(status.dataset_config)
        self.assertIsNotNone(status.dataset_config.insights)
        self.assertEqual('en', status.dataset_config.insights.language)

    def test_xml_builder_minimal(self):
        """Reference: Java GetMetaQueryStatusResultTest.xmlBuilderMinimal()"""
        xml_data = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<MetaQueryStatus>'
            b'  <State>Ready</State>'
            b'  <Phase>FullScanning</Phase>'
            b'  <MetaQueryMode>basic</MetaQueryMode>'
            b'</MetaQueryStatus>'
        )
        result = model.GetMetaQueryStatusResult()
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
        self.assertIsNotNone(result.status)
        self.assertEqual('Ready', result.status.state)
        self.assertEqual('FullScanning', result.status.phase)
        self.assertEqual('basic', result.status.meta_query_mode)
        self.assertIsNone(result.status.workflow_parameters)
        self.assertIsNone(result.status.route_rule)


# ==================== CloseMetaQuery ====================


class TestCloseMetaQueryRequest(unittest.TestCase):
    def test_empty_constructor(self):
        request = model.CloseMetaQueryRequest()
        self.assertIsNone(request.bucket)

    def test_full_constructor(self):
        request = model.CloseMetaQueryRequest(bucket='examplebucket')
        self.assertEqual('examplebucket', request.bucket)

    def test_xml_builder(self):
        """Reference: Java CloseMetaQueryRequestTest.xmlBuilder()"""
        request = model.CloseMetaQueryRequest(bucket='examplebucket')
        op_input = serde.serialize_input(request, OperationInput(
            op_name='CloseMetaQuery',
            method='POST',
            parameters={'metaQuery': '', 'action': 'closeMetaQuery'},
            bucket=request.bucket,
        ))
        self.assertEqual('examplebucket', op_input.bucket)
        self.assertEqual('closeMetaQuery', op_input.parameters.get('action'))


class TestCloseMetaQueryResult(unittest.TestCase):
    def test_empty_constructor(self):
        result = model.CloseMetaQueryResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_xml_builder(self):
        """Reference: Java CloseMetaQueryResultTest.xmlBuilder()"""
        result = model.CloseMetaQueryResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({'x-oss-request-id': 'req-close'}),
                http_response=MockHttpResponse(
                    status_code=200,
                    headers={'x-oss-request-id': 'req-close'},
                    body=None,
                ),
            ),
        )
        self.assertEqual(200, result.status_code)


# ==================== DoMetaQuery ====================


class TestDoMetaQueryRequest(unittest.TestCase):
    def test_empty_constructor(self):
        request = model.DoMetaQueryRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.mode)
        self.assertIsNone(request.meta_query_body)

    def test_full_constructor_basic(self):
        """Reference: Java DoMetaQueryRequestTest.testFullBuilderBasicMode()"""
        agg = q_model.Aggregation(field='Size', operation='sum')
        body = model.MetaQueryDoBody(
            query='{"Field":"Size","Operation":"gt","Value":"1048576"}',
            sort='Size',
            order='desc',
            aggregations=model.MetaQueryAggregations(aggregation=[agg]),
            max_results=100,
            next_token='token-basic-001',
            with_fields=model.WithFields(with_field=['Filename', 'Size', 'FileModifiedTime']),
            without_total_hits='True',
        )
        request = model.DoMetaQueryRequest(
            bucket='examplebucket',
            mode='basic',
            meta_query_body=body,
        )
        self.assertEqual('examplebucket', request.bucket)
        self.assertEqual('basic', request.mode)
        self.assertEqual('{"Field":"Size","Operation":"gt","Value":"1048576"}', request.meta_query_body.query)
        self.assertEqual('Size', request.meta_query_body.sort)
        self.assertEqual('desc', request.meta_query_body.order)
        self.assertEqual(100, request.meta_query_body.max_results)
        self.assertEqual('True', request.meta_query_body.without_total_hits)

    def test_full_constructor_semantic(self):
        """Reference: Java DoMetaQueryRequestTest.testFullBuilderSemanticMode()"""
        body = model.MetaQueryDoBody(
            query='客厅里的猫',
            media_types=model.MediaTypes(media_type=['image']),
            simple_query='{"Field":"Size","Operation":"gt","Value":"102400"}',
            max_results=20,
            with_fields=model.WithFields(with_field=['Filename', 'Size', 'Insights', 'Labels']),
            smart_cluster_ids=model.SmartClusterIds(smart_cluster_id=['cluster-abc123def456', 'cluster-xyz789']),
        )
        request = model.DoMetaQueryRequest(
            bucket='examplebucket',
            mode='semantic',
            meta_query_body=body,
        )
        self.assertEqual('semantic', request.mode)
        self.assertEqual('客厅里的猫', request.meta_query_body.query)
        self.assertEqual(1, len(request.meta_query_body.media_types.media_type))
        self.assertEqual(2, len(request.meta_query_body.smart_cluster_ids.smart_cluster_id))

    def test_xml_builder_basic(self):
        """Reference: Java DoMetaQueryRequestTest.testBasicModeXmlBuilder()"""
        # Step 1: Expected XML (equivalent to Java expected xml string)
        expected_xml = (
            '<MetaQuery>'
            '  <Query>{"Field":"Size","Operation":"gt","Value":"1048576"}</Query>'
            '  <Sort>Size</Sort>'
            '  <Order>desc</Order>'
            '  <Aggregations>'
            '    <Aggregation>'
            '      <Field>Size</Field>'
            '      <Operation>sum</Operation>'
            '    </Aggregation>'
            '  </Aggregations>'
            '  <MaxResults>100</MaxResults>'
            '</MetaQuery>'
        )

        # Step 2: Parse expected XML and re-serialize to get canonical form
        # (equivalent to Java: xmlMapper.readValue → xmlMapper.writeValueAsString)
        expected_body = model.MetaQueryDoBody()
        serde.deserialize_xml(
            expected_xml.encode('utf-8'),
            expected_body,
            expect_tag='MetaQuery',
        )
        expected_xml_bytes = serde.serialize_xml(expected_body, root='MetaQuery')

        # Step 3: Build body
        agg = q_model.Aggregation(field='Size', operation='sum')
        body = model.MetaQueryDoBody(
            query='{"Field":"Size","Operation":"gt","Value":"1048576"}',
            sort='Size',
            order='desc',
            aggregations=model.MetaQueryAggregations(aggregation=[agg]),
            max_results=100,
        )
        request = model.DoMetaQueryRequest(
            bucket='examplebucket',
            mode='basic',
            meta_query_body=body,
        )
        op_input = serde.serialize_input(request, OperationInput(
            op_name='DoMetaQuery',
            method='POST',
            parameters={'metaQuery': '', 'action': 'doMetaQuery'},
            bucket=request.bucket,
        ))
        self.assertEqual('examplebucket', op_input.bucket)
        self.assertEqual('doMetaQuery', op_input.parameters.get('action'))
        self.assertEqual('basic', op_input.parameters.get('mode'))

        # Step 4: Verify body XML
        _xml_map = getattr(body, '_xml_map', {})
        xml_bytes = serde.serialize_xml(body, root=_xml_map.get('name', None))
        xml_content = xml_bytes.decode('utf-8')
        self.assertIn('<MetaQuery>', xml_content)
        self.assertIn('<Sort>Size</Sort>', xml_content)
        self.assertIn('<Order>desc</Order>', xml_content)
        self.assertIn('<MaxResults>100</MaxResults>', xml_content)
        self.assertIn('<Field>Size</Field>', xml_content)
        self.assertIn('<Operation>sum</Operation>', xml_content)

        # Step 5: Exact comparison (equivalent to Java assertThat(xmlContent).isEqualTo(expectedXml))
        self.assertEqual(xml_bytes, expected_xml_bytes)

    def test_xml_builder_semantic(self):
        """Reference: Java DoMetaQueryRequestTest.testSemanticModeXmlBuilder()"""
        # Step 1: Expected XML (equivalent to Java expected xml string)
        expected_xml = (
            '<MetaQuery>'
            '  <Query>客厅里的猫</Query>'
            '  <MediaTypes>'
            '    <MediaType>image</MediaType>'
            '  </MediaTypes>'
            '  <SimpleQuery>{"Field":"Size","Operation":"gt","Value":"102400"}</SimpleQuery>'
            '  <MaxResults>20</MaxResults>'
            '</MetaQuery>'
        )

        # Step 2: Parse expected XML and re-serialize to get canonical form
        # (equivalent to Java: xmlMapper.readValue → xmlMapper.writeValueAsString)
        expected_body = model.MetaQueryDoBody()
        serde.deserialize_xml(
            expected_xml.encode('utf-8'),
            expected_body,
            expect_tag='MetaQuery',
        )
        expected_xml_bytes = serde.serialize_xml(expected_body, root='MetaQuery')

        # Step 3: Build body
        body = model.MetaQueryDoBody(
            query='客厅里的猫',
            media_types=model.MediaTypes(media_type=['image']),
            simple_query='{"Field":"Size","Operation":"gt","Value":"102400"}',
            max_results=20,
        )
        request = model.DoMetaQueryRequest(
            bucket='examplebucket',
            mode='semantic',
            meta_query_body=body,
        )
        op_input = serde.serialize_input(request, OperationInput(
            op_name='DoMetaQuery',
            method='POST',
            parameters={'metaQuery': '', 'action': 'doMetaQuery'},
            bucket=request.bucket,
        ))
        self.assertEqual('semantic', op_input.parameters.get('mode'))

        # Step 4: Verify body XML
        _xml_map = getattr(body, '_xml_map', {})
        xml_bytes = serde.serialize_xml(body, root=_xml_map.get('name', None))
        xml_content = xml_bytes.decode('utf-8')
        self.assertIn('<MetaQuery>', xml_content)
        self.assertIn('<Query>客厅里的猫</Query>', xml_content)
        self.assertIn('<MediaType>image</MediaType>', xml_content)
        self.assertIn('<SimpleQuery>', xml_content)
        self.assertIn('<MaxResults>20</MaxResults>', xml_content)

        # Step 5: Exact comparison (equivalent to Java assertThat(xmlContent).isEqualTo(expectedXml))
        self.assertEqual(xml_bytes, expected_xml_bytes)


class TestDoMetaQueryResult(unittest.TestCase):
    def test_empty_constructor(self):
        result = model.DoMetaQueryResult()
        self.assertIsNone(result.next_token)
        self.assertIsNone(result.total_hits)
        self.assertIsNone(result.files)
        self.assertIsNone(result.aggregations)

    def test_xml_builder_basic_mode(self):
        """Reference: Java DoMetaQueryResultTest.xmlBuilderBasicMode()"""
        xml_data = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<MetaQuery>'
            b'  <NextToken>next-page-token-abc</NextToken>'
            b'  <TotalHits>123</TotalHits>'
            b'  <Files>'
            b'    <File>'
            b'      <Filename>photos/sunset.jpg</Filename>'
            b'      <Size>2097152</Size>'
            b'      <FileModifiedTime>2026-05-19T15:30:00.000+08:00</FileModifiedTime>'
            b'      <ContentType>image/jpeg</ContentType>'
            b'      <ObjectACL>default</ObjectACL>'
            b'      <StorageClass>Standard</StorageClass>'
            b'    </File>'
            b'    <File>'
            b'      <Filename>photos/mountain.png</Filename>'
            b'      <Size>5242880</Size>'
            b'    </File>'
            b'  </Files>'
            b'  <Aggregations>'
            b'    <Aggregation>'
            b'      <Field>Size</Field>'
            b'      <Operation>sum</Operation>'
            b'      <Value>12345678</Value>'
            b'    </Aggregation>'
            b'  </Aggregations>'
            b'</MetaQuery>'
        )
        result = model.DoMetaQueryResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({'x-oss-request-id': 'req-do-meta-query-basic'}),
                http_response=MockHttpResponse(
                    status_code=200,
                    headers={'x-oss-request-id': 'req-do-meta-query-basic'},
                    body=xml_data,
                ),
            ),
            custom_deserializer=[serde.deserialize_output_xmlbody],
        )
        self.assertEqual(200, result.status_code)
        self.assertEqual('req-do-meta-query-basic', result.headers.get('x-oss-request-id'))

        # Verify basic mode fields
        self.assertEqual('next-page-token-abc', result.next_token)
        self.assertEqual(123, result.total_hits)

        # Verify files
        self.assertIsNotNone(result.files)
        self.assertEqual(2, len(result.files.file))
        self.assertEqual('photos/sunset.jpg', result.files.file[0].filename)
        self.assertEqual(2097152, result.files.file[0].size)
        self.assertEqual('photos/mountain.png', result.files.file[1].filename)

        # Verify aggregations
        self.assertIsNotNone(result.aggregations)
        self.assertEqual(1, len(result.aggregations.aggregation))
        self.assertEqual('Size', result.aggregations.aggregation[0].field)
        self.assertEqual('sum', result.aggregations.aggregation[0].operation)
        self.assertEqual(12345678.0, result.aggregations.aggregation[0].value)

    def test_xml_builder_basic_mode_with_group_by(self):
        """Reference: Java DoMetaQueryResultTest.xmlBuilderBasicModeWithGroupBy()"""
        xml_data = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<MetaQuery>'
            b'  <TotalHits>50</TotalHits>'
            b'  <Aggregations>'
            b'    <Aggregation>'
            b'      <Field>StorageClass</Field>'
            b'      <Operation>group_by</Operation>'
            b'      <Groups>'
            b'        <Group><Value>Standard</Value><Count>30</Count></Group>'
            b'        <Group><Value>IA</Value><Count>20</Count></Group>'
            b'      </Groups>'
            b'    </Aggregation>'
            b'  </Aggregations>'
            b'</MetaQuery>'
        )
        result = model.DoMetaQueryResult()
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
        self.assertEqual(50, result.total_hits)
        self.assertEqual(1, len(result.aggregations.aggregation))
        self.assertEqual('StorageClass', result.aggregations.aggregation[0].field)
        self.assertEqual('group_by', result.aggregations.aggregation[0].operation)
        self.assertEqual(2, len(result.aggregations.aggregation[0].groups.group))
        self.assertEqual('Standard', result.aggregations.aggregation[0].groups.group[0].value)
        self.assertEqual(30, result.aggregations.aggregation[0].groups.group[0].count)
        self.assertEqual('IA', result.aggregations.aggregation[0].groups.group[1].value)
        self.assertEqual(20, result.aggregations.aggregation[0].groups.group[1].count)

    def test_xml_builder_semantic_mode(self):
        """Reference: Java DoMetaQueryResultTest.xmlBuilderSemanticMode()"""
        # semantic mode: no NextToken, no Aggregations
        xml_data = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<MetaQuery>'
            b'  <TotalHits>2</TotalHits>'
            b'  <Files>'
            b'    <File>'
            b'      <Filename>photos/cat-in-living-room.jpg</Filename>'
            b'      <Size>3145728</Size>'
            b'      <OSSStorageClass>Standard</OSSStorageClass>'
            b'      <Labels>'
            b'        <Label>'
            b'          <LabelName>cat</LabelName>'
            b'          <LabelConfidence>0.98</LabelConfidence>'
            b'        </Label>'
            b'      </Labels>'
            b'    </File>'
            b'    <File>'
            b'      <Filename>photos/kitten-sofa.jpg</Filename>'
            b'      <Size>2621440</Size>'
            b'    </File>'
            b'  </Files>'
            b'</MetaQuery>'
        )
        result = model.DoMetaQueryResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({'x-oss-request-id': 'req-do-meta-query-semantic'}),
                http_response=MockHttpResponse(
                    status_code=200,
                    headers={'x-oss-request-id': 'req-do-meta-query-semantic'},
                    body=xml_data,
                ),
            ),
            custom_deserializer=[serde.deserialize_output_xmlbody],
        )
        self.assertEqual(200, result.status_code)
        self.assertEqual('req-do-meta-query-semantic', result.headers.get('x-oss-request-id'))

        # semantic mode: no next_token, no aggregations
        self.assertIsNone(result.next_token)
        self.assertIsNone(result.aggregations)
        self.assertEqual(2, result.total_hits)

        # Verify files
        self.assertIsNotNone(result.files)
        self.assertEqual(2, len(result.files.file))
        self.assertEqual('photos/cat-in-living-room.jpg', result.files.file[0].filename)
        self.assertEqual(3145728, result.files.file[0].size)
        self.assertEqual('Standard', result.files.file[0].oss_storage_class)
        self.assertIsNotNone(result.files.file[0].labels)
        self.assertEqual(1, len(result.files.file[0].labels.label))
        self.assertEqual('cat', result.files.file[0].labels.label[0].label_name)
        self.assertEqual(0.98, result.files.file[0].labels.label[0].label_confidence)
        self.assertEqual('photos/kitten-sofa.jpg', result.files.file[1].filename)


if __name__ == '__main__':
    unittest.main()
