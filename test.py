import requests

# remote
BASE = "https://heroku-tests-app-1a282992c1f2.herokuapp.com/"

# local
# BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE)
print(response.json())

input()
response = requests.post(BASE + "bow_tags", data={"question": "I'm having trouble with arrays"})
print(response.json())

input()
response = requests.post(BASE + "bow_tags", data={"question": "JavaScript is worse than Python."})
print(response.json())
