import os
from models import rdb
from rq import Worker, Queue, Connection


listen = ['default',]


if __name__ == '__main__':
    with Connection(rdb):
        worker = Worker(map(Queue, listen))
        worker.work(burst=True)
