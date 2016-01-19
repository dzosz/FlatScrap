"""
Running this script will update the database.
Run it every day in scheduler.
"""

import re
import requests
from bs4 import BeautifulSoup
from utils import match_words
from models import redis, rqueue, convert_address, db_update_keys, db_get_keys
from config import MAX_PAGE_NUMBER


def scrap_ad_list(link):
    """Get the list of advertisements"""
    page = requests.get(link).content
    soup = BeautifulSoup(page, 'html.parser')
    rows = soup.find_all('h3', 'x-large lheight20 margintop5')
    links = [row.find('a').get('href').split('.html')[0]+'.html' for row in rows]
    return links


def verify_links(links):
    """Get rid of already existing in db ads"""
    all_ads = db_get_keys()
    return [link for link in links if link.encode() not in all_ads]


def scrap_and_enqueue(link):
    """Looks for the title, price and keywords in the board"""

    data = {}

    # get static data
    ad_page = requests.get(link).content
    ad_page_soup = BeautifulSoup(ad_page, 'html.parser')
    data['title'] = ad_page_soup.find('h1', 'brkword lheight28').text.strip()

    price_tag = ad_page_soup.find('div', 'pricelabel tcenter').text
    data['price'] = int(''.join(re.findall(r'\d', price_tag)))

    # get important keywords
    tables = ad_page_soup.find('table', 'details fixed marginbott20 margintop5 full').find_all('table', 'item')
    for table in tables:
        key = table.find('th').text.strip()
        data[key] = table.find('td','value').text.strip()

    # analyze content
    ad_content = ad_page_soup.find('div', id='textContent').find('p', 'pding10 lheight20 large').text
    # preappend title to content for better matching
    full_text = '{}. {}'.format(data['title'], ad_content)
    locations = match_words(ad_content)

    if locations:
        rqueue.enqueue(convert_address, link, data, locations)
        return True
    return False


if __name__ == '__main__':
    for i in range(1, MAX_PAGE_NUMBER):
        start = 'http://olx.pl/nieruchomosci/stancje-pokoje/wroclaw/?page={}'.format(i)
        links = scrap_ad_list(start)
        unique = verify_links(links)

        # add sets to visited set
        db_update_keys(unique)

        # add jobs to worker
        added = [link for link in unique if scrap_and_enqueue(link)]

        print('Done with page {}'.format(i))
        print('Total: {} --- Unique: {} --- Enqueued: {}\n\n'.format(
            len(links), len(unique), len(added)))
        if len(unique) < 7:
            # Reached already processed before pages
            break






