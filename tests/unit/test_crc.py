# pylint: skip-file
import unittest
from alibabacloud_oss_v2 import crc

class TestCrc(unittest.TestCase):
    def test_crc64_combine(self):
        _POLY = 0x142F0E1EBA9EA3693
        _XOROUT = 0XFFFFFFFFFFFFFFFF

        string_a = b'12345'
        string_b = b'67890'

        crc64_a = crc.Crc64(0)
        crc64_a.update(string_a)
        crc1 = crc64_a.sum64()

        crc64_b = crc.Crc64(0)
        crc64_b.update(string_b)
        crc2 = crc64_b.sum64()

        crc_combine = crc.Crc64.combine(crc1, crc2, len(string_b))

        crc64_c = crc.Crc64(0)
        crc64_c.update(string_a + string_b)
        crc_raw = crc64_c.sum64()

        self.assertEqual(crc_combine, crc_raw)

 

