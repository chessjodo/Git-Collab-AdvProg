import datetime
import unittest

from parse_dates import parse_time


class TestParseTime(unittest.TestCase):
    def setUp(self):
        pass

    def test_words_for_hours(self):
        self.assertEqual(parse_time("Five O'Clock"), datetime.time(4, 0))

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
