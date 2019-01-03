import pyaudio
import struct
import statistics as stats
import numpy

# Constants

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

max_amplitude = 175000 #was 250000
max_frequency = 20000 #was/should be 0.5

#Graph settings (Elements Per Row, Number of Rows)

EPR = 128 #128
NR = 40

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

def print_graph(graph):
    disp = ''
    for row in range(0, len(graph)):
        #poob = row, ''.join(graph[row])
        #poob = ''.join(graph[row][0 : len(graph[row])/2]), row
        poob = ''.join(graph[row][0 : len(graph[row])]), row
        disp += (str(poob) + '\n')
    print(disp)
    
#-------------------------------------------------------------------#
# Main loop
#-------------------------------------------------------------------#

#Variables for averaging
grouping_size = 4
repetitions = int(CHUNK / grouping_size)

#Variables for other
threshhold = .5
frame_count = 0

while stream.is_active():

    disp = ''
    waves = {}
    frame_count += 1

    graph = [['-' for _ in range(EPR)] for _ in range(NR)]
   
    
    # Binary data
    data = stream.read(CHUNK, exception_on_overflow = False)

    # Convert data to integers

    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)

    # Getting rid of every other value

    data_formatted = data_int[::2]

    #Using Fourier Transformation on formatted data
    
    numpy_data = numpy.fft.fft(data_formatted, n = None, axis =-1)
    numpy_data = numpy_data[0 : len(numpy_data)/2]
    frequencies = numpy.fft.fftfreq(len(numpy_data))
    amplitudes = abs(numpy_data)

    #Numbered dictionary
    freqDict = {}
    for i in frequencies:
        freqDict[i] = amplitudes [i]

    freqDict2 = freqDict

    orderedFrequencies = []
    orderedAmplitudes = []

    for i in range(0, len(freqDict)):
        orderedAmplitudes.append(freqDict[min(freqDict)])
        freqDict.pop(min(freqDict))
        #orderedFrequencies.append(min(freqDict2))
        #freqDict2.pop(min(freqDict2))
        #print(orderedAmplitudes)
    #For loop for constructing graph onto blank template. (AF: Average Frequencies AA: Average Amplitudes)
    inc = 0

    for x in range(1,repetitions/2+1):
        #print(inc,grouping_size + inc)
        #print(orderedAmplitudes[inc : inc+grouping_size])
        #AA =  stats.mean(orderedAmplitudes[inc : inc + grouping_size])
        #print(AA)
        #inc = x * grouping_size
        #inc = inc + grouping_size
        x = x - 1
        for i in range(1, NR+1):
            AA =  stats.mean(orderedAmplitudes[inc : inc + grouping_size])
            inc = inc + grouping_size
            i = i - 1
            if AA/10000 <= (((max_amplitude/1000) / NR) * i):
                graph[i][x] = '#'
                #print(AA, max_amplitude/100*i)

            
    #Print graph (once per frame)
    print_graph(graph)


    
    
    




    













