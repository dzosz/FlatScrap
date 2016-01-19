# run it with cron as "python rqworker.py"

import os
from models import redis
from rq import Worker, Queue, Connection


listen = ['default',]


if __name__ == '__main__':
    with Connection(redis):
        worker = Worker(map(Queue, listen))
        worker.work(burst=True)
