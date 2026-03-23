# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_object_worm_configuration as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse


class TestPutBucketObjectWormConfiguration(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutBucketObjectWormConfigurationRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.object_worm_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutBucketObjectWormConfigurationRequest(
            bucket='bucketexampletest',
            object_worm_configuration=model.ObjectWormConfiguration(
                object_worm_enabled='Enabled',
                rule=model.ObjectWormConfigurationRule(
                    default_retention=model.ObjectWormConfigurationRuleDefaultRetention(
                        mode=model.ObjectWormConfigurationModeType.GOVERNANCE,
                        days=1,
                    ),
                ),
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('Enabled', request.object_worm_configuration.object_worm_enabled)
        self.assertEqual(model.ObjectWormConfigurationModeType.GOVERNANCE, request.object_worm_configuration.rule.default_retention.mode)
        self.assertEqual(1, request.object_worm_configuration.rule.default_retention.days)

    def test_serialize_request(self):
        request = model.PutBucketObjectWormConfigurationRequest(
            bucket='bucketexampletest',
            object_worm_configuration=model.ObjectWormConfiguration(
                object_worm_enabled='Enabled',
                rule=model.ObjectWormConfigurationRule(
                    default_retention=model.ObjectWormConfigurationRuleDefaultRetention(
                        mode=model.ObjectWormConfigurationModeType.GOVERNANCE,
                        days=1,
                    ),
                ),
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutBucketObjectWormConfiguration',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutBucketObjectWormConfiguration', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.PutBucketObjectWormConfigurationResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutBucketObjectWormConfigurationResult()
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


class TestGetBucketObjectWormConfiguration(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketObjectWormConfigurationRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetBucketObjectWormConfigurationRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.GetBucketObjectWormConfigurationRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketObjectWormConfiguration',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetBucketObjectWormConfiguration', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetBucketObjectWormConfigurationResult()
        self.assertIsNone(result.object_worm_configuration)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketObjectWormConfigurationResult(
            object_worm_configuration=model.ObjectWormConfiguration(
                object_worm_enabled='Enabled',
                rule=model.ObjectWormConfigurationRule(
                    default_retention=model.ObjectWormConfigurationRuleDefaultRetention(
                        mode=model.ObjectWormConfigurationModeType.GOVERNANCE,
                        days=1,
                    ),
                ),
            ),
        )
        self.assertEqual('Enabled', result.object_worm_configuration.object_worm_enabled)
        self.assertEqual(model.ObjectWormConfigurationModeType.GOVERNANCE, result.object_worm_configuration.rule.default_retention.mode)
        self.assertEqual(1, result.object_worm_configuration.rule.default_retention.days)

    def test_deserialize_result(self):
        xml_data = r'''
        <ObjectWormConfiguration>
        </ObjectWormConfiguration>'''

        result = model.GetBucketObjectWormConfigurationResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <ObjectWormConfiguration>
          <ObjectWormEnabled>Enabled</ObjectWormEnabled>
          <Rule>
            <DefaultRetention>
              <Mode>GOVERNANCE</Mode>
              <Days>1</Days>
            </DefaultRetention>
          </Rule>
        </ObjectWormConfiguration>
        '''

        result = model.GetBucketObjectWormConfigurationResult()
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
        self.assertEqual('Enabled', result.object_worm_configuration.object_worm_enabled)
        self.assertEqual('GOVERNANCE', result.object_worm_configuration.rule.default_retention.mode)
        self.assertEqual(1, result.object_worm_configuration.rule.default_retention.days)


    def test_validation(self):
        print("Testing WORM rule validation...")
        print("=" * 80)
    
        # Test 1: Both days and years are None (should fail)
        print("\nTest 1: Both days and years are None (should fail)")
        try:
            retention = model.ObjectWormConfigurationRuleDefaultRetention(
                mode='GOVERNANCE'
            )
            print("  ✗ FAILED: Should have raised ValueError")
        except ValueError as e:
            print(f"  ✓ PASSED: {str(e)}")
        except Exception as e:
            print(f"  ✗ FAILED: Unexpected error: {str(e)}")
    
        # Test 2: days = 0 (should fail)
        print("\nTest 2: days = 0 (should fail)")
        try:
            retention = model.ObjectWormConfigurationRuleDefaultRetention(
                mode='GOVERNANCE',
                days=0
            )
            print("  ✗ FAILED: Should have raised ValueError")
        except ValueError as e:
            print(f"  ✓ PASSED: {str(e)}")
        except Exception as e:
            print(f"  ✗ FAILED: Unexpected error: {str(e)}")
    
        # Test 3: days < 0 (should fail)
        print("\nTest 3: days < 0 (should fail)")
        try:
            retention = model.ObjectWormConfigurationRuleDefaultRetention(
                mode='GOVERNANCE',
                days=-5
            )
            print("  ✗ FAILED: Should have raised ValueError")
        except ValueError as e:
            print(f"  ✓ PASSED: {str(e)}")
        except Exception as e:
            print(f"  ✗ FAILED: Unexpected error: {str(e)}")
    
        # Test 4: years = 0 (should fail)
        print("\nTest 4: years = 0 (should fail)")
        try:
            retention = model.ObjectWormConfigurationRuleDefaultRetention(
                mode='GOVERNANCE',
                years=0
            )
            print("  ✗ FAILED: Should have raised ValueError")
        except ValueError as e:
            print(f"  ✓ PASSED: {str(e)}")
        except Exception as e:
            print(f"  ✗ FAILED: Unexpected error: {str(e)}")
    
        # Test 5: years < 0 (should fail)
        print("\nTest 5: years < 0 (should fail)")
        try:
            retention = model.ObjectWormConfigurationRuleDefaultRetention(
                mode='GOVERNANCE',
                years=-3
            )
            print("  ✗ FAILED: Should have raised ValueError")
        except ValueError as e:
            print(f"  ✓ PASSED: {str(e)}")
        except Exception as e:
            print(f"  ✗ FAILED: Unexpected error: {str(e)}")
    
        # Test 6: Only days specified (should pass)
        print("\nTest 6: Only days specified (should pass)")
        try:
            retention = model.ObjectWormConfigurationRuleDefaultRetention(
                mode='GOVERNANCE',
                days=30
            )
            print(f"  ✓ PASSED: Created with days={retention.days}, years={retention.years}")
        except Exception as e:
            print(f"  ✗ FAILED: {str(e)}")
    
        # Test 7: Only years specified (should pass)
        print("\nTest 7: Only years specified (should pass)")
        try:
            retention = model.ObjectWormConfigurationRuleDefaultRetention(
                mode='COMPLIANCE',
                years=5
            )
            print(f"  ✓ PASSED: Created with days={retention.days}, years={retention.years}")
        except Exception as e:
            print(f"  ✗ FAILED: {str(e)}")
    
        # Test 8: Both days and years specified (should pass)
        print("\nTest 8: Both days and years specified (should pass)")
        try:
            retention = model.ObjectWormConfigurationRuleDefaultRetention(
                mode='GOVERNANCE',
                days=365,
                years=1
            )
            print(f"  ✓ PASSED: Created with days={retention.days}, years={retention.years}")
        except Exception as e:
            print(f"  ✗ FAILED: {str(e)}")
    
        # Test 9: days = 1 (boundary, should pass)
        print("\nTest 9: days = 1 (boundary, should pass)")
        try:
            retention = model.ObjectWormConfigurationRuleDefaultRetention(
                mode='GOVERNANCE',
                days=1
            )
            print(f"  ✓ PASSED: Created with days={retention.days}")
        except Exception as e:
            print(f"  ✗ FAILED: {str(e)}")
    
        # Test 10: years = 1 (boundary, should pass)
        print("\nTest 10: years = 1 (boundary, should pass)")
        try:
            retention = model.ObjectWormConfigurationRuleDefaultRetention(
                mode='GOVERNANCE',
                years=1
            )
            print(f"  ✓ PASSED: Created with years={retention.years}")
        except Exception as e:
            print(f"  ✗ FAILED: {str(e)}")
    
        print("\n" + "=" * 80)
        print("Validation tests completed!")