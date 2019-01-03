import pyaudio
import struct
import statistics as stats
import numpy
import random

# Constants

CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

max_amplitude = 250000
max_frequency = 0.5

#Graph settings (Elements Per Row, Number of Rows)

EPR = 128
NR = 10

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

#Functions

def blank_graph(elements_per_row, rows):
    
    blank_row = ['-'] * elements_per_row
    graph = [blank_row] * rows
    return graph

def print_graph(graph):
    
    for row in range(0, len(graph)):
        print(''.join(graph[row]))
tan = 0
poob = 0
#-------------------------------------------------------------------#
# Main loop
#-------------------------------------------------------------------#

#Variables for averaging
grouping_size = 8
repetitions = int((CHUNK / grouping_size)/2)

#Variables for other
threshhold = .5
frame_count = 0

while stream.is_active():

    disp = ''
    waves = {}
    frame_count += 1

    graph = blank_graph(EPR, NR)
    
    # Binary data
    data = stream.read(CHUNK)

    # Convert data to integers

    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)

    # Getting rid of every other value

    data_formatted = data_int[::2]

    #Using Fourier Transformation on formatted data
    
    numpy_data = numpy.fft.fft(data_formatted, n = None, axis =-1)
    frequencies = numpy.fft.fftfreq(len(numpy_data))
    amplitudes = abs(numpy_data)

    tan = 0    

    if max(amplitudes) > tan:
        tan = '-' * int(max(amplitudes)/5000) + '#'
    print(tan)
                   
    
    inc = 0

    #Creating dictionary to be ordered
    specc = {}
    
    #for x in range(1, repetitions)

        #specc += { frequencies[x] : amplitudes[x] }
        #specc[stats.mean(frequencies[inc : x*grouping_size])] = stats.mean(amplitudes[inc : x*grouping_size])

    #For loop for constructing graph onto blank template. (AF: Average Frequencies AA: Average Amplitudes)

##    for x in range(1,repetitions):
##        AF = stats.mean(frequencies[inc : x*grouping_size])
##        AA = stats.mean(amplitudes[inc : x*grouping_size])
##        inc += 1
##
##        for i in range(1, NR):
##            print(repetitions)
##            #250,000 / 10 = 25,000
##            if AA <= (max_amplitude / NR) * i:
##                graph[i][x] = '#'
        
    #Various print statements (Output)

    
    #print(rand)
    #print(len(numpy_data))
    #print(disp + ' | ' + str(frame_count))
    #print(data_formatted)
    #print(str(numpy_data) + ' | ' + str(frame_count))
    #print(str(numpy_data[rand]) + ' | ' + str(data_formatted[0]) + ' | ' + str(frame_count))
    #print(specc)
    #print_graph(graph)


    #Leave to tell the different cycles
    #print('--------------------------------------------')
    
    
    




    














