import paho.mqtt.client as mqtt 
import time
import pyaudio
import audioop
import threading


broker="test.mosquitto.org"
port=1883

def on_connect(client, userdata, flags, rc):

    if rc == 0:
        print("Connected to broker")
    else:
        print("Connection failed")
    #print("Connected with result code: ", str(rc))
    client.subscribe("Status")
    print("subscribing to topic : " + "Status")
    
    
def disconnect():
    print("client is disconnecting..")
    client.disconnect()


def on_message(client, userdata, message):
    global stop_threads
    msg = message.payload.decode("utf-8")
    print("Data requested "+str(msg))
    if msg == "False":
        stop_threads = True
        pub.join()
        disconnect()
    if msg == "True":
        stop_threads = False
        pub.start() 


def main():
    p = pyaudio.PyAudio()
    
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    #RECORD_SECONDS = 20 #Tempo de aquisição

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    print("* recording")
    
    while True:
        global stop_threads
        if stop_threads:
            break
        #for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        rms = audioop.rms(data, 2)
        client.publish("AAIBsom", rms)
        print("Just published " + str(rms) + " to topic AAIBsom")
        time.sleep(1/RATE)
        
    print("* done recording")
    stream.stop_stream()
    stream.close()
    p.terminate()
        

### MQTT ###
client = mqtt.Client("test/AAIB")
client.connect(broker, port) 
client.on_connect= on_connect


def subscribing():
    client.on_message = on_message
    client.loop_forever()


sub=threading.Thread(target=subscribing)
pub=threading.Thread(target=main)

### Start MAIN ###
stop_threads = False
sub.start()
