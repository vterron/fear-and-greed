#! /usr/bin/env python3

import cnn

from absl.testing import absltest
from absl.testing import parameterized


# Template for the HTML code used in the unit tests.
html = """<ul><li>Fear &amp; Greed Now: {} ({})</li>....<div id="needleAsOfDate">Last updated {}</div>""".format


class FetchFearGreedIndexTest(parameterized.TestCase):
    @parameterized.named_parameters(
        {
            "testcase_name": "Extreme greed",
            "html": html(91, "Extreme greed", "Nov 27 at 5:00pm"),
            "want": cnn.FearGreedIndex(91, "Extreme greed", "Nov 27 at 5:00pm"),
        },
    )
    def test_get(self, html, want):
        fake_fetcher = lambda: html
        got = cnn.get(fake_fetcher)
        self.assertEqual(got, want)


if __name__ == "__main__":
    absltest.main()
