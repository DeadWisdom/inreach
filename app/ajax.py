import json, datetime, decimal
from django.http import HttpResponse


class EnhancedJSONEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time and decimal types.
    """
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return tuple(o.timetuple())
        elif isinstance(o, datetime.date):
            return tuple(o.timetuple())
        elif isinstance(o, datetime.time):
            return tuple(o.timetuple())
        elif isinstance(o, decimal.Decimal):
            return str(o)
        else:
            return super(EnhancedJSONEncoder, self).default(o)


def to_json(simple_object):
    """
    Serializes the ``simple_object`` to JSON using the EnhancedJSONEncoder above.
    """
    return json.dumps(simple_object, cls=EnhancedJSONEncoder)


def from_json(src):
    """
    Simply deserializes the given json ``src``, provided for consistancy with ``to_json()``.
    """
    return json.loads(src)


class JsonResponse(HttpResponse):
    """
    An HttpResponse class that automatically serializes the response content with JSON using
    the EnhancedJSONEncoder above to deal with date/time and decimal types.
    """
    def __init__(self, simple_object, status=None, content_type="application/json"):
        super(JsonResponse, self).__init__(to_json(simple_object), status=status, content_type=content_type)

