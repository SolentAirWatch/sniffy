#!/bin/sh


sleep 30 # avoid starting the scrip before the network is up
cd /
cd home/pi/monitor_v1
sudo python pmsX003.py
sudo bmp180.py
cd /
