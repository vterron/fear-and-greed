#! /usr/bin/env python3

import datetime
import os.path
import tempfile
import typing

import requests
import requests_cache

from random import choice

requests_cache.install_cache(
    cache_name=os.path.join(tempfile.gettempdir(), "cnn_cache"),
    expire_after=datetime.timedelta(minutes=1),
)

URL = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"

USER_AGENTS = [
    # Chrome on Windows 10
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
    # Chrome on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
    # Chrome on Linux
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
    # Firefox on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
    # Firefox on Macos
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12.4; rv:100.0) Gecko/20100101 Firefox/100.0",
]


class FearGreedIndex(typing.NamedTuple):
    value: float
    description: str
    last_update: datetime.datetime


class Fetcher:
    """Fetcher gets the HTML contents of CNN's Fear & Greed Index website."""

    def __call__(self) -> dict:
        user_agent = choice(USER_AGENTS)
        headers = {
            "User-Agent": user_agent,
        }
        r = requests.get(URL, headers=headers)
        r.raise_for_status()
        return r.json()


def get(fetcher: Fetcher = None) -> FearGreedIndex:
    """Returns CNN's Fear & Greed Index."""

    if fetcher is None:
        fetcher = Fetcher()

    response = fetcher()["fear_and_greed"]
    return FearGreedIndex(
        value=response["score"],
        description=response["rating"],
        last_update=datetime.datetime.fromisoformat(response["timestamp"]),
    )
