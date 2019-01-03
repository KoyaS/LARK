import pyaudio
import struct
import statistics as stats
import numpy

#Aproximate FPS: 40

# Constants

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

max_amplitude = 250000
max_frequency = 20000# was/should be 0.5?

VIB = 5
WEIGHT = 10000.0

#Graph settings (Elements Per Row, Number of Rows)

EPR = 128
NR = 20

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
        poob = row, ''.join(graph[row])
        disp += (str(poob) + '\n')
    print(disp)
    
#-------------------------------------------------------------------#
# Main loop
#-------------------------------------------------------------------#

#Variables for averaging
grouping_size = 8
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
    data = stream.read(CHUNK)

    # Convert data to integers

    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)

    # Getting rid of every other value

    data_formatted = data_int[::2]

    #-------------------------------------------------------------------#
    #Fourier Transform
    #-------------------------------------------------------------------#
    
    numpy_data = numpy.fft.fft(data_formatted, n = None, axis =-1)
    amplitudes = abs(numpy_data)

    #Frequencies
    n = len(numpy_data)
    d = 1.0/RATE
    frequencies = numpy.fft.fftfreq(n,d)

    #For loop for generating weighted frequencies

    count = 0
    weightedFrequencies = []
    FWF = []
    AWA = []

    #Repeats for number of Haptic Modules
    for x in range(0, VIB):

        x+=1
        frq = frequencies[count : (len(frequencies)/VIB)*x]

        #Loop which applies weight to each frequency
        for y in range(0,len(frq)):

            fr = frq[y]
            weight = amplitudes[y] / WEIGHT 
            holder = fr * (1.0 + weight)
            weightedFrequencies.append(holder)

        if len(weightedFrequencies) >= 1:

            averageWeightedFrequency = [stats.mean(weightedFrequencies[ : len(weightedFrequencies)])]
            averageAmplitude = [stats.mean(numpy.ndarray.tolist(amplitudes)[ : len(amplitudes)])]
            AWA += averageAmplitude
            FWF += averageWeightedFrequency
            count = (len(frequencies)/VIB * x)

    weightedFrequencies = []
    averageAmplitude = []
                            

    #Print Frequency values (once per frame)
    for x in range(0,len(FWF)):
        print(FWF[x],AWA)


    FWF = []
    AWA = []

    print("----------------------------------------")

    
    
    




    













