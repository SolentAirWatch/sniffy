# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 23:16:17 2017

@author: mihaela
"""

import sys, time
from socket import *
import numpy as np
import json
import datetime

s = socket(AF_INET, SOCK_DGRAM)
MYPORT = 33333
message = {'timestamp': str(datetime.datetime.now()),
        'NO2WE': 0,
        'NO2AE': 0,
        'SO2WE': 0,
        'SO2AE': 0,
        'TEMP': 0,
        'VREF': 0}
sep = '\n'

Fs = 10
t = 0.0
omega1 = 2 * np.pi
omega2 = np.pi

while True:
    payload=json.dumps(message)
    s.sendto(payload, ('127.0.0.1', MYPORT))
    time.sleep (1/Fs)
    