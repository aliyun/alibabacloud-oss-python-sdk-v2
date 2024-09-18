# pylint: skip-file
import unittest
from alibabacloud_oss_v2 import utils

class TestUtils(unittest.TestCase):
    def test_escape_xml_value(self):
        data = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
        encstr= '&#00;&#01;&#02;&#03;&#04;&#05;&#06;&#07;&#08;&#09;&#10;&#11;&#12;&#13;&#14;&#15;'
        edata = utils.escape_xml_value(data.decode())
        self.assertEqual(encstr, edata)

        data = b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\xe4\xbd\xa0\xe5\xa5\xbd'
        encstr= '&#16;&#17;&#18;&#19;&#20;&#21;&#22;&#23;&#24;&#25;&#26;&#27;&#28;&#29;&#30;&#31; !你好'
        edata = utils.escape_xml_value(data.decode())
        self.assertEqual(encstr, edata)


        data = '<>&"'
        encstr= '&lt;&gt;&amp;&quot;'
        edata = utils.escape_xml_value(data)
        self.assertEqual(encstr, edata)

 

