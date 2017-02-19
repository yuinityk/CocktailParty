import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
#from sklearn.decomposition import FastICA
from mypackage import ComplexFastICA
import os.path

RATE =  8000
components=2

#input voice data
input1 = wav.read('input1.wav')[1]
input2 = wav.read('input2.wav')[1]

data_length=os.path.getsize("input1.wav")/2-100
delta1=0
delta2=0
S = np.c_[input1[delta1:delta1+data_length],input2[delta2:delta2+data_length]]
S = S.astype(np.complex64)
S = S * 1.0j
S /= S.std(axis = 0)


ica = ComplexFastICA(n_components=components)
S_ = ica.fit_transform(S)

#casting complex values to real
S_real = np.real(S_)

#volume up = normalization
if np.max(np.abs(S_real))!=0:
    S_real = S_real/np.max(np.abs(S_real))*32767
S_real = S_real.astype(np.int16)


filenames = [('output_real' + str(i+1) + '.wav') for i in range(components)]
for i in range(components):
    wav.write(filenames[i],RATE,S_real[:,i])

#casting complex values to real
S_imag = np.imag(S_)

#volume up = normalization
if np.max(np.abs(S_imag))!=0:
    S_imag = S_imag/np.max(np.abs(S_imag))*32767
S_imag = S_imag.astype(np.int16)


filenames = [('output_imag' + str(i+1) + '.wav') for i in range(components)]
for i in range(components):
    wav.write(filenames[i],RATE,S_imag[:,i])



