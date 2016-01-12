from unittest import TestCase, mock
from models import rdb, convert_address
import json


class RedisTestCase(TestCase):

    @mock.patch('time.sleep')
    @mock.patch('geopy.geocoders.GoogleV3.geocode')
    def test_db_add(self, geocoder, timer):
        data = {'latitude': 51.1, 'longitude': 17.0}
        geocoder.return_value.configure_mock(**data)
        timer.return_value = True

        link = 'fake_link'
        ad_data = {'locations': ['fake_street']}

        self.assertTrue(convert_address(link, ad_data))
        self.assertTrue(rdb.get(link))

        # check if added correctly
        db_json = json.loads(rdb.get(link).decode())
        self.assertIn('51.1, 17.0', db_json['coords'])
        self.assertIn('locations', db_json)

    def test_db_remove(self):
        self.assertTrue(rdb.delete('fake_link'))




