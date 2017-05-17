#coding:utf-8
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import scipy.signal
import os.path
from fdicapy import fdica

RATE =  44100
components=2
frame_length = 4096

#input voice data
filenames = [('mixed' + str(i+1) + '.wav') for i in range(components)]
length_array = [(os.path.getsize(filenames[i])-44)/2 for i in range(components)]
data_length = min(length_array)
input = np.zeros([components,data_length])

for i in range(components):
    input[i] = wav.read(filenames[i])[1][0:data_length]

output = fdica(input, frame_length)


#volume up = normalization
output = output/np.max(np.abs(output[:,0:data_length-RATE]))*32767
output = output.astype(np.int16)

filenames = [('output' + str(i+1) + '.wav') for i in range(components)]
for i in range(components):
    wav.write(filenames[i],RATE,output[i][0:data_length])

    fs, data = wav.read(filenames[i])
    x = np.frombuffer(data, dtype="int16") / 32768.0
    nyq = fs / 2.0  # ナイキスト周波数
    # フィルタの設計
    # ナイキスト周波数が1になるように正規化
    fe1 = 4000.0 / nyq      # カットオフ周波数1
    numtaps = 255           # フィルタ係数（タップ）の数（要奇数）
    b = scipy.signal.firwin(numtaps, fe1)
    y = scipy.signal.lfilter(b, 1, x)

    y = np.array(y)
    y = y/(3*np.max(np.abs(y)))*32767
    y = y.astype(np.int16)
    wav.write("filtered-"+filenames[i],RATE,y)

print("\a\a\a")