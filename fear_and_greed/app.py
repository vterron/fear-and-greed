import cnn
import datetime
import json


class DateTimeEncoder(json.JSONEncoder):
    """JSON encoder to serialize datetime objects in ISO 8601 format."""

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()


def lambda_handler(event, context, fetcher=None):
    """Pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    index = cnn.get(fetcher=fetcher)
    return {
        "statusCode": 200,
        "body": json.dumps(index._asdict(), cls=DateTimeEncoder),
    }
