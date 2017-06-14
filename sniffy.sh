#!/bin/sh


sleep 30 # avoid starting the scrip before the network is up
cd /
cd home/pi/sniffy
sudo python standalonePMS.py # pmsX003.py
# sudo bmp180.py
