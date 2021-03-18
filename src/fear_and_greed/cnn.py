#! /usr/bin/env python3

import collections
import datetime
import logging
import os.path
import pytz
import re
import requests
import requests_cache
import tempfile
import typing


requests_cache.install_cache(
    cache_name=os.path.join(tempfile.gettempdir(), "cnn_cache"),
    expire_after=datetime.timedelta(minutes=1),
)


URL = "https://money.cnn.com/data/fear-and-greed/"
REGEXP = re.compile(
    """
    Greed\ Now:\ (?P<value>\d+)                       # the index value, [0-100].
    \s
    \((?P<description>.*?)\)                          # e.g. "Neutral", non-greedy.
    .*                                                # ignore in-between HTML code.
    Last\ updated\ (?P<last_update>.*?(?:am|pm))  # e.g. "Nov 27 at 5:00pm"
""",
    re.VERBOSE,
)


class FearGreedIndex(typing.NamedTuple):
    value: int
    description: str
    last_update: datetime.datetime


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


def get(fetcher=None) -> FearGreedIndex:
    """Returns CNN's Fear & Greed Index."""

    if fetcher is None:
        fetcher = Fetcher()

    match = re.search(REGEXP, fetcher())
    if match:
        group = match.group
        return FearGreedIndex(
            int(group("value")),
            group("description"),
            _parse_date(group("last_update")),
        )
    raise ValueError("couldn't parse {}".format(URL))
