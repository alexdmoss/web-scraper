import main
import pytest
import logging
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.INFO,
                    format="-> [%(levelname)s] [%(asctime)s] %(message)s",
                    datefmt="%Y-%m-%d %H:%M")


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


def test_init(mocker):
    # run wrapper validity: https://medium.com/opsops/how-to-test-if-name-main-1928367290cb
    mocker.patch.object(main, "main", return_value=42)
    mocker.patch.object(main, "__name__", "__main__")
    mocker.patch.object(main.sys, 'exit')
    main.init()
    assert main.sys.exit.call_args[0][0] == 42


def test_main_for_successful_match(mocker, caplog):
    caplog.set_level(logging.INFO)
    stub_html = mocker.patch('main.load_url_as_soup')
    stub_html.return_value = BeautifulSoup(open("tests/mocks/test_data_successful_match.html"), "html.parser")
    main.main()
    print(caplog.text)
    assert "[SUCCESS]" in caplog.text


def test_main_for_failed_match(mocker, caplog):
    caplog.set_level(logging.INFO)
    stub_html = mocker.patch('main.load_url_as_soup')
    stub_html.return_value = BeautifulSoup(open("tests/mocks/test_data_failed_match.html"), "html.parser")
    main.main()
    print(caplog.text)
    assert "[FAILED]" in caplog.text
