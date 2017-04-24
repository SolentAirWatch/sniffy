# monitor_v1


The scripts have been tested using Raspberry Pi 3 and Raspberry Pi Zero W with Rasbian Jessie Lite. This can be downloaded at
https://www.raspberrypi.org/downloads/raspbian/.

# The easy way to enable ssh and setup wireless

The boot partition is readable using a card reader with any opertating system. Create the file /boot/wpa_supplicant.conf. Add your wifi settings as follows:

    network={
        ssid="YOUR_SSID"
        psk="YOUR_PASSWORD"
        key_mgmt=WPA-PSK
    }

On the first boot raspbian will copy the file to the normal location (/etc/wpa_supplicant/wpa_supplicant.conf).
To enable SSH on the raspberry pi, make an empty file named shh on the boot partition. 

Currently only Python 2.7 is supported until the bitwise operations are updated to support python 3.

The monitor is in the early stages of development, this means things can change. It is recommneded to develop using a virtual environement. The install script assumes you have python 2.7 and pip installed. If you need to install it run the following:

    sudo apt-get install python python-pip virtualenv
    
Create a python 2.7 environment using

    virtualenv -p python2 environmentName

activate the virtual environement using

    source ./environmentName/bin/activate

To install the latest monitor scripts clone the reposetory and run

    git clone https://github.com/hantsairquality/monitor_v1/
    ./install.sh
    
This includes the scipts for the analogue gas sensors which interface via the MCP3008 ADC chip on the SPI bus.

This will install the current dependances.

The monitor currently runs seperate scripts for each sensor. These send data to a SQL via UDP. This is tempoary until we migrate to MQTT. To run the
