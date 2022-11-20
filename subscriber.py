import paho.mqtt.client as mqtt
import csv
import time
    

def on_message(client, userdata, message):    
        data = message.payload.decode("utf-8")
        print("received message: " ,str(data))
        with open('dados.txt', 'a', encoding='UTF8') as f:
            # Append text at the end of file
            f.write(data + "\n")
        time.sleep(1) #colocar aqui a freq de aquisição

def on_connect(client, userdata, flags, rc):

    if rc == 0:
        print("Connected to broker")

        global Connected                #Use global variable
        Connected = True                #Signal connection
    else:
        print("Connection failed")

def disconnect():
    print("client is disconnecting..")
    client.disconnect()
    Connected = False


Connected = False   #global variable for the state of the connection
mqttBroker ="test.mosquitto.org"

client = mqtt.Client("Gitpod")
client.connect(mqttBroker, port=1883)
client.on_connect= on_connect 


client.loop_start()

client.subscribe("NumberAAIB")
client.on_message=on_message 
 

time.sleep(10*60) #substituir por 10 minutos de aquisição
client.loop_stop()
disconnect()

