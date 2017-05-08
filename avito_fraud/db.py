from avito_fraud.conf import DBNAME
from avito_fraud.utils import timeit
import logging
import sqlite3


logger = logging.getLogger('avito.fraud')


@timeit
def save_to_db(data_list):
    logger.info('Start save rank list to {}'.format(DBNAME))
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS rank (fn text, rank real, fraud_warn bool, fraud_error bool)')
    c.execute('DELETE FROM rank')
    c.executemany('INSERT INTO rank VALUES (?,?,?,?)', data_list)
    conn.commit()
    conn.close()
