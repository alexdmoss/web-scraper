import main


def test_can_load_url():
    data = main.load_url_as_soup('https://pythonprogramming.net/parsememcparseface/')
    assert '<html' in str(data)
