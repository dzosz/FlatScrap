import geopy
import time
import json
from redis import Redis
from rq import Queue
from config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
from datetime import date, timedelta


redis = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
)

rqueue = Queue(connection=redis)


def db_get_keys(days=14):
    """get set of visited links"""

    # get dates
    date_range = [(date.today() - timedelta(x)).strftime('%d%m%Y')
                    for x in range(days)]

    # get keys
    pipe = redis.pipeline()
    for day in date_range:
        pipe.smembers(day)

    return pipe.execute()


def db_get_values(keys):
    """get information about visited ads"""

    records = {}
    for i, res in enumerate(keys):
        pipe2 = redis.pipeline()
        links = [link.decode() for link in res if pipe2.get(link)]
        for j, data in enumerate(pipe2.execute()):
            # get data of existing ads
            if data:
                records[links[j]] = json.loads(data.decode())
                records[links[j]].update({'age': i}) # add AGE key to json

    return records


def db_update_keys(links):

    pipe = redis.pipeline()
    today = date.today().strftime('%d%m%Y')
    for link in links:
        pipe.sadd(today, link)

    return pipe.execute()


def convert_address(link, ad_data, locations):
    """
    ### WORKER JOB ###
    Converts location name to latitude and longituted,
    then pushes the data to redis db.
    """

    # does not provide fitting these bounds
    bounds = [51.035, 16.86, 51.20, 17.17]
    geolocator = geopy.geocoders.GoogleV3()

    for address in locations:

        # prevent ip block
        time.sleep(1)

        new_loc = geolocator.geocode('{}, Wrocław'.format(address), bounds=bounds, language='pl')
        if ((new_loc.latitude != 51.1078852 and new_loc.longitude != 17.0385376) and
                51.035 < new_loc.latitude < 51.20 and
                16.86 < new_loc.longitude < 17.17):

            # add coordinates to json
            ad_data['coords'] = "{}, {}".format(new_loc.latitude, new_loc.longitude)
            redis.set(link, json.dumps(ad_data))
            redis.expire(link, 60*60*24*14)
            return True # do not check other addresses

    return False


