import requests

# remote
BASE = "https://heroku-tests-app-1a282992c1f2.herokuapp.com/"

# local
# BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE)
print(response.json())

input()
response = requests.post(BASE + "tags", data={"title": "C arrays issue", "body": "I'm looking for a way to understand how arrays work in C."})
print(response.json())

input()
response = requests.post(BASE + "tags", data={"title": "How does JavaScript work?", "body": "This for example <b> you know? </b>"})
print(response.json())
