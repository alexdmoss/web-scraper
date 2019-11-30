import main
from bs4 import BeautifulSoup


def test_can_load_url():
    data = main.load_url_as_soup('https://pythonprogramming.net/parsememcparseface/')
    assert '<html' in str(data)


def test_can_read_title():
    data = BeautifulSoup(open("tests/mocks/test_data.html"), "html.parser")
    title = main.get_title(data)
    assert 'Python' in title


def test_successfully_find_word_in_source():
    data = BeautifulSoup(open("tests/mocks/test_data.html"), "html.parser")
    word = 'Readability'
    assert main.find_word_in_source(data, word) is True


def test_fail_to_find_word_in_source():
    data = BeautifulSoup(open("tests/mocks/test_data.html"), "html.parser")
    word = 'Bananas'
    assert main.find_word_in_source(data, word) is False
