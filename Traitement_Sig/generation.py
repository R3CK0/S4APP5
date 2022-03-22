import numpy as np
from scipy.io import wavfile
import winsound
import matplotlib.pyplot as plt

class generation:

    def __init__(self):
        pass


    def save_wav(self, filename, sample_rate, data):
        scaled = np.int16(data / np.max(np.abs(data)) * 32767)
        wavfile.write(filename+'.wav', sample_rate, scaled)
        print('sound saved!')

    def create_sinus(self, freq, length, magn, rate, phase):
        t = np.arange(length, dtype=float) / rate
        sin_note = magn * np.sin(2 * np.pi * freq * t + phase)
        return sin_note

    def generate(self, note, magnitude, harmonique, phase, envelop, sample_rate):

        son = []

        facteur_SOL = float(np.power(2.0, -3.0 / 12.0))  # Indice -1
        facteur_MI = float(np.power(2, -6.0 / 12.0))
        facteur_FA = float(np.power(2, -5.0 / 12.0))
        facteur_RE = float(np.power(2, -8.0 / 12.0))

        for h in harmonique:  # Facteurs sur les 32 harmoniques
            if note == "sol":
                son = np.append(son, facteur_SOL * h)
            if note == "mi":
                son = np.append(son, facteur_MI * h)
            if note == "fa":
                son = np.append(son, facteur_FA * h)
            if note == "re":
                son = np.append(son, facteur_RE * h)
            else:
                son = 1 * harmonique

        sinus = np.zeros(len(envelop))

        for i in range(32):
            sinus += self.create_sinus(son[i], len(envelop), magnitude[i], sample_rate, phase[i])
        #sinus /= np.max(np.abs(sinus))

        # Création des notes
        note_finale = sinus * envelop
        print('Sound Generated')

        # Ecriture des notes dans fichier wav
        self.save_wav(note, sample_rate, note_finale)

        return note_finale, sinus, envelop

    def play_wav(self, filename):
        winsound.PlaySound(filename+'.wav', winsound.SND_FILENAME)


