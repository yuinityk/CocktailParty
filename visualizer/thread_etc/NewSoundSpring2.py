# -*- coding:utf-8 -*-
import numpy as np
import pyaudio
import pygame
from pygame.locals import *
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import sys
from multiprocessing import Pool

import package.SoundSpring as ss
import package.invSpectrumAnalyzer as sa

def main():
	pool = Pool(2)
	pool.apply_async(ss.main)
	pool.apply_async(sa.main)

if __name__ == "__main__":
    main()


