import numpy as np
import scipy.io.wavfile as wav
import os.path

#sampling rate
RATE=8000
#number of data
components = 2

#original data
filenames = [('input' + str(i+1) + '.wav') for i in range(components)]
input=[(wav.read(filenames[i])[1]) for i in range(components)]

#finite impulse reactions   ---delta---
impulse_length=64
impulse=np.array([[np.zeros(impulse_length),np.zeros(impulse_length)],[np.zeros(impulse_length),np.zeros(impulse_length)]])

impulse[0,0][0]=1.0
impulse[0,1][0]=0.5
impulse[1,0][0]=0.5
impulse[1,1][0]=1.0

#output mixed data to wave file
data_length=(os.path.getsize(filenames[0])-44)/2
filenames = [('mixed_delta' + str(i+1) + '.wav') for i in range(components)]
for i in range(components):
    output_data=np.zeros(data_length)
    for j in range(components):
        output_data += np.convolve(input[j],impulse[i,j],mode='full')[0:data_length]
    output_data=output_data/np.max(np.abs(output_data))*32767
    output_data=output_data.astype(np.int16)
    wav.write(filenames[i],RATE,output_data)



#finite impulse reactions   ---short_exp---
CYCLE=1.0/RATE
impulse_length=32
impulse=np.array([[np.zeros(impulse_length),np.zeros(impulse_length)],[np.zeros(impulse_length),np.zeros(impulse_length)]])

_time=np.arange(0,CYCLE*impulse_length,impulse_length)
_exp=np.exp(_time/(-1.*CYCLE*impulse_length/64))

impulse[0,0][4:impulse_length]=1.0*_exp[0:impulse_length-4]
impulse[0,1][8:impulse_length]=0.5*_exp[0:impulse_length-8]
impulse[1,0][8:impulse_length]=0.5*_exp[0:impulse_length-8]
impulse[1,1][4:impulse_length]=1.0*_exp[0:impulse_length-4]

#output mixed data to wave file
data_length=(os.path.getsize(filenames[0])-44)/2
filenames = [('mixed_short_exp' + str(i+1) + '.wav') for i in range(components)]
for i in range(components):
    output_data=np.zeros(data_length)
    for j in range(components):
        output_data += np.convolve(input[j],impulse[i,j],mode='full')[0:data_length]
    output_data=output_data/np.max(np.abs(output_data))*32767
    output_data=output_data.astype(np.int16)
    wav.write(filenames[i],RATE,output_data)


#finite impulse reactions   ---long_exp---
CYCLE=1.0/RATE
impulse_length=256
impulse=np.array([[np.zeros(impulse_length),np.zeros(impulse_length)],[np.zeros(impulse_length),np.zeros(impulse_length)]])

_time=np.arange(0,CYCLE*impulse_length,impulse_length)
_exp=np.exp(_time/(-1.*CYCLE*impulse_length/64))

impulse[0,0][4:impulse_length]=1.0*_exp[0:impulse_length-4]
impulse[0,1][8:impulse_length]=0.5*_exp[0:impulse_length-8]
impulse[1,0][8:impulse_length]=0.5*_exp[0:impulse_length-8]
impulse[1,1][4:impulse_length]=1.0*_exp[0:impulse_length-4]

#output mixed data to wave file
data_length=(os.path.getsize(filenames[0])-44)/2
filenames = [('mixed_long_exp' + str(i+1) + '.wav') for i in range(components)]
for i in range(components):
    output_data=np.zeros(data_length)
    for j in range(components):
        output_data += np.convolve(input[j],impulse[i,j],mode='full')[0:data_length]
    output_data=output_data/np.max(np.abs(output_data))*32767
    output_data=output_data.astype(np.int16)
    wav.write(filenames[i],RATE,output_data)

