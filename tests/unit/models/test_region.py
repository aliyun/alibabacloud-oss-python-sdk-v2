# pylint: skip-file
import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import region as model
from alibabacloud_oss_v2.types import OperationInput
from .. import MockHttpResponse

class TestDescribeRegions(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DescribeRegionsRequest()
        self.assertIsInstance(request, serde.Model)

        request = model.DescribeRegionsRequest(
            regions='oss-cn-hangzhou',
        )
        self.assertEqual('oss-cn-hangzhou', request.regions)

        request = model.DescribeRegionsRequest(
            regions='oss-cn-hangzhou',
            invalid_field='invalid_field'
        )
        self.assertTrue(hasattr(request, 'regions'))
        self.assertEqual('oss-cn-hangzhou', request.regions)
        self.assertFalse(hasattr(request, 'invalid_field'))

    def test_serialize_request(self):
        # case 1
        request = model.DescribeRegionsRequest(
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DescribeRegions',
            method='GET',
            parameters={
                'regions': request.regions,
            },
        ))

        self.assertEqual('DescribeRegions', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('', op_input.parameters.get('regions'))
        self.assertEqual(1, len(op_input.parameters.items()))

        # case 2
        request = model.DescribeRegionsRequest(
            regions='oss-cn-hangzhou',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DescribeRegions',
            method='GET',
            parameters={
                'regions': request.regions,
            },
        ))

        self.assertEqual('DescribeRegions', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('oss-cn-hangzhou', op_input.parameters.get('regions'))
        self.assertEqual(1, len(op_input.parameters.items()))

    def test_constructor_result(self):
        result = model.DescribeRegionsResult()
        self.assertIsNone(result.region_info)
        self.assertIsInstance(result, serde.Model)

        result = model.DescribeRegionsResult(
            region_info=[model.RegionInfo(
                region='oss-cn-hangzhou',
                internet_endpoint='oss-cn-hangzhou.aliyuncs.com',
                internal_endpoint='oss-cn-hangzhou-internal.aliyuncs.com',
                accelerate_endpoint='oss-accelerate.aliyuncs.com',
            )],
        )
        self.assertEqual('oss-cn-hangzhou', result.region_info[0].region)
        self.assertEqual('oss-cn-hangzhou-internal.aliyuncs.com', result.region_info[0].internal_endpoint)
        self.assertEqual('oss-cn-hangzhou.aliyuncs.com', result.region_info[0].internet_endpoint)
        self.assertEqual('oss-accelerate.aliyuncs.com', result.region_info[0].accelerate_endpoint)

        result = model.DescribeRegionsResult(
            region_info=[model.RegionInfo(
                region='oss-cn-hangzhou',
                internet_endpoint='oss-cn-hangzhou.aliyuncs.com',
                internal_endpoint='oss-cn-hangzhou-internal.aliyuncs.com',
                accelerate_endpoint='oss-accelerate.aliyuncs.com',
            )],
            invalid_field='invalid_field'
        )
        self.assertEqual('oss-cn-hangzhou', result.region_info[0].region)
        self.assertEqual('oss-cn-hangzhou-internal.aliyuncs.com', result.region_info[0].internal_endpoint)
        self.assertEqual('oss-cn-hangzhou.aliyuncs.com', result.region_info[0].internet_endpoint)
        self.assertEqual('oss-accelerate.aliyuncs.com', result.region_info[0].accelerate_endpoint)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = r'''
<RegionInfoList>
  <RegionInfo>
     <Region>oss-cn-hangzhou</Region>
     <InternetEndpoint>oss-cn-hangzhou.aliyuncs.com</InternetEndpoint>
     <InternalEndpoint>oss-cn-hangzhou-internal.aliyuncs.com</InternalEndpoint>
     <AccelerateEndpoint>oss-accelerate.aliyuncs.com</AccelerateEndpoint>  
  </RegionInfo>
  <RegionInfo>
     <Region>oss-cn-shanghai</Region>
     <InternetEndpoint>oss-cn-shanghai.aliyuncs.com</InternetEndpoint>
     <InternalEndpoint>oss-cn-shanghai-internal.aliyuncs.com</InternalEndpoint>
     <AccelerateEndpoint>oss-accelerate.aliyuncs.com</AccelerateEndpoint>  
  </RegionInfo>
</RegionInfoList>'''

        result = model.DescribeRegionsResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)
        self.assertEqual('oss-cn-hangzhou', result.region_info[0].region)
        self.assertEqual('oss-cn-hangzhou-internal.aliyuncs.com', result.region_info[0].internal_endpoint)
        self.assertEqual('oss-cn-hangzhou.aliyuncs.com', result.region_info[0].internet_endpoint)
        self.assertEqual('oss-accelerate.aliyuncs.com', result.region_info[0].accelerate_endpoint)
        self.assertEqual('oss-cn-shanghai', result.region_info[1].region)
        self.assertEqual('oss-cn-shanghai-internal.aliyuncs.com', result.region_info[1].internal_endpoint)
        self.assertEqual('oss-cn-shanghai.aliyuncs.com', result.region_info[1].internet_endpoint)
        self.assertEqual('oss-accelerate.aliyuncs.com', result.region_info[1].accelerate_endpoint)