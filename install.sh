#!/bin/bash
sudo apt-get update
sudo apt-get install -y adafruit-mcp3008
curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo apt-get install -y npm
sudo apt-get install -y upstart