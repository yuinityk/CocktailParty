import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
from sklearn.decomposition import FastICA

RATE =  44100
np.random.seed(0)

#input voice data
input1 = wav.read('input1.wav')[1]
input2 = wav.read('input2.wav')[1]
input3 = wav.read('input3.wav')[1]

S = np.c_[input1[0:430000],input2[0:430000],input3[0:430000]]
S = S.astype(np.float64)
S /= S.std(axis = 0)

#mix matrix
A=np.array([[1.0,0.7,-0.3],[0.7,-0.3,1.0],[-0.3,1.0,0.7]])
#mixed voice data
S=np.dot(S,A.T)


ica = FastICA(n_components=3)
S_ = ica.fit_transform(S)



#volume up = normalization
S = S/np.max(np.abs(S))*32767
S = S.astype(np.int16)

names = ['mix1', 'mix2', 'mix3']

filenames = [(names[i] + '.wav') for i in range(3)]
for i in range(3):
    wav.write(filenames[i],RATE,S[:,i])


#volume up = normalization
S_ = S_/np.max(np.abs(S_))*32767
S_ = S_.astype(np.int16)


names = ['output1', 'output2', 'output3']

filenames = [(names[i] + '.wav') for i in range(3)]
for i in range(3):
    wav.write(filenames[i],RATE,S_[:,i])

