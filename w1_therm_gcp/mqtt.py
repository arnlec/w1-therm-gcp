import logging
import ssl
import paho.mqtt.client as mqtt
import jwt
import datetime
import time

class GCPClient:
    def __init__(self,gcpConfiguration,on_connect_callback=None,on_disconnect_callback=None,on_publish_callback=None,on_message_callback=None):
        self.configuration = gcpConfiguration 
        self.on_connect_callback=on_connect_callback
        self.on_disconnect_callback=on_disconnect_callback
        self.on_publish_callback=on_publish_callback
        self.on_message_callback=on_message_callback
        self.current = None
        self.connected = False

    def is_connected(self):
        return self.connected
    
    def error_str(self,rc):
        return '{}: {}'.format(rc,mqtt.error_string(rc))
    
    def on_connect(self, client, userdata, flags, rc):
        logging.debug('on_connect')
        self.connected = True
        if self.on_connect_callback != None:
            self.on_connect_callback(client,userdata,flags,rc)

    def on_disconnect(self, client, userdata, rc):
        logging.debug('on_disconnect')
        self.connected = False
        if self.on_disconnect_callback != None:
            self.on_disconnect_callback(client,userdata,rc)

    def on_publish(self, client, userdata, mid):
        logging.debug('on_publish %s %s %s',client,userdata,mid)

    def on_message(self, client, userdata, message):
        pass
        payload = str(message.payload.decode('utf-8'))
        logging.debug('Received message \'{}\' on topic \'{}\' with Qos {}'.format(
            payload, 
            message.topic, 
            str(message.qos))
        )
        if self.on_message_callback !=None:
            self.on_message_callback(client,userdata,message)
    
    def create_jwt(self):
        token = {
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'aud' : self.configuration['mqtt']['project_id']
        }
        with open(self.configuration['mqtt']['private_key_file'], 'r') as f:
            private_key = f.read()
        
        return jwt.encode(token,private_key,algorithm=self.configuration['mqtt']['algorithm'])

    def wait_for_connection(self, timeout):
        total_time = 0
        while not self.is_connected() and total_time < timeout:
            logging.debug("wait_for_connection %d" % timeout)
            total_time +=1
            time.sleep(1)
        if not self.is_connected():
            raise RuntimeError('Could not connect to MQTT bridge.')
        logging.debug("wait_for_connection terminated %s" % self.is_connected())

    def disconnect(self):
        if self.current != None:
            self.current.loop_stop()
            self.current.disconnect()

    def connect(self):
        client_id = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(
            self.configuration['mqtt']['project_id'],
            self.configuration['mqtt']['region'],
            self.configuration['mqtt']['registry_id'],
            self.configuration['mqtt']['device_id']
        )
        client = mqtt.Client(client_id=client_id)
        client.username_pw_set(
            username = 'unused',
            password = self.create_jwt()
        )
        client.enable_logger(logging)
        client.tls_set(
            ca_certs =self.configuration['mqtt']['ca_certs'], 
            tls_version= ssl.PROTOCOL_TLSv1_2)
        client.on_connect = self.on_connect
        client.on_publish = self.on_publish
        client.on_disconnect = self.on_disconnect
        client.on_message = self.on_message
        logging.debug('connecting client %s ...' % client_id)
        self.current = client
        client.connect_async(
            self.configuration['mqtt']['mqtt_bridge_hostname'],
            self.configuration['mqtt']['mqtt_bridge_port']
        )
        client.loop_start()
        self.wait_for_connection(self.configuration['mqtt']['mqtt_connection_timeout'])

    def publish(self,value):      
        logging.debug("send %s to gcp" % value)
        if self.current == None:
            self.connect()
        if self.is_connected == False:
            self.current.reconnect()
        result = self.current.publish(
            topic="/devices/%s/events" % self.configuration['mqtt']['device_id'],
            payload=value,
            qos=0) 
        result.wait_for_publish()
        return result.is_published()


