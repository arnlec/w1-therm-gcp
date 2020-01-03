import unittest
import w1_therm_gcp.configuration as configuration

class TestConfiguration(unittest.TestCase):
    def test_factory(self):
        conf = configuration.factory('./configuration.yaml')
        self.assertEqual('w1-therm-dev',conf['device_id'])
    
        