#! /usr/bin/env python3

import datetime
import os.path
import tempfile
import typing

import requests
import requests_cache

requests_cache.install_cache(
    cache_name=os.path.join(tempfile.gettempdir(), "cnn_cache"),
    expire_after=datetime.timedelta(minutes=1),
)

URL = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"


class FearGreedIndex(typing.NamedTuple):
    value: float
    description: str
    last_update: datetime.datetime


class Fetcher:
    """Fetcher gets the HTML contents of CNN's Fear & Greed Index website."""

    def __call__(self) -> dict:
        r = requests.get(URL)
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
