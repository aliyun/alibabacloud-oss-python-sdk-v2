# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_data_redundancy_transition as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse


class TestCreateBucketDataRedundancyTransition(unittest.TestCase):
    def test_constructor_request(self):
        request = model.CreateBucketDataRedundancyTransitionRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.target_redundancy_type)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.CreateBucketDataRedundancyTransitionRequest(
            bucket='bucketexampletest',
            target_redundancy_type='ZRS',
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('ZRS', request.target_redundancy_type)

    def test_serialize_request(self):
        request = model.CreateBucketDataRedundancyTransitionRequest(
            bucket='bucketexampletest',
            target_redundancy_type='ZRS',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='CreateBucketDataRedundancyTransition',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('CreateBucketDataRedundancyTransition', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)
        self.assertEqual('ZRS', op_input.parameters.get('x-oss-target-redundancy-type'))

    def test_constructor_result(self):
        result = model.CreateBucketDataRedundancyTransitionResult()
        self.assertIsNone(result.bucket_data_redundancy_transition)
        self.assertIsInstance(result, serde.Model)

        result = model.CreateBucketDataRedundancyTransitionResult(
            bucket_data_redundancy_transition=model.BucketDataRedundancyTransition(
                task_id='4be5beb0f74f490186311b268bf6****',
            ),
        )
        self.assertEqual('4be5beb0f74f490186311b268bf6****', result.bucket_data_redundancy_transition.task_id)

    def test_deserialize_result(self):
        xml_data = r'''
        <BucketDataRedundancyTransition>
        </BucketDataRedundancyTransition>'''

        result = model.CreateBucketDataRedundancyTransitionResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <BucketDataRedundancyTransition>
          <TaskId>4be5beb0f74f490186311b268bf6****</TaskId>
        </BucketDataRedundancyTransition>
        '''

        result = model.CreateBucketDataRedundancyTransitionResult()
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=xml_data,
            )
        )
        deserializer = [serde.deserialize_output_xmlbody]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertEqual('4be5beb0f74f490186311b268bf6****', result.bucket_data_redundancy_transition.task_id)


class TestGetBucketDataRedundancyTransition(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketDataRedundancyTransitionRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.redundancy_transition_taskid)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetBucketDataRedundancyTransitionRequest(
            bucket='bucketexampletest',
            redundancy_transition_taskid='test_redundancy_transition_taskid',
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('test_redundancy_transition_taskid', request.redundancy_transition_taskid)

    def test_serialize_request(self):
        request = model.GetBucketDataRedundancyTransitionRequest(
            bucket='bucketexampletest',
            redundancy_transition_taskid='test_redundancy_transition_taskid',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketDataRedundancyTransition',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetBucketDataRedundancyTransition', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)
        self.assertEqual('test_redundancy_transition_taskid', op_input.parameters.get('x-oss-redundancy-transition-taskid'))

    def test_constructor_result(self):
        result = model.GetBucketDataRedundancyTransitionResult()
        self.assertIsNone(result.bucket_data_redundancy_transition)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketDataRedundancyTransitionResult(
            bucket_data_redundancy_transition=model.BucketDataRedundancyTransition(
                bucket='bucketexampletest',
                task_id='909c6c818dd041d1a44e0fdc66aa****',
                status='enabled',
                create_time='2023-11-17T09:14:39.000Z',
                start_time='2023-11-17T09:14:39.000Z',
                end_time='2023-11-18T09:14:39.000Z',
                process_percentage=100,
                estimated_remaining_time=0,
            ),
        )
        self.assertEqual('bucketexampletest', result.bucket_data_redundancy_transition.bucket)
        self.assertEqual('909c6c818dd041d1a44e0fdc66aa****', result.bucket_data_redundancy_transition.task_id)
        self.assertEqual('enabled', result.bucket_data_redundancy_transition.status)
        self.assertEqual('2023-11-17T09:14:39.000Z', result.bucket_data_redundancy_transition.create_time)
        self.assertEqual('2023-11-17T09:14:39.000Z', result.bucket_data_redundancy_transition.start_time)
        self.assertEqual('2023-11-18T09:14:39.000Z', result.bucket_data_redundancy_transition.end_time)
        self.assertEqual(100, result.bucket_data_redundancy_transition.process_percentage)
        self.assertEqual(0, result.bucket_data_redundancy_transition.estimated_remaining_time)

    def test_deserialize_result(self):
        xml_data = r'''
        <BucketDataRedundancyTransition>
        </BucketDataRedundancyTransition>'''

        result = model.GetBucketDataRedundancyTransitionResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <BucketDataRedundancyTransition>
          <Bucket>examplebucket</Bucket>
          <TaskId>909c6c818dd041d1a44e0fdc66aa****</TaskId>
          <Status>Finished</Status>
          <CreateTime>2023-11-17T09:14:39.000Z</CreateTime>
          <StartTime>2023-11-17T09:14:39.000Z</StartTime>
          <ProcessPercentage>100</ProcessPercentage>
          <EstimatedRemainingTime>0</EstimatedRemainingTime>
          <EndTime>2023-11-18T09:14:39.000Z</EndTime>
        </BucketDataRedundancyTransition>
        '''

        result = model.GetBucketDataRedundancyTransitionResult()
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=xml_data,
            )
        )
        deserializer = [serde.deserialize_output_xmlbody]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertEqual('909c6c818dd041d1a44e0fdc66aa****', result.bucket_data_redundancy_transition.task_id)
        self.assertEqual('Finished', result.bucket_data_redundancy_transition.status)
        self.assertEqual('2023-11-17T09:14:39.000Z', result.bucket_data_redundancy_transition.create_time)
        self.assertEqual('2023-11-17T09:14:39.000Z', result.bucket_data_redundancy_transition.start_time)
        self.assertEqual(100, result.bucket_data_redundancy_transition.process_percentage)
        self.assertEqual(0, result.bucket_data_redundancy_transition.estimated_remaining_time)
        self.assertEqual('2023-11-18T09:14:39.000Z', result.bucket_data_redundancy_transition.end_time)


class TestListBucketDataRedundancyTransition(unittest.TestCase):
    def test_constructor_request(self):
        request = model.ListBucketDataRedundancyTransitionRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.ListBucketDataRedundancyTransitionRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.ListBucketDataRedundancyTransitionRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='ListBucketDataRedundancyTransition',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('ListBucketDataRedundancyTransition', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.ListBucketDataRedundancyTransitionResult()
        self.assertIsNone(result.list_bucket_data_redundancy_transition)
        self.assertIsInstance(result, serde.Model)

        result = model.ListBucketDataRedundancyTransitionResult(
            list_bucket_data_redundancy_transition=model.ListBucketDataRedundancyTransition(
                bucket_data_redundancy_transition=[model.BucketDataRedundancyTransition(
                    bucket='bucketexampletest',
                    task_id='4be5beb0f74f490186311b268bf6****',
                    status='enabled',
                    create_time='2023-11-17T08:40:17.000Z',
                    start_time='2023-11-17T10:40:17.000Z',
                    end_time='2023-11-18T09:40:17.000Z',
                    process_percentage=50,
                    estimated_remaining_time=16,
                ), model.BucketDataRedundancyTransition(
                    bucket='bucketexampletest2',
                    task_id='4be5beb0f78bf6j****',
                    status='disabled',
                    create_time='2024-11-17T08:40:17.000Z',
                    start_time='2024-11-17T11:40:17.000Z',
                    end_time='2024-11-18T09:40:17.000Z',
                    process_percentage=100,
                    estimated_remaining_time=0,
                )],
                is_truncated=True,
                next_continuation_token='NextChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            ),
        )
        self.assertEqual('bucketexampletest', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].bucket)
        self.assertEqual('4be5beb0f74f490186311b268bf6****', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].task_id)
        self.assertEqual('enabled', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].status)
        self.assertEqual('2023-11-17T08:40:17.000Z', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].create_time)
        self.assertEqual('2023-11-17T10:40:17.000Z', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].start_time)
        self.assertEqual('2023-11-18T09:40:17.000Z', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].end_time)
        self.assertEqual(50, result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].process_percentage)
        self.assertEqual(16, result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].estimated_remaining_time)
        self.assertEqual('bucketexampletest2', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].bucket)
        self.assertEqual('4be5beb0f78bf6j****', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].task_id)
        self.assertEqual('disabled', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].status)
        self.assertEqual('2024-11-17T08:40:17.000Z', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].create_time)
        self.assertEqual('2024-11-17T11:40:17.000Z', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].start_time)
        self.assertEqual('2024-11-18T09:40:17.000Z', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].end_time)
        self.assertEqual(100, result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].process_percentage)
        self.assertEqual(0, result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].estimated_remaining_time)
        self.assertEqual(True, result.list_bucket_data_redundancy_transition.is_truncated)
        self.assertEqual('NextChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', result.list_bucket_data_redundancy_transition.next_continuation_token)

    def test_deserialize_result(self):
        xml_data = r'''
        <ListBucketDataRedundancyTransition>
        </ListBucketDataRedundancyTransition>'''

        result = model.ListBucketDataRedundancyTransitionResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <ListBucketDataRedundancyTransition>
          <IsTruncated>false</IsTruncated>
          <NextContinuationToken></NextContinuationToken>
          <BucketDataRedundancyTransition>
            <Bucket>examplebucket1</Bucket>
            <TaskId>4be5beb0f74f490186311b268bf6****</TaskId>
            <Status>Queueing</Status>
            <CreateTime>2023-11-17T08:40:17.000Z</CreateTime>
          </BucketDataRedundancyTransition>
          <BucketDataRedundancyTransition>
            <Bucket>examplebucket2</Bucket>
            <TaskId>4be5beb0f74f490186311b268bf6j****</TaskId>
            <Status>Processing</Status>
            <CreateTime>2023-11-17T08:40:17.000Z</CreateTime>
            <StartTime>2023-11-17T10:40:17.000Z</StartTime>
            <ProcessPercentage>50</ProcessPercentage>
            <EstimatedRemainingTime>16</EstimatedRemainingTime>
          </BucketDataRedundancyTransition>
          <BucketDataRedundancyTransition>
            <Bucket>examplebucket3</Bucket>
            <TaskId>4be5beb0er4f490186311b268bf6j****</TaskId>
            <Status>Finished</Status>
            <CreateTime>2023-11-17T08:40:17.000Z</CreateTime>
            <StartTime>2023-11-17T11:40:17.000Z</StartTime>
            <ProcessPercentage>100</ProcessPercentage>
            <EstimatedRemainingTime>0</EstimatedRemainingTime>
            <EndTime>2023-11-18T09:40:17.000Z</EndTime>
          </BucketDataRedundancyTransition>
        </ListBucketDataRedundancyTransition>
        '''

        result = model.ListBucketDataRedundancyTransitionResult()
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=xml_data,
            )
        )
        deserializer = [serde.deserialize_output_xmlbody]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertEqual(False, result.list_bucket_data_redundancy_transition.is_truncated)
        self.assertEqual(None, result.list_bucket_data_redundancy_transition.next_continuation_token)
        self.assertEqual('examplebucket1', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].bucket)
        self.assertEqual('4be5beb0f74f490186311b268bf6****', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].task_id)
        self.assertEqual('Queueing', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].status)
        self.assertEqual('2023-11-17T08:40:17.000Z', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].create_time)
        self.assertEqual('examplebucket2', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].bucket)
        self.assertEqual('4be5beb0f74f490186311b268bf6j****', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].task_id)
        self.assertEqual('Processing', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].status)
        self.assertEqual('2023-11-17T08:40:17.000Z', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].create_time)
        self.assertEqual('2023-11-17T10:40:17.000Z', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].start_time)
        self.assertEqual(50, result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].process_percentage)
        self.assertEqual(16, result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].estimated_remaining_time)
        self.assertEqual('examplebucket3', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[2].bucket)
        self.assertEqual('4be5beb0er4f490186311b268bf6j****', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[2].task_id)
        self.assertEqual('Finished', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[2].status)
        self.assertEqual('2023-11-17T08:40:17.000Z', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[2].create_time)
        self.assertEqual('2023-11-17T11:40:17.000Z', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[2].start_time)
        self.assertEqual(100, result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[2].process_percentage)
        self.assertEqual(0, result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[2].estimated_remaining_time)
        self.assertEqual('2023-11-18T09:40:17.000Z', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[2].end_time)


class TestListUserDataRedundancyTransition(unittest.TestCase):
    def test_constructor_request(self):
        request = model.ListUserDataRedundancyTransitionRequest(
        )
        self.assertIsNone(request.max_keys)
        self.assertIsNone(request.continuation_token)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.ListUserDataRedundancyTransitionRequest(
            max_keys=10,
            continuation_token='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
        )
        self.assertEqual(10, request.max_keys)
        self.assertEqual('ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', request.continuation_token)

    def test_serialize_request(self):
        request = model.ListUserDataRedundancyTransitionRequest(
            max_keys=10,
            continuation_token='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='ListUserDataRedundancyTransition',
            method='POST',
        ))
        self.assertEqual('ListUserDataRedundancyTransition', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual(10, int(op_input.parameters.get('max-keys')))
        self.assertEqual('ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', op_input.parameters.get('continuation-token'))

    def test_constructor_result(self):
        result = model.ListUserDataRedundancyTransitionResult()
        self.assertIsNone(result.list_bucket_data_redundancy_transition)
        self.assertIsInstance(result, serde.Model)

        result = model.ListUserDataRedundancyTransitionResult(
            list_bucket_data_redundancy_transition=model.ListBucketDataRedundancyTransition(
                bucket_data_redundancy_transition=[model.BucketDataRedundancyTransition(
                    bucket='bucketexampletest',
                    task_id='4be5beb0f74f490186311b268bf6****',
                    status='enabled',
                    create_time='2023-11-17T08:40:17.000Z',
                    start_time='2023-11-17T10:40:17.000Z',
                    end_time='2023-11-18T09:40:17.000Z',
                    process_percentage=50,
                    estimated_remaining_time=16,
                ), model.BucketDataRedundancyTransition(
                    bucket='bucketexampletest',
                    task_id='4be5beb0f74f490186311b268bf6j****',
                    status='enabled',
                    create_time='2023-11-17T08:40:17.000Z',
                    start_time='2023-11-17T11:40:17.000Z',
                    end_time='2023-11-18T09:40:17.000Z',
                    process_percentage=100,
                    estimated_remaining_time=0,
                )],
                is_truncated=True,
                next_continuation_token='NextChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            ),
        )
        self.assertEqual('bucketexampletest', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].bucket)
        self.assertEqual('4be5beb0f74f490186311b268bf6****', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].task_id)
        self.assertEqual('enabled', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].status)
        self.assertEqual('2023-11-17T08:40:17.000Z', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].create_time)
        self.assertEqual('2023-11-17T10:40:17.000Z', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].start_time)
        self.assertEqual('2023-11-18T09:40:17.000Z', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].end_time)
        self.assertEqual(50, result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].process_percentage)
        self.assertEqual(16, result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].estimated_remaining_time)
        self.assertEqual('bucketexampletest', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].bucket)
        self.assertEqual('4be5beb0f74f490186311b268bf6j****', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].task_id)
        self.assertEqual('enabled', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].status)
        self.assertEqual('2023-11-17T08:40:17.000Z', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].create_time)
        self.assertEqual('2023-11-17T11:40:17.000Z', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].start_time)
        self.assertEqual('2023-11-18T09:40:17.000Z', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].end_time)
        self.assertEqual(100, result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].process_percentage)
        self.assertEqual(0, result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].estimated_remaining_time)
        self.assertEqual(True, result.list_bucket_data_redundancy_transition.is_truncated)
        self.assertEqual('NextChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', result.list_bucket_data_redundancy_transition.next_continuation_token)


    def test_deserialize_result(self):
        xml_data = r'''
        <ListBucketDataRedundancyTransition>
        </ListBucketDataRedundancyTransition>'''

        result = model.ListUserDataRedundancyTransitionResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <ListBucketDataRedundancyTransition>
          <IsTruncated>false</IsTruncated>
          <NextContinuationToken>aaa</NextContinuationToken>
          <BucketDataRedundancyTransition>
            <Bucket>examplebucket1</Bucket>
            <TaskId>4be5beb0f74f490186311b268bf6****</TaskId>
            <Status>Queueing</Status>
            <CreateTime>2023-11-17T08:40:17.000Z</CreateTime>
          </BucketDataRedundancyTransition>
          <BucketDataRedundancyTransition>
            <Bucket>examplebucket2</Bucket>
            <TaskId>4be5beb0f74f490186311b268bf6j****</TaskId>
            <Status>Processing</Status>
            <CreateTime>2023-11-17T08:40:17.000Z</CreateTime>
            <StartTime>2023-11-17T10:40:17.000Z</StartTime>
            <ProcessPercentage>50</ProcessPercentage>
            <EstimatedRemainingTime>16</EstimatedRemainingTime>
          </BucketDataRedundancyTransition>
          <BucketDataRedundancyTransition>
            <Bucket>examplebucket3</Bucket>
            <TaskId>4be5beb0er4f490186311b268bf6j****</TaskId>
            <Status>Finished</Status>
            <CreateTime>2023-11-17T08:40:17.000Z</CreateTime>
            <StartTime>2023-11-17T11:40:17.000Z</StartTime>
            <ProcessPercentage>100</ProcessPercentage>
            <EstimatedRemainingTime>0</EstimatedRemainingTime>
            <EndTime>2023-11-18T09:40:17.000Z</EndTime>
          </BucketDataRedundancyTransition>
        </ListBucketDataRedundancyTransition>
        '''

        result = model.ListUserDataRedundancyTransitionResult()
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=xml_data,
            )
        )
        deserializer = [serde.deserialize_output_xmlbody]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertEqual(False, result.list_bucket_data_redundancy_transition.is_truncated)
        self.assertEqual('aaa', result.list_bucket_data_redundancy_transition.next_continuation_token)
        self.assertEqual('examplebucket1', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].bucket)
        self.assertEqual('4be5beb0f74f490186311b268bf6****', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].task_id)
        self.assertEqual('Queueing', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].status)
        self.assertEqual('2023-11-17T08:40:17.000Z', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].create_time)
        self.assertEqual('examplebucket2', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].bucket)
        self.assertEqual('4be5beb0f74f490186311b268bf6j****', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].task_id)
        self.assertEqual('Processing', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].status)
        self.assertEqual('2023-11-17T08:40:17.000Z', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].create_time)
        self.assertEqual('2023-11-17T10:40:17.000Z', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].start_time)
        self.assertEqual(50, result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].process_percentage)
        self.assertEqual(16, result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[1].estimated_remaining_time)
        self.assertEqual('examplebucket3', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[2].bucket)
        self.assertEqual('4be5beb0er4f490186311b268bf6j****', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[2].task_id)
        self.assertEqual('Finished', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[2].status)
        self.assertEqual('2023-11-17T08:40:17.000Z', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[2].create_time)
        self.assertEqual('2023-11-17T11:40:17.000Z', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[2].start_time)
        self.assertEqual(100, result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[2].process_percentage)
        self.assertEqual(0, result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[2].estimated_remaining_time)
        self.assertEqual('2023-11-18T09:40:17.000Z', result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[2].end_time)


class TestDeleteBucketDataRedundancyTransition(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DeleteBucketDataRedundancyTransitionRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.redundancy_transition_taskid)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DeleteBucketDataRedundancyTransitionRequest(
            bucket='bucketexampletest',
            redundancy_transition_taskid='test_redundancy_transition_taskid',
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('test_redundancy_transition_taskid', request.redundancy_transition_taskid)

    def test_serialize_request(self):
        request = model.DeleteBucketDataRedundancyTransitionRequest(
            bucket='bucketexampletest',
            redundancy_transition_taskid='test_redundancy_transition_taskid',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteBucketDataRedundancyTransition',
            method='DELETE',
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteBucketDataRedundancyTransition', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)
        self.assertEqual('test_redundancy_transition_taskid', op_input.parameters.get('x-oss-redundancy-transition-taskid'))

    def test_constructor_result(self):
        result = model.DeleteBucketDataRedundancyTransitionResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.DeleteBucketDataRedundancyTransitionResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                    'x-oss-version-id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('x-oss-version-id'))
