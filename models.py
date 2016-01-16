import redis
from rq import Queue
import geopy
# import geopy.geocoders import GoogleV3
import time
import json
from config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD


rdb = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD
)


rqueue = Queue(connection=rdb)


def convert_address(link, ad_data, locations):
    """
    ### WORKER JOB ###
    Converts location name to latitude and longituted,
    then pushes the data to redis db.
    """
    geolocator = geopy.geocoders.GoogleV3()
    for address in locations:

        # prevent ip block
        time.sleep(1)

        new_loc = geolocator.geocode('{}, Wrocław'.format(address.encode('utf-8')))
        if new_loc.latitude != 51.1078852 and \
                51.035 < new_loc.latitude < 51.20 and \
                16.86 < new_loc.longitude < 17.17:

            # add coordinates to json
            ad_data['coords'] = "{}, {}".format(new_loc.latitude, new_loc.longitude)
            rdb.set(link, json.dumps(ad_data))
            rdb.expire(link, 60*60*24*14)
            return True # do not check other addresses
    return False

