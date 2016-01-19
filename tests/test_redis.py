from unittest import TestCase, mock
from models import redis, convert_address
import json


class RedisTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.query1 = 'fake-link-1', {}, ['fake-street-1']
        cls.geomock1 = {'latitude': 51.1, 'longitude': 17.0}
        cls.query2 = 'fake-link-2', {}, ['fake-street-2']
        cls.geomock2 = {'latitude': 51.15, 'longitude': 17.03}

    @mock.patch('time.sleep')
    @mock.patch('geopy.geocoders.GoogleV3.geocode')
    def test_db_add(self, geocoder, timer):
        timer.return_value = True

        geocoder.return_value.configure_mock(**self.geomock1)
        self.assertTrue(convert_address(*self.query1))

        geocoder.return_value.configure_mock(**self.geomock2)
        self.assertTrue(convert_address(*self.query2))

    def test_db_get(self):
        response1 = redis.get(self.query1[0])
        self.assertTrue(response1)

        response2 = redis.get(self.query2[0])
        self.assertTrue(response2)

        # check if added correctly
        db_json1 = json.loads(response1.decode())
        self.assertTrue(self.query1[1].items() <= db_json1.items())
        self.assertEqual(
            "{}, {}".format(self.geomock1['latitude'], self.geomock1['longitude']),
            db_json1['coords']
        )

        db_json2 = json.loads(response2.decode())
        self.assertTrue(self.query2[1].items() <= db_json2.items())
        self.assertEqual(
            "{}, {}".format(self.geomock2['latitude'], self.geomock2['longitude']),
            db_json2['coords']
        )

    def test_db_remove(self):
        self.assertTrue(redis.delete(self.query1[0]))
        self.assertTrue(redis.delete(self.query2[0]))



