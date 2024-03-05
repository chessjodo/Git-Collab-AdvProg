import datetime
import unittest

import ephem
import jewish

from parse_dates import parse_time


class TestParseTime(unittest.TestCase):
    def setUp(self):
        pass

    def test_words_for_hours(self):
        self.assertEqual(parse_time("four o'clock"), datetime.time(4, 0))

    def test_to(self):
        self.assertEqual(parse_time("five to ten"), datetime.time(9, 55))

    def test_past(self):
        self.assertEqual(parse_time("ten past two"), datetime.time(2, 10))

    def test_to_fraction(self):
        self.assertEqual(
            parse_time("a quarter to three"), datetime.time(2, 45)
        )

    def test_fractions(self):
        self.assertEqual(parse_time("half twelve"), datetime.time(11, 30))
        self.assertEqual(parse_time("half past one"), datetime.time(1, 30))

    def test_ago(self):
        long_date = datetime.datetime.now() - datetime.timedelta(minutes=10)
        self.assertAlmostEqual(
            parse_time("ten minutes ago"),
            long_date,
            delta=datetime.timedelta(seconds=1),
        )

        self.assertAlmostEqual(
            parse_time("three weeks ago"),
            datetime.datetime.now() - datetime.timedelta(days=21),
            delta=datetime.timedelta(seconds=1),
        )

    def test_in(self):
        long_date = datetime.datetime.now() + datetime.timedelta(minutes=20)
        self.assertAlmostEqual(
            parse_time("in twenty minutes' time"),
            long_date,
            delta=datetime.timedelta(seconds=1),
        )

    def test_next(self):
        day_of_the_week = datetime.datetime.now().weekday()
        difference = (1 - day_of_the_week) % 7
        result = datetime.datetime.now() + datetime.timedelta(days=difference)
        self.assertEqual(parse_time("next Tuesday"), result.date())

    def test_last(self):
        day_of_the_week = datetime.datetime.now().weekday()
        difference = (4 - day_of_the_week) % 7 - 7
        result = datetime.datetime.now() + datetime.timedelta(days=difference)
        self.assertEqual(parse_time("last Friday"), result.date())

    def test_tomorrow(self):
        new_datetime = datetime.datetime.now() + datetime.timedelta(days=1)
        new_date = new_datetime.date()
        self.assertEqual(
            parse_time("tomorrow at half three"),
            datetime.datetime.combine(
                new_date,
                datetime.time(2, 30),
            ),
        )

    def test_in_future(self):
        long_date = datetime.datetime.now() + datetime.timedelta(hours=2)
        self.assertAlmostEqual(
            parse_time("in two hours"),
            long_date,
            delta=datetime.timedelta(seconds=1),
        )

    def test_easter(self):
        equinox = ephem.localtime(ephem.next_equinox(ephem.now()))
        full_moon = ephem.localtime(
            ephem.next_full_moon(equinox - datetime.timedelta(days=1))
        )
        weekday_fullmoon = full_moon.weekday()
        diff_to_sunday = 6 - weekday_fullmoon
        easter_date = full_moon + datetime.timedelta(days=diff_to_sunday)
        self.assertEqual(parse_time("next Easter"), easter_date.date())

    def test_ramadan(self):
        observer = ephem.Observer()
        observer.date = datetime.datetime.now()
        new_moon = ephem.next_new_moon(observer.date)
        new_moon_date = ephem.localtime(new_moon).date()
        ramadan_date = new_moon_date + datetime.timedelta(days=1)
        self.assertEqual(parse_time("start of ramadan"), ramadan_date)

    def test_hebrew_new_year(self):
        t_j = jewish.JewishDate.from_date(datetime.datetime.now())
        hebrew_new_year_date = jewish.JewishDate(t_j.year + 1, 1, 1)
        self.assertEqual(
            parse_time("hebrew new year"), hebrew_new_year_date.to_date()
        )

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
