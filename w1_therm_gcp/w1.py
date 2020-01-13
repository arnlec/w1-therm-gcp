import logging
import time
from w1thermsensor import W1ThermSensor
import json

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
        self.gcp.connect()
        self.started = True
        while self.started:
            self.readTemperature()
            time.sleep(int(self.configuration['timer']))
        self.gcp.disconnect()

    def readTemperature(self):
        temp = self.sensor.get_temperature()
        logging.debug("readTemperature %s" % temp)
        data = {'temperature':temp}
        self.gcp.publish(json.dumps(data),'state')