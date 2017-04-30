#!/bin/bash
mkdir ~/AirQuality
mkdir ~/AirQuality/client
cd
virtualenv -p python2 py2Sniffy
source ./py2Sniffy/bin/activate
sudo apt-get update
curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash -
sudo pip install paho-mqtt
sudo pip install pyserial
sudo pip install adafruit-mcp3008
sudo pip install spidev
