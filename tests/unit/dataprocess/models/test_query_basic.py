# pylint: skip-file
"""Unit tests for dataprocess query models.

Follows the Java SDK test structure:
- test_empty_constructor: verify all fields default to None (like testEmptyBuilder)
- test_full_constructor: set all fields, verify values (like testFullBuilder)
- test_xml_builder: XML serialization/deserialization end-to-end (like xmlBuilder)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))
import json
import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.dataprocess.models import query_basic as model
from alibabacloud_oss_v2.dataprocess.models import meta_query_basic
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict
from tests.unit import MockHttpResponse


# ==================== Sub-model tests ====================


class TestAggregation(unittest.TestCase):
    def test_empty_constructor(self):
        agg = model.Aggregation()
        self.assertIsNone(agg.field)
        self.assertIsNone(agg.operation)

    def test_full_constructor(self):
        agg = model.Aggregation(field='Size', operation='sum')
        self.assertEqual('Size', agg.field)
        self.assertEqual('sum', agg.operation)


class TestAggregationGroup(unittest.TestCase):
    def test_empty_constructor(self):
        group = model.AggregationGroup()
        self.assertIsNone(group.value)
        self.assertIsNone(group.count)

    def test_full_constructor(self):
        group = model.AggregationGroup(value='image', count=42)
        self.assertEqual('image', group.value)
        self.assertEqual(42, group.count)


class TestAggregationInfo(unittest.TestCase):
    def test_empty_constructor(self):
        info = model.AggregationInfo()
        self.assertIsNone(info.field)
        self.assertIsNone(info.operation)
        self.assertIsNone(info.value)
        self.assertIsNone(info.groups)

    def test_full_constructor(self):
        info = model.AggregationInfo(
            field='Size',
            operation='sum',
            value=1024.0,
            groups=model.Groups(group=[model.AggregationGroup(value='image', count=10)]),
        )
        self.assertEqual('Size', info.field)
        self.assertEqual('sum', info.operation)
        self.assertEqual(1024.0, info.value)
        self.assertEqual(1, len(info.groups.group))


class TestSimpleQuery(unittest.TestCase):
    def test_empty_constructor(self):
        sq = model.SimpleQuery()
        self.assertIsNone(sq.field)
        self.assertIsNone(sq.value)
        self.assertIsNone(sq.operation)
        self.assertIsNone(sq.sub_queries)

    def test_full_constructor(self):
        sq = model.SimpleQuery(field='Filename', value='test', operation='prefix')
        self.assertEqual('Filename', sq.field)
        self.assertEqual('test', sq.value)
        self.assertEqual('prefix', sq.operation)

    def test_nested_sub_queries(self):
        sub = model.SimpleQuery(field='Size', value='100', operation='gt')
        sq = model.SimpleQuery(
            field='', value='', operation='and',
            sub_queries=[sub],
        )
        self.assertEqual(1, len(sq.sub_queries))
        self.assertEqual('Size', sq.sub_queries[0].field)

    def test_to_parameter_value(self):
        """Nested queries use the SubQueries key, not the XML SimpleQuery name."""
        sq = model.SimpleQuery(operation='and', sub_queries=[
            model.SimpleQuery(field='Size', value='1048576', operation='gt'),
            model.SimpleQuery(field='MediaType', value='image', operation='eq'),
        ])
        self.assertEqual({
            'Operation': 'and',
            'SubQueries': [
                {'Field': 'Size', 'Value': '1048576', 'Operation': 'gt'},
                {'Field': 'MediaType', 'Value': 'image', 'Operation': 'eq'},
            ],
        }, json.loads(sq.to_parameter_value()))

    def test_to_parameter_value_recursive(self):
        """SubQueries nests to arbitrary depth."""
        sq = model.SimpleQuery(operation='and', sub_queries=[
            model.SimpleQuery(field='Size', value='1048576', operation='gt'),
            model.SimpleQuery(operation='or', sub_queries=[
                model.SimpleQuery(field='MediaType', value='image', operation='eq'),
                model.SimpleQuery(operation='and', sub_queries=[
                    model.SimpleQuery(field='Filename', value='a', operation='prefix'),
                ]),
            ]),
        ])
        self.assertEqual({
            'Operation': 'and',
            'SubQueries': [
                {'Field': 'Size', 'Value': '1048576', 'Operation': 'gt'},
                {
                    'Operation': 'or',
                    'SubQueries': [
                        {'Field': 'MediaType', 'Value': 'image', 'Operation': 'eq'},
                        {
                            'Operation': 'and',
                            'SubQueries': [
                                {'Field': 'Filename', 'Value': 'a', 'Operation': 'prefix'},
                            ],
                        },
                    ],
                },
            ],
        }, json.loads(sq.to_parameter_value()))

    def test_to_parameter_value_empty(self):
        self.assertEqual('{}', model.SimpleQuery().to_parameter_value())


# ==================== SimpleQuery ====================


class TestSimpleQueryRequest(unittest.TestCase):
    def test_empty_constructor(self):
        """Reference: Java SimpleQueryRequestTest.testEmptyBuilder()"""
        request = model.SimpleQueryRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.dataset_name)
        self.assertIsNone(request.max_results)
        self.assertIsNone(request.next_token)
        self.assertIsNone(request.sort)
        self.assertIsNone(request.order)
        self.assertIsNone(request.with_fields)
        self.assertIsNone(request.aggregations)
        self.assertIsNone(request.query)
        self.assertIsNone(request.without_total_hits)

    def test_full_constructor(self):
        """Reference: Java SimpleQueryRequestTest.testFullBuilder()"""
        sq = model.SimpleQuery(field='Filename', value='test', operation='prefix')
        agg = model.Aggregation(field='Size', operation='sum')
        request = model.SimpleQueryRequest(
            bucket='examplebucket',
            dataset_name='my-dataset',
            query=sq.to_parameter_value(),
            next_token='token-123',
            max_results=10,
            sort='Filename',
            order='asc',
            aggregations=meta_query_basic.MetaQueryAggregations(aggregation=[agg]).to_parameter_value(),
            with_fields=meta_query_basic.WithFields(with_field=['Filename', 'Size']).to_parameter_value(),
            without_total_hits=False,
        )
        self.assertEqual('examplebucket', request.bucket)
        self.assertEqual('my-dataset', request.dataset_name)
        self.assertEqual('{"Field": "Filename", "Value": "test", "Operation": "prefix"}', request.query)
        self.assertEqual('token-123', request.next_token)
        self.assertEqual(10, request.max_results)
        self.assertEqual('Filename', request.sort)
        self.assertEqual('asc', request.order)
        self.assertEqual('[{"Field": "Size", "Operation": "sum"}]', request.aggregations)
        self.assertEqual('["Filename", "Size"]', request.with_fields)
        self.assertFalse(request.without_total_hits)

    def test_xml_builder(self):
        """Reference: Java SimpleQueryRequestTest.xmlBuilder()"""
        sq = model.SimpleQuery(field='Size', value='1048576', operation='gt')
        agg = model.Aggregation(field='Size', operation='sum')
        request = model.SimpleQueryRequest(
            bucket='examplebucket',
            dataset_name='photos-2026',
            query=sq.to_parameter_value(),
            max_results=100,
            sort='Size',
            order='desc',
            aggregations=meta_query_basic.MetaQueryAggregations(aggregation=[agg]).to_parameter_value(),
            with_fields=meta_query_basic.WithFields(with_field=['OSSURI', 'Size', 'FileHash']).to_parameter_value(),
            without_total_hits=False,
        )
        op_input = serde.serialize_input(request, OperationInput(
            op_name='SimpleQuery',
            method='POST',
            parameters={'metaQuery': '', 'action': 'simpleQuery'},
            bucket=request.bucket,
        ))
        self.assertEqual('examplebucket', op_input.bucket)
        self.assertEqual('simpleQuery', op_input.parameters.get('action'))
        self.assertEqual('', op_input.parameters.get('metaQuery'))
        self.assertEqual('photos-2026', op_input.parameters.get('datasetName'))
        self.assertEqual('100', op_input.parameters.get('maxResults'))
        self.assertEqual('Size', op_input.parameters.get('sort'))
        self.assertEqual('desc', op_input.parameters.get('order'))
        self.assertEqual('false', op_input.parameters.get('withoutTotalHits'))
        self.assertIsNotNone(op_input.parameters.get('query'))
        self.assertEqual('POST', op_input.method)


class TestSimpleQueryResult(unittest.TestCase):
    def test_empty_constructor(self):
        """Reference: Java SimpleQueryResultTest.testEmptyBuilder()"""
        result = model.SimpleQueryResult()
        self.assertIsNone(result.next_token)
        self.assertIsNone(result.total_hits)
        self.assertIsNone(result.files)
        self.assertIsNone(result.aggregations)

    def test_xml_builder(self):
        """Reference: Java SimpleQueryResultTest.xmlBuilder()"""
        xml_data = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<MetaQuery>'
            '  <NextToken>next-page-token-xyz</NextToken>'
            '  <TotalHits>42</TotalHits>'
            '  <Files>'
            '    <File>'
            '      <Filename>photos/sunset.jpg</Filename>'
            '      <Size>2097152</Size>'
            '      <FileModifiedTime>2026-05-19T15:30:00.000+08:00</FileModifiedTime>'
            '      <ContentType>image/jpeg</ContentType>'
            '      <ObjectACL>default</ObjectACL>'
            '      <OSSStorageClass>Standard</OSSStorageClass>'
            '      <ETag>"D41D8CD98F00B204E9800998ECF8427E"</ETag>'
            '      <OSSTagging>'
            '        <Tagging>'
            '          <Key>routing-dataset</Key>'
            '          <Value>photos-2026</Value>'
            '        </Tagging>'
            '      </OSSTagging>'
            '      <Labels>'
            '        <Label>'
            '          <LabelName>夕阳</LabelName>'
            '          <LabelConfidence>0.98</LabelConfidence>'
            '        </Label>'
            '      </Labels>'
            '    </File>'
            '  </Files>'
            '</MetaQuery>'
        ).encode('utf-8')
        result = model.SimpleQueryResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({'x-oss-request-id': 'req-simple-query'}),
                http_response=MockHttpResponse(
                    status_code=200,
                    headers={'x-oss-request-id': 'req-simple-query'},
                    body=xml_data,
                ),
            ),
            custom_deserializer=[serde.deserialize_output_xmlbody],
        )
        self.assertEqual(200, result.status_code)
        self.assertEqual('req-simple-query', result.headers.get('x-oss-request-id'))

        # Verify response fields
        self.assertEqual('next-page-token-xyz', result.next_token)
        self.assertEqual(42, result.total_hits)

        # Verify files
        self.assertIsNotNone(result.files)
        self.assertEqual(1, len(result.files.file))
        file = result.files.file[0]
        self.assertEqual('photos/sunset.jpg', file.filename)
        self.assertEqual(2097152, file.size)
        self.assertEqual('2026-05-19T15:30:00.000+08:00', file.file_modified_time)
        self.assertEqual('image/jpeg', file.content_type)
        self.assertEqual('default', file.object_acl)
        self.assertEqual('Standard', file.oss_storage_class)
        self.assertEqual('"D41D8CD98F00B204E9800998ECF8427E"', file.e_tag)

        # Verify labels
        self.assertIsNotNone(file.labels)
        self.assertEqual(1, len(file.labels.label))
        self.assertEqual('夕阳', file.labels.label[0].label_name)
        self.assertEqual(0.98, file.labels.label[0].label_confidence)


# ==================== SemanticQuery ====================


class TestSemanticQueryRequest(unittest.TestCase):
    def test_empty_constructor(self):
        """Reference: Java SemanticQueryRequestTest.testEmptyBuilder()"""
        request = model.SemanticQueryRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.dataset_name)
        self.assertIsNone(request.max_results)
        self.assertIsNone(request.query)
        self.assertIsNone(request.with_fields)
        self.assertIsNone(request.media_types)
        self.assertIsNone(request.source_uri)
        self.assertIsNone(request.simple_query)

    def test_full_constructor(self):
        """Reference: Java SemanticQueryRequestTest.testFullBuilder()"""
        sq = model.SimpleQuery(field='Filename', value='test', operation='eq')
        request = model.SemanticQueryRequest(
            bucket='examplebucket',
            dataset_name='test-dataset',
            max_results=10,
            query='blue shirt man walking to table',
            with_fields=meta_query_basic.WithFields(with_field=['Filename', 'Size', 'MediaType']).to_parameter_value(),
            media_types=meta_query_basic.MediaTypes(media_type=['video', 'image']).to_parameter_value(),
            source_uri='oss://bucket/prefix/',
            simple_query=sq.to_parameter_value(),
        )
        self.assertEqual('examplebucket', request.bucket)
        self.assertEqual('test-dataset', request.dataset_name)
        self.assertEqual(10, request.max_results)
        self.assertEqual('blue shirt man walking to table', request.query)
        # with_fields is serialized as JSON
        self.assertEqual('["Filename", "Size", "MediaType"]', request.with_fields)
        # media_types is serialized as JSON
        self.assertEqual('["video", "image"]', request.media_types)
        self.assertEqual('oss://bucket/prefix/', request.source_uri)
        # simple_query is serialized as JSON
        parsed_sq = json.loads(request.simple_query)
        self.assertEqual('Filename', parsed_sq['Field'])
        self.assertEqual('test', parsed_sq['Value'])
        self.assertEqual('eq', parsed_sq['Operation'])

    def test_xml_builder(self):
        """Reference: Java SemanticQueryRequestTest.xmlBuilder()"""
        request = model.SemanticQueryRequest(
            bucket='examplebucket',
            dataset_name='photos-2026',
            query='客厅里的猫',
            media_types=meta_query_basic.MediaTypes(media_type=['image', 'video']).to_parameter_value(),
            simple_query='{"Field":"Size","Value":"102400","Operation":"gt"}',
            with_fields=meta_query_basic.WithFields(with_field=['OSSURI', 'Insights']).to_parameter_value(),
            max_results=20,
        )
        op_input = serde.serialize_input(request, OperationInput(
            op_name='SemanticQuery',
            method='POST',
            parameters={'metaQuery': '', 'action': 'semanticQuery'},
            bucket=request.bucket,
        ))
        self.assertEqual('examplebucket', op_input.bucket)
        self.assertEqual('semanticQuery', op_input.parameters.get('action'))
        self.assertEqual('', op_input.parameters.get('metaQuery'))
        self.assertEqual('photos-2026', op_input.parameters.get('datasetName'))
        self.assertEqual('客厅里的猫', op_input.parameters.get('query'))
        self.assertEqual('20', op_input.parameters.get('maxResults'))
        self.assertIsNotNone(op_input.parameters.get('mediaTypes'))
        self.assertIsNotNone(op_input.parameters.get('simpleQuery'))
        self.assertEqual('POST', op_input.method)

    def test_xml_builder_with_source_uri(self):
        """Reference: Java SemanticQueryRequestTest.xmlBuilderWithSourceURI()"""
        request = model.SemanticQueryRequest(
            bucket='examplebucket',
            dataset_name='photos-2026',
            source_uri='oss://examplebucket/photos/cat.jpg',
            media_types=meta_query_basic.MediaTypes(media_type=['image']).to_parameter_value(),
            max_results=10,
        )
        op_input = serde.serialize_input(request, OperationInput(
            op_name='SemanticQuery',
            method='POST',
            parameters={'metaQuery': '', 'action': 'semanticQuery'},
            bucket=request.bucket,
        ))
        self.assertEqual('examplebucket', op_input.bucket)
        self.assertEqual('semanticQuery', op_input.parameters.get('action'))
        self.assertEqual('oss://examplebucket/photos/cat.jpg', op_input.parameters.get('sourceURI'))
        self.assertEqual('POST', op_input.method)


class TestSemanticQueryResult(unittest.TestCase):
    def test_empty_constructor(self):
        """Reference: Java SemanticQueryResultTest.testEmptyBuilder()"""
        result = model.SemanticQueryResult()
        self.assertIsNone(result.files)

    def test_xml_builder(self):
        """Reference: Java SemanticQueryResultTest.testXmlBuilder()"""
        xml_data = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<MetaQuery>'
            '  <Files>'
            '    <File>'
            '      <Addresses/>'
            '      <AudioCovers/>'
            '      <AudioStreams>'
            '        <AudioStream>'
            '          <Bitrate>128000</Bitrate>'
            '          <ChannelLayout>stereo</ChannelLayout>'
            '          <Channels>2</Channels>'
            '          <CodecLongName>AAC (Advanced Audio Coding)</CodecLongName>'
            '          <CodecName>aac</CodecName>'
            '          <CodecTag>0x6134706d</CodecTag>'
            '          <CodecTagString>mp4a</CodecTagString>'
            '          <Duration>16.021769</Duration>'
            '          <FrameCount>690</FrameCount>'
            '          <Index>1</Index>'
            '          <SampleFormat>fltp</SampleFormat>'
            '          <SampleRate>44100</SampleRate>'
            '          <TimeBase>1/44100</TimeBase>'
            '        </AudioStream>'
            '      </AudioStreams>'
            '      <Bitrate>1656706</Bitrate>'
            '      <ContentMd5>5oJccWuBoqVXS8zrzckPlg==</ContentMd5>'
            '      <ContentType>video/mp4</ContentType>'
            '      <CreateTime>2026-04-21T20:28:17.018858947+08:00</CreateTime>'
            '      <CroppingSuggestions/>'
            '      <DatasetName>test-dataset-sem-vid-1776774492</DatasetName>'
            '      <Duration>16.034</Duration>'
            '      <ETag>"E6825C716B81A2A5574BCCEBCDC90F96"</ETag>'
            '      <Elements/>'
            '      <Figures/>'
            '      <FileHash>E6825C716B81A2A5574BCCEBCDC90F96</FileHash>'
            '      <FileModifiedTime>2026-04-21T20:28:13+08:00</FileModifiedTime>'
            '      <Filename>test-temp/sem-vid-1776774492774503000.mp4</Filename>'
            '      <FormatLongName>QuickTime / MOV</FormatLongName>'
            '      <FormatName>mov,mp4,m4a,3gp,3g2,mj2</FormatName>'
            '      <Insights>'
            '        <Video>'
            '          <Caption>蓝衣男走向餐桌</Caption>'
            '          <Description>这是一段室内高角度监控录像，场景为一个客厅。</Description>'
            '        </Video>'
            '      </Insights>'
            '      <Labels/>'
            '      <MediaType>video</MediaType>'
            '      <OCRContents/>'
            '      <OSSCRC64>2327801188977127298</OSSCRC64>'
            '      <OSSObjectType>Normal</OSSObjectType>'
            '      <OSSStorageClass>Standard</OSSStorageClass>'
            '      <OSSTagging>'
            '        <Tagging>'
            '          <Key>routing-dataset</Key>'
            '          <Value>test-dataset-sem-vid-1776774492</Value>'
            '        </Tagging>'
            '      </OSSTagging>'
            '      <OSSTaggingCount>1</OSSTaggingCount>'
            '      <ObjectACL>default</ObjectACL>'
            '      <Size>3320455</Size>'
            '      <StreamCount>2</StreamCount>'
            '      <Subtitles/>'
            '      <URI>oss://oss-metaquery-dataset-test/test-temp/sem-vid-1776774492774503000.mp4</URI>'
            '      <UpdateTime>2026-04-21T20:28:27.359034257+08:00</UpdateTime>'
            '      <VideoHeight>1080</VideoHeight>'
            '      <VideoStreams>'
            '        <VideoStream>'
            '          <AverageFrameRate>21645000/721493</AverageFrameRate>'
            '          <BitDepth>8</BitDepth>'
            '          <Bitrate>1521221</Bitrate>'
            '          <CodecLongName>H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10</CodecLongName>'
            '          <CodecName>h264</CodecName>'
            '          <CodecTag>0x31637661</CodecTag>'
            '          <CodecTagString>avc1</CodecTagString>'
            '          <ColorPrimaries>bt709</ColorPrimaries>'
            '          <ColorRange>tv</ColorRange>'
            '          <ColorSpace>bt709</ColorSpace>'
            '          <ColorTransfer>bt709</ColorTransfer>'
            '          <DisplayAspectRatio>16:9</DisplayAspectRatio>'
            '          <Duration>16.033178</Duration>'
            '          <FrameCount>481</FrameCount>'
            '          <FrameRate>90000/2999</FrameRate>'
            '          <Height>1080</Height>'
            '          <Level>31</Level>'
            '          <PixelFormat>yuv420p</PixelFormat>'
            '          <Profile>High</Profile>'
            '          <SampleAspectRatio>1:1</SampleAspectRatio>'
            '          <TimeBase>1/90000</TimeBase>'
            '          <Width>1920</Width>'
            '        </VideoStream>'
            '      </VideoStreams>'
            '      <VideoWidth>1920</VideoWidth>'
            '    </File>'
            '  </Files>'
            '</MetaQuery>'
        ).encode('utf-8')
        result = model.SemanticQueryResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({'x-oss-request-id': 'req-semantic'}),
                http_response=MockHttpResponse(
                    status_code=200,
                    headers={'x-oss-request-id': 'req-semantic'},
                    body=xml_data,
                ),
            ),
            custom_deserializer=[serde.deserialize_output_xmlbody],
        )
        self.assertEqual(200, result.status_code)
        self.assertEqual('req-semantic', result.headers.get('x-oss-request-id'))
        self.assertIsNotNone(result.files)
        self.assertEqual(1, len(result.files.file))

        file = result.files.file[0]
        self.assertEqual('test-dataset-sem-vid-1776774492', file.dataset_name)
        self.assertEqual('test-temp/sem-vid-1776774492774503000.mp4', file.filename)
        self.assertEqual('video', file.media_type)
        self.assertEqual('video/mp4', file.content_type)
        self.assertEqual(3320455, file.size)
        self.assertEqual(1920, file.video_width)
        self.assertEqual(1080, file.video_height)
        self.assertEqual(16.034, file.duration)
        self.assertEqual(1656706, file.bitrate)
        self.assertEqual(2, file.stream_count)
        self.assertEqual('Normal', file.oss_object_type)
        self.assertEqual('Standard', file.oss_storage_class)
        self.assertEqual('default', file.object_acl)

        # AudioStreams
        self.assertIsNotNone(file.audio_streams)
        self.assertEqual(1, len(file.audio_streams.audio_stream))
        audio_stream = file.audio_streams.audio_stream[0]
        self.assertEqual(128000, audio_stream.bitrate)
        self.assertEqual(2, audio_stream.channels)
        self.assertEqual('aac', audio_stream.codec_name)

        # VideoStreams
        self.assertIsNotNone(file.video_streams)
        self.assertEqual(1, len(file.video_streams.video_stream))
        video_stream = file.video_streams.video_stream[0]
        self.assertEqual(1920, video_stream.width)
        self.assertEqual(1080, video_stream.height)
        self.assertEqual('h264', video_stream.codec_name)
        self.assertEqual('High', video_stream.profile)

        # Insights
        self.assertIsNotNone(file.insights)
        self.assertIsNotNone(file.insights.video)
        self.assertEqual('蓝衣男走向餐桌', file.insights.video.caption)

    def test_xml_builder_with_labels_and_scene_elements(self):
        """Reference: Java SemanticQueryResultTest.testXmlBuilderWithLabelsAndSceneElements()"""
        xml_data = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<MetaQuery>'
            '  <Files>'
            '    <File>'
            '      <Addresses/>'
            '      <AudioCovers/>'
            '      <AudioStreams>'
            '        <AudioStream>'
            '          <Bitrate>14983</Bitrate>'
            '          <ChannelLayout>mono</ChannelLayout>'
            '          <Channels>1</Channels>'
            '          <CodecLongName>AAC (Advanced Audio Coding)</CodecLongName>'
            '          <CodecName>aac</CodecName>'
            '          <CodecTag>0x6134706d</CodecTag>'
            '          <CodecTagString>mp4a</CodecTagString>'
            '          <Duration>7.936</Duration>'
            '          <FrameCount>62</FrameCount>'
            '          <Index>1</Index>'
            '          <SampleFormat>fltp</SampleFormat>'
            '          <SampleRate>8000</SampleRate>'
            '          <TimeBase>1/8000</TimeBase>'
            '        </AudioStream>'
            '      </AudioStreams>'
            '      <Bitrate>196284</Bitrate>'
            '      <ContentMd5>5/ZLrWYXpuQfDfxEf4+lyA==</ContentMd5>'
            '      <ContentType>video/mp4</ContentType>'
            '      <CreateTime>2026-04-21T10:51:38.264045621+08:00</CreateTime>'
            '      <CroppingSuggestions/>'
            '      <DatasetName>dataset-aianalysis-walk</DatasetName>'
            '      <Duration>8</Duration>'
            '      <ETag>"E7F64BAD6617A6E41F0DFC447F8FA5C8"</ETag>'
            '      <Elements/>'
            '      <Figures/>'
            '      <FileHash>E7F64BAD6617A6E41F0DFC447F8FA5C8</FileHash>'
            '      <FileModifiedTime>2026-04-21T10:51:25+08:00</FileModifiedTime>'
            '      <Filename>mp4file/AE09411YAG00081_AE09411YAG00081-0_e723c79f850047458a3e0c0115c4b108_20260421104610825sf0-203372.mp4</Filename>'
            '      <FormatLongName>QuickTime / MOV</FormatLongName>'
            '      <FormatName>mov,mp4,m4a,3gp,3g2,mj2</FormatName>'
            '      <Labels>'
            '        <Label>'
            '          <LabelConfidence>1</LabelConfidence>'
            '          <LabelName>有人走过</LabelName>'
            '          <ParentLabelName>自定义标签</ParentLabelName>'
            '          <Clips>'
            '            <Clip>'
            '              <TimeRange>200</TimeRange>'
            '              <TimeRange>5533</TimeRange>'
            '            </Clip>'
            '          </Clips>'
            '        </Label>'
            '      </Labels>'
            '      <MediaType>video</MediaType>'
            '      <OCRContents/>'
            '      <OSSCRC64>16628192875747293357</OSSCRC64>'
            '      <OSSObjectType>Normal</OSSObjectType>'
            '      <OSSStorageClass>Standard</OSSStorageClass>'
            '      <OSSTagging>'
            '        <Tagging>'
            '          <Key>alarmId</Key>'
            '          <Value>AE09411YAG0008117767395421908241</Value>'
            '        </Tagging>'
            '        <Tagging>'
            '          <Key>test-routing-dataset</Key>'
            '          <Value>dataset-aianalysis-walk</Value>'
            '        </Tagging>'
            '      </OSSTagging>'
            '      <OSSTaggingCount>2</OSSTaggingCount>'
            '      <OSSUserMeta>'
            '        <UserMeta>'
            '          <Key>X-Oss-Meta-Author</Key>'
            '          <Value>oss</Value>'
            '        </UserMeta>'
            '      </OSSUserMeta>'
            '      <ObjectACL>default</ObjectACL>'
            '      <ProduceTime>2026-04-21T10:46:10+08:00</ProduceTime>'
            '      <SceneElements>'
            '        <SceneElement>'
            '          <FrameTimes>6000</FrameTimes>'
            '          <TimeRange>4133</TimeRange>'
            '          <TimeRange>8533</TimeRange>'
            '          <VideoStreamIndex>0</VideoStreamIndex>'
            '          <Labels/>'
            '        </SceneElement>'
            '      </SceneElements>'
            '      <Size>196284</Size>'
            '      <StreamCount>2</StreamCount>'
            '      <Subtitles/>'
            '      <URI>oss://paas-smart-cloud-test/mp4file/AE09411YAG00081_AE09411YAG00081-0_e723c79f850047458a3e0c0115c4b108_20260421104610825sf0-203372.mp4</URI>'
            '      <UpdateTime>2026-04-21T10:52:39.412605575+08:00</UpdateTime>'
            '      <VideoHeight>360</VideoHeight>'
            '      <VideoStreams>'
            '        <VideoStream>'
            '          <AverageFrameRate>15/1</AverageFrameRate>'
            '          <BitDepth>8</BitDepth>'
            '          <Bitrate>178202</Bitrate>'
            '          <CodecLongName>H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10</CodecLongName>'
            '          <CodecName>h264</CodecName>'
            '          <CodecTag>0x31637661</CodecTag>'
            '          <CodecTagString>avc1</CodecTagString>'
            '          <Duration>8</Duration>'
            '          <FrameCount>120</FrameCount>'
            '          <FrameRate>500/33</FrameRate>'
            '          <Height>360</Height>'
            '          <Level>22</Level>'
            '          <PixelFormat>yuv420p</PixelFormat>'
            '          <Profile>Main</Profile>'
            '          <TimeBase>1/1000</TimeBase>'
            '          <Width>640</Width>'
            '        </VideoStream>'
            '      </VideoStreams>'
            '      <VideoWidth>640</VideoWidth>'
            '    </File>'
            '  </Files>'
            '</MetaQuery>'
        ).encode('utf-8')
        result = model.SemanticQueryResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({'x-oss-request-id': 'req-semantic-labels'}),
                http_response=MockHttpResponse(
                    status_code=200,
                    headers={'x-oss-request-id': 'req-semantic-labels'},
                    body=xml_data,
                ),
            ),
            custom_deserializer=[serde.deserialize_output_xmlbody],
        )
        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.files)
        self.assertEqual(1, len(result.files.file))

        file = result.files.file[0]
        self.assertEqual('dataset-aianalysis-walk', file.dataset_name)
        self.assertEqual(
            'mp4file/AE09411YAG00081_AE09411YAG00081-0_e723c79f850047458a3e0c0115c4b108_20260421104610825sf0-203372.mp4',
            file.filename)
        self.assertEqual('video', file.media_type)
        self.assertEqual('video/mp4', file.content_type)
        self.assertEqual(196284, file.size)
        self.assertEqual(640, file.video_width)
        self.assertEqual(360, file.video_height)
        self.assertEqual(8.0, file.duration)
        self.assertEqual(196284, file.bitrate)
        self.assertEqual(2, file.stream_count)
        self.assertEqual('Normal', file.oss_object_type)
        self.assertEqual('Standard', file.oss_storage_class)
        self.assertEqual('default', file.object_acl)
        self.assertEqual('2026-04-21T10:46:10+08:00', file.produce_time)

        # AudioStreams
        self.assertIsNotNone(file.audio_streams)
        self.assertEqual(1, len(file.audio_streams.audio_stream))
        audio_stream = file.audio_streams.audio_stream[0]
        self.assertEqual(14983, audio_stream.bitrate)
        self.assertEqual(1, audio_stream.channels)
        self.assertEqual('aac', audio_stream.codec_name)
        self.assertEqual('mono', audio_stream.channel_layout)
        self.assertEqual(8000, audio_stream.sample_rate)

        # VideoStreams
        self.assertIsNotNone(file.video_streams)
        self.assertEqual(1, len(file.video_streams.video_stream))
        video_stream = file.video_streams.video_stream[0]
        self.assertEqual(640, video_stream.width)
        self.assertEqual(360, video_stream.height)
        self.assertEqual('h264', video_stream.codec_name)
        self.assertEqual('Main', video_stream.profile)
        self.assertEqual(178202, video_stream.bitrate)
        self.assertEqual(120, video_stream.frame_count)

        # Labels
        self.assertIsNotNone(file.labels)
        self.assertEqual(1, len(file.labels.label))
        label = file.labels.label[0]
        self.assertEqual('有人走过', label.label_name)
        self.assertEqual('自定义标签', label.parent_label_name)
        self.assertEqual(1.0, label.label_confidence)
        self.assertIsNotNone(label.clips)
        self.assertEqual(1, len(label.clips.clip))
        self.assertEqual([200, 5533], label.clips.clip[0].time_range)

        # SceneElements
        self.assertIsNotNone(file.scene_elements)
        self.assertEqual(1, len(file.scene_elements.scene_element))
        scene_element = file.scene_elements.scene_element[0]
        self.assertEqual([6000], scene_element.frame_times)
        self.assertEqual(0, scene_element.video_stream_index)
        self.assertEqual([4133, 8533], scene_element.time_range)


if __name__ == '__main__':
    unittest.main()
