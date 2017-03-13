# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 23:37:10 2017

@author: bob
"""

import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5001

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
                     
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    
    print("received message:", float(data.decode()))
    
