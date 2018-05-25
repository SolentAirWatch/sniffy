@import math
import paho.mqtt.client as mqtt
import time
import datetime
import json
import csv
from pprint import pprint  # makes data more pretty

# setup onboard serial port NB RPi 3 address
clientNo = "xxx"
pwrd = "IReallyLikeNO2!"
broker = "209.97.143.180"
monitorID = '10'  # id 0 is reserved for test
monitorLocation = [50.9262, -1.4092]
topic = "/sniffy/test"
csvFile = "dummy.csv" # keep a local copy for debug

def on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))
    # do nothing we're connected
    pass

def on_publish(client, userdata, mid):
    print(mid)
    # print('published a message')
    pass

def on_disconnect(client, userdata, rc):
    if rc !=0:
        print('unexpected disconect with code' + str(rc))
        client.reconnect()

# set up objects
f = open(csvFile,'a')  # open the csv file but 'a'ppend it if it already exists
# Authenticate with opensensors.io
client = mqtt.Client(client_id=clientNo)
client.username_pw_set("data", password=pwrd)
# set up callbacks
client.on_connect = on_connect
client.on_publish = on_publish
client.connect(broker)  # (address, port, timeout (sec) )


client.loop_start()  # start the network loop
t = 0

while True: # PMSx003 sensor by default streams data and non-uniform intervals - replace with timed polling
    try:
        # rcv = read_pm_line(port)
        message = t*10
        client.publish(topic, message, qos=0, retain=False)
        time.sleep(0.1) # wait 100 millisonds
        t=t+0.1
    except KeyboardInterrupt:
        break
        
