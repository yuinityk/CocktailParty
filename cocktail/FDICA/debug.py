import numpy as np
from fdicapy.fdica_ import _multiple_stft
from fdicapy.stft_ import stft
from scipy.fftpack import fft

x=np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
impulse = np.zeros([2,20])
impulse[0,0] = 1.0
impulse[1,1] = 1.0
y=np.zeros([2,20])
            
y[0]=np.convolve(x,impulse[0],'full')[0:20]
y[1]=np.convolve(x,impulse[1],'full')[0:20]

#xx=stft(x,10)
xx=fft(x)
h0=fft(impulse[0])
h1=fft(impulse[1])

yy=_multiple_stft(y,10)
yy1=fft(y[1])

#print xx
#print h0
#print h1

#print np.exp(-2.0j*np.pi*1.0/10)

#z=h1[:,np.newaxis]

#print yy[0]
#print yy[1] - np.dot(xx,z)
print yy1 - xx * h1

