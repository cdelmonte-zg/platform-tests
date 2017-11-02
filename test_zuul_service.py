import unittest
import logging
import json
import string
import argparse
import os
import urllib
from httplib2 import Http

class TestZuulService(unittest.TestCase):

    def build_headers(self):
        return {'Content-Type': 'application/json; charset=UTF-8',
                'connection': 'close',
                'Accept': 'application/json',
                'Authorization': 'Bearer {}'.format(oauthtoken)}

    def call_zuul_service(self):
         targetUri = "http://{}:5555/routes".format(containerIP)
         http_obj = Http(".cache")
         (resp, content) = http_obj.request(
         uri=targetUri,
         method='GET',
         headers=self.build_headers())
         return resp,content

def retrieve_oauth_service():
    targetUri = "http://{}:5555/api/auth/oauth/token ".format(containerIP)
    http = Http(".cache")
    body = {'grant_type': 'password',
            'scope': 'webclient',
            'username':'william.gibson',
            'password':'password2'}

    content = http.request(
            uri=targetUri,
            method="POST",
            headers={'Content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Basic Y2RlbG1vbnRlOnRoaXNpc3NlY3JldA=='},
            body=urllib.urlencode(body))
    results = json.loads(content[1])
    return results.get("access_token")

if __name__ == '__main__':
    containerIP = os.getenv('CONTAINER_IP',"192.168.99.100")
    print "Running zuul service platform tests against container ip: {}".format(containerIP)
    oauthtoken = retrieve_oauth_service()
    print "OAuthToken successfully retrieved: {}".format(oauthtoken)
    unittest.main()
