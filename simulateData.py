import math
import paho.mqtt.client as mqtt
import time
import datetime
import json
import argparse
from pprint import pprint  # makes data more pretty

# setup onboard serial port NB RPi 3 address

# useage - python simulateData.py -n n 
# where n is the client id

pwrd = "IReallyLikeNO2!"
broker = "awdrop"
topic = "/sniffy/test"

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


parser = argparse.ArgumentParser(description='simulation of sniffy data')
parser.add_argument('-c', '--clientID', help='clientID number') 
parser.add_argument('-l', '--location', help='geohash for location')

args = parser.parse_args()

monitorID = args.clientID
monitorLocation = args.location
print monitorID
print monitorLocation


# set up objects
client = mqtt.Client()  # client_id=clientNo - not using a client number
client.username_pw_set("data", password=pwrd)
# set up callbacks
client.on_connect = on_connect
client.on_publish = on_publish
client.connect(broker)  # (address, port, timeout (sec) )


# write a blank message to CSV so we can add headers at the start of the file
message = {
    'time': "init",
    'id': monitorID,
    'PM1': 0,
    'PM25': 0,
    'PM10': 0,
    'geohash': monitorLocation
    }

client.loop_start()  # start the network loop
t = 0

while True: # PMSx003 sensor by default streams data and non-uniform intervals - replace with timed polling
    try:
        # rcv = read_pm_line(port)
        message = {
            'sendTime': str(datetime.datetime.now()),
            'id': monitorID,
            'PM1': 20+20*math.sin(t/60),
            'PM25': 20+20*math.sin(((t/60)*2)+3),
            'PM10': 20 + (20 * math.sin( ((t/60)*0.5)+4 )),
            'geohash': monitorLocation
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
        pprint(message)
        client.publish(topic, payload=json.dumps(message), qos=0, retain=False)
        #w = csv.DictWriter(f, message.keys())
        #w.writerow(message)
        time.sleep(0.5) # wait 100 millisonds
        t=t+0.1
    except KeyboardInterrupt:
        break
        
