import pyaudio
import struct
import statistics as stats
import numpy
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D as lin
#from drawnow import drawnow

# Constants

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
SPACING = 1/RATE

max_amplitude = 250000
max_frequency = 20000 #was/should be 0.5

# Instance of pyAudio

p = pyaudio.PyAudio()

# Open Stream

stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    output = True,
    frames_per_buffer = CHUNK
    )
    
#-------------------------------------------------------------------#
# Main loop
#-------------------------------------------------------------------#

#Variables for averaging
grouping_size = 8
repetitions = int(CHUNK / grouping_size)

#Variables for other
threshhold = .5
frame_count = 0

def makeFig(x,y):
    plt.plot(x,y)

def frequency(n, sample_rate = RATE, sample_size = CHUNK):
    return(n * sample_rate / sample_size)

#graph setup
line = lin([],[])
fig = plt.figure()
ax = fig.add_subplot(111)
plt.show(block = False)

while stream.is_active():

    disp = ''
    waves = {}
    frame_count += 1
   
    
    # Binary data
    data = stream.read(CHUNK, exception_on_overflow = False)

    # Convert data to integers

    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)

    # Getting rid of every other value

    data_formatted = data_int[:int((len(data_int) / 2) + 1)]

    #Using Fourier Transformation on formatted data
    frequencies = []
    numpy_data = numpy.fft.fft(data_formatted, n = None, axis =-1)

    #-------------------------------------------------------------------#
    #GETTING FREQUENCIES

    #WHEN IN SUBLIME
    for i in range(0, len(numpy_data)):
        frequencies.append(frequency(i))

    #WHEN IN IDLE
    #frequencies = numpy.fft.fftfreq(len(numpy_data), SPACING)

    #-------------------------------------------------------------------#
    #GETTING AMPLITUDES

    amplitudes = abs(numpy_data)
    count = 0
    for i in amplitudes:
        if i > 20000:
            amplitudes = numpy.delete(amplitudes, count)
            frequencies = numpy.delete(frequencies, count)
            count -= 1
        count += 1
    #-------------------------------------------------------------------#

    #Eliminating reflected half of the data
    slyce = slice(1, len(numpy_data) / 2 + 1)
    frequencies = frequencies[slyce]
    amplitudes = amplitudes[slyce]
    #frequencies = frequencies[: int(len(frequencies)/2)]
    #amplitudes = amplitudes[: int(len(amplitudes)/2)]
            
    #Print graph
    #plt.scatter(frequencies[:len(frequencies/2)],amplitudes[len(amplitudes/2)])
    #plt.plot(frequencies,amplitudes)
    line.set_data(frequencies, amplitudes)
    #ax.add_line(line)
    plt.plot(frequencies, amplitudes)
    #drawnow(plt.plot(frequencies, amplitudes))
    #plt.show()
    makeFig(frequencies, amplitudes)
    plt.draw()
    print("plot")
    
    #plt.show()
    #fig.gca().relim()
    #FuncAnimation(fig, update, interval=200)
    #fig.gca().autoscale_view()
    plt.pause(0.0001)
    plt.cla()
    
    
    




    













