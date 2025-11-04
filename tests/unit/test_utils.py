# pylint: skip-file
import unittest
import io
from alibabacloud_oss_v2 import utils
from alibabacloud_oss_v2 import __version__


class TestUtils(unittest.TestCase):

    def test_safety_str(self):
        self.assertEqual('abc', utils.safety_str('abc'))
        self.assertEqual('', utils.safety_str(''))
        self.assertEqual('', utils.safety_str(None))

    def test_safety_bool(self):
        self.assertEqual(True, utils.safety_bool(True))
        self.assertEqual(False, utils.safety_bool(False))
        self.assertEqual(False, utils.safety_bool(None))

    def test_safety_int(self):
        self.assertEqual(123, utils.safety_int(123))
        self.assertEqual(0, utils.safety_int(0))
        self.assertEqual(0, utils.safety_int(None))

    def test_ensure_boolean(self):
        self.assertEqual(True, utils.ensure_boolean(True))
        self.assertEqual(False, utils.ensure_boolean(False))
        self.assertEqual(True, utils.ensure_boolean('true'))
        self.assertEqual(True, utils.ensure_boolean('True'))

        self.assertEqual(False, utils.ensure_boolean('abc'))
        self.assertEqual(False, utils.ensure_boolean(None))

    def test_lowercase_dict(self):
        dict1 = {"A":'A', 'b':'B', 'Ca':'123'}
        dict2 = utils.lowercase_dict(dict1)

        self.assertEqual(3, len(dict2.items()))
        self.assertEqual('A', dict2['a'])
        self.assertEqual('B', dict2['b'])
        self.assertEqual('123', dict2['ca'])

        self.assertIsNone(dict2.get('A', None))
        self.assertIsNone(dict2.get('Ca', None))


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

 
    def test_guess_content_type(self):
        self.assertEqual("text/html", utils.guess_content_type("demo.html", None))
        self.assertEqual("text/html", utils.guess_content_type("demo.htm", None))
        self.assertEqual("text/plain", utils.guess_content_type("demo.txt", None))
        self.assertEqual("application/javascript", utils.guess_content_type("demo.js", None))
        self.assertEqual("application/vnd.android.package-archive", utils.guess_content_type("demo.apk", None))
        self.assertEqual(None, utils.guess_content_type("demo", None))
        self.assertEqual(None, utils.guess_content_type("demo.321", None))
        self.assertEqual('', utils.guess_content_type("demo.321", ''))

        self.assertEqual("text/html", utils.guess_content_type("demo.txt.html", None))


    def test_guess_content_length(self):
        self.assertEqual(0, utils.guess_content_length(None))
        self.assertEqual(3, utils.guess_content_length(b'123'))
        self.assertEqual(11, utils.guess_content_length('hello world'))

        with open("./tests/data/example.jpg", 'rb') as f:
            self.assertEqual(21839, utils.guess_content_length(f))

        self.assertEqual(None, utils.guess_content_length(ValueError('')))


    def test_parse_content_range(self):
        # bytes 22-33/42 and bytes 22-33/* format
        values = utils.parse_content_range('bytes 22-33/42')
        self.assertEqual(22, values[0])
        self.assertEqual(33, values[1])
        self.assertEqual(42, values[2])

        values = utils.parse_content_range('bytes 22-33/*')
        self.assertEqual(22, values[0])
        self.assertEqual(33, values[1])
        self.assertEqual(-1, values[2])

        try:
            utils.parse_content_range(None)
            self.fail('shoud not here')
        except Exception as err:
            self.assertIn('Invalid content-range header, it is none or empty.', str(err))

        try:
            utils.parse_content_range('')
            self.fail('shoud not here')
        except Exception as err:
            self.assertIn('Invalid content-range header, it is none or empty.', str(err))

        try:
            utils.parse_content_range('invalid')
            self.fail('shoud not here')
        except Exception as err:
            self.assertIn('Invalid content-range header, it dose not start with bytes.', str(err))

        for value in ['bytes abc', 'bytes */42', 'bytes abc/42', 'bytes abc-33/42', 'bytes 11-abc/42', 'bytes 11-33/abc']:
            try:
                utils.parse_content_range(value)
                self.fail('shoud not here')
            except ValueError as err:
                errstr = str(err)
                self.assertTrue(errstr.startswith('invalid literal for int()') or errstr.startswith('Invalid content-range header'))


    def test_parse_content_length(self):
        value = utils.parse_content_length({'Content-Length':'123'})
        self.assertEqual(123, value)

        try:
            utils.parse_content_length({'Content-Length':'-1'})
            self.fail('shoud not here')
        except Exception as err:
            self.assertIn('Invalid content-length header', str(err))

        try:
            utils.parse_content_length({})
            self.fail('shoud not here')
        except Exception as err:
            self.assertIn('Missing content-length header', str(err))

        try:
            utils.parse_content_length({'Content-Length':'abc'})
            self.fail('shoud not here')
        except Exception as err:
            self.assertIn('invalid literal for int()', str(err))


    def test_parse_http_range(self):
        values = utils.parse_http_range('bytes=22-33')
        self.assertEqual(22, values[0])
        self.assertEqual(33, values[1])

        values = utils.parse_http_range('bytes=-33')
        self.assertEqual(-1, values[0])
        self.assertEqual(33, values[1])

        values = utils.parse_http_range('bytes=22-')
        self.assertEqual(22, values[0])
        self.assertEqual(-1, values[1])

        for value in [None, '', 'bytes=1-42,55-60', 'bytes=1', 'bytes=abc-123', 'bytes=123-abc']:
            try:
                utils.parse_http_range(value)
                self.fail('shoud not here')
            except ValueError as err:
                pass


    def test_is_seekable(self):
        # non-file-like object
        self.assertEqual(False, utils.is_seekable(None))
        self.assertEqual(False, utils.is_seekable('abc'))
        self.assertEqual(False, utils.is_seekable(b'abc'))

        self.assertEqual(True, utils.is_seekable(io.BytesIO(b'abc')))
        self.assertEqual(True, utils.is_seekable(io.StringIO('abc')))
        with open("./tests/data/example.jpg", 'rb') as f:
            self.assertEqual(True, utils.is_seekable(f))


    def test_is_fileobj(self):
        self.assertEqual(False, utils.is_fileobj(None))
        self.assertEqual(False, utils.is_fileobj('abc'))
        self.assertEqual(False, utils.is_fileobj(b'abc'))

        self.assertEqual(True, utils.is_fileobj(io.BytesIO(b'abc')))
        self.assertEqual(True, utils.is_fileobj(io.StringIO('abc')))
        with open("./tests/data/example.jpg", 'rb') as f:
            self.assertEqual(True, utils.is_fileobj(f))


    def test_get_default_user_agent(self):
        val = utils.get_default_user_agent()
        self.assertTrue(val.startswith(f'alibabacloud-python-sdk-v2/{__version__}'))
