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

    def test_c_arrays(self):
        response = self.app.post(BASE + "tags", data={"title": "C arrays issue", "body": "I'm looking for a way to understand how arrays work in C."})
        result = json.loads(response.data.decode('utf-8'))['data']
        result_as_set = set(result)
        self.assertEqual(result_as_set, {'c', 'arrays'})

    def test_javascript(self):
        response = self.app.post(BASE + "tags", data={"title": "How does JavaScript work?", "body": "This for example <b> you know? </b>"})
        result = json.loads(response.data.decode('utf-8'))['data']
        result_as_set = set(result)
        self.assertEqual(result_as_set, {'javascript'})

    def test_long_body(self):
        long_body = 'lorem ipsum' * 1_000_000
        response = self.app.post(BASE + "tags", data={"title": "Brace yourselves for a long question", "body": long_body})
        result = json.loads(response.data.decode('utf-8'))['data']
        result_as_set = set(result)

        # For this test we just want no error. We're not expecting any specific tags.
        # So if the test arrives to this assert statement, we're fine.
        self.assert_(True)

    # This test should fail if you add it. Add it if you want to test that tests fail properly.

    # def test_to_fail(self):
    #     response = self.app.post(BASE + "tags", data={"title": "How does JavaScript work?", "body": "This for example <b> you know? </b>"})
    #     result = json.loads(response.data.decode('utf-8'))['data']
    #     result_as_set = set(result)
    #     self.assertEqual(result_as_set, {'impossible_tag'})

if __name__ == '__main__':
    unittest.main()
