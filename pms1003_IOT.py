import serial
import time
import datetime
import paho.mqtt.client as mqtt
import json

mqttc = mqtt.Client(client_id="5721")
mqttc.username_pw_set("josh", password="lmNh8CI5")
mqttc.connect("mqtt.opensensors.io")

# setup onboard serial port NB RPi 3 address
port = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=2.0)

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

# initalise variables
loop = 0
rcv_list = []

while True: # replace with timed polling
    try:
        rcv = read_pm_line(port)
# probably a more 'python' way of doing this        
        
        
        res = {'timestamp': str(datetime.datetime.now()),
            'apm10': ord(rcv[4]) * 256 + ord(rcv[5]),
            'apm25': ord(rcv[6]) * 256 + ord(rcv[7]),
            'apm100': ord(rcv[8]) * 256 + ord(rcv[9]),
            'pm10': ord(rcv[10]) * 256 + ord(rcv[11]),
            'pm25': ord(rcv[12]) * 256 + ord(rcv[13]),
            'pm100': ord(rcv[14]) * 256 + ord(rcv[15]),
            'gt03um': ord(rcv[16]) * 256 + ord(rcv[17]),
            'gt05um': ord(rcv[18]) * 256 + ord(rcv[19]),
            'gt10um': ord(rcv[20]) * 256 + ord(rcv[21]),
            'gt25um': ord(rcv[22]) * 256 + ord(rcv[23]),
            'gt50um': ord(rcv[24]) * 256 + ord(rcv[25]),
            'gt100um': ord(rcv[26]) * 256 + ord(rcv[27])
            }
        
        # convert message to JSON
        
        message = ('===============\n'
            'timestamp :{}\n'
            'PM1.0(CF=1): {}\n'
            'PM2.5(CF=1): {}\n'
            'PM10 (CF=1): {}\n'
            'PM1.0 (STD): {}\n'
            'PM2.5 (STD): {}\n'
            'PM10  (STD): {}\n'
            '>0.3um     : {}\n'
            '>0.5um     : {}\n'
            '>1.0um     : {}\n'
            '>2.5um     : {}\n'
            '>5.0um     : {}\n'
            '>10um      : {}'.format(res['timestamp'], res['apm10'], res['apm25'], res['apm100'],
                                    res['pm10'], res['pm25'], res['pm100'],
                                    res['gt03um'], res['gt05um'], res['gt10um'],
                                    res['gt25um'], res['gt50um'], res['gt100um']))
        
        print(message)
        time.sleep(0.01) # wait a millisond
        mqttc.publish("/users/josh/odi/airquality/PMcount", payload=json.dumps(res), qos=0, retain=False)
        
        rcv_list.append(res.copy())
        loop += 1
    except KeyboardInterrupt:
        break