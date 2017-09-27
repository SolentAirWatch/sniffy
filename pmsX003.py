import serial
import paho.mqtt.client as mqtt
import time
import datetime
import json
import csv
from pprint import pprint  # makes data more pretty

# setup onboard serial port NB RPi 3 address
clientNo = "xxx"
pwrd = "xxx"
monitorID = '2'  # id 0 is reserved for test
monitorLocation = [50.9262, -1.4092]
port = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=2.0)
broker = "mqtt.opensensors.io"  # "46.101.13.195"     # test broker
topic = "/orgs/solentairwatch/sniffy"
csvFile = "PMSx003.csv" # keep a local copy for debug

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
    

# function to parse a line of binary data from PMSx003 -- needs updating for python 3
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
f = open(csvFile,'a')  # open the csv file but 'a'ppend it if it already exists
# Authenticate with opensensors.io
client = mqtt.Client(client_id=clientNo)
client.username_pw_set("solentairwatch", password=pwrd)
# set up callbacks
client.on_connect = on_connect
client.on_publish = on_publish
client.connect(broker)  # (address, port, timeout (sec) )


# write a blank message to CSV so we can add headers at the start of the file
message = {
    'time': "init",
    'id': monitorID,
    'cityName': "",
    'stationName': "",
    'averaging': 0,
    'latitude': monitorLocation[0],
    'longitude': monitorLocation[1],
    'PM1': 0,
    'PM25': 0,
    'PM10': 0}
w = csv.DictWriter(f, message.keys())
w.writeheader()

client.loop_start()  # start the network loop

while True: # PMSx003 sensor by default streams data and non-uniform intervals - replace with timed polling
    try:
        rcv = read_pm_line(port)
        message = {
            'time': str(datetime.datetime.now()),
            'id': monitorID,
            'cityName': "Southampton",
            'stationName': "Common#1",
            'latitude': monitorLocation[0],
            'longitude': monitorLocation[1],
            'averaging': 0,
            'PM1': ord(rcv[4]) * 256 + ord(rcv[5]),
            'PM25': ord(rcv[6]) * 256 + ord(rcv[7]),
            'PM10': ord(rcv[8]) * 256 + ord(rcv[9]),
            #'PM10_STD': ord(rcv[10]) * 256 + ord(rcv[11]),
            #'PM25_STD': ord(rcv[12]) * 256 + ord(rcv[13]),
            #'PM100_STD': ord(rcv[14]) * 256 + ord(rcv[15]),
            #'gr03um': ord(rcv[16]) * 256 + ord(rcv[17]),
            #'gt05um': ord(rcv[18]) * 256 + ord(rcv[19]),
            #'gr10um': ord(rcv[20]) * 256 + ord(rcv[21]),
            #'gr25um': ord(rcv[22]) * 256 + ord(rcv[23]),
            #'gr50um': ord(rcv[24]) * 256 + ord(rcv[25]),
            #'gr100um': ord(rcv[26]) * 256 + ord(rcv[27])
            }
        # pprint(message)
        client.publish(topic, payload=json.dumps(message), qos=0, retain=False)
        w = csv.DictWriter(f, message.keys())
        w.writerow(message)
        time.sleep(0.1) # wait 100 millisonds
    except KeyboardInterrupt:
        break
        
