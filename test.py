import main
import unittest
import json

# remote
BASE = "https://heroku-tests-app-1a282992c1f2.herokuapp.com/"

# local
# BASE = "http://127.0.0.1:5000/"

class MyTestCase(unittest.TestCase):

    def setUp(self):
        main.app.testing = True
        self.app = main.app.test_client()

    def test_home(self):
        response = self.app.post(BASE + "tags", data={"title": "C arrays issue", "body": "I'm looking for a way to understand how arrays work in C."})
        result = json.loads(response.data.decode('utf-8'))['data']
        result_as_set = set(result)
        self.assertEqual(result_as_set, {'c', 'arrays'})

if __name__ == '__main__':
    unittest.main()

# response = requests.get(BASE)
# print(response.json())
#
# input()
# response = requests.post(BASE + "tags", data={"title": "C arrays issue", "body": "I'm looking for a way to understand how arrays work in C."})
# print(response.json())
#
# input()
# response = requests.post(BASE + "tags", data={"title": "How does JavaScript work?", "body": "This for example <b> you know? </b>"})
# print(response.json())
#
