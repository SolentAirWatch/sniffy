
#!/usr/bin/env python2
import paho.mqtt.client as mqtt
import datetime
import time
import json
from pprint import pprint  # makes data more pretty
from influxdb import InfluxDBClient

username = 'data'
password = 'IReallyLikeNO2!'
broker = 'localhost'


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("/sniffy/#")
    
def on_message(client, userdata, msg):
    print("Received a message on topic: " + msg.topic)
    receiveTime = datetime.datetime.utcnow()  # Use utc as timestamp
    data = json.loads(msg.payload.decode('utf-8'))  # decode the json message 
    isfloatValue=False

    print(str(receiveTime) + ": " + msg.topic + " " + str(data))

#        json_body = [
#            {
#                "measurement": msg.topic,
#                "time": receiveTime,
#                "fields": {
#                    "value": val
#                }
#            }
#        ]
    dbclient.write_points(data)
    print("Finished writing to InfluxDB")
        
# Set up a client for InfluxDB
dbclient = InfluxDBClient('localhost', 8086, 'root', 'root', 'sensordata')

# Initialize the MQTT client that should connect to the Mosquitto broker
client = mqtt.Client()
client.username_pw_set(username, password=password)
client.on_connect = on_connect
client.on_message = on_message
connOK=False
while(connOK == False):
    try:
        client.connect(broker)
        connOK = True
    except:
        connOK = False
    time.sleep(2)

# Blocking loop to the Mosquitto broker
client.loop_forever()
