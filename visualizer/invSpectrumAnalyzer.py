# -*- coding:utf-8 -*-

#プロット関係のライブラリ
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import sys

#音声関係のライブラリ
import pyaudio
import struct


class PlotWindow:
    def __init__(self):
        #マイクインプット設定
        self.CHUNK=1024            #1度に読み取る音声のデータ幅
        self.RATE=44100             #サンプリング周波数
        self.update_seconds=1      #更新時間[ms]
        self.audio=pyaudio.PyAudio()
        self.stream=self.audio.open(format=pyaudio.paInt16,
                                    channels=1,
                                    rate=self.RATE,
                                    input=True,
                                    input_device_index=4,
                                    frames_per_buffer=self.CHUNK)

        #音声データの格納場所(プロットデータ)
        self.data=np.zeros(self.CHUNK)
        self.axis=np.fft.fftfreq(len(self.data), d=1.0/self.RATE)

        #プロット初期設定
        self.win=pg.GraphicsWindow()
        self.win.setWindowTitle("SpectrumAnalyzer")
        self.win.resize(680,680)
        self.plt=self.win.addPlot() #プロットのビジュアル関係
        self.plt.setLogMode(True,True)
        self.plt.setXRange(0,2.5)
        self.plt.setYRange(np.log10(30),np.log10(self.RATE/2*1.1))



        #アップデート時間設定
        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(self.update_seconds)    #10msごとにupdateを呼び出し

    def update(self):
        self.data=np.append(self.data,self.AudioInput())
        if len(self.data)/1024 > 10:
            self.data=self.data[1024:]
        self.fft_data=self.FFT_AMP(self.data)
        self.axis=np.fft.fftfreq(len(self.data), d=1.0/self.RATE)
        self.y=self.axis[1:len(self.axis)/2]
        self.x=self.fft_data[1:len(self.fft_data)/2]
        self.plt.plot(x=self.x, y=self.y, clear=True, pen="y")
        #symbol="o", symbolPen="y", symbolBrush="b")

    def AudioInput(self):
        ret=self.stream.read(self.CHUNK,exception_on_overflow=False)    #音声の読み取り(バイナリ) CHUNKが大きいとここで時間かかる
        #バイナリ → 数値(int16)に変換
        #32768.0=2^16で割ってるのは正規化(絶対値を1以下にすること)
        ret=np.frombuffer(ret, dtype="int16")/32768.0
        return ret

    def FFT_AMP(self, data):
        data=np.hamming(len(data))*data
        data=np.fft.fft(data)
        data=np.abs(data)
        return data

if __name__=="__main__":
    plotwin=PlotWindow()
    if (sys.flags.interactive!=1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()