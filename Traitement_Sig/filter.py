import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.io import wavfile
from os.path import dirname, join as pjoin
import winsound

class Filter:

    def __init__(self):

        def order

            index = np.array([])
            res = 0
            for n in range(1, 1000):
            # En utilisant la méthode des fenêtres
                hn = np.power(np.e, (-1j * n * np.pi / 1000))
                res = res + hn
                Hw = 1 / n * res
                index = np.append(index, Hw)

            index = np.asarray(index)
            ordre = (np.abs(np.abs(index) - 1 / np.sqrt(2))).argmin()
            # Prend la valeur la plus près de 0.707 --> -3dB

            return ordre