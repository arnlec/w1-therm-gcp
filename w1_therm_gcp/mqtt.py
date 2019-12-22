import logging

class GCPClient:
    def __init__(self,gcpConfiguration):
        self.configuration = gcpConfiguration 
        self.current == None

    def publish(self,value):
        if self.hasToBePublished(value):
            self.send(value)

    def send(self,value):
        logging.debug("send %s to gcp" % value)
        self.current = int(value)


    def hasToBePublished(self,value):
        if self.current == None:
            return True
        else:
            diff = abs(self.current - int(value))
            return diff <= int(self.configuration['precision'])
