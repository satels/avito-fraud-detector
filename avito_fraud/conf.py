import sys

if sys.version_info.major < 3:
    raise RuntimeError('Python (>=3) required')


from logging import config as log_config
import multiprocessing


DBNAME = 'rank.db'

TOP_WORDS = 5

DOC_DIR = '/Users/satels/avito_files/'  # customize it

NUM_PROCESSES = multiprocessing.cpu_count() // 2  # customize it

WORDS_CACHE_SIZE = 15000  # size of words cache by worker

LOGGING_CONF = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
    },
    'handlers': {
        'console': {
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'avito.fraud': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


log_config.dictConfig(LOGGING_CONF)
