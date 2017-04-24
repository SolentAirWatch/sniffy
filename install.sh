#!/bin/bash

mkdir ~/AirQuality
mkdir ~/AirQuality/client
sudo apt-get update
curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo apt-get install -y npm
sudo apt-get install -y upstart
pip install paho-mqtt
pip install pyserial
pip install Adafruit_GPIO.SPI
pip install adafruit-mcp3008
pip install spidev

