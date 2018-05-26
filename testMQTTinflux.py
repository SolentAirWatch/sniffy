
#!/usr/bin/env python2
import paho.mqtt.client as mqtt
import datetime
import time
import json
from pprint import pprint  # makes data more pretty
from influxdb import InfluxDBClient

username = 'data'
password = 'IReallyLikeNO2!'
host = 'awdrop'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("/sniffy/#")
    
def on_message(client, userdata, msg):
    print("Received a message on topic: " + msg.topic)
    receiveTime = datetime.datetime.utcnow()  # Use utc as timestamp
    data = json.loads(msg.payload.decode('utf-8'))  # decode the json message 
    isfloatValue=False
    #pprint(data)
    print(data["PM1"])
    num = data["PM1"]
    print(isinstance(num, float))

##    cursor.execute('''INSERT INTO sniffy

    jsonData = [
        {
            "id": data["id"],
            "time": data["sendTime"],
            "fields":{
                "PM10": data["PM10"],
                "PM25": data["PM25"],
                "PM1": data["PM1"]
                }
            }
        ]
    
    print(str(receiveTime) + ": " + msg.topic + " " + str(data))
    dbclient.write_points(jsonData)
        
# Set up a client for InfluxDB
dbclient = InfluxDBClient('localhost', 8086, 'root', 'root', 'sensordata')

# Initialize the MQTT client that should connect to the Mosquitto broker
client = mqtt.Client()
client.username_pw_set(username, password=password)
client.on_connect = on_connect
client.on_message = on_message
connOK=False

# Try connecting, if failed try again after 2 seconds
while(connOK == False):
    try:
        client.connect(broker)
        connOK = True
    except:
        connOK = False
    time.sleep(2)

# Blocking loop to the Mosquitto broker
client.loop_forever()
