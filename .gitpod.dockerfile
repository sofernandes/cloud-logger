FROM gitpod/workspace-full

RUN sudo apt-get update \
 && sudo apt-get install -y \
    ##To install streamlit
    sudo pip3 install streamlit

    ##To install MQTT service
    sudo apt install -y mosquitto
    sudo apt install mosquitto-clients
    sudo service mosquitto start
    sudo service mosquitto status

    ##To install Paho-MQTT
    sudo pip3 install paho-mqtt
    git clone https://github.com/eclipse/paho.mqtt.python.git
    cd paho.mqtt.python
python setup.py install \
 && sudo rm -rf /var/lib/apt/lists/*
