import unittest
import requests
import time

class RESTTestCase(unittest.TestCase):
    baseURL = 'https://localhost:1337/api/'
    token = None
    session = None

    def setUp(self):
        """Wait for the REST server to come up, then grab a token"""
        self.session = requests.Session()
        self.session.verify = False
        jsonRequest = {'username': 'empireadmin', 'password': 'empire'}
        while self.token is None:
            try:
                r = self.session.post(self.baseURL + 'admin/login', json = jsonRequest)
                self.token = r.json()['token']
            except:
                # sleep for 1/2 a second and retry
                time.sleep(.5)
                pass

    def tearDown(self):
        r = self.session.get(self.baseURL + 'admin/shutdown', params = {'token': self.token})

    def post(self, urlFragment, data = {}):
        """Utility method to POST dictionaries as JSON"""
        jsonRequest = data['token'] = self.token
        r = self.session.post(self.baseURL + urlFragment, json = jsonRequest)
        r.json()

    def get(self, urlFragment, params = {}):
        """Utility method to GET data from REST API"""
        paramsWithToken = data['token'] = self.token
        r = self.session.get(self.baseURL + urlFragment, params = paramsWithToken)
        r.json()

    def test_token(self):
        self.assertIsNotNone(self.token, msg = 'REST Token not set')

    def test_permanent_token(self):
        response = self.get('admin/permanenttoken')
        self.assertIsNotNone(response['token'], msg = 'REST Token not set')

if __name__ == '__main__':
    unittest.main()