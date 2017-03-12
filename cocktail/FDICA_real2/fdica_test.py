import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import os.path
from fdicapy import fdica

RATE =  44100
components=2
frame_length = 1024

#input voice data
filenames = [('mixed' + str(i+1) + '.wav') for i in range(components)]
length_array = [(os.path.getsize(filenames[i])-44)/2 for i in range(components)]
data_length = min(length_array)
input = np.zeros([components,data_length])

for i in range(components):
    input[i] = wav.read(filenames[i])[1][0:data_length]

output = fdica(input, frame_length)


#volume up = normalization
output = output/np.max(np.abs(output[:,0:data_length-RATE]))*32767
output = output.astype(np.int16)

filenames = [('output' + str(i+1) + '.wav') for i in range(components)]
for i in range(components):
    wav.write(filenames[i],RATE,output[i][0:data_length-RATE])


