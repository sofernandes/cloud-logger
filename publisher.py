import paho.mqtt.client as mqtt 
import numpy as np
import time


mqttBroker ="test.mosquitto.org" 

client = mqtt.Client("test/AAIB")
client.connect(mqttBroker, port=1883) 
x=0
while True:
    x += 1
    randNumber = np.sin(x)
    client.publish("NumberAAIB", randNumber)
    print("Just published " + str(randNumber) + " to topic NumberAAIB")
    time.sleep(1)