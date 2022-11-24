import paho.mqtt.client as mqtt
import threading
import time
import time
import pyaudio
import wave

# CHUNK = 1024
# FORMAT = pyaudio.paInt16
# CHANNELS = 2
RATE = 44100

# p = pyaudio.PyAudio()
# frames = []

broker="test.mosquitto.org"
port=1883
topic = "AAIBsom"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print("Connection failed")
        
    client.subscribe(topic)
    print("subscribing to topic : " + topic)


def disconnect():
    print("client is disconnecting..")
    client.disconnect()


def on_message(client, userdata, message):
    data = message.payload.decode('utf-8')
    print("received message: " ,str(data))
    with open('dadosSOM.txt', 'a', encoding='UTF8') as f:
        # Append text at the end of file
        f.write(data + "\n")
    time.sleep(1/RATE) #colocar aqui a freq de aquisição
    #frames.append(data)
    


### MQTT ###
client = mqtt.Client("Gitpod")
client.connect(broker, port) 
client.on_connect= on_connect

def subscribing():
    client.on_message = on_message
    client.loop_forever()


sub=threading.Thread(target=subscribing)

### Start MAIN ###
#stop_threads = False
sub.start()




# with wave.open("sound1.wav", "w") as wf:
#          wf.setnchannels(CHANNELS)
#          wf.setsampwidth(p.get_sample_size(FORMAT))
#          wf.setframerate(RATE)
#          wf.writeframes(b''.join(frames))
#          print("Sound file saved.")
         


