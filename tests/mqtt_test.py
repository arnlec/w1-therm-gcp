import unittest
import logging
from w1_therm_gcp.mqtt import GCPClient
import jwt
import time
import json

class TestGcpClient(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.configuration={
            'precision' : '500',
            'mqtt': {
                'project_id': 'iot-dev-260617',
                'region': 'europe-west1',
                'registry_id': 'mylab',
                'device_id': 'w1-therm-dev',
                'private_key_file': './w1-therm-dev.key',
                'algorithm': 'RS256',
                'ca_certs': './mqtt.googleapis.com.pem',
                'mqtt_bridge_hostname': 'mqtt.googleapis.com',
                'mqtt_bridge_port': 443,
                'mqtt_connection_timeout': 5
            }
        }

    def test_create_token(self):
        client = GCPClient(self.configuration)
        token = client.create_jwt()
        self.assertIsNotNone(token)

    def test_connect(self):
        client = GCPClient(self.configuration)
        client.connect()
        self.assertTrue(client.is_connected())
    
    def test_publish_events(self):
        client = GCPClient(self.configuration)
        result = client.publish("{'value':'21500'}")
        client.disconnect()
        self.assertTrue(result)
    
    def test_publish_state(self):
        client = GCPClient(self.configuration)
        result = client.publish(json.dumps({'temperature':'20.5'}),'state')
        client.disconnect()
        self.assertTrue(result)
        
