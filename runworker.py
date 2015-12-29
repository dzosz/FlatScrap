import os

from redis import Redis
from rq import Worker, Queue, Connection
from config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD

listen = ['high', 'default', 'low']

conn = Redis(host=REDIS_HOST,
    port=REDIS_PORT,
    db=0,
    password=REDIS_PASSWORD)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work(burst=True)
