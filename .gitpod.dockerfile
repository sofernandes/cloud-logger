FROM gitpod/workspace-full

RUN sudo apt-get update \
 && sudo apt-get install -y \
    ##To install streamlit
    streamlit \

    ##To install MQTT service
    -y mosquitto \
    mosquitto-clients \
    service mosquitto start \
    service mosquitto status \

    ##To install Paho-MQTT
    paho-mqtt \
    git clone https://github.com/eclipse/paho.mqtt.python.git \
    cd paho.mqtt.python \
    python setup.py install \
 && sudo rm -rf /var/lib/apt/lists/*
