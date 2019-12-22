import logging
import time
from w1thermsensor import W1ThermSensor

from .mqtt import GCPClient
from .configuration import factory as configuration_factory

class W1ThermGCP:
    def __init__(self,configuration_file=None):
        self.configuration = configuration_factory(configuration_file)
        self.gcp = GCPClient(self.configuration['gcp'])
        self.sensor = W1ThermSensor()

    def run(self): 
        logging.info("w1_therm_gcp started")
        logging.debug(self.configuration)
        while True:
            self.readTemperature()
            time.sleep(int(self.configuration['timer']))

    def readTemperature(self):
        temp = self.sensor.get_temperature()
        logging.debug("readTemperature %s" % temp)
        self.gcp.publish(temp)