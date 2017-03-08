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

data_length=os.path.getsize("input1.wav")/2-44
S = np.c_[input1[0:data_length],input2[0:data_length]]
S = S.astype(np.complex64)

#mix matrix
A=np.array([[1.0+2.j,0.6+0.1j],[0.6-0.1j,1.0-3.j]])
#mixed voice data
S=np.dot(S,A.T)
S /= S.std(axis = 0)


ica = ComplexFastICA(n_components=components)
S_ = ica.fit_transform(S)
KW = ica.components_
A_ = ica.mixing_

PD = np.dot(KW,A)

#print KW

#volume up = normalization
S_ = S_/(np.max(np.abs(S_))) * 32767

#casting complex values to real
S_real = np.real(S_)
S_real = S_real.astype(np.int16)

filenames = [('output_real' + str(i+1) + '.wav') for i in range(components)]
for i in range(components):
    wav.write(filenames[i],RATE,S_real[:,i])


#casting complex values to real
S_imag = np.imag(S_)
S_imag = S_imag.astype(np.int16)

filenames = [('output_imag' + str(i+1) + '.wav') for i in range(components)]
for i in range(components):
    wav.write(filenames[i],RATE,S_imag[:,i])

