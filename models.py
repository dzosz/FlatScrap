import redis
from rq import Queue
from geopy.geocoders import GoogleV3
import time
import json
from config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD


rdb = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD
    )

rqueue = Queue(connection=rdb)
geolocator = GoogleV3()


def convert_address(link, ad_data):
    """
    ### WORKER JOB ###
    Converts location name to latitude and longituted,
    then pushes the data to redis db.
    """

    for location in ad_data['locations']:
        # prevent ip block
        time.sleep(1)
        new_loc = geolocator.geocode('{}, Wrocław'.format(location.encode('utf-8')))
        if new_loc:
            if new_loc.latitude == 51.1078852 or \
                    51.035 > new_loc.latitude > 51.20 or \
                    16.86 > new_loc.longitude > 17.17:
                continue # did not find the right address

            ad_data['coords'] = "{}, {}".format(new_loc.latitude, new_loc.longitude)
            rdb.set(link, json.dumps(ad_data))
            rdb.expire(link, 60*60*24*14)
            # do not check other keywords
            return True
    return False

