import unittest
import logging
import json
import string
import argparse
import os
from httplib2 import Http

class TestConfigServer(unittest.TestCase):

    def call_config_service(self,serviceName,serviceEnv): 
         targetUri = "http://{}:5555/api/configserver/{}/{}".format(containerIP,serviceName,serviceEnv)
         
         print "Running config service platform tests against target URI: {}".targetUri
         
         http_obj = Http(".cache")
         (resp, content) = http_obj.request(
         uri=targetUri,
         method='GET',
         headers={'Content-Type': 'application/json; charset=UTF-8', 'connection': 'close'})
         return resp,content


    def test_alienservice_aws_dev(self):
         http_obj = Http(".cache")
         (resp, content) = self.call_config_service("alienservice","aws-dev")
         results = json.loads(content.decode("utf-8"))
         self.assertEqual(resp.status, 200)
         self.assertEquals("https://github.com/cdelmonte-zg/config-repo/alienservice/alienservice-aws-dev.yml",
                           results["propertySources"][0]["name"])

    def test_alienservice_default(self):
         http_obj = Http(".cache")
         (resp, content) = self.call_config_service("alienservice","default")
         results = json.loads(content.decode("utf-8"))
         self.assertEqual(resp.status, 200)
         self.assertEquals("https://github.com/cdelmonte-zg/config-repo/alienservice/alienservice.yml",
                           results["propertySources"][0]["name"])

    def test_planetservice_default(self):
         http_obj = Http(".cache")
         (resp, content) = self.call_config_service("planetservice","default")
         results = json.loads(content.decode("utf-8"))
         self.assertEqual(resp.status, 200)
         self.assertEquals("https://github.com/cdelmonte-zg/config-repo/planetservice/planetservice.yml",
                           results["propertySources"][0]["name"])

    def test_planetservice_aws_dev(self):
         http_obj = Http(".cache")
         (resp, content) = self.call_config_service("planetservice","aws-dev")
         results = json.loads(content.decode("utf-8"))
         self.assertEqual(resp.status, 200)
         self.assertEquals("https://github.com/cdelmonte-zg/config-repo/planetservice/planetservice-aws-dev.yml",
                           results["propertySources"][0]["name"])




if __name__ == '__main__':
    containerIP = os.getenv('CONTAINER_IP',"192.168.99.100")
    print "Running config service platform tests against container ip: {}".format(containerIP)
    unittest.main()
