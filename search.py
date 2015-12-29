"""
Running this script will update the database.
Run it every day in scheduler.
"""

import os
import re
import requests
from bs4 import BeautifulSoup
from utils import match_words
from models import rdb, rqueue, convert_address
from datetime import date, timedelta
from config import MAX_PAGE_NUMBER

def scrap_ad_list(link):
    """Get the list of advertisements"""
    page = requests.get(link).content
    soup = BeautifulSoup(page, 'html.parser')
    rows = soup.find_all('h3', 'x-large lheight20 margintop5')
    links = [row.find('a').get('href') for row in rows]
    return links


def verify_links(links):
    """Get rid of already existing in db ads"""

    last_14_days = [(date.today() - timedelta(x)).strftime('%d%m%Y')
        for x in range(14)]
    all_ads = rdb.sunion(last_14_days)
    verified = list(filter(
        lambda link: not link.encode() in all_ads, links))
    return verified


def push_link(link):
    """Insert flat advertisements to database"""

    # add ad's link to visited set
    rdb.sadd(date.today().strftime('%d%m%Y'), link)

    ad_data = scrap_subpage(link)
    if ad_data:
        # create key and expire it after 2 weeks
        rqueue.enqueue(convert_address, link, ad_data)
        return True
    return False


def scrap_subpage(link):
    """Looks for the title, price and keywords in the board"""

    ad_page = requests.get(link).content
    ad_page_soup = BeautifulSoup(ad_page, 'html.parser')
    title = ad_page_soup.find('h1', 'brkword lheight28').text.strip()

    price_tag = ad_page_soup.find('div', 'pricelabel tcenter').text
    price = int(''.join(re.findall(r'\d', price_tag)))

    # analyze content
    ad_content = ad_page_soup.find('div', id='textContent').find('p', 'pding10 lheight20 large').text
    full_text = '{}. {}'.format(title, ad_content)
    locations = match_words(ad_content)
    if locations and title and price:
        return {'title': title, 'price': price, 'locations': locations}

    # print('Err (No data): [..]{}'.format(link[13:]))
    return False


if __name__ == '__main__':

    for i in range(1, MAX_PAGE_NUMBER):
        start = 'http://olx.pl/nieruchomosci/stancje-pokoje/wroclaw/?page={}'.format(i)
        links = scrap_ad_list(start)
        verified = verify_links(links)

        # add to database
        added = [link for link in verified if push_link(link)]

        print('Done with page {}'.format(i))
        print('Total: {} --- Unique: {} --- Adding: {}\n\n'.format(
            len(links), len(verified), len(added)))
        if len(verified) < 7:
            # Reached already processed pages
            break






