Python wrapper for CNN's [Fear & Greed Index](https://money.cnn.com/data/fear-and-greed/).

Fetches CNN's website, parses the index value and returns the data as a three-element tuple.

# Installation

```bash
pip install fear-and-greed
```

# Usage example

```python
import fear_and_greed

fear_and_greed.get()
```

Returns a three-element namedtuple with (a) the current value of the Fear & Greed Index, (b) a description of the category into which the index value falls (from "Extreme Fear" to "Extreme Greed") and (c) the timestamp at which the index value was last updated on CNN's website. Example:

```python
FearGreedIndex(
    value=58,
    description='Greed',
    last_update=datetime.datetime(2020, 3, 18, 14, 11, tzinfo=<DstTzInfo 'US/Eastern' LMT-1 day, 19:04:00 STD>)),
 )
```

Requests to CNN's website are locally [cached](https://pypi.org/project/requests-cache/) for 1m.

[![Test workflow](https://github.com/vterron/fear-and-greed/actions/workflows/test.yml/badge.svg)](https://github.com/vterron/fear-and-greed/actions/workflows/test.yml)
[![Black badge](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
