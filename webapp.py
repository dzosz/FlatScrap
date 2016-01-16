from flask import Flask, render_template, jsonify
from redis import Redis
from datetime import date, timedelta
import json


app = Flask(__name__)
app.config.from_pyfile('config.py')
redis = Redis(
    host=app.config['REDIS_HOST'],
    port=app.config['REDIS_PORT'],
    password=app.config['REDIS_PASSWORD']
)


@app.route('/get_recent_ads')
def get_recent_ads():
    """
    Returns ads from last 14 days that have an address.
    Queries redis for 14 unique sets (each for a day) of gathered links, then gets each key.
    """

    last_14_days = [(date.today() - timedelta(x)).strftime('%d%m%Y')
                    for x in range(14)]

    # METHOD ONE
    # links = redis.sunion(last_14_days)
    # records = {}
    # for link in links:
    #     data = redis.get(link)
    #     if data:
    #         records[link.decode()] = json.loads(data.decode())
    # return jsonify(records)

    # METHOD TWO - get 14 different sets
    pipe = redis.pipeline()
    for day in last_14_days:
        pipe.smembers(day)


    records = {}
    for i, res in enumerate(pipe.execute()):
        pipe2 = redis.pipeline()
        links = [link.decode() for link in res if res and pipe2.get(link)]
        for j, data in enumerate(pipe2.execute()):
            if data:
                records[links[j]] = json.loads(data.decode())
                records[links[j]].update({'age': i})

    return jsonify(records)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
