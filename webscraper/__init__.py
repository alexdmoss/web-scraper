# flake8: noqa

from flask import Flask

app = Flask(__name__)

from webscraper import scrape
