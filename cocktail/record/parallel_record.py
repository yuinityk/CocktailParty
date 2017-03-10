# -*- coding: utf-8 -*-
import numpy as np

def adjust(sig_1, sig_2, glim = 50):
    '''
    correct the deviation of time between two signals sig_1, sig_2

    parameters
    ----
    sig_1, sig_2 : 1-D array of signal
    glim : max deviation of time (dependent on the frame rate)

    returns
    ----
    Array of:
    0: cut sig_1
    1: cut sig_2
    '''
    minlen = min(sig_1.shape[0],sig_2.shape[0])
    lim = min(glim, minlen/4.)

    dist = np.linalg.norm(sig_1[:minlen] - sig_2[:minlen])
    min_i = 0
    cut_s1 = sig_1
    cut_s2 = sig_2
    for i in range(1, int(min(lim,minlen))):

        tmp_s1 = sig_1[i:]
        tmp_s2 = sig_2[:min( len(sig_1)-i, len(sig_2))]
        #print(tmp_s1)
        #print(tmp_s2)
        tmp_dist = np.linalg.norm(tmp_s1 - tmp_s2)

        if tmp_dist < dist:
            dist = tmp_dist
            min_i = i
            cut_s1 = tmp_s1
            cut_s2 = tmp_s2

        tmp_s1 = sig_1[:min(len(sig_1),len(sig_2)-i)]
        tmp_s2 = sig_2[i:]
        #print(tmp_s1)
        #print(tmp_s2)
        tmp_dist = np.linalg.norm(tmp_s1 - tmp_s2)

        if tmp_dist < dist:
            dist = tmp_dist
            min_i = -i
            cut_s1 = tmp_s1
            cut_s2 = tmp_s2

    return np.array([cut_s1, cut_s2])

if __name__ == '__main__':
    s = np.array([1.,2.,3.,7.,8.,6.,7.,8.,9.,23.,12.,6.,4.,8.,4.,11.])
    t = np.array([3.,4.,1.,2.,3.,7.,8.,6.,7.,8.,9.,23.,12.,6.,4.,8.])
    print(adjust(s,t))
