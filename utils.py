import datetime
from functools import wraps


def logger(wrapped):
    @wraps(wrapped=wrapped)
    def wrapper(*args, **kwargs):
        print("Invoked {} at {}".format(wrapped.__name__, datetime.datetime.now()))
        return wrapped(*args, **kwargs)

    return wrapper
