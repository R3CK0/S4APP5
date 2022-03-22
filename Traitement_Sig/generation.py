import numpy as np
from scipy.io import wavfile
import winsound
import matplotlib.pyplot as plt

class generation:

    def __init__(self, magnitude, harmonique, phase, envelop, sample_rate):
        self.magnitude = magnitude
        self.harmonique = harmonique
        self.phase = phase
        self.envelop = envelop
        self.sample_rate = sample_rate
        pass


    def save_wav(self, filename, data):
        scaled = np.int16(data / np.max(np.abs(data)) * 32767)
        wavfile.write(filename+'.wav', self.sample_rate, scaled)
        print('sound saved!')

    def create_sinus(self, freq, length, magn, phase):
        t = np.arange(length, dtype=float) / self.sample_rate
        sin_note = magn * np.sin(2 * np.pi * freq * t + phase)
        return sin_note

    def generate(self, note):

        son = []

        facteur_SOL = float(np.power(2.0, -3.0 / 12.0))  # Indice -1
        facteur_MI = float(np.power(2, -6.0 / 12.0))
        facteur_FA = float(np.power(2, -5.0 / 12.0))
        facteur_RE = float(np.power(2, -8.0 / 12.0))

        for h in self.harmonique:  # Facteurs sur les 32 harmoniques
            if note == "sol":
                son = np.append(son, facteur_SOL * h)
            if note == "mi":
                son = np.append(son, facteur_MI * h)
            if note == "fa":
                son = np.append(son, facteur_FA * h)
            if note == "re":
                son = np.append(son, facteur_RE * h)
            else:
                son = 1 * self.harmonique

        sinus = np.zeros(len(self.envelop))

        for i in range(32):
            sinus += self.create_sinus(son[i], len(self.envelop), self.magnitude[i], self.phase[i])
        #sinus /= np.max(np.abs(sinus))

        # Création des notes
        note_finale = sinus * self.envelop
        print('Sound Generated')

        # Ecriture des notes dans fichier wav

        return note_finale

    def play_wav(self, filename):
        winsound.PlaySound(filename+'.wav', winsound.SND_FILENAME)

    def beethoven(self):
        sequence = ['sol', 'sol', 'sol', 'mi', 0, 'fa', 'fa', 'fa', 're']
        song = []
        for note in sequence:
            if note != 0:
                song = np.append(song, self.generate(note)[8000:30000])
            else:
                song = np.append(song, np.zeros(30000))
        return song

