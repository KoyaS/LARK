import pyaudio
import struct
import statistics as stats
import numpy
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D as lin
import time as t

#CONSTANTS
CHUNK = 1024                   
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
THRESHOLD = 2e9

# Instance of pyAudio
p = pyaudio.PyAudio()

#Functions
def makeFig(x,y):
    plt.plot(x,y)

def frequency(n, sample_rate = RATE, sample_size = CHUNK):
    return(n * sample_rate / sample_size)

#Graph setup
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

slyce = numpy.arange(1, CHUNK/2+1)

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
    numpy_data = numpy.fft.fft(data_int)

    #-------------------------------------------------------------------#
    #GETTING FREQUENCIES
    frequencies = numpy.fft.fftfreq(len(numpy_data), 1.0 / RATE)
    for i in range(0,len(frequencies)):
        frequencies[i] *= 2
    #-------------------------------------------------------------------#
    #Power Spectral Density/slicing
    psd = abs(numpy_data[slyce]**2) + abs(numpy_data[-slyce]**2)
    realSlyce = numpy.where(psd>THRESHOLD)
    #-------------------------------------------------------------------#
    #Drawing plot
    line.set_data(frequencies[slyce], psd)
    plt.plot(frequencies[slyce], psd)
    makeFig(frequencies[slyce], psd)
    plt.ylim(top = 8e9)
    plt.draw()

    plt.axhline(y = THRESHOLD, linewidth=1, color='r')

    #-------------------------------------------------------------------#
    #Time Based Calculations

    timeElapsed = t.time() - startTime
    frame_count += 1
    fps = frame_count/timeElapsed

    mainFRQ = []
    for i in slyce[realSlyce].tolist():
        mainFRQ.append(frequencies[i])
        #plt.axvline(x = i, linewidth = 1, color = 'b')

    plt.pause(0.00000001)
    plt.cla()

    print("-------------------------------------------------------------------")
    print("FPS: " + str(fps))
    print(mainFRQ)
    
    