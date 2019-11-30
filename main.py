#!/usr/bin/env python3

import logging
import sys
from urllib.request import urlopen
import ssl
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.INFO,
                    format="-> [%(levelname)s] [%(asctime)s] %(message)s",
                    datefmt="%Y-%m-%d %H:%M")

logger = logging.getLogger(__name__)


def main():

    logger.info('web-scraper has started')

    # TODO: load from config
    url = 'https://www.olympiccinema.co.uk/film/Star-Wars:-Rise-Of-Skywalker'
    word_to_find = 'book'

    data = load_url_as_soup(url)

    title = get_title(data)
    logger.info(f'Title of Page is: {title}')

    if find_word_in_source(data, word_to_find):
        logger.info('[SUCCESS] Word matched on web page')
    else:
        logger.info('[FAILED] Word is not present on web page')

    logger.info('web-scraper has completed')


def load_url_as_soup(url):
    source = urlopen(url, context=ssl._create_unverified_context()).read()
    return BeautifulSoup(source, 'html.parser')


def get_title(data):
    return str(data.title)


def find_word_in_source(data, word):
    raw_text = data.get_text()
    if word in raw_text:
        return True
    else:
        return False


def init():
    if __name__ == "__main__":
        sys.exit(main())


init()
