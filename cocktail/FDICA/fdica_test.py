import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import os.path
from fdicapy import fdica

RATE =  8000
components=2
frame_length = 512

#input voice data
filenames = [('mixed_delta' + str(i+1) + '.wav') for i in range(components)]
input=[(wav.read(filenames[i])[1]) for i in range(components)]

input = np.array(input)
output = fdica(input, frame_length)

#volume up = normalization
output = output/np.max(np.abs(output))*32767
output = output.astype(np.int16)

filenames = [('output_delta' + str(i+1) + '.wav') for i in range(components)]
for i in range(components):
    wav.write(filenames[i],RATE,output[i])


#input voice data
filenames = [('mixed_short_exp' + str(i+1) + '.wav') for i in range(components)]
input=[(wav.read(filenames[i])[1]) for i in range(components)]

input = np.array(input)
output = fdica(input, frame_length)

#volume up = normalization
output = output/np.max(np.abs(output))*32767
output = output.astype(np.int16)

filenames = [('output_short_exp' + str(i+1) + '.wav') for i in range(components)]
for i in range(components):
    wav.write(filenames[i],RATE,output[i])

