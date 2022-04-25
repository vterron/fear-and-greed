#! /usr/bin/env python3

import datetime
import json
import pathlib
import zoneinfo

from absl.testing import absltest
from fear_and_greed import cnn

FAKE_JSON_RESPONSE_GOLDEN_FILE = (
    pathlib.Path(__file__).parent / "response-golden.json"
).resolve()


class FetchFearGreedIndexTest(absltest.TestCase):
    def test_get(self):
        with open(FAKE_JSON_RESPONSE_GOLDEN_FILE, "rt") as fd:
            # Lambda is evaluated lazily, force JSON load while file is open.
            content = json.load(fd)
            fake_fetcher = lambda: content
        got = cnn.get(fetcher=fake_fetcher)

        want = cnn.FearGreedIndex(
            30.8254,
            "fear",
            datetime.datetime(
                year=2022,
                month=4,
                day=25,
                hour=16,
                minute=21,
                second=9,
                microsecond=254000,
                tzinfo=zoneinfo.ZoneInfo("UTC"),
            ),
        )
        self.assertEqual(got, want)


if __name__ == "__main__":
    absltest.main()
