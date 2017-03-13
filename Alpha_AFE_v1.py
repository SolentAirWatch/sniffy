# Author Joshua Taylor
# License: GPLv3

# import  standard libraries for timing, csv and udp coms
import time
import csv
import socket
import json
import datetime
# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# set the reference voltage for the ADC
Vref = 3.3 # ADC reference voltage
Fs = 10.0 # sample rate in Hz
ADCbits = 10.0 # bits on ADC
csvFile = ('logfile.csv')


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
    message = {'timestamp': str(datetime.datetime.now()),
        'NO2WE': values[0],
        'NO2AE': values[1],
        'SO2WE': values[2],
        'SO2AE': values[3],
        'TEMP': values[4],
        'VREF': values[5]}
    
    print('===============\n'.
        'timestamp :{}\n'
        'NO2 WE (mv): {}\n'
        'NO2 AE (mv) : {}\n'
        'SO2 WE (mv): {}\n'
        'SO2 AE (mv): {}\n'
        'TEMP (mv): {}\n'
        'VREF (mv): {}\n'.format(message['timestamp'], message['NO2WE'], message['NO2AE'], message['SO2WE'],
                                message['SO2AE'], message['TEMP'], message['VREF']))
                                
    w.writerow(values) # write the current line to CSV
    payload=json.dumps(message) # convert to json format
              
    # Pause for sample period
    time.sleep(1/Fs)

