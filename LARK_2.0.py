import pyaudio
import struct
import statistics as stats
import numpy
import random

# Constants

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

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

# Declaring variables for the main loop

threshhold = 125
frame_count = 0

# Setting counting variables for averaging
grouping_size = 8

# Main loop

while stream.is_active():

    disp = ''
    frame_count += 1
    
    # Binary data
    data = stream.read(CHUNK)

    # Convert data to integers

    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)

    # Getting rid of every other value

    data_formatted = data_int[::2]

    #Using Fourier Transformation on formatted data
    
    numpy_data = numpy.fft.fft(data_formatted, n = None, axis =-1)
    #numpy_data_real = numpy_data.real
    #numpy_data_imag = numpy_data.imag

##--------------WRONG------------------------------------------------##

##    #Creating a dictionary of x and y values for spectrogram
##    speccX = []
##    speccY = []
##    specc_filthy = {}
##
##    for x in range(0,len(numpy_data)):
##        specc_filthy.update({numpy_data[x].real : numpy_data[x].imag})
##        print(specc_filthy)
##    specc_sortedX = sorted(specc_filthy)
##    
##    for x in range(0,len(numpy_data)):
##        speccX.append(specc_sortedX[x])
##        speccY.append(specc_filthy[speccX[x]])
##        print(x)
##
##    print(speccX)
##    print('------------------')
##    print(speccY)
    
    #Variable for averaging
    repetitions = len(numpy_data-1) / grouping_size
    
    # Devides data into sets of 32, averages each set, and then adds '-' or '*'
    # based on if average is over threshold or not

    inc = 0
##    for x in range(1,repetitions):
##        
##        if stats.mean(numpy_data[inc : x*grouping_size]) <= threshhold:
##            disp += '*'
##        else:
##            disp += '-'
##        inc = x*grouping_size

    #rand = random.randint(1,512)

    #Various print statements (Output)
    
    #print(rand)
    #print(len(numpy_data))
    #print(disp + ' | ' + str(frame_count))
    #print(data_formatted)
    #print(str(numpy_data) + ' | ' + str(frame_count))
    #print(str(numpy_data[rand]) + ' | ' + str(data_formatted[0]) + ' | ' + str(frame_count))
    #print(specc)
    print(numpy_data)




    














