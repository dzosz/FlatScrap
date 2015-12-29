from flask import Flask, render_template
from redis import Redis
from datetime import date, timedelta
import json


app = Flask(__name__)
app.config.from_pyfile('config.py')
redis = Redis(
    host=app.config['REDIS_HOST'],
    port=app.config['REDIS_PORT'],
    password=app.config['REDIS_PASSWORD'])


def get_recent_ads():
    """
    Returns ads from last 14 days that have an address.
    Queries 14 sets (each for day) of visited links, then lookups each key.
    """

    last_14_days = [(date.today() - timedelta(x)).strftime('%d%m%Y')
        for x in range(14)]
    links = redis.sunion(last_14_days)

    ads = []
    for link in links:
        item = redis.get(link)
        if item:
            ad = json.loads(item.decode())
            ad['link'] = link.decode()
            ads.append(ad)
    return ads


@app.route('/')
def index():
    ads = get_recent_ads()
    return render_template('index.html', ads=ads)


if __name__ == '__main__':
    app.run()
