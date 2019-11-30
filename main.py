#!/usr/bin/env python3

import logging
import sys
import urllib.request
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.INFO,
                    format="-> [%(levelname)s] [%(asctime)s] %(message)s",
                    datefmt="%Y-%m-%d %H:%M")

logger = logging.getLogger(__name__)


def main():

    logger.info('web-scraper has started')

    url = 'https://pythonprogramming.net/parsememcparseface/'
    data = load_url_as_soup(url)
    print(data)

    logger.info('web-scraper has completed')


def load_url_as_soup(url):
    source = urllib.request.urlopen(url).read()
    return BeautifulSoup(source, 'html.parser')


def init():
    if __name__ == "__main__":
        sys.exit(main())


init()
