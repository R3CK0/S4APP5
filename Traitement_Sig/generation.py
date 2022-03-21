import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.io import wavfile
from os.path import dirname, join as pjoin
import winsound

class generation:

    def __init__(self):



        def extract_wav(name, samplerate, son):

            data_dir = dirname(__file__)
            wav_fname = pjoin(data_dir, name)
            scaled = np.int16(son / np.max(np.abs(son)) * 32767)
            wavfile.write(wav_fname, samplerate, scaled)

        def create_sinus(freq, length, magn, rate, phase):

            t = np.arange(length, dtype=float) / rate
            sin_note = magn * np.sin(2 * np.pi * freq * t + phase)
            return sin_note

        def generate(note, magnitude ,harmonique ,phase ,envelop ,samplerate):

            son = []

            facteur_SOL = float(np.power(2.0, -3.0 / 12.0))  # Indice -1
            facteur_MI = float(np.power(2, -6.0 / 12.0))
            facteur_FA = float(np.power(2, -5.0 / 12.0))
            facteur_RE = float(np.power(2, -8.0 / 12.0))

            for h in harmonique:  # Facteurs sur les 32 harmoniques
                if note == "sol":
                    son.append(facteur_SOL * h)
                if note == "mi":
                    son.append(facteur_MI * h)
                if note == "fa":
                    son.append(facteur_FA * h)
                if note == "re":
                    son.append(facteur_RE * h)
                else:
                    son = 1 * harmonique

            sinus = np.zeros(len(envelop))

            for y in range(0, 32):
                sinus += create_sinus(son[y], len(envelop), magnitude[y], samplerate, phase[y])

            # Création des notes
            note_finale = sinus * envelop

            # Ecriture des notes dans fichier wav
            extract_wav(note + ".wav", samplerate, note_finale)