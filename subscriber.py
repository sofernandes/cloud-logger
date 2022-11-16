import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))
    
def disconnect():
    print("client is disconnecting..")
    client.disconnect()


mqttBroker ="test.mosquitto.org"

client = mqtt.Client("Gitpod")
client.connect(mqttBroker, port=1883) 

client.loop_start()

client.subscribe("NumberAAIB")
client.on_message=on_message 

time.sleep(30) #colocar 10 minutos de aquisição
client.loop_stop()
disconnect()

