RESTful API to access CNN's [Fear & Greed Index](https://money.cnn.com/data/fear-and-greed/).

# URL(s):

- https://fear.vterron.xyz
- https://greed.vterron.xyz

Both URLs resolve to the same endpoint.

# Sample usage

```
$ curl fear.vterron.xyz
{"value": 92, "description": "Extreme Greed", "last_update": "2020-11-27T17:00:00-04:56"}

$ curl --silent greed.vterron.xyz | jq '.value'
92
```

This wouldn't have been necessary if CNN provided historical data.
