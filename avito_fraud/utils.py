import functools
import logging
import time


logger = logging.getLogger('avito.fraud')


def timeit(method):

    @functools.wraps(method)
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        logger.info('Timeit: {} {:2.2f} sec'.format(method.__name__, te - ts))
        return result

    return timed

