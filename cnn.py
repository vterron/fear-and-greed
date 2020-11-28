#! /usr/bin/env python3

import collections
import datetime
import pytz
import re
import requests
import typing

URL = "https://money.cnn.com/data/fear-and-greed/"
# TODO(vterron): document this regexp with inline comments.
REGEXP = "Greed Now: (?P<value>\d+) \((?P<description>.*?)\).*Last updated (?P<date>.*?(?:am|pm))"

# TODO(vterron): use requests-cache.


class FearGreedIndex(typing.NamedTuple):
    value: int
    description: str
    date: datetime.datetime


class Fetcher:
    """Fetcher gets the HTML contents of CNN's Fear & Greed Index website."""

    def __call__(self) -> str:
        r = requests.get(URL)
        return r.text


def _parse_date(d: str) -> datetime.datetime:
    """Parses e.g. 'Nov 27 at 5:00pm' into a datetime object."""

    # The string timestamp doesn't include the year, assumed to be the current one.
    # If the resulting datetime object refers to a point in time in the future (e.g.
    # we parse "Dec 31 at 3:00pm" on January 1st) we need to subtract one year: the
    # Fear & Greed index value cannot have been generated in the future, after all.

    # From CNN's website: "All times are ET."
    eastern = pytz.timezone("US/Eastern")
    now = datetime.datetime.now(tz=eastern)
    date = datetime.datetime.strptime(d, "%b %d at %I:%M%p").replace(year=now.year)
    date = date.replace(tzinfo=eastern)
    if date > now:
        date = date.replace(year=now.year - 1)
    return date


def get(fetcher) -> FearGreedIndex:
    """Returns CNN's Fear & Greed Index."""

    match = re.search(REGEXP, fetcher())
    if match:
        group = match.group
        return FearGreedIndex(
            int(group("value")), group("description"), _parse_date(group("date"))
        )
    raise ValueError("couldn't parse {}".format(URL))


if __name__ == "__main__":
    fetcher = Fetcher()
    print(get(fetcher))
