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


class Fetcher:
    """Fetcher gets the HTML contents of CNN's Fear & Greed Index website."""

    def __call__(self):
        r = requests.get(URL)
        return r.text


def get(fetcher):
    """Returns CNN's Fear & Greed Index."""

    group = re.search(REGEXP, fetcher()).group
    # TODO(vterron): parse the date to a timestamp.
    return FearGreedIndex(int(group("value")), group("description"), group("date"))


if __name__ == "__main__":
    fetcher = Fetcher()
    print(get(fetcher))
