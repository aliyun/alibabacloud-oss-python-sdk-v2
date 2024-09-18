# pylint: skip-file

import unittest
from alibabacloud_oss_v2.retry import backoff

attempted_celling = 64

class TestBackoff(unittest.TestCase):

    def test_equal_jitter_backoff(self):
        basedelay = 1
        maxdelay = 20
        r = backoff.EqualJitterBackoff(base_delay=basedelay,max_backoff=maxdelay)
        self.assertIsNotNone(r)

        for i in range(attempted_celling * 2):
            delay = r.backoff_delay(i, None)
            self.assertGreater(delay, 0.0)
            self.assertLess(delay, maxdelay + 1)

    def test_full_jitter_backoff(self):
        basedelay = 1
        maxdelay = 20
        r = backoff.FullJitterBackoff(base_delay=basedelay,max_backoff=maxdelay)
        self.assertIsNotNone(r)

        for i in range(attempted_celling * 2):
            delay = r.backoff_delay(i, None)
            self.assertGreater(delay, 0.0)
            self.assertLess(delay, maxdelay + 1)


    def test_fixed_delay_backoff(self):
        maxdelay = 20
        r = backoff.FixedDelayBackoff(maxdelay)
        self.assertIsNotNone(r)

        for i in range(attempted_celling * 2):
            delay = r.backoff_delay(i, None)
            self.assertEqual(delay,maxdelay)
