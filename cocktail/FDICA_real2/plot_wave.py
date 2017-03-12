import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
from sklearn.decomposition import FastICA

RATE =  44100

mixed1 = wav.read('mixed1.wav')[1]
mixed2 = wav.read('mixed2.wav')[1]
output1 = wav.read('output1.wav')[1]
output2 = wav.read('output2.wav')[1]

plt.subplot(4,1,1)
plt.plot(mixed1)
plt.title('mixed1')
plt.subplot(4,1,2)
plt.plot(mixed2)
plt.title('mixed2')
plt.subplot(4,1,3)
plt.plot(output1)
plt.title('output1')
plt.subplot(4,1,4)
plt.plot(output2)
plt.title('output2')


#plt.subplots_adjust(0.09,0.04,0.94,0.94,0.26,0.46)

plt.show()


