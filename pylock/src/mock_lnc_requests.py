import requests

r = requests.post("http://127.0.0.1:8000", "hello")

for i in r:
    print(i)