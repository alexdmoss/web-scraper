import main
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


def test_for_successful_match(monkeypatch, mocker, caplog):
    caplog.set_level(logging.INFO)
    monkeypatch.setenv("TARGET_URL", "http://fake-url.com")
    monkeypatch.setenv("WORD_TO_FIND", "book")
    stub_html = mocker.patch('main.load_url_as_soup')
    stub_html.return_value = BeautifulSoup(open("tests/mocks/test_data_successful_match.html"), "html.parser")
    main.main()
    assert "[SUCCESS]" in caplog.text


def test_for_failed_match(monkeypatch, mocker, caplog):
    caplog.set_level(logging.INFO)
    monkeypatch.setenv("TARGET_URL", "http://fake-url.com")
    monkeypatch.setenv("WORD_TO_FIND", "book")
    stub_html = mocker.patch('main.load_url_as_soup')
    stub_html.return_value = BeautifulSoup(open("tests/mocks/test_data_failed_match.html"), "html.parser")
    main.main()
    assert "[FAILED]" in caplog.text


def test_for_missing_url(monkeypatch, mocker, caplog):
    caplog.set_level(logging.INFO)
    monkeypatch.setenv("WORD_TO_FIND", "book")
    main.main()
    assert "URL not specified" in caplog.text


def test_for_missing_word_to_find(monkeypatch, mocker, caplog):
    caplog.set_level(logging.INFO)
    monkeypatch.setenv("TARGET_URL", "http://fake-url.com")
    stub_html = mocker.patch('main.load_url_as_soup')
    stub_html.return_value = BeautifulSoup(open("tests/mocks/test_data_failed_match.html"), "html.parser")
    main.main()
    assert "Word to search for not specified" in caplog.text
