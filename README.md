# cloud-logger
Instrumentation Cloud Logger made for the UC AAIB in 2022/2023. 

An interface was developed with streamlit where the user can control signal acquistion flow (start and stop). For this, streamlit will connect to MQTT Broker to send a "Status" message that the publisherSOM.py file will recieve and react accordingly.

Data will be acquired through the computer's microphone. The measure of the power in the audio signal (rms) will be sent to the MQTT broker on command (after "Start" button press). The acquisition will stop when the user so decides, by pressing "Stop" button. 

Both streamlit and subscribeSOM.py will run on Gitpod, for that a installation file was created (requirements.txt and .gitpod.yml). After installations are finished the script for opening the streamlit webpage and subscriberSOM.py will automatically run. 
Data can be downloaded either by saving the "dataSOM.txt" file in Gitpod's directory or by pressing the button "Download" that will transfer a "dataSOM.csv" file directly into the users computer. 

In the streamlit application the user will be able to acess:
- Real life plot of the acquired signal
- Data visualization: Plots sonogram, frequency domain signal (FFT) and spectrogram. The signal can be filtered with desired low-cut and high-cut frequency and the result will be shown on said graphs.
- Features: visualization of different features related to the rms signal.

The architecture diagram is as follows:
![arquitetura1](https://user-images.githubusercontent.com/117996837/204275646-95c7fa05-f264-41da-8ae5-f16aa4eacea1.png)
