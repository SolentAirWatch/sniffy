# Simple example of reading the MCP3008 analog input channels and printin# them all out.
# License: Public Domain
# import  standard libraries for timing, csv and udp coms
import time
import csv
import socket
import json
import datetime
# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

local_PORT = 33333;
local_HOST = '127.0.0.1'

remote_PORT = 33333
remote_HOST = '138.68.134.165'

# set the reference voltage for the ADC
Vref = 3.3 # ADC reference voltage
Fs = 10.0 # sample rate in Hz
ADCbits = 10.0 # bits on ADC
csvFile = ('/home/pi/AirQuality/client/logfile.csv')

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
w = csv.writer(open(csvFile,'a'),dialect='excel') # open/make the CSV file

print('Reading MCP3008 values, press Ctrl-C to quit...')
while True:
    # Read all the ADC channel values in a list.
    values = [0.0]*8
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = mcp.read_adc(i) * (Vref / (2.0**ADCbits)) * 1000.0

    # Print the ADC values.

    no2we_corr = (values[0] +(-286 +280)*10.0)
    no2ae_corr = 1.18*(values[1]+(-300 + 280)*10.0)
    so2we_corr = values[2] +(- 280 + 280)*10.0
    so2ae_corr = 1.15*(values[3] +(- 285 + 280)*10.0)

    sensitivity_no2 =10*0.22046
    sensitivity_so2 = 10*0.328

    no2_ppb = abs(no2we_corr - no2ae_corr)/(1000*sensitivity_no2)
    so2_ppb = abs(so2we_corr - no2ae_corr)/(1000*sensitivity_so2)

    message = {
        "_type": "a4",
        '$timestamp': str(datetime.datetime.now()),
        '$NO2WE': values[0],
        '$NO2AE': values[1],
        '$SO2WE': values[2],
        '$SO2AE': values[3],
        '$TEMP': values[4],
        '$VREF': values[5],
        '$NO2_ppb': no2_ppb,
        '$SO2_ppb': so2_ppb}

 #   w.writerow(values) # write the current line to CSV
    payload=json.dumps(message) # convert to json format
    w.writerow(values)
    print(payload)
    sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
    sock.sendto(payload, (local_HOST, local_PORT))
    sock.sendto(payload, (remote_HOST, remote_PORT))

    # Pause for sample period
    time.sleep(10/Fs) #1 times the sample rate - 1 miliseconds
