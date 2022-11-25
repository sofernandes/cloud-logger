import time  # to simulate a real time data, time loop
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import streamlit as st  # data web app development
import matplotlib.pyplot as plt
from pathlib import Path 
from scipy.signal import butter, lfilter
import paho.mqtt.client as mqtt 
import librosa
import librosa.display
import sklearn
from numpy.fft import fft


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter(order, [lowcut, highcut], fs=fs, btype='band')
    y = lfilter(b, a, data)
    return y


def plot_senogram(y):
    fig, ax = plt.subplots(figsize=(14, 4)) 
    st.write('Sonogram plot')
    ax.set_xlabel("Time /s")
    ax.set_ylabel("Data")
    ax.set_title("Sonogram plot", fontsize = 15)
    ax.plot(y)
    plt.show()
    st.pyplot(fig) 


def plot_fft(y, fs):
    st.write('Frequency Domain plot')
    #plot FFT
    X = fft(y)
    N = len(X)
    n = np.arange(N)
    T = N/fs
    freq = n/T 
    # Get the one-sided specturm
    n_oneside = N//2
    # get the one side frequency
    f_oneside = freq[:n_oneside]
    
    fig, ax = plt.subplots(figsize=(14, 4)) 
    plt.plot(f_oneside, np.abs(X[:n_oneside]), 'b')
    plt.xlabel('Freq /Hz')
    plt.ylabel('FFT Amplitude')
    ax.set_title("Fourier transform plot", fontsize = 15)
    plt.show()
    st.pyplot(fig)
    
def plot_spetrogram(y,fs):
    st.write('Spectrogram plot')
    fig, ax = plt.subplots(1, figsize=(14, 8))
    fig.tight_layout(pad=10.0)
    ax.specgram(y, Fs=fs)
    ax.set_xlabel(xlabel='Time /sec')
    ax.set_ylabel(ylabel='Frequency Amplitude / rad/s')
    helper = [0, 2500, 5000, 7500, 10000, 12500, 15000, 17500, 20000]
    spec_yticks = [6.28 * i for i in helper]
    ax.set_yticks(helper)
    ax.set_yticklabels(spec_yticks)
    ax.set_title("Signal Spectrogram", fontsize = 15)
    st.pyplot(fig)


st.set_page_config(
 page_title='Audio Visualization',
 layout="centered",
 initial_sidebar_state="auto",
)

def publish_status():
    client.publish("Status", st.session_state["start"])
 
    
 
mqttBroker ="test.mosquitto.org" 
client = mqtt.Client("soundcloud")
client.connect(mqttBroker, port=1883) 
fs = 44100

#read txt from a URL
def get_data():
    with open("/workspace/cloud-logger/dadosSOM.txt","r") as f:
    #with open("dadosSOM.txt","r") as f:
        last_line = f.readlines()[-1]
        return float(last_line[:-1])


st.markdown("<h1 style='text-align: center; color: white; padding:20px'>Sound Aquisition Logger</h1>", unsafe_allow_html=True)
st.write('___')

start = st.button("Start Aquisition")
if start:
    st.session_state['start'] = True
    publish_status()    



my_file = Path("/workspace/cloud-logger/dadosSOM.txt")
#my_file = Path("dadosSOM.txt")
if my_file.is_file() and 'start' in st.session_state: #if file exists
    
    with st.sidebar:
        if 'start' in st.session_state and st.session_state["start"] == True:
            st.success("Running")
        else:
            st.error("Stopped")  
        st.write('___')

    col1,col11, col12, col13, col14, col2 = st.columns(6)
        
    with col1:
        if st.button('Stop'):
            st.session_state['start'] = False
            publish_status()
    with col2:
        rst = st.button('Reset')




    radio = st.sidebar.radio("Choose method",("Real-time Plot", "Data visualization","Features"))
        
    
    with st.sidebar:
        st.write('___')
        if 'data' in st.session_state:    
            csv = st.session_state['data'].to_csv(index=False).encode('utf-8')
        
        save = st.download_button( label="Download", data = csv, file_name="dataSOM.csv"  )

    if rst: 
        del st.session_state['data']
        del st.session_state['start']
        st.warning("Data was deleted!")
       # seconds = 0
    
    if save:
        if 'data' not in st.session_state:
            st.write("Please generate data")
        else:
            with st.sidebar:
                with st.spinner('Saving...'):
                        time.sleep(0.5)
                        
                        st.success("Done!")
            
        
    if radio == "Real-time Plot" and 'start' in st.session_state:
        # Initialization
        if 'data' not in st.session_state and st.session_state['start'] == True:
            seconds = 0
            df = pd.DataFrame({"data": []})
            plot = st.line_chart(data=None,width=15, height=5)
               
            while st.session_state['start'] == True:
                point = pd.DataFrame({"data": [get_data()]})
                
                plot.add_rows(point)
                
                df = df.append(point,ignore_index = True)
                
                time.sleep(0.1)
                seconds += 0.1
        
                st.session_state['data'] = df
        else:
            st.line_chart(st.session_state['data'])
            
        
        is_check = st.checkbox("Display Data")
        if is_check:
            st.write(st.session_state['data'].T)
        
    
    if radio == "Data visualization" and 'start' in st.session_state:
        st.write('___')
        st.write("Filter data by choosing low-cut and high-cut frequency")
        #get filter parameters
        my_expander = st.expander('Band Pass filter')
        my_expander.write('Choose low-cut and high-cut frequencies:')
        lowcut = my_expander.slider("Low-cut frequency", 0.01, 22049.9, 0.01)
        highcut = my_expander.slider("High-cut frequency", 0.01, 22049.9, 22049.9)
        
    
        #choose what to plot, by default it plots sonogram
        show = st.multiselect("Select plot", ['Sonogram','Spectrogram','Frequency Domain'], ['Sonogram'])

        y = butter_bandpass_filter(st.session_state['data']['data'], lowcut, highcut, fs)
        
        if len(show) == 1:
            if show[0] == 'Sonogram':
                 plot_senogram(y)
            
            if show[0] == 'Spectrogram':
                plot_spetrogram(y, fs)
                
            if show[0] == 'Frequency Domain':
                plot_fft(y, fs)
        
        if len(show) == 2:
            if 'Sonogram' in show and 'Spectrogram' in show:
                 plot_senogram(y)
                 plot_spetrogram(y, fs)
                 
            if 'Sonogram' in show and 'Frequency Domain' in show:
                plot_senogram(y)
                plot_fft(y, fs)   
                
            if 'Spectrogram' in show and 'Frequency Domain' in show:
                plot_spetrogram(y, fs)
                plot_fft(y, fs)   
            
        if len(show) == 3:
            plot_senogram(y)
            plot_fft(y, fs) 
            plot_spetrogram(y, fs)

        
    
    if radio == "Features" and 'start' in st.session_state:
        y = st.session_state['data']['data'].to_numpy()
        
        st.header("Feature extraction")
        
        st.subheader("Time domain")
        
        col1, col2 = st.columns([1,1])
        with col1:
            #amplitude envelope
            y_harmonic, y_percussive = librosa.effects.hpss(y)
            st.write("Componente harmónica")
            fig, ax = plt.subplots(figsize=(10, 6)) 
            ax.set_xlabel("Time /s")
            ax.set_ylabel("Amplitude")
            ax.plot(y_harmonic)
            st.pyplot(fig)
        
        with col2:
            st.write("Componente Percurssiva")
            fig, ax = plt.subplots(figsize=(10, 6)) 
            ax.set_xlabel("Time /s")
            ax.set_ylabel("Amplitude")
            ax.plot(y_percussive)
            st.pyplot(fig)
        
        #root mean square energy
        
        
        
        #zero-crossing rate
    
        
        
        st.subheader('Time-frequency domain')

        #spectral centroid
        st.write("Spectral Centroid")
        spectral_centroids = librosa.feature.spectral_centroid(y, sr=fs)[0]
        fig, ax = plt.subplots(figsize=(14, 4)) 
        frames = range(len(spectral_centroids))
        t = librosa.frames_to_time(frames)
        # Normalising the spectral centroid for visualisation
        def normalize(y, axis=0):
            return sklearn.preprocessing.minmax_scale(y, axis=axis)
        #Plotting the Spectral Centroid along the waveform
        librosa.display.waveshow(y, sr=fs, alpha=0.4)
        ax.plot(t, normalize(spectral_centroids), color='b')
        st.pyplot(fig)
    
        #chromagram
        st.write("Chromagram")
        chroma = librosa.feature.chroma_cqt(y=y, sr=fs)
        fig, ax = plt.subplots(figsize=(14, 4)) 
        img = librosa.display.specshow(chroma, y_axis='chroma', x_axis='time', ax=ax)
        ax.set(title='Chromagram')
        fig.colorbar(img, ax=ax)
        st.pyplot(fig)
                    
else:
    st.info("Please generate a new file")
    with st.sidebar:
        st.title("About")
        st.info('This project was created as a data logger for recorded sounds that allows real-time visualization, analysis of the signal/features and to save the information to a file. All the source code can be found in https://github.com/sofernandes/cloud-logger')
