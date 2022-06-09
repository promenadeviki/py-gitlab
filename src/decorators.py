#!/usr/bin/python
import urllib
from functools import wraps


def namespace(fn):
    """
    If using namespaced projects call make sure that the
    NAMESPACE/PROJECT_NAME is URL-encoded.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'id' in kwargs:
            if '%2F' in kwargs['id']:
                # ID is already URL encoded, do not pass through `urlencode`
                # method
                return fn(*args, **kwargs)
            else:
                # Remove the `id=` portion of the string generated via the
                # `urlencode` method
                id = urllib.urlencode({'id': kwargs['id']})[3:]
                kwargs['id'] = id
                return fn(*args, **kwargs)
    return wrapper
