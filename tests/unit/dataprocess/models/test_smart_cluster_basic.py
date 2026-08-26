# pylint: skip-file
"""Unit tests for dataprocess smart cluster models.

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
from alibabacloud_oss_v2.dataprocess.models import smart_cluster_basic as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict
from tests.unit import MockHttpResponse


# ==================== Sub-model tests ====================


class TestSmartClusterRule(unittest.TestCase):
    def test_empty_constructor(self):
        rule = model.SmartClusterRule()
        self.assertIsNone(rule.rule_type)
        self.assertIsNone(rule.base_uris)
        self.assertIsNone(rule.keywords)
        self.assertIsNone(rule.sensitivity)

    def test_full_constructor(self):
        rule = model.SmartClusterRule(
            rule_type='face',
            base_uris=['oss://examplebucket/refs/face1.jpg'],
            keywords=['人物', '车辆'],
            sensitivity=0.7,
        )
        self.assertEqual('face', rule.rule_type)
        self.assertEqual(1, len(rule.base_uris))
        self.assertEqual(2, len(rule.keywords))
        self.assertEqual(0.7, rule.sensitivity)

    def test_to_parameter_value(self):
        rule = model.SmartClusterRule(
            rule_type='face',
            base_uris=['oss://examplebucket/refs/face1.jpg'],
            keywords=['人物'],
            sensitivity=0.7,
        )
        self.assertEqual({
            'RuleType': 'face',
            'BaseURIs': ['oss://examplebucket/refs/face1.jpg'],
            'Keywords': ['人物'],
            'Sensitivity': 0.7,
        }, json.loads(rule.to_parameter_value()))
        self.assertEqual('{}', model.SmartClusterRule().to_parameter_value())


class TestSmartClusterMNS(unittest.TestCase):
    def test_empty_constructor(self):
        mns = model.SmartClusterMNS()
        self.assertIsNone(mns.topic_name)

    def test_full_constructor(self):
        mns = model.SmartClusterMNS(topic_name='imm-cluster-notification')
        self.assertEqual('imm-cluster-notification', mns.topic_name)


class TestSmartClusterNotificationInfo(unittest.TestCase):
    def test_empty_constructor(self):
        notif = model.SmartClusterNotificationInfo()
        self.assertIsNone(notif.mns)

    def test_full_constructor(self):
        notif = model.SmartClusterNotificationInfo(
            mns=model.SmartClusterMNS(topic_name='my-topic'),
        )
        self.assertEqual('my-topic', notif.mns.topic_name)

    def test_to_parameter_value(self):
        notif = model.SmartClusterNotificationInfo(
            mns=model.SmartClusterMNS(topic_name='my-topic'),
        )
        self.assertEqual('{"MNS": {"TopicName": "my-topic"}}', notif.to_parameter_value())
        self.assertEqual('{}', model.SmartClusterNotificationInfo().to_parameter_value())


class TestRules(unittest.TestCase):
    def test_empty_constructor(self):
        rules = model.Rules()
        self.assertIsNone(rules.rule)

    def test_full_constructor(self):
        rules = model.Rules(rule=[
            model.SmartClusterRule(rule_type='face', sensitivity=0.7),
            model.SmartClusterRule(rule_type='keywords'),
        ])
        self.assertEqual(2, len(rules.rule))
        self.assertEqual('face', rules.rule[0].rule_type)
        self.assertEqual('keywords', rules.rule[1].rule_type)

    def test_to_parameter_value(self):
        """The <Rule> wrapper is XML-only: JSON is a flat array."""
        rules = model.Rules(rule=[
            model.SmartClusterRule(rule_type='face', sensitivity=0.7),
            model.SmartClusterRule(rule_type='keywords'),
        ])
        self.assertEqual(
            '[{"RuleType": "face", "Sensitivity": 0.7}, {"RuleType": "keywords"}]',
            rules.to_parameter_value(),
        )
        self.assertEqual('[]', model.Rules().to_parameter_value())


class TestSmartClusterInfo(unittest.TestCase):
    def test_empty_constructor(self):
        info = model.SmartClusterInfo()
        self.assertIsNone(info.object_id)
        self.assertIsNone(info.cluster_type)
        self.assertIsNone(info.name)
        self.assertIsNone(info.description)
        self.assertIsNone(info.reason)
        self.assertIsNone(info.create_time)
        self.assertIsNone(info.update_time)
        self.assertIsNone(info.rules)
        self.assertIsNone(info.notification)

    def test_full_constructor(self):
        info = model.SmartClusterInfo(
            object_id='cluster-abc123',
            cluster_type='figure',
            name='face-cluster-alice',
            description='Face cluster for alice',
            create_time='2026-05-20T11:00:00.000+08:00',
            rules=model.Rules(rule=[model.SmartClusterRule(rule_type='face', sensitivity=0.7)]),
        )
        self.assertEqual('cluster-abc123', info.object_id)
        self.assertEqual('figure', info.cluster_type)
        self.assertEqual('face-cluster-alice', info.name)
        self.assertEqual(1, len(info.rules.rule))


# ==================== CreateSmartCluster ====================


class TestCreateSmartClusterRequest(unittest.TestCase):
    def test_empty_constructor(self):
        """Reference: Java CreateSmartClusterRequestTest.testEmptyBuilder()"""
        request = model.CreateSmartClusterRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.dataset_name)
        self.assertIsNone(request.name)
        self.assertIsNone(request.description)
        self.assertIsNone(request.cluster_type)
        self.assertIsNone(request.rules)
        self.assertIsNone(request.notification)

    def test_full_constructor(self):
        """Reference: Java CreateSmartClusterRequestTest.testFullBuilder()"""
        rule = model.SmartClusterRule(rule_type='Keyword')
        request = model.CreateSmartClusterRequest(
            bucket='examplebucket',
            dataset_name='my-dataset',
            name='my-cluster',
            cluster_type='keyword',
            description='test cluster',
            rules=model.Rules(rule=[rule]).to_parameter_value(),
            notification=model.SmartClusterNotificationInfo(
                mns=model.SmartClusterMNS(topic_name='my-topic')
            ).to_parameter_value(),
        )
        self.assertEqual('examplebucket', request.bucket)
        self.assertEqual('my-dataset', request.dataset_name)
        self.assertEqual('my-cluster', request.name)
        self.assertEqual('keyword', request.cluster_type)
        self.assertEqual('[{"RuleType": "Keyword"}]', request.rules)
        self.assertEqual('{"MNS": {"TopicName": "my-topic"}}', request.notification)

    def test_xml_builder(self):
        """Reference: Java CreateSmartClusterRequestTest.xmlBuilder()"""
        rule = model.SmartClusterRule(
            rule_type='face',
            base_uris=['oss://examplebucket/refs/face1.jpg'],
            sensitivity=0.7,
        )
        request = model.CreateSmartClusterRequest(
            bucket='examplebucket',
            dataset_name='photos-2026',
            name='face-cluster-alice',
            cluster_type='figure',
            description='Face cluster for alice',
            rules=model.Rules(rule=[rule]).to_parameter_value(),
        )
        op_input = serde.serialize_input(request, OperationInput(
            op_name='CreateSmartCluster',
            method='POST',
            parameters={'metaQuery': '', 'action': 'createSmartCluster'},
            bucket=request.bucket,
        ))
        self.assertEqual('examplebucket', op_input.bucket)
        self.assertEqual('createSmartCluster', op_input.parameters.get('action'))
        self.assertEqual('', op_input.parameters.get('metaQuery'))
        self.assertEqual('photos-2026', op_input.parameters.get('datasetName'))
        self.assertEqual('face-cluster-alice', op_input.parameters.get('name'))
        self.assertEqual('figure', op_input.parameters.get('clusterType'))
        self.assertEqual('Face cluster for alice', op_input.parameters.get('description'))
        self.assertIsNotNone(op_input.parameters.get('rules'))
        self.assertEqual('POST', op_input.method)


class TestCreateSmartClusterResult(unittest.TestCase):
    def test_empty_constructor(self):
        """Reference: Java CreateSmartClusterResultTest.testEmptyBuilder()"""
        result = model.CreateSmartClusterResult()
        self.assertIsNone(result.object_id)

    def test_xml_builder(self):
        """Reference: Java CreateSmartClusterResultTest.xmlBuilder()"""
        xml_data = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<CreateSmartClusterResponse>'
            b'<ObjectId>cluster-abc123def456</ObjectId>'
            b'</CreateSmartClusterResponse>'
        )
        result = model.CreateSmartClusterResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({'x-oss-request-id': 'req-create'}),
                http_response=MockHttpResponse(
                    status_code=200,
                    headers={'x-oss-request-id': 'req-create'},
                    body=xml_data,
                ),
            ),
            custom_deserializer=[serde.deserialize_output_xmlbody],
        )
        self.assertEqual(200, result.status_code)
        self.assertEqual('cluster-abc123def456', result.object_id)


# ==================== GetSmartCluster ====================


class TestGetSmartClusterRequest(unittest.TestCase):
    def test_empty_constructor(self):
        request = model.GetSmartClusterRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.dataset_name)
        self.assertIsNone(request.object_id)

    def test_full_constructor(self):
        request = model.GetSmartClusterRequest(
            bucket='examplebucket',
            dataset_name='photos-2026',
            object_id='cluster-abc123',
        )
        self.assertEqual('examplebucket', request.bucket)
        self.assertEqual('cluster-abc123', request.object_id)

    def test_xml_builder(self):
        """Reference: Java GetSmartClusterRequestTest.xmlBuilder()"""
        request = model.GetSmartClusterRequest(
            bucket='examplebucket',
            dataset_name='photos-2026',
            object_id='cluster-abc123',
        )
        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetSmartCluster',
            method='POST',
            parameters={'metaQuery': '', 'action': 'getSmartCluster'},
            bucket=request.bucket,
        ))
        self.assertEqual('cluster-abc123', op_input.parameters.get('objectId'))
        self.assertEqual('getSmartCluster', op_input.parameters.get('action'))


class TestGetSmartClusterResult(unittest.TestCase):
    def test_empty_constructor(self):
        """Reference: Java GetSmartClusterResultTest.testEmptyBuilder()"""
        result = model.GetSmartClusterResult()
        self.assertIsNone(result.smart_cluster)

    def test_xml_builder(self):
        """Reference: Java GetSmartClusterResultTest.xmlBuilder()"""
        xml_data = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<GetSmartClusterResponse>'
            '  <SmartCluster>'
            '    <ObjectId>cluster-abc123def456</ObjectId>'
            '    <ClusterType>figure</ClusterType>'
            '    <Name>face-cluster-alice</Name>'
            '    <Description>Face cluster for alice</Description>'
            '    <Rules>'
            '    <Rule>'
            '      <RuleType>face</RuleType>'
            '      <BaseURIs>oss://examplebucket/refs/alice1.jpg</BaseURIs>'
            '      <BaseURIs>oss://examplebucket/refs/alice2.jpg</BaseURIs>'
            '      <Keywords>人物</Keywords>'
            '      <Keywords>车辆</Keywords>'
            '      <Sensitivity>0.7</Sensitivity>'
            '    </Rule>'
            '    </Rules>'
            '    <Reason></Reason>'
            '    <Notification>'
            '      <MNS><TopicName>imm-cluster-notification</TopicName></MNS>'
            '    </Notification>'
            '    <CreateTime>2026-05-20T11:00:00.000+08:00</CreateTime>'
            '    <UpdateTime>2026-05-20T11:08:00.000+08:00</UpdateTime>'
            '  </SmartCluster>'
            '</GetSmartClusterResponse>'
        ).encode('utf-8')
        result = model.GetSmartClusterResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({'x-oss-request-id': 'req-get-smartcluster'}),
                http_response=MockHttpResponse(
                    status_code=200,
                    headers={'x-oss-request-id': 'req-get-smartcluster'},
                    body=xml_data,
                ),
            ),
            custom_deserializer=[serde.deserialize_output_xmlbody],
        )
        self.assertEqual(200, result.status_code)
        self.assertEqual('req-get-smartcluster', result.headers.get('x-oss-request-id'))
        self.assertIsNotNone(result.smart_cluster)

        sc = result.smart_cluster
        self.assertEqual('cluster-abc123def456', sc.object_id)
        self.assertEqual('figure', sc.cluster_type)
        self.assertEqual('face-cluster-alice', sc.name)
        self.assertEqual('Face cluster for alice', sc.description)
        self.assertEqual('2026-05-20T11:00:00.000+08:00', sc.create_time)
        self.assertEqual('2026-05-20T11:08:00.000+08:00', sc.update_time)

        # Rules
        self.assertIsNotNone(sc.rules)
        self.assertEqual(1, len(sc.rules.rule))
        self.assertEqual('face', sc.rules.rule[0].rule_type)
        self.assertEqual(2, len(sc.rules.rule[0].base_uris))
        self.assertEqual('oss://examplebucket/refs/alice1.jpg', sc.rules.rule[0].base_uris[0])
        self.assertEqual(2, len(sc.rules.rule[0].keywords))
        self.assertEqual('人物', sc.rules.rule[0].keywords[0])
        self.assertEqual(0.7, sc.rules.rule[0].sensitivity)

        # Notification
        self.assertIsNotNone(sc.notification)
        self.assertIsNotNone(sc.notification.mns)
        self.assertEqual('imm-cluster-notification', sc.notification.mns.topic_name)


# ==================== UpdateSmartCluster ====================


class TestUpdateSmartClusterRequest(unittest.TestCase):
    def test_empty_constructor(self):
        request = model.UpdateSmartClusterRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.object_id)
        self.assertIsNone(request.name)
        self.assertIsNone(request.rules)
        self.assertIsNone(request.rule)
        self.assertIsNone(request.notification)

    def test_full_constructor(self):
        request = model.UpdateSmartClusterRequest(
            bucket='examplebucket',
            dataset_name='ds',
            object_id='sc-1',
            name='updated-name',
            description='updated desc',
        )
        self.assertEqual('sc-1', request.object_id)
        self.assertEqual('updated-name', request.name)

    def test_xml_builder(self):
        """Reference: Java UpdateSmartClusterRequestTest.xmlBuilder()"""
        rule = model.SmartClusterRule(rule_type='face', sensitivity=0.7)
        request = model.UpdateSmartClusterRequest(
            bucket='examplebucket',
            dataset_name='photos-2026',
            object_id='cluster-abc123',
            name='updated-cluster',
            rules=model.Rules(rule=[rule]).to_parameter_value(),
            rule=rule.to_parameter_value(),
        )
        op_input = serde.serialize_input(request, OperationInput(
            op_name='UpdateSmartCluster',
            method='POST',
            parameters={'metaQuery': '', 'action': 'updateSmartCluster'},
            bucket=request.bucket,
        ))
        self.assertEqual('cluster-abc123', op_input.parameters.get('objectId'))
        self.assertEqual('updated-cluster', op_input.parameters.get('name'))
        self.assertEqual('updateSmartCluster', op_input.parameters.get('action'))
        self.assertIsNotNone(op_input.parameters.get('rules'))
        self.assertEqual('{"RuleType": "face", "Sensitivity": 0.7}', op_input.parameters.get('rule'))


class TestUpdateSmartClusterResult(unittest.TestCase):
    def test_empty_constructor(self):
        result = model.UpdateSmartClusterResult()
        self.assertIsNone(result.object_id)

    def test_xml_builder(self):
        """Reference: Java UpdateSmartClusterResultTest.xmlBuilder()"""
        xml_data = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<UpdateSmartClusterResponse>'
            b'<ObjectId>sc-1</ObjectId>'
            b'</UpdateSmartClusterResponse>'
        )
        result = model.UpdateSmartClusterResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({'x-oss-request-id': 'req-update'}),
                http_response=MockHttpResponse(
                    status_code=200,
                    headers={'x-oss-request-id': 'req-update'},
                    body=xml_data,
                ),
            ),
            custom_deserializer=[serde.deserialize_output_xmlbody],
        )
        self.assertEqual('sc-1', result.object_id)


# ==================== DeleteSmartCluster ====================


class TestDeleteSmartClusterRequest(unittest.TestCase):
    def test_empty_constructor(self):
        request = model.DeleteSmartClusterRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.dataset_name)
        self.assertIsNone(request.object_id)

    def test_full_constructor(self):
        request = model.DeleteSmartClusterRequest(
            bucket='examplebucket',
            dataset_name='photos-2026',
            object_id='cluster-abc123',
        )
        self.assertEqual('cluster-abc123', request.object_id)

    def test_xml_builder(self):
        """Reference: Java DeleteSmartClusterRequestTest.xmlBuilder()"""
        request = model.DeleteSmartClusterRequest(
            bucket='examplebucket',
            dataset_name='photos-2026',
            object_id='cluster-abc123',
        )
        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteSmartCluster',
            method='POST',
            parameters={'metaQuery': '', 'action': 'deleteSmartCluster'},
            bucket=request.bucket,
        ))
        self.assertEqual('cluster-abc123', op_input.parameters.get('objectId'))
        self.assertEqual('deleteSmartCluster', op_input.parameters.get('action'))


class TestDeleteSmartClusterResult(unittest.TestCase):
    def test_empty_constructor(self):
        result = model.DeleteSmartClusterResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_xml_builder(self):
        result = model.DeleteSmartClusterResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({'x-oss-request-id': 'req-del'}),
                http_response=MockHttpResponse(
                    status_code=200,
                    headers={'x-oss-request-id': 'req-del'},
                    body=None,
                ),
            ),
        )
        self.assertEqual(200, result.status_code)


# ==================== ListSmartClusters ====================


class TestListSmartClustersRequest(unittest.TestCase):
    def test_empty_constructor(self):
        request = model.ListSmartClustersRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.dataset_name)
        self.assertIsNone(request.max_results)
        self.assertIsNone(request.next_token)
        self.assertIsNone(request.cluster_type)
        self.assertIsNone(request.rule_types)

    def test_full_constructor(self):
        request = model.ListSmartClustersRequest(
            bucket='examplebucket',
            dataset_name='photos-2026',
            max_results=10,
            cluster_type='figure',
            rule_types='["face", "keywords"]',
        )
        self.assertEqual('examplebucket', request.bucket)
        self.assertEqual(10, request.max_results)
        self.assertEqual('figure', request.cluster_type)
        self.assertEqual('["face", "keywords"]', request.rule_types)

    def test_xml_builder(self):
        """Reference: Java ListSmartClustersRequestTest.xmlBuilder()"""
        request = model.ListSmartClustersRequest(
            bucket='examplebucket',
            dataset_name='photos-2026',
            max_results=5,
            cluster_type='figure',
        )
        op_input = serde.serialize_input(request, OperationInput(
            op_name='ListSmartClusters',
            method='POST',
            parameters={'metaQuery': '', 'action': 'listSmartClusters'},
            bucket=request.bucket,
        ))
        self.assertEqual('5', op_input.parameters.get('maxResults'))
        self.assertEqual('figure', op_input.parameters.get('clusterType'))
        self.assertEqual('listSmartClusters', op_input.parameters.get('action'))


class TestListSmartClustersResult(unittest.TestCase):
    def test_empty_constructor(self):
        result = model.ListSmartClustersResult()
        self.assertIsNone(result.smart_clusters)
        self.assertIsNone(result.next_token)

    def test_xml_builder(self):
        """Reference: Java ListSmartClustersResultTest.xmlBuilder()"""
        xml_data = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<ListSmartClustersResponse>'
            b'  <SmartClusters>'
            b'  <SmartCluster>'
            b'    <ObjectId>sc-1</ObjectId>'
            b'    <Name>cluster-1</Name>'
            b'    <ClusterType>face</ClusterType>'
            b'  </SmartCluster>'
            b'  <SmartCluster>'
            b'    <ObjectId>sc-2</ObjectId>'
            b'    <Name>cluster-2</Name>'
            b'    <ClusterType>keywords</ClusterType>'
            b'  </SmartCluster>'
            b'  </SmartClusters>'
            b'  <NextToken>token456</NextToken>'
            b'</ListSmartClustersResponse>'
        )
        result = model.ListSmartClustersResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({'x-oss-request-id': 'req-list'}),
                http_response=MockHttpResponse(
                    status_code=200,
                    headers={'x-oss-request-id': 'req-list'},
                    body=xml_data,
                ),
            ),
            custom_deserializer=[serde.deserialize_output_xmlbody],
        )
        self.assertIsNotNone(result.smart_clusters)
        self.assertEqual(2, len(result.smart_clusters.smart_cluster))
        self.assertEqual('sc-1', result.smart_clusters.smart_cluster[0].object_id)
        self.assertEqual('cluster-1', result.smart_clusters.smart_cluster[0].name)
        self.assertEqual('face', result.smart_clusters.smart_cluster[0].cluster_type)
        self.assertEqual('sc-2', result.smart_clusters.smart_cluster[1].object_id)
        self.assertEqual('keywords', result.smart_clusters.smart_cluster[1].cluster_type)
        self.assertEqual('token456', result.next_token)


if __name__ == '__main__':
    unittest.main()
