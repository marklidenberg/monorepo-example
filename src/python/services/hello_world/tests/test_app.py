import requests

assert requests.get("http://localhost:5050").text == "Hello, World!"
