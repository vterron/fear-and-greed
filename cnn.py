#! /usr/bin/env python3

import collections
import re
import requests

URL = "https://money.cnn.com/data/fear-and-greed/"
# TODO(vterron): document this regexp with inline comments.
REGEXP = "Greed Now: (?P<value>\d+) \((?P<description>.*?)\).*Last updated (?P<date>.*?(?:am|pm))"

# TODO(vterron): use requests-cache.
# TODO(vterron): add type annotations.

# TODO(vterron): use typed namedtuple instead.
FearGreedIndex = collections.namedtuple("FearGreedIndex", "value, description, date")


def fetch():
    """Fetches the Fear & Greed Index from CNN's website."""

    r = requests.get(URL)
    group = re.search(REGEXP, r.text).group
    # TODO(vterron): parse the date to a timestamp.
    return FearGreedIndex(int(group("value")), group("description"), group("date"))


if __name__ == "__main__":
    print(fetch())
