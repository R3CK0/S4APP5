import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.io import wavfile
from os.path import dirname, join as pjoin
import winsound

class Filter:

    def __init__(self):

        def order():

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

        def coupe_bande(samplerate):

            N = 1024  # Ordre du coupe-bande
            fe = samplerate
            f_range = 40
            w0 = 2 * np.pi * 1000 / fe
            hlp = []

            n = np.arange((-N / 2) + 1, (N / 2) + 1, 1)  # Sommation de -N/2 à N/2
            K = (f_range / fe) * N * 2 + 1  # Largeur du filtre

            #Conception du passe bas
            for index in n:
                if index == 0:
                    hlp.append(K / N)  # Division par zéro
                else:
                    hlp.append((1 / N) * (np.sin(((np.pi * index * K) / N)) / (np.sin(((np.pi * index) / N)))))  # réponse impulsionnelle lp

            # Coupe-bande à partir du passe bas
            delta = np.zeros(N)
            delta[int(N / 2)] = 1  # 1 si N=0 et 0 reste
            hbs = []
            for i in range(0, N):
                hbs.append(delta[i] - (2 * hlp[i] * np.cos(w0 * n[i])))  # réponse impulsionnelle bandstop avec eq donnée

            return