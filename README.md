RESTful API to access CNN's [Fear & Greed Index](https://money.cnn.com/data/fear-and-greed/).

# URL

https://fear-and-greed.vterron.xyz

# Sample usage

```
$ curl fear-and-greed.vterron.xyz
{"value": 92, "description": "Extreme Greed", "last_update": "2020-11-27T17:00:00-04:56"}

$ curl --silent fear-and-greed.vterron.xyz | jq '.value'
92
```

This wouldn't have been necessary if CNN had provided historical data.
