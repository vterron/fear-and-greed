#! /usr/bin/env python3

# [START gae_python38_app]

import flask
import datetime
import json

import cnn


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = flask.Flask(__name__)


class DateTimeEncoder(json.JSONEncoder):
    """JSON encoder to serialize datetime objects in ISO 8601 format."""

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()


@app.route("/")
def get_fear_greed_çindex():
    index = cnn.get()
    return flask.Response(
        json.dumps(index._asdict(), cls=DateTimeEncoder),
        mimetype="application/json",
    )


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)

# [END gae_python38_app]
