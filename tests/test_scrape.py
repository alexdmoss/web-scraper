import webscraper.scrape as scrape
import logging
from bs4 import BeautifulSoup
from webscraper import app

logging.basicConfig(level=logging.INFO,
                    format="-> [%(levelname)s] [%(asctime)s] %(message)s",
                    datefmt="%Y-%m-%d %H:%M")


def test_can_load_url():
    data = scrape.load_url_as_soup("https://pythonprogramming.net/parsememcparseface/")
    assert "<html" in str(data)


def test_can_read_title():
    data = BeautifulSoup(open("tests/mocks/test_data.html"), "html.parser")
    title = scrape.get_title(data)
    assert "Python" in title


def test_successfully_find_word_in_source():
    data = BeautifulSoup(open("tests/mocks/test_data.html"), "html.parser")
    word = "Readability"
    assert scrape.find_word_in_source(data, word) is True


def test_fail_to_find_word_in_source():
    data = BeautifulSoup(open("tests/mocks/test_data.html"), "html.parser")
    word = "Bananas"
    assert scrape.find_word_in_source(data, word) is False


def test_for_successful_match(monkeypatch, mocker, caplog):
    caplog.set_level(logging.INFO)
    monkeypatch.setenv("TARGET_URL", "http://fake-url.com")
    monkeypatch.setenv("WORD_TO_FIND", "book")
    stub_html = mocker.patch("webscraper.scrape.load_url_as_soup")
    stub_html.return_value = BeautifulSoup(open("tests/mocks/test_data_successful_match.html"), "html.parser")
    with app.test_request_context("/", method="GET"):
        rv = app.dispatch_request()
        response = app.make_response(rv)
        assert response.status_code == 200
        assert "[SUCCESS]" in response.get_data(as_text=True)
        assert "[SUCCESS]" in caplog.text


def test_for_failed_match(monkeypatch, mocker, caplog):
    caplog.set_level(logging.INFO)
    monkeypatch.setenv("TARGET_URL", "http://fake-url.com")
    monkeypatch.setenv("WORD_TO_FIND", "book")
    stub_html = mocker.patch("webscraper.scrape.load_url_as_soup")
    stub_html.return_value = BeautifulSoup(open("tests/mocks/test_data_failed_match.html"), "html.parser")
    with app.test_request_context("/", method="GET"):
        rv = app.dispatch_request()
        response = app.make_response(rv)
        assert response.status_code == 200
        assert "[FAILED]" in response.get_data(as_text=True)
        assert "[FAILED]" in caplog.text


def test_for_missing_url(monkeypatch, mocker, caplog):
    caplog.set_level(logging.INFO)
    monkeypatch.setenv("WORD_TO_FIND", "book")
    with app.test_request_context("/", method="GET"):
        rv = app.dispatch_request()
        response = app.make_response(rv)
        assert response.status_code == 200
        assert "URL not specified" in response.get_data(as_text=True)
        assert "URL not specified" in caplog.text


def test_for_missing_word_to_find(monkeypatch, mocker, caplog):
    caplog.set_level(logging.INFO)
    monkeypatch.setenv("TARGET_URL", "http://fake-url.com")
    stub_html = mocker.patch("webscraper.scrape.load_url_as_soup")
    stub_html.return_value = BeautifulSoup(open("tests/mocks/test_data_failed_match.html"), "html.parser")
    with app.test_request_context("/", method="GET"):
        rv = app.dispatch_request()
        response = app.make_response(rv)
        assert response.status_code == 200
        assert "Word to search for not specified" in response.get_data(as_text=True)
        assert "Word to search for not specified" in caplog.text
