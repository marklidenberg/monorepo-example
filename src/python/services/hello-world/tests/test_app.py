import requests


def test_app():
    try:
        assert requests.get("http://server:5050").text == "Hello, World!"
    except:
        assert requests.get("http://localhost:5050").text == "Hello, World!"
