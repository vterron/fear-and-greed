#! /usr/bin/env python3

import cnn

import datetime
import pytz
import unittest.mock
import freezegun

from absl.testing import absltest
from absl.testing import parameterized

# Template for the HTML code used in the unit tests.
html = """<ul><li>Fear &amp; Greed Now: {} ({})</li>....<div id="needleAsOfDate">Last updated {}</div>""".format


class FetchFearGreedIndexTest(parameterized.TestCase):
    # Note: all these test cases assume the current year is 2020 (see freeze_time() below).
    # They are all actual readings of the index, via Wayback Machine.
    @parameterized.named_parameters(
        {
            "testcase_name": "Extreme fear",
            "html": html(13, "Extreme fear", "Feb 28 at 5:06am"),
            "want": cnn.FearGreedIndex(
                13,
                "Extreme fear",
                datetime.datetime(
                    year=2020,
                    month=2,
                    day=28,
                    hour=5,
                    minute=6,
                    tzinfo=pytz.timezone("US/Eastern"),
                ),
            ),
        },
        {
            "testcase_name": "Fear",
            "html": html(38, "Fear", "May 13 at 5:14pm"),
            "want": cnn.FearGreedIndex(
                38,
                "Fear",
                datetime.datetime(
                    year=2020,
                    month=5,
                    day=13,
                    hour=17,
                    minute=14,
                    tzinfo=pytz.timezone("US/Eastern"),
                ),
            ),
        },
        {
            "testcase_name": "Neutral",
            "html": html(52, "Neutral", "Jun 19 at 6:30pm"),
            "want": cnn.FearGreedIndex(
                52,
                "Neutral",
                datetime.datetime(
                    year=2020,
                    month=6,
                    day=19,
                    hour=18,
                    minute=30,
                    tzinfo=pytz.timezone("US/Eastern"),
                ),
            ),
        },
        {
            "testcase_name": "Greed",
            "html": html(63, "Greed", "Jul 15 at 5:19pm"),
            "want": cnn.FearGreedIndex(
                63,
                "Greed",
                datetime.datetime(
                    year=2020,
                    month=7,
                    day=15,
                    hour=17,
                    minute=19,
                    tzinfo=pytz.timezone("US/Eastern"),
                ),
            ),
        },
        {
            "testcase_name": "Extreme greed",
            "html": html(91, "Extreme greed", "Nov 27 at 5:00pm"),
            "want": cnn.FearGreedIndex(
                91,
                "Extreme greed",
                datetime.datetime(
                    year=2020,
                    month=11,
                    day=27,
                    hour=17,
                    minute=0,
                    tzinfo=pytz.timezone("US/Eastern"),
                ),
            ),
        },
        {
            "testcase_name": "New Year's Eve",
            "html": html(90, "Extreme greed", "Dec 31 at 4:59pm"),
            "want": cnn.FearGreedIndex(
                90,
                "Extreme greed",
                datetime.datetime(
                    year=2019,
                    month=12,
                    day=31,
                    hour=16,
                    minute=59,
                    tzinfo=pytz.timezone("US/Eastern"),
                ),
            ),
        },
    )
    @freezegun.freeze_time("2020-11-28")
    def test_get(self, html, want):
        fake_fetcher = lambda: html
        got = cnn.get(fake_fetcher)
        self.assertEqual(got, want)


if __name__ == "__main__":
    absltest.main()
