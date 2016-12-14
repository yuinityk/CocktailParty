import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
from sklearn.decomposition import FastICA

RATE =  44100
np.random.seed(0)

mix1 = wav.read('input1.wav')[1]
mix2 = wav.read('input2.wav')[1]
mix3 = wav.read('input3.wav')[1]
mix4 = wav.read('input4.wav')[1]

S = np.c_[mix1[0:430000],mix2[0:430000],mix3[0:430000],mix4[0:430000]]
S = S.astype(np.float64)
S += 5000*np.random.normal(size=S.shape)
S /= S.std(axis = 0)

A=np.array([[1.0,1.0,1.0,-0.5],[1.0,1.0,-1.0,0.5],[1.0,-1.0,1.0,0.5]])
S=np.dot(S,A.T)

names = ['mix4_1', 'mix4_2', 'mix4_3']

filenames = [(names[i] + '.wav') for i in range(3)]
for i in range(3):
    wav.write(filenames[i],RATE,S[:,i])

ica = FastICA(n_components=3)
S_ = ica.fit_transform(S)
S_100 = S_ * 300


names = ['output1', 'output2', 'output3']

filenames = [(names[i] + '.wav') for i in range(3)]
for i in range(3):
    wav.write(filenames[i],RATE,S_[:,i])

filenames = [(names[i] + '_100.wav') for i in range(3)]
for i in range(3):
    wav.write(filenames[i],RATE,S_100[:,i])

