import requests, json

url = 'http://localhost:8000/events'
f = open("staticdata.json", 'r')
data = json.load(f)
for item in data:
    payload = item
    header = {}
    res = requests.post(url, json = payload, headers = {})