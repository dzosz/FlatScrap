import unittest
from unittest import TestCase


class FlaskTestCase(TestCase):

    @unittest.skip('tbc')
    def TestViews(self):
        pass
