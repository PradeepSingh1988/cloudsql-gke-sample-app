from functools import wraps
import time
from datetime import datetime

def retry(exceptions=Exception, tries=3, delay=1, logger=None):
    def decorate(func):
        @wraps(func)
        def retried(*args, **kwargs):
            _tries, _delay = tries, delay
            while _tries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    _tries -= 1
                    if not _tries:
                        raise
                    if logger is not None:
                        logger.warning("%s, retrying in %s seconds...", e, _delay)
                    time.sleep(_delay)

        return retried

    return decorate