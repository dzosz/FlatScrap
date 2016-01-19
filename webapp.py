import json
from flask import Flask, render_template, jsonify
from models import db_get_keys, db_get_values, redis


app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/get_recent_ads')
def get_recent_ads():
    """
    Returns ads from last 14 days that have an address.
    Queries redis for 14 unique sets (each for a day) of gathered links, then gets each key.
    """


    # METHOD ONE
    # links = redis.sunion(last_14_days)
    # records = {}
    # for link in links:
    #     data = redis.get(link)
    #     if data:
    #         records[link.decode()] = json.loads(data.decode())
    # return jsonify(records)

    # METHOD TWO - get 14 different sets

    all_keys = db_get_keys(days=14)

    all_ads = db_get_values(all_keys)

    return jsonify(all_ads)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
