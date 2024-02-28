import datetime
import unittest

from parse_dates import parse_time


class TestParseTime(unittest.TestCase):
    def setUp(self):
        pass

    def test_words_for_hours(self):
        self.assertEqual(parse_time("four o'clock"), datetime.time(4, 0))

    def test_past_to(self):
        self.assertEqual(parse_time("ten past two"), datetime.time(2, 10))
        self.assertEqual(parse_time("five to ten"), datetime.time(9, 55))

    def test_fractions(self):
        self.assertEqual(
            parse_time("a quarter to three"), datetime.time(2, 45)
        )
        self.assertEqual(parse_time("half twelve"), datetime.time(11, 30))
        self.assertEqual(parse_time("half past one"), datetime.time(1, 30))

    def test_ago(self):
        long_date = datetime.datetime.now() - datetime.timedelta(minutes=10)
        time_10_ago = long_date.time()
        self.assertEqual(parse_time("ten minutes ago"), time_10_ago)

        long_date = datetime.datetime.now() - datetime.timedelta(
            hours=1, minutes=30
        )
        time_1_5_hours_ago = long_date.time()
        self.assertEqual(
            parse_time("one and a half hours ago"), time_1_5_hours_ago
        )

        self.assertEqual(
            parse_time("three weeks ago"),
            datetime.datetime.now() - datetime.timedelta(days=21),
        )

    def test_in(self):
        long_date = datetime.datetime.now() + datetime.timedelta(minutes=20)
        time_20_minutes = long_date.time()
        self.assertEqual(
            parse_time("in twenty minutes' time"),
            time_20_minutes,
        )

    def test_next(self):
        day_of_the_week = datetime.datetime.now().weekday()
        difference = (1 - day_of_the_week) % 7
        self.assertEqual(
            parse_time("next Tuesday"),
            datetime.datetime.now() + datetime.timedelta(days=difference),
        )

    def test_last(self):
        day_of_the_week = datetime.datetime.now().weekday()
        difference = (4 - day_of_the_week) % 7 - 7
        self.assertEqual(
            parse_time("last Friday"),
            datetime.datetime.now() + datetime.timedelta(days=difference),
        )

    def test_tomorrow(self):
        self.assertEqual(
            parse_time("tomorrow at half three"),
            datetime.datetime.combine(
                datetime.datetime.now() + datetime.timedelta(days=1),
                datetime.time(2, 30),
            ),
        )

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
