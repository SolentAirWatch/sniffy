# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 23:16:17 2017

@author: bob
"""

import sys, time
from socket import *
import numpy as np
import json

s = socket(AF_INET, SOCK_DGRAM)
MYPORT = 5001
message = "hello \n"
sep = '\n'

Fs = 10
t = 0.0
omega1 = 2 * np.pi
omega2 = np.pi

while True:
    t = t + 1/Fs
    data1 = str(np.sin(omega1*t))
    data2 = str(np.sin(omega2*t))
    message = json.encoder([data1, data2])
    s.sendto(message.encode(), ('127.0.0.1', MYPORT))
    time.sleep (1/Fs)
    