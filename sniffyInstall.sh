#!/bin/bash
mkdir ~/AirQuality
mkdir ~/AirQuality/client
cd
sudo apt-get update
sudo pip install paho-mqtt
sudo pip install pyserial
sudo pip install adafruit-mcp3008
sudo pip install spidev
