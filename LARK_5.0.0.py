import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D as lin
import time as t
from scipy.signal import argrelextrema
#This program listens and creates a spectrogram with matplotlib
#CONSTANTS
CHUNK = 1024                   
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

#ADJUST SETTINGS
#-------------------------------------------------------------------#
THRESHOLD = 2e9
PLOT = True
LOG = True
#Y
YMIN = 0
YMAX = 8e9
#X
XMIN = 42
XMAX = 2e4
#-------------------------------------------------------------------#

# Instance of pyAudio
p = pyaudio.PyAudio()

#Functions
def makeFig(x,y):
    plt.plot(x,y)

def frequency(n, sample_rate = RATE, sample_size = CHUNK):
    return(n * sample_rate / sample_size)

#Graph setup
if PLOT:
    line = lin([],[])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.show(block = False)

#-------------------------------------------------------------------#
# Main loop
#-------------------------------------------------------------------#

fps = 1
frame_count = 0
startTime = t.time()

slyce = np.arange(1, CHUNK/2+1)

# Open Stream
stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    output = False,
    frames_per_buffer = CHUNK
    )

while stream.is_active():
    
    #-------------------------------------------------------------------#
    # Cleansing Audio Stream

    data = stream.read(CHUNK, exception_on_overflow = False)

    # Convert data to integers
    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)

    #Using Fourier Transformation on formatted data
    frequencies = []
    np_data = np.fft.fft(data_int)

    #-------------------------------------------------------------------#
    #GETTING FREQUENCIES
    frequencies = np.fft.fftfreq(len(np_data), 1.0 / RATE)
    for i in range(0,len(frequencies)):
        frequencies[i] *= 2
    #-------------------------------------------------------------------#
    #Power Spectral Density/slicing
    psd = abs(np_data[slyce]**2) + abs(np_data[-slyce]**2)
    realSlyce = np.where(psd>THRESHOLD)
    #-------------------------------------------------------------------#
    #Drawing plot
    if PLOT:
        line.set_data(frequencies[slyce], psd)
        plt.plot(frequencies[slyce], psd)
        makeFig(frequencies[slyce], psd)

        plt.ylim(bottom = YMIN, top = YMAX)
        plt.xlim(left = XMIN, right = XMAX)

        if LOG:
            ax.set_xscale('log')

        plt.draw()


        plt.axhline(y = THRESHOLD, linewidth=1, color='r', label = "Threshold: " + str(THRESHOLD))
        plt.legend(loc = 'best')

    #-------------------------------------------------------------------#
    #Time Based Calculations

    timeElapsed = t.time() - startTime
    frame_count += 1
    fps = frame_count/timeElapsed

    mainFRQ = []

    localMax = argrelextrema(psd, np.greater)
    for i in localMax:
        mainFRQ.append(frequencies[i])

    for i in slyce[realSlyce].tolist():
        mainFRQ.append(frequencies[i])
        #plt.axvline(x = i, linewidth = 1, color = 'b')
        
    if PLOT:
        plt.pause(0.0001)
        plt.cla()

    print("-------------------------------------------------------------------")
    print(mainFRQ)
    print("FPS: " + str(fps))
    
    