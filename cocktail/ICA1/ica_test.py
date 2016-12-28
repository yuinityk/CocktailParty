import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
from sklearn.decomposition import FastICA

RATE =  44100

mix1 = wav.read('mix5_1.wav')[1]
mix2 = wav.read('mix5_2.wav')[1]
mix3 = wav.read('mix5_3.wav')[1]
mix4 = wav.read('mix5_4.wav')[1]
mix5 = wav.read('mix5_5.wav')[1]

plt.subplot(5,1,1)
plt.plot(mix1)
plt.title('mix1')
plt.subplot(5,1,2)
plt.plot(mix2)
plt.title('mix2')
plt.subplot(5,1,3)
plt.plot(mix3)
plt.title('mix3')
plt.subplot(5,1,4)
plt.plot(mix4)
plt.title('mix4')
plt.subplot(5,1,5)
plt.plot(mix5)
plt.title('mix5')

plt.subplots_adjust(0.09,0.04,0.94,0.94,0.26,0.46)

#plt.show()

S = np.c_[mix1,mix2,mix3,mix4,mix5]
S = S.astype(np.float64)
S /= S.std(axis = 0)

ica = FastICA(n_components=5)
S_ = ica.fit_transform(S)
plt.figure()
names = ['sep1', 'sep2', 'sep3', 'sep4', 'sep5']

for i in range(5):
    plt.subplot(5, 1, i+1)
    plt.title(names[i])
    plt.plot(S_[:,i])

plt.subplots_adjust(0.09,0.04,0.94,0.94,0.26,0.46)
#plt.show()

filenames = [(names[i] + '.wav') for i in range(5)]
for i in range(5):
    wav.write(filenames[i],RATE,S_[:,i])
