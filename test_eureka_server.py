import unittest
import logging
import json
import string
import argparse
import os
from httplib2 import Http

class TestEurekaServer(unittest.TestCase):

    def call_eureka_service(self,serviceName):
         targetUri = "http://{}:8761/eureka/apps/{}".format(containerIP,serviceName)
         http_obj = Http(".cache")
         (resp, content) = http_obj.request(
         uri=targetUri,
         method='GET',
         headers={'Content-Type': 'application/json; charset=UTF-8', 'connection': 'close', 'Accept': 'application/json'})
         return resp,content

    def service_present(self, results, serviceName):
        if results["application"]["name"]==serviceName:
          return True
        False

    def assert_eureka_service(self,servicename):
        http_obj = Http(".cache")
        (resp, content) = self.call_eureka_service(servicename)
        results = json.loads(content.decode("utf-8"))
        self.assertEqual(resp.status, 200)
        self.assertEquals(True, self.service_present(results, servicename))

    def test_configservice(self):
        self.assert_eureka_service("CONFIGSERVER")

    def test_zuulservice(self):
        self.assert_eureka_service("ZUULSERVICE")
        
    def test_authenticationservice(self):
        self.assert_eureka_service("AUTHENTICATIONSERVICE")

    def test_alienservice(self):
        self.assert_eureka_service("ALIENSERVICE")

    def test_planetservice(self):
        self.assert_eureka_service("PLANETSERVICE")

if __name__ == '__main__':
    containerIP = "18.196.20.94"
    print "Running eureka service platform tests against container ip: {}".format(containerIP)
    unittest.main()
