# pylint: skip-file
import io
import unittest
from alibabacloud_oss_v2 import io_utils

class TestIoUtils(unittest.TestCase):
    def test_limit_reader(self):
        rb = io.StringIO("hello")
        r = io_utils.LimitReader(rb, 2)
        d = r.read()
        self.assertEqual('he', d)

        rb = io.StringIO("hello")
        r = io_utils.LimitReader(rb, 3)
        d = r.read(10)
        self.assertEqual('hel', d)
 
        rb = io.StringIO("hello")
        r = io_utils.LimitReader(rb, 3)
        d = r.read(1)
        self.assertEqual('h', d)


        rb = io.BytesIO(b"hello")
        r = io_utils.LimitReader(rb, 2)
        d = r.read()
        self.assertEqual(b'he', d)

        rb = io.BytesIO(b"hello")
        r = io_utils.LimitReader(rb, 3)
        d = r.read(10)
        self.assertEqual(b'hel', d)
 
        rb = io.BytesIO(b"hello")
        r = io_utils.LimitReader(rb, 3)
        d = r.read(1)
        self.assertEqual(b'h', d)


