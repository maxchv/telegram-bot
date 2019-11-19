from datetime import datetime
from functools import wraps


def logger(wrapped):
    @wraps(wrapped=wrapped)
    def wrapper(*args, **kwargs):
        print(f"Invoked {wrapped.__name__} at {datetime.now()}")
        return wrapped(*args, **kwargs)

    return wrapper
