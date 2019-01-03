import pyaudio
import struct
import statistics as stats

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
grouping_size = 32
repetitions = CHUNK / grouping_size

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

    # Devides data into sets of 32, averages each set, and then adds '-' or '*'
    # based on if average is over threshold or not

    inc = 0
    for x in range(1,repetitions):
        if stats.mean(data_formatted[inc : x*grouping_size]) >= threshhold:
            disp += '*'
        else:
            disp += '-'
        inc = x*grouping_size
        
    print(disp + ' | ' + str(frame_count))
    #print(data_formatted)














