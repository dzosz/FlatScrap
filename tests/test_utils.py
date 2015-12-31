from unittest import TestCase, mock
from utils import match_words
from search import scrap_ad_list, scrap_subpage
import requests


class UtilsTestCase(TestCase):

    def test_street_regex(self):
        text="""mieszkanie na ulicy Reja 83 , blisko do Pasaży \
        grunwaldzkiego (10min piechotą) tak samo UP i politechnika, \
        dobre połączenie z Rynkiem , dworcem pkp i pks (ul.piastowska, \
        górnickiego -10 min) pokój duży słoneczny z wyjsciem na mały \
        ogródek , obecnie mieszkają w nim dwie dziewczyny od stycznia \
        będzie wolny dla jednej osoby , w mieszkaniu wyposażona kuchnia, \
        łazienka i pokój jednoosobowy wynajmowany przez chłopaka. \
        Współlokatorzy mili, spokojni, niekonfliktowi. Studentka i \
        student z UP. W czynsz 625 zł wliczone wszystkie opłaty, \
        dodatkowo jednorazowa zwrotna kaucja 625 zł. pokój około 20m2."""

        result = match_words(text)
        #print(result)

        self.assertEqual(len(result), 2)
        self.assertTrue('ul piastowska' in result)
        self.assertTrue('ulicy Reja' in result)

    @mock.patch('requests.get')
    def test_ad_finder(self, mock_get):
        mock_response = mock.Mock()
        with open('tests/mainpage_mock.html') as opener:
            mock_response.content = opener.read()
        mock_get.return_value = mock_response

        self.assertEqual(len(scrap_ad_list('fakelink')), 2)

    @mock.patch('requests.get')
    def test_subpage_read(self, mock_get):
        mock_response = mock.Mock()
        with open('tests/subpage_mock.html') as opener:
            mock_response.content = opener.read()
        mock_get.return_value = mock_response

        data_goal = {
            'title': 'Pokój do wynajęcia w okolicy Obornickiej',
            'price': 650,
            'locations': ['ulic Obornickiej']
        }
        result = scrap_subpage('fakelink')
        self.assertDictEqual(scrap_subpage('fakelink'), data_goal)

