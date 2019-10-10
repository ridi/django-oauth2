import time
from typing import Callable

DEFAULT_MEMORIZE_TIMEOUT = 60


def memorize(timeout: int = DEFAULT_MEMORIZE_TIMEOUT):
    def _wrapper(func: Callable):
        _cache = {}
        _timeouts = {}

        def _decorator(*args, clear: bool = False, **kwargs):
            if clear:
                return func(*args, **kwargs)

            key = func.__name__ + str(args) + str(kwargs)
            if key not in _cache:
                _timeouts[key] = time.time()
                _cache[key] = func(*args, **kwargs)

            delta = time.time() - _timeouts[key]
            if delta > timeout:
                _timeouts[key] = time.time()
                _cache[key] = func(*args, **kwargs)

            return _cache[key]
        return _decorator
    return _wrapper
