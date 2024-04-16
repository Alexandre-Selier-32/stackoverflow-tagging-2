import requests

# remote
BASE = "https://heroku-tests-app-1a282992c1f2.herokuapp.com/"

# local
# BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE)
print(response.json())

input()
# works
# response = requests.post(BASE + "hello")
# works too, even with unexpected data
response = requests.post(BASE + "hello", data={"toto": 4})
print(response.json())

input()
response = requests.post(BASE + "prod", data={"a": 7, "b": 4})
print(response.json())

input()
response = requests.post(BASE + "is_js", data={"sentence": "Hello there"})
print(response.json())

input()
response = requests.post(BASE + "is_js", data={"sentence": "How does JavaScript work?"})
print(response.json())

input()
response = requests.post(BASE + "is_js", data={"sentence": "Javascript confuses me"})
print(response.json())

input()
response = requests.post(BASE + "house_price", data={"area": 120, "garden": 1})
print(response.json())

input()
response = requests.post(BASE + "dummy_tags", data={"question": "I'm having trouble with arrays"})
print(response.json())
