# -*- coding: utf-8 -*-
# ==================================
#
#    Frequency Domain ICA
#
# ==================================
from .complex_fastica_ import ComplexFastICA, complexfastica
from .stft_ import stft, istft
import numpy as np
import scipy as sp
import sys


def _multiple_stft(X, frame_length, win=None, step=None):

    """
        STFT of multiple data series.
        
    parameters
    ----------
    X : ndarray of shape (n_samples, n_features)
        input multiple data series, where n_samples is the number of samples and n_features is the number of features.
    
    frame_length : a length of one frame.
        
    win : ndarray of shape (frame_length)
        window function.
        hamming window is default (win=None) and another option is now hannig window only.
        
    step : step size. stpe = frame_length/4 is default.(step=None)
    
    
    S : ndarray of shape (n_samples, n_frames, n_frequencies)
        output spectogram (3D) matrix, where n_samples is the number of samples, n_frames is the number of frames, and n_frequencies is the number of discrete frequencies (,which equals the length of one frame).
    """
    n_samples = X.shape[0]
    n_features = X.shape[1]
    n_frequencies = frame_length
    
    if step is None:
        step = frame_length / 4
    elif step > frame_length:
        print "step is longer than frame_length.\n"
        sys.exit()
    elif step <= 0:
        print "step is invalid.\n"
        sys.exit()
    
    n_frames = int(sp.ceil(float(n_features - frame_length + step) / step))

    S=np.zeros([n_samples, n_frames, n_frequencies], dtype=np.complex64)
    for i in range(n_samples):
        S[i] = stft(X[i], frame_length, win, step)

    return S

def _ica_by_freq(S):
    """
        apply ComplexfastICA Fourier-transformed data by frequency,
        and get separated spectra.
        
    parameters
    ----------
    S : ndarray of shape (n_samples, n_frames, n_frequencies)
        input spectogram (3D) matrix, where n_samples is the number of samples, n_frames is the number of frames, and n_frequencies is the number of discrete frequencies (,which equals the length of one frame).
        
    T : ndarray of shape (n_samples, n_frames, n_frequencies)
        output separated spectrogram (3D) matrix, whose size is the same as S.
        this is the result of application of (complex) ICA to S by frequency
        
    WK : ndarray of shape (n_samples, n_samples, n_frequencies)
        output demixing matrix. 
        i.e. the matrix product of matrix W and K, where W is the estimated un-mixing matrix and K is the estimated pre-whitening matrix.
    """
    
    n_samples, n_frames , n_frequencies= S.shape
    T = np.zeros(S.shape, dtype=np.complex64)
    WK = np.zeros([n_samples, n_samples, n_frequencies], dtype=np.complex64)

    for l in range(n_frequencies):
        M = S[:,:,l].T
        M = M.astype(np.complex64)
        M /= M.std(axis = 0)
        ica = ComplexFastICA(n_components=n_samples)
        N = ica.fit_transform(M).T
        T[:,:,l] = N
        WK[:,:,l] = ica.components_

    return T, WK

def _get_split_spectrum(T,WK):
    """
        get split spectra from separated spectra.
        
    parameters
    ----------
    T : ndarray of shape (n_samples, n_frames, n_frequencies)
        input separated spectrogram (3D) matrix, where n_samples is the number of samples, n_frames is the number of frames, and n_frequencies is the number of discrete frequencies (,which equals the length of one frame).
        
    WK : ndarray of shape (n_samples, n_samples, n_frequencies)
        input demixing matrix.
        i.e. the matrix product of matrix W and K, where W is the estimated un-mixing matrix and K is the estimated pre-whitening matrix.
        
    U : ndarray of shape (n_samples, n_samples, n_frames, n_frequencies)
        output split spectrogram matreces, where n_samples is the number of samples, n_frames is the number of frames, and n_frequencies is the number of discrete frequencies (,which equals the length of one frame).
        U[n] denotes the split spectrogram matrix of the n-th separated spectrogram,
            i.e. U[n,:,k,l] = (WK[l])^(-1) [0, ... , T[n,k,l], ..., 0].T

    """

    n_samples, n_frames, n_frequencies = T.shape
    U = np.zeros([n_samples, n_samples, n_frames, n_frequencies], dtype=np.complex64)
    
    for l in range(n_frequencies):
        for n in range(n_samples):
            _T = np.zeros([n_samples, n_frames], dtype=np.complex64)
            _T[n,:] = T[n,:,l]
            inv_WK = np.linalg.inv(WK[:,:,l])
            U[n,:,:,l] = np.dot(inv_WK, _T)
    
    return U

def _get_power_of_spectrum(U):
    """
        get the power of split spectrum sequence
        
    parameters
    ----------
    U : ndarray of shape (n_samples, n_samples, n_frames, n_frequencies)
        input split spectrogram matreces, where n_samples is the number of samples, n_frames is the number of frames, and n_frequencies is the number of discrete frequencies (,which equals the length of one frame).
        U[n] denotes the split spectrogram matrix of the n-th separated spectrogram,
        i.e. U[n,:,k,l] = (WK[l])^(-1) [0, ... , T[n,k,l], ..., 0].T
    
    P : ndarray of shape (n_samples, n_samples, n_frequencies)
        output power matrix, where n_samples is the number of samples and n_frequencies is the number of discrete frequencies (,which equals the length of one frame).
        P[n,m,l] denotes the power of spectrum sequence of the source n through the system m at frequency l.
    """
    
    _, n_samples, n_frames, n_frequencies = U.shape
    del _

    P = np.zeros([n_samples, n_samples, n_frequencies], dtype=np.complex64)
    P = np.sum(np.abs(U)**2, axis=2) / n_frames
    
    return P


def _correct_dual_permutation(U, transfer=True):
    """
        correct permutation of split spectra.
        
    parameters
    ----------
    U : ndarray of shape (n_samples, n_samples, n_frames, n_frequencies)
        input split spectrogram matreces, where n_samples is the number of samples, n_frames is the number of frames, and n_frequencies is the number of discrete frequencies (,which equals the length of one frame).
        U[n] denotes the split spectrogram matrix of the n-th separated spectrogram,
        i.e. U[n,:,k,l] = (WK[l])^(-1) [0, ... , T[n,k,l], ..., 0].T
        
    V : ndarray of shape (n_samples, n_frames, n_frequencies)
        output permutation-corrected split spectrogram matrix.
        
    """
    _, n_samples, n_frames, n_frequencies = U.shape
    del _
    
    if n_samples != 2:
        print "the number of samples should exactly be 2.\n"
        sys.exit()
    
    V = np.zeros([n_samples, n_frames, n_frequencies], dtype=np.complex64)

    P = _get_power_of_spectrum(U)
    
    for l in range(n_frequencies):
        P_plus1 = P[0,0,l] + P[0,1,l]
        P_plus2 = P[1,0,l] + P[1,1,l]
        P_minus1 = P[0,0,l] - P[0,1,l]
        P_minus2 = P[1,0,l] - P[1,1,l]

        if P_plus1 > P_plus2:
            if transfer:
                if P_minus1 > 0:
                    V[0,:,l] = U[0,0,:,l]
                    V[1,:,l] = U[1,1,:,l]
                else:
                    V[0,:,l] = U[1,0,:,l]
                    V[1,:,l] = U[0,1,:,l]
        else:
            if transfer:
                if P_minus2 < 0:
                    V[0,:,l] = U[0,0,:,l]
                    V[1,:,l] = U[1,1,:,l]
                else:
                    V[0,:,l] = U[1,0,:,l]
                    V[1,:,l] = U[0,1,:,l]




    return V


def _multiple_istft(U, frame_length, win=None, step=None):

    """
    U : ndarray of shape (n_samples, n_frames, n_frequencies)
        input spectogram (3D) matrix, where n_samples is the number of samples, n_frames is the number of frames, and n_frequencies is the number of discrete frequencies (,which equals the length of one frame).
    
    frame_length : a length of one frame.
    
    win : ndarray of shape (frame_length)
        window function.
        hamming window is default (win=None) and another option is now hannig window only.
    
    step : step size. stpe = frame_length/4 is default.(step=None)
    
    Y : ndarray of shape (n_samples, n_features)
        output multiple data series, where n_samples is the number of samples and n_features is the number of features.
    """
        
    n_samples, n_frames , n_frequencies= U.shape
    
    if step is None:
        step = frame_length / 4
    elif step > frame_length:
        print "step is longer than frame_length.\n"
        sys.exit()
    elif step <= 0:
        print "step is invalid.\n"
        sys.exit()
    
    datalength = (n_frames - 1) * step + n_frequencies
    Y=np.zeros([n_samples, datalength])
    for i in range(n_samples):
        Y[i] = istft(U[i], frame_length, win, step)

    return Y

def fdica(X, frame_length, win=None, step=None):

    S = _multiple_stft(X, frame_length, win, step)
    T, WK = _ica_by_freq(S)
    
    #print WK[:,:,1]
    
    del S
    U = _get_split_spectrum(T, WK)
    del T, WK
    V = _correct_dual_permutation(U)
    del U
    Y = _multiple_istft(V, frame_length, win, step)

    return Y










