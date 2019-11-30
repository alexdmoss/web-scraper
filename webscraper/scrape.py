import logging
import ssl

from webscraper import app

from os import getenv
from urllib.request import urlopen
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.INFO,
                    format="-> [%(levelname)s] [%(asctime)s] %(message)s",
                    datefmt="%Y-%m-%d %H:%M")

logger = logging.getLogger(__name__)


@app.route("/", methods=["GET"])
def scrape():
    data = None
    url = getenv("TARGET_URL")
    word_to_find = getenv("WORD_TO_FIND")

    if url:
        logger.info(f"URL to scrape set to {url}")
        data = load_url_as_soup(url)
        title = get_title(data)
        logger.info(f"Page Title: {title}")
    else:
        logger.error("URL not specified")
        return "[ERROR] URL not specified"

    if data and word_to_find:
        logger.info(f"Word to search for set to {word_to_find}")
        if find_word_in_source(data, word_to_find):
            logger.info("[SUCCESS] Word matched on web page")
            return "[SUCCESS] Word matched on web page"
        else:
            logger.info("[FAILED] Word is not present on web page")
            return "[FAILED] Word is not present on web page"
    else:
        logger.error("Word to search for not specified")
        return "[ERROR] Word to search for not specified"


def load_url_as_soup(url):
    source = urlopen(url, timeout=10, context=ssl._create_unverified_context()).read()
    return BeautifulSoup(source, "html.parser")


def get_title(data):
    return str(data.title)


def find_word_in_source(data, word):
    raw_text = data.get_text()
    if word in raw_text:
        return True
    else:
        return False


# if __name__ == "__main__":
#     app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
