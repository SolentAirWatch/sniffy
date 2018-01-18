# Sniffy Monitor

Solent Air Watch (www.solentairwatch.co.uk) is a community project. Please help support us by suggesting improvements to our code or documentation  via pull requests. Build plans for the sniffy air quality monitor are available at 

Sniffy is an air quality monitor based on the raspberry pi. It is designed to accept a number of different air quality sensors. We currently use the Plantower PMS5003 to estimate concentrations of PM1, PM2.5 and PM10. We use Alphasense's gas sensors to measure NO2.

Our current efforts are in developing the monitor to work reliably on public and private wifi and we're looking at extending to long range wireless networks (GSM, LTE, LoRaWAN and sigfox). The Sniffy communicates via MQTT.

The scripts in this repository have been tested using Raspberry Pi 3 and Raspberry Pi Zero W with Rasbian Jessie Lite. This can be downloaded at
https://www.raspberrypi.org/downloads/raspbian/.

Currently only Python 2.7 is supported until the bitwise operations are updated to python 3.

The following instructions assume you have a fresh install of raspbian Lite and are not familiar with the Raspbery Pi.

# The easy way to enable ssh and setup wireless on the Raspberry Pi

The boot partition is readable using a card reader with any opertating system. Create the file /boot/wpa_supplicant.conf. Add your wifi settings as follows:

    network={
        ssid="YOUR_SSID"
        psk="YOUR_PASSWORD"
        key_mgmt=WPA-PSK
    }

On the first boot raspbian will copy the file to the normal location (/etc/wpa_supplicant/wpa_supplicant.conf).
To enable SSH on the raspberry pi, copy an empty file named shh to the boot partition. 

# Installing monitor software to Raspbery Pi
Find the IP address of your Pi. The easiest way is through your home router. Then login using ssh. The default password is raspberry.

    shh pi@<your ip address>

Firstly change the default password by typing 

    passwd

The PM sensor uses the serial port, the environmental sensor uses I2C and the ADC uses SPI. THese interfaces should be turned on using by running

    sudo raspi-config

Go to /Interfacing Options/Serial answer no to a login shell and yes to the serial port being enabled. Also turn on SPI and I2C. You will be prompted to reboot when you exit.

The monitor is in the early stages of development, this means things can change. Because of this it is recommneded to use a virtual environement. The install script assumes you have python 2.7 and pip installed. If you need to install it run the following:

    sudo apt-get update
    sudo apt-get install -y python-pip git build-essential python-dev python-smbus
    
To install the latest monitor scripts clone the reposetory and run

    cd
    git clone https://github.com/solentairwatch/sniffy
    ./sniffy/install.sh
    
This includes the scipts for the analogue gas sensors which interface via the MCP3008 ADC chip on the SPI bus.

The monitor currently runs seperate scripts for each sensor.

To start the monitor when the pi boots 
    
    sudo crontab -e

then add the following line (currently starts PM monitor only)
NB script assumes that your not using virtualenv.

    @reboot sh /home/pi/sniffy/sniffy.sh >/home/pi/logs/cronlog 2>&1
    

# Important scripts

- pmsx003.py           this sends PM data from the PMS1003 senosr to the opensensors.io  via MQTT
- standalonePMS.py     as above but logs to SD instead of MQTT for offline use
