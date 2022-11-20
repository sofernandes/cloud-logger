import time  # to simulate a real time data, time loop
from streamlit_autorefresh import st_autorefresh

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import streamlit as st  # 🎈 data web app development
import matplotlib.pyplot as plt
from pathlib import Path 
from scipy.fft import rfft, rfftfreq
import math
import librosa 
from scipy.signal import butter, lfilter

def butter_bandpass(lowcut, highcut, fs, order=5):
    return butter(order, [lowcut, highcut], fs=fs, btype='band')

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def plot_senogram(data, lowcut, highcut):
    st.write('Sonogram plot')
    ax.set_xlabel("Time /s")
    ax.set_ylabel("Data")
    fs = 44100
    y = butter_bandpass_filter(data, lowcut, highcut, fs)
    ax.plot(y)
    plt.show()
    st.pyplot(fig) 

st.set_page_config(
 page_title='Audio Visualization',
 layout="centered",
 initial_sidebar_state="auto",
)


#read csv from a URL
def get_data():
    with open("dados.txt","r") as f:
        last_line = f.readlines()[-1]
        return float(last_line[:-1])

st.markdown("#### Microphone aquisition Cloud Logger")

start = st.button("Start Aquisition")
if start:
    st.session_state['start'] = True

my_file = Path("dados.txt")
if my_file.is_file() and 'start' in st.session_state: #if file exists
    
    with st.sidebar:
        if 'start' in st.session_state and st.session_state["start"] == True:
            st.success("Running")
        else:
            st.error("Stopped")        

    col1, col2, col3, col4 = st.columns([1,1,1,2])
    with col2:
        if st.button('Stop'):
            st.session_state['start'] = False
    with col3:
        rst = st.button('Reset')
    with col4:
        dwl = st.button('Download File')

    radio = st.sidebar.radio("Choose method",("Real-time Plot", "Data visualization","Features"))
        

    if rst: 
        del st.session_state['data']
        del st.session_state['start']
       # seconds = 0
    
    if dwl:
        with st.spinner('Saving...'):
                time.sleep(0.5)
                np.savetxt(r'C:/Users/Susana/Downloads/data.txt', st.session_state['data'].values, fmt='%f', delimiter='\t')
                st.success("Done!")
        
        
    if radio == "Real-time Plot" and 'start' in st.session_state:
        # Initialization
        if 'data' not in st.session_state and st.session_state['start'] == True:
            seconds = 0
        
            df = pd.DataFrame({"data": []})
            width = st.sidebar.slider("Plot width", 1, 20, 15)
            height = st.sidebar.slider("Plot height", 1, 10, 5)
            plot = st.line_chart(data=None,width=width,height=height)
               
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
         
        #get filter parameters
        my_expander = st.expander('Band Pass filter')
        my_expander.write('Choose low-cut and high-cut frequencies:')
        lowcut = my_expander.slider("Low-cut frequency", 0.01, 20000.0, 0.01)
        highcut = my_expander.slider("High-cut frequency", 0.01, 20000.0, 20000.0)
        
    
        #choose what to plot, by default it plots sonogram
        show = st.multiselect("Select plot", ['Sonogram','Time Domain','Frequency Domain'], ['Sonogram'])
        
        width = st.sidebar.slider("Plot width", 1, 20, 15)
        height = st.sidebar.slider("Plot height", 1, 10, 5)
        
  
        fig, ax = plt.subplots(figsize=(width, height)) 
        plt.subplots(figsize=(width, height)) 
        
        if len(show) == 1:
            if show[0] == 'Sonogram':
                 plot_senogram(st.session_state['data'], lowcut, highcut)
            
            if show[0] == 'Time Domain':
                st.write('Time Domain plot')
                
            if show[0] == 'Frequency Domain':
                st.write('Frequency Domain plot')
        
        
        if len(show) == 2:
            if 'Sonogram' in show and 'Time Domain' in show:
                 plot_senogram(st.session_state['data'], lowcut, highcut)
                 
                 st.write('Time Domain plot')
                 
            if 'Sonogram' in show and 'Frequency Domain' in show:
                plot_senogram(st.session_state['data'], lowcut, highcut)
                  
                st.write('Frequency Domain plot')     
                
            if 'Time Domain' in show and 'Frequency Domain' in show:
                st.write('Time Domain plot')
                   
                st.write('Frequency Domain plot')     
      
            
        if len(show) == 3:
            plot_senogram(st.session_state['data'], lowcut, highcut)
            
            st.write('Time Domain plot')
             
            st.write('Frequency Domain plot')

        
    
    if radio == "Features" and 'start' in st.session_state:
        st.header("Feature extraction")
        st.subheader("Time domain")
        #amplitude envelope
        
        #root mean square energy
        
        #zero-crossing rate
        
        st.subheader('Frequency domain')
        
        st.subheader('Time-frequency domain')
        #spectrogram
        
        #Spectral centroid
     
        #chroma energy
    
    
else:
    st.write("Please generate a new file")