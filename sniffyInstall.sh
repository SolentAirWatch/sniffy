#!/bin/bash
mkdir ~/AirQuality
mkdir ~/AirQuality/client
cd
virtualenv -p python2 py2Sniffy
source ./py2Sniffy/bin/activate
sudo apt-get update
sudo pip install paho-mqtt
sudo pip install pyserial
sudo pip install adafruit-mcp3008
sudo pip install spidev
