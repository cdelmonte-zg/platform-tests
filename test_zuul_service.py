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
    
    def call_alien_service(self):
         targetUri = "http://{}:5555/api/aliens/v1/aliens/f3831f8c-c338-4ebe-a82a-e2fc1d1ff78a".format(containerIP)
         http_obj = Http(".cache")
         (resp, content) = http_obj.request(
         uri=targetUri,
         method='GET',
         headers=self.build_headers())
         return resp,content
     
    
    def call_planet_service(self):
         targetUri = "http://{}:5555/api/planets/v1/planets/e254f8c-c442-4ebe-a82a-e2fc1d1ff78a/aliens".format(containerIP)
         http_obj = Http(".cache")
         (resp, content) = http_obj.request(
         uri=targetUri,
         method='GET',
         headers=self.build_headers())
         return resp,content
    
    def test_zuul_service_routes(self):
        (resp, content) = self.call_zuul_service()
        results = json.loads(content.decode("utf-8"))
        self.assertEqual(resp.status, 200)
        self.assertEquals("alienservice", results["/api/aliens/**"])
        self.assertEquals("planetservice", results[ "/api/planets/**"])
        self.assertEquals("authenticationservice", results["/api/authenticationservice/**"])
        self.assertEquals("configserver", results["/api/configserver/**"])
        #self.assertEquals(6, len(results))
    
    def test_alien_service(self):
        (resp, content) = self.call_alien_service()
        results = json.loads(content.decode("utf-8"))
        self.assertEqual(resp.status, 200)
        self.assertEqual("f3831f8c-c338-4ebe-a82a-e2fc1d1ff78a", results["id"])
        self.assertEqual("dangerous", results["alienType"])
        self.assertEqual("venusian megaloman", results["name"])
        self.assertEqual("e254f8c-c442-4ebe-a82a-e2fc1d1ff78a", results["planetId"])
    
    def test_planet_service(self):
        (resp, content) = self.call_planet_service()
        results = json.loads(content.decode("utf-8"))
        self.assertEqual(resp.status, 200)
        self.assertEqual("f3831f8c-c338-4ebe-a82a-e2fc1d1ff78a", results[0]["id"])
        self.assertEqual("dangerous", results[0]["alienType"])
        self.assertEqual("venusian megaloman", results[0]["name"])
        self.assertEqual("e254f8c-c442-4ebe-a82a-e2fc1d1ff78a", results[0]["planetId"])
     
def retrieve_oauth_service():
    targetUri = "http://{}:5555/api/authenticationservice/auth/oauth/token ".format(containerIP)
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
    containerIP = "35.156.253.72"
    print "Running zuul service platform tests against container ip: {}".format(containerIP)
    oauthtoken = retrieve_oauth_service()
    print "OAuthToken successfully retrieved: {}".format(oauthtoken)
    unittest.main()
