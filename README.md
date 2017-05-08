# avito-fraud-detector


INSTALL
=======

**Python3** required.

$ ``cd avito_fraud``

$ ``python3 -m venv env``

$ ``source env/bin/activate``

(env) $ ``pip install -r requirements.txt``

(env) $ ``python initial_nltk.py``

EDIT CONF
=========

``edit avito_fraud/conf.py``

and see

``DOC_DIR``

``NUM_PROCESSES``

RUN COMMAND
===========

(env) $ ``time python run.py``

Result like

| Timeit: import_nltk 0.45 sec
| Timeit: fill_queue 0.00 sec
| Timeit: create_processes 0.00 sec
| Timeit: start_processes 0.01 sec
| Worker started
| Worker started
| Worker started
| Worker started
| Worker finished
| Timeit: worker 2.56 sec
| Worker finished
| Worker finished
| Timeit: worker 2.61 sec
| Timeit: worker 2.62 sec
| Worker finished
| Timeit: worker 2.63 sec
| Timeit: join_processes 2.64 sec
| Start save rank list to rank.db
| Timeit: save_to_db 0.14 sec

RUN TESTS
=========

(env) $ ``nosetests --cover-package=avito_fraud --with-coverage -s``
