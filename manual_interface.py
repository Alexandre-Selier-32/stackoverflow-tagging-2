import requests

BASE = "https://heroku-tests-app-1a282992c1f2.herokuapp.com/"

title = "This is a headache."

body = "Shouldn't C++ arrays behave differently?"

response = requests.post(BASE + "tags", data={'title': title, 'body': body})
print(response.json())
