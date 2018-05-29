
#!/usr/bin/env python2
import paho.mqtt.client as mqtt
import datetime
import time
import json
from pprint import pprint  # makes data more pretty
from influxdb import InfluxDBClient

# error if field name is mispelt which causes a crash 
topicName = "/sniffy/#"
username = 'data'
password = 'IReallyLikeNO2!'
database = 'sniffy'
host = '209.97.143.180'# 'localhost' #'209.97.143.180'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topicName, qos=0)
    
def on_message(client, userdata, msg):
    print("Received a message on topic: " + msg.topic)
    receiveTime = datetime.datetime.utcnow()  # Use utc as timestamp
    data = json.loads(msg.payload.decode('utf-8'))  # decode the json message 
    pprint(data)
    
    jsonData = [
        {
            "measurement": 'sniffy',
            "tags": {
                    "id": data["id"],
                    "geohash": data["geohash"]
                    },
            "fields":{
                "PM10": data["PM10"],    
                "PM25": data["PM25"],
                "PM1":  data["PM1"] 
                },
            #"time": data["sendTime"]
            }
        ]

    pprint(jsonData)
    # print(str(receiveTime) + ": " + msg.topic + " " + str(data))
    dbclient.write_points(jsonData)
        
# Set up a client for InfluxDB
dbclient = InfluxDBClient(host, 8086, 'root', 'root', 'sensordata')

# Initialize the MQTT client that should connect to the Mosquitto broker
client = mqtt.Client()
client.username_pw_set(username, password=password)

# set MQTT call back functions
client.on_connect = on_connect
client.on_message = on_message

connOK = False
connAttemp = 1
    
# Try connecting, if failed try again after 2 seconds
while(connOK == False):
    try:
        print('trying to connect to MQTT broker, attempt ' + str(connAttemp))
        client.connect(host)
        connOK = True
    except:
        connOK = False
        print('failed to connect, trying again')
        connAttemp = connAttemp + 1 
    time.sleep(2)

# Blocking loop to the Mosquitto broker
client.loop_forever()
