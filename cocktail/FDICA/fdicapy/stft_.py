# -*- coding: utf-8 -*-
# ==================================
#
#    Short Time Fourier Trasform
#
# ==================================
from scipy import ceil, complex64, float64, hamming, hanning, zeros
from scipy.fftpack import fft# , ifft
from scipy import ifft # こっちじゃないとエラー出るときあった気がする
from scipy.io.wavfile import read
from matplotlib import pylab as pl
import sys

__all__ = ['stft', 'istft']


"""
x : ndarray of shape (n_features)
    input data vector, where n_features is the number of features.
    
win : ndarray of shape (L)
    window function, where L is a length of one frame.
    
step : step size.
    
X : ndarray of shape (K, L)
    output spectrogram matrix, where K is the number of frames and L is the number of discrete frequencies (which equals to the length of one frame).
    i.e. X[k,l] is the spectrogram of frame k and frequency l. 
"""

# ======
#  STFT
# ======

def _stft(x, win, step):
    l = len(x) # 入力信号の長さ
    N = len(win) # 窓幅、つまり切り出す幅
    M = int(ceil(float(l - N + step) / step)) # スペクトログラムの時間フレーム数
    
    new_x = zeros(N + ((M - 1) * step), dtype = float64)
    new_x[: l] = x # 信号をいい感じの長さにする
    
    X = zeros([M, N], dtype = complex64) # スペクトログラムの初期化(複素数型)
    #行はフレーム、列は（規格化）周波数に対応
    #つまり(k,l)成分がkフレーム目のl番目の周波数成分
    for m in xrange(M):
        start = step * m
        X[m, :] = fft(new_x[start : start + N] * win)
    return X

# =======
#  iSTFT
# =======
def _istft(X, win, step):
    M, N = X.shape
    assert (len(win) == N), "FFT length and window length are different."
    
    l = (M - 1) * step + N
    x = zeros(l, dtype = float64)
    wsum = zeros(l, dtype = float64)
    for m in xrange(M):
        start = step * m
        ### 滑らかな接続
        x[start : start + N] = x[start : start + N] + ifft(X[m, :]).real * win
        wsum[start : start + N] += win ** 2
    pos = (wsum != 0)
    x_pre = x.copy()
    ### 窓分のスケール合わせ
    x[pos] /= wsum[pos]
    return x



"""
as to window function, hamming window is default
    and another option is hannig function.
as to step size, stpe = fftLen/4 is default.
"""

def stft(data, fftLen, win=None, step=None):
    
    if win is None:
        win = hamming(fftLen)
    elif win == 'hanning':
        win = hanning(fftLen)
    else:
        print "Window name is invalid.\n"
        sys.exit()

    if step is None:
        step = fftLen / 4
    elif step >fftLen:
        print "step is longer than fftLen.\n"
        sys.exit()
    elif step <= 0:
        print "step is invalid.\n"
        sys.exit()

    spectrogram = _stft(data, win, step)

    return spectrogram

def istft(spectrogram, fftLen, win=None, step=None):
    
    if win is None:
        win = hamming(fftLen)
    elif win == 'hanning':
        win = hanning(fftLen)
    else:
        print "Window name is invalid.\n"
        sys.exit()
    
    if step is None:
        step = fftLen / 4
    elif step >fftLen:
        print "step is longer than fftLen.\n"
        sys.exit()
    elif step <= 0:
        print "step is invalid.\n"
        sys.exit()
    
    data = _istft(spectrogram, win, step)

    return data



if __name__ == "__main__":
    wavfile = "input1.wav"
    fs, data = read(wavfile)
    
    fftLen = 512 # とりあえず

    ### STFT
    spectrogram = stft(data, fftLen)
    
    ### iSTFT
    resyn_data = istft(spectrogram, fftLen)
    
    ### Plot
    fig = pl.figure()
    fig.add_subplot(311)
    pl.plot(data)
    pl.xlim([0, len(data)])
    pl.title("Input signal", fontsize = 20)
    fig.add_subplot(312)
    pl.imshow(abs(spectrogram[:, : fftLen / 2 + 1].T), aspect = "auto", origin = "lower")
    pl.title("Spectrogram", fontsize = 20)
    fig.add_subplot(313)
    pl.plot(resyn_data)
    pl.xlim([0, len(resyn_data)])
    pl.title("Resynthesized signal", fontsize = 20)
    pl.show()
