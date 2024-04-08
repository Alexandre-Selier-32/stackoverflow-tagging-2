import requests

# remote
BASE = "https://murmuring-reef-63091-f9619afb8f40.herokuapp.com/"

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
