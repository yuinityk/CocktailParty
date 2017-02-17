import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
from scipy.fftpack import fft,ifft
from sklearn.decomposition import FastICA
import os.path

RATE =  8000
components=2

#input mixed voice data --delta--
filenames = [('mixed_delta' + str(i+1) + '.wav') for i in range(components)]
input=[(wav.read(filenames[i])[1]) for i in range(components)]

data_length=(os.path.getsize(filenames[0])-44)/2

S = input[0]
for i in range(components-1):
    S=np.c_[S,input[i+1]]
S = S.astype(np.float64)
S /= S.std(axis = 0)

ica = FastICA(n_components=components)
S_ = ica.fit_transform(S)

#volume up = normalization
S_ = S_/np.max(np.abs(S_))*32767
S_ = S_.astype(np.int16)

#output to wave file
filenames = [('output_delta' + str(i+1) + '.wav') for i in range(components)]
for i in range(components):
    wav.write(filenames[i],RATE,S_[:,i])


#input mixed voice data  --short_exp--
filenames = [('mixed_short_exp' + str(i+1) + '.wav') for i in range(components)]
input=[(wav.read(filenames[i])[1]) for i in range(components)]

data_length=(os.path.getsize(filenames[0])-44)/2

S = input[0]
for i in range(components-1):
    S=np.c_[S,input[i+1]]
S = S.astype(np.float64)
S /= S.std(axis = 0)

ica = FastICA(n_components=components)
S_ = ica.fit_transform(S)


#volume up = normalization
S_ = S_/np.max(np.abs(S_))*32767
S_ = S_.astype(np.int16)

#output to wave file
filenames = [('output_short_exp' + str(i+1) + '.wav') for i in range(components)]
for i in range(components):
    wav.write(filenames[i],RATE,S_[:,i])




#input mixed voice data  --long_exp--
filenames = [('mixed_long_exp' + str(i+1) + '.wav') for i in range(components)]
input=[(wav.read(filenames[i])[1]) for i in range(components)]

data_length=(os.path.getsize(filenames[0])-44)/2

S = input[0]
for i in range(components-1):
    S=np.c_[S,input[i+1]]
S = S.astype(np.float64)
S /= S.std(axis = 0)

ica = FastICA(n_components=components)
S_ = ica.fit_transform(S)


#volume up = normalization
S_ = S_/np.max(np.abs(S_))*32767
S_ = S_.astype(np.int16)

#output to wave file
filenames = [('output_long_exp' + str(i+1) + '.wav') for i in range(components)]
for i in range(components):
    wav.write(filenames[i],RATE,S_[:,i])

