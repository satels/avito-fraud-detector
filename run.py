from avito_fraud.cache import WordsCache
from avito_fraud.conf import DOC_DIR, NUM_PROCESSES
from avito_fraud.db import save_to_db
from avito_fraud.rank import get_rank
from avito_fraud.utils import timeit
import logging
import multiprocessing as mp
import os
import random


logger = logging.getLogger('avito.fraud')


@timeit
def worker(queue, rank_list):

    logger.info('Worker started')

    local_cache = WordsCache()

    num = 0

    while not queue.empty():
        fn_lst = queue.get()

        for fn in fn_lst:

            fn_path = os.path.join(DOC_DIR, fn)

            text = open(fn_path, 'rb').read().decode('utf-8', 'ignore')

            item = get_rank(text, local_cache)

            rank_list.append((fn,) + item)

            num += 1

            if num % 10 == 0 and local_cache.stop_write():
                logger.info('Stop write to worker local cache')

    logger.info('Worker finished')


@timeit
def fill_queue(queue):
    chunk = []
    fn_list = os.listdir(DOC_DIR)
    random.shuffle(fn_list)
    chunk_size = len(fn_list) // NUM_PROCESSES
    for fn in fn_list:
        chunk.append(fn)
        if len(chunk) % chunk_size == 0:
            queue.put_nowait(chunk)
            chunk = []
    if chunk:
        queue.put_nowait(chunk)
        chunk = []


@timeit
def create_processes(queue, rank_list):
    ret = []
    for num in range(NUM_PROCESSES):
        p = mp.Process(
            target=worker,
            args=(queue, rank_list))
        ret.append(p)
    return ret


@timeit
def start_processes(proc_lst):
    for p in proc_lst:
        p.start()


@timeit
def join_processes(proc_lst):
    for p in proc_lst:
        p.join()


if __name__ == '__main__':

    manager = mp.Manager()

    queue = mp.Queue()

    rank_list = manager.list()

    fill_queue(queue)

    proc_lst = create_processes(queue, rank_list)

    start_processes(proc_lst)

    join_processes(proc_lst)

    save_to_db(rank_list)
