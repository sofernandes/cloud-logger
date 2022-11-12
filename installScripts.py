# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 15:37:30 2022

@author: Susana Fernandes 55321

Script to install all packages used
"""

##To install streamlit
sudo pip3 install streamlit

##To install MQTT service
sudo apt install -y mosquitto
sudo apt install mosquitto-clients
sudo service mosquitto start
sudo service mosquitto status
0
##To install Paho-MQTT
sudo pip3 install paho-mqtt
git clone https://github.com/eclipse/paho.mqtt.python.git
cd paho.mqtt.python
python setup.py install