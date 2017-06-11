import serial
import paho.mqtt.client as mqtt
import time
import datetime
import json
import csv
from pprint import pprint  # makes data more pretty

# add a config file which is unique to each sniffy.
sensorID = 1 # Imput a sensor number here 

# setup onboard serial port NB RPi 3 address
port = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=2.0)
broker = "mqtt.opensensors.io"  # "46.101.13.195"     # test broker
topic = "/orgs/solentairwatch/sniffy"
monitorID = 'SOTON0001'  # id 0 is reserved for test
monitorLocation = [50.9262, -1.4092]
csvFile="/home/pi/AirQuality/client/pm.log" # keep a local copy for debug
t = 0
ts = 1
monitorLocation = [50.9262, -1.4092]
global t
global ts

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    # do nothing we're connected
    pass


def on_publish(client, userdata, mid):
    print(mid)
    print('published a message')
    pass


def on_disconnect(client, userdata, rc):
    # need some ability to error log and reconnect
    print('disconected with code' + str(rc))
    

# function to read a line of serial data
def read_pm_line(_port):
    rv = b''
    while True:
        ch1 = _port.read()
        if ch1 == b'\x42':
            ch2 = _port.read()
            if ch2 == b'\x4d':
                rv += ch1 + ch2
                rv += _port.read(28)
                return rv

# set up objects
w = csv.writer(open(csvFile,'a'),dialect='excel')
client = mqtt.Client(client_id="6421")
client.username_pw_set("solentairwatch", password="oIVRMg3R")
client.loop()


while True: # PMSx003 sensor by default streams data and non-uniform intervals - replace with timed polling
    try:
        print("trying to read")
        rcv = read_pm_line(port)
        print("is reading")
        #  The following needs updating to work on python 3
        message = {
            'id': monitorID,
            'cityName': "Southampton",
            'stationName': "Common#1",
            'latitude': monitorLocation[0],
            'longitude': monitorLocation[1],
            'time': str(datetime.datetime.now()),
            'averaging': 0,
            '$PM10': ord(rcv[4]) * 256 + ord(rcv[5]),
            '$PM25_CF1': ord(rcv[6]) * 256 + ord(rcv[7]),
            '$PM100_CF1': ord(rcv[8]) * 256 + ord(rcv[9]),
            '$PM10_STD': ord(rcv[10]) * 256 + ord(rcv[11]),
            '$PM25_STD': ord(rcv[12]) * 256 + ord(rcv[13]),
            '$PM100_STD': ord(rcv[14]) * 256 + ord(rcv[15]),
            '$gr03um': ord(rcv[16]) * 256 + ord(rcv[17]),
            '$gt05um': ord(rcv[18]) * 256 + ord(rcv[19]),
            '$gr10um': ord(rcv[20]) * 256 + ord(rcv[21]),
            '$gr25um': ord(rcv[22]) * 256 + ord(rcv[23]),
            '$gr50um': ord(rcv[24]) * 256 + ord(rcv[25]),
            '$gr100um': ord(rcv[26]) * 256 + ord(rcv[27])
            }
        pprint(json.dumps(message))
        client.publish(topic, payload=json.dumps(message), qos=0, retain=False)
        client.loop()
        w.writerow(json.dumps(message))
        time.sleep(0.1) # wait 100 millisonds

    except KeyboardInterrupt:
        break
