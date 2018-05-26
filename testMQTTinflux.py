
#!/usr/bin/env python2
import paho.mqtt.client as mqtt
import datetime
import time
import json
from pprint import pprint  # makes data more pretty
from influxdb import InfluxDBClient

topicName = "/sniffy/#"
username = 'data'
password = 'IReallyLikeNO2!'
host = '209.97.143.180'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topicName, qos=0)
    
def on_message(client, userdata, msg):
    print("Received a message on topic: " + msg.topic)
    receiveTime = datetime.datetime.utcnow()  # Use utc as timestamp
    data = json.loads(msg.payload.decode('utf-8'))  # decode the json message 
    #pprint(data)
    print(data["PM1"])
    num = data["PM1"]
    print(isinstance(num, float))
    PM1 = data["PM1"]
    PM25 =  data["PM25"]
    PM10 =  data["PM10"],

    jsonData = [
        {
            "id": data["id"],
            "time": data["sendTime"],
            "fields":{
                "PM25": PM25,
                "PM1":  PM1
                }
            }
        ]

    pprint(jsonData)
    # print(str(receiveTime) + ": " + msg.topic + " " + str(data))
    # dbclient.write_points(jsonData)
        
# Set up a client for InfluxDB
dbclient = InfluxDBClient(host, 8086, 'root', 'root', 'sensordata')

# Initialize the MQTT client that should connect to the Mosquitto broker
client = mqtt.Client()
client.username_pw_set(username, password=password)

# set MQTT call back functions
client.on_connect = on_connect
client.on_message = on_message

connOK = False
    
# Try connecting, if failed try again after 2 seconds
while(connOK == False):
    try:
        print('trying to connect to MQTT broker')
        client.connect(host)
        connOK = True
    except:
        connOK = False
        print('failed to connect, trying again')
    time.sleep(2)

# Blocking loop to the Mosquitto broker
client.loop_forever()
