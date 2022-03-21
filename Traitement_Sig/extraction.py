from numpy.fft import fft
import numpy as np
from scipy import signal
from scipy.io import wavfile
import os
from os.path import dirname, join as pjoin
import matplotlib.pyplot as plt

class Extractor:

    def __init__(self, filename=None):
        self.filename = filename
        self.sample_rate = None
        self.data = None
        if filename is not None:
            print('fetching data...')
            self.read(self.filename)
            print('data loaded successfully')

    def read(self, filename):
        self.sample_rate, self.data = wavfile.read(filename)

    def get_raw_data(self, item=None):
        return self.sample_rate, self.data

    def extract_param(self, note=None, sample_rate=None):
        if sample_rate is None:
            sample_rate = self.sample_rate
        if note is None:
            note = self.data

        note = np.array(note)
        #on considere seuelement les 32 sinusoides principales
        temps_centre = np.arange(-note.size/2, note.size/2, 1)
        self.axe_freq = temps_centre / note.size * sample_rate

        #le filtre de hanning permet de reduire l'effet de leaking autour des frequence principale
        Hanning = np.hanning(note.size)

        self.note_LA_FFT = fft(note * Hanning, note.size)
        self.magnitude_FFT = np.abs(self.note_LA_FFT)
        self.magnitude_FFT_dB = 20 * np.log10(self.magnitude_FFT[:80000])
        self.phase_FFT = np.angle(self.note_LA_FFT[:80000])

        self.peak, _ = signal.find_peaks(self.magnitude_FFT_dB, distance=1000, prominence=10)
        self.peak = self.peak[1:32]
        
        self.features = {'magnitude': self.magnitude_FFT[self.peak], 'harmonique': self.peak / note.size * self.sample_rate,
                         'magnitude_dB': self.magnitude_FFT_dB[self.peak], 'phase': self.phase_FFT[self.peak]}

        return {'peak': self.peak, 'FFT_magnitude': self.magnitude_FFT, 'FFT_magnitude_dB': self.magnitude_FFT_dB,
                'FFT_phase': self.phase_FFT, 'freq': self.axe_freq}


    def extract_envelope(self, order):
        hn = np.ones(order) / order
        self.envelope = signal.lfilter(hn, 1, np.abs(self.data))
        return self.envelope

    def save(self, filename):
        save = np.array([self.features['magnitude'], self.features['harmonique'], self.features['phase'],
                         self.features['magnitude_dB']])
        np.savetxt(filename+'.csv', save, delimiter=',')
        print('saved to '+filename+'.csv')
        return self.features
        
    def load(self, filename):
        load_data = np.genfromtxt(filename+'.csv', delimiter=',')
        self.features = {'magnitude': load_data[0], 'harmonique': load_data[1], 'phase': load_data[2],
                         'magnitude_dB': load_data[3]}
        print('values loaded from '+filename+'.csv')
        return self.features
    
    def display_extracted_parameters(self):
        plt.figure(1)
        plt.plot(np.arange(0, self.data.size, 1)/self.sample_rate, self.data)
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.figure(2)
        plt.plot(self.axe_freq, self.magnitude_FFT)
        plt.ylabel('amplitude')
        plt.xlabel('Hz')
        plt.figure(3)
        plt.plot(self.axe_freq[80000:], self.magnitude_FFT_dB)   
        plt.ylabel('amplitude (dB)')
        plt.xlabel('Hz')
        plt.figure(4)
        plt.plot(self.axe_freq[80000:], self.magnitude_FFT_dB)
        plt.plot(self.peak / self.data.size * self.sample_rate, self.magnitude_FFT_dB[self.peak], "x")
        plt.figure(5)
        plt.plot(self.envelope)
        plt.title("Enveloppe du LA#")
        plt.xlabel("nombre d'échantillons")
        plt.ylabel("Amplitude")

if __name__ == '__main__':
    guitare = Extractor('note_guitare_LAd.wav')
    sample_rate, data = guitare.get_raw_data()
    features = guitare.extract_param()
    envelope = guitare.extract_envelope(885)
    b = guitare.save('test')
    a = guitare.load('test')
    guitare.display_extracted_parameters()
    