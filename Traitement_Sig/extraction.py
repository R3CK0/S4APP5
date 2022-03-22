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
        self.original = True # True if never changed

        self.axe_freq = None
        self.magnitude_FFT = None
        self.magnitude_FFT_dB = None
        self.peak = None
        self.phase_FFT = None
        self.features = dict()
        self.raw = dict()

        if filename is not None:
            print('fetching data...')
            self.read(self.filename)
            print('data loaded successfully')

    def read(self, filename):
        self.sample_rate, self.data = wavfile.read(filename)

    def update_data(self, sample_rate, data):
        self.sample_rate = sample_rate
        self.data = data

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

        note_FFT = fft(note * Hanning, note.size)
        self.magnitude_FFT = np.abs(note_FFT)
        self.magnitude_FFT_dB = 20 * np.log10(self.magnitude_FFT[:int(note.size/2)])
        self.phase_FFT = np.angle(note_FFT[:int(note.size/2)])
        


        self.raw = {'FFT_magnitude': self.magnitude_FFT, 'FFT_magnitude_dB': self.magnitude_FFT_dB,
                'FFT_phase': self.phase_FFT, 'freq': self.axe_freq}

        return self.raw


    def extract_peaks(self, peaks_to_extract, ignore=None, distance=1000, prominence=10):
        self.peak, _ = signal.find_peaks(self.magnitude_FFT_dB, distance=distance, prominence=prominence)
        self.peak = self.peak[ignore:peaks_to_extract+ignore]

        self.features['magnitude'] = self.magnitude_FFT[self.peak]
        self.features['harmonique'] = self.peak / self.data.size * self.sample_rate
        self.features['magnitude_dB'] = self.magnitude_FFT_dB[self.peak]
        self.features['phase'] = self.phase_FFT[self.peak]
        self.features['peaks'] = self.peak

        return self.peak


    def extract_envelope(self, order):
        hn = np.ones(order) / order
        self.envelope = signal.lfilter(hn, 1, np.abs(self.data))
        self.features['envelop'] = self.envelope
        return self.envelope

    def save(self, filename):
        save_features = np.array([self.features['magnitude'], self.features['harmonique'], self.features['phase'],
                         self.features['magnitude_dB']])
        np.savetxt(filename+'.csv', save_features, delimiter=',')
        np.savetxt(filename+'_enveloppe.csv', self.envelope, delimiter=',')
        print('saved to '+filename+'.csv')
        return self.features
        
    def load(self, filename):
        load_data = np.genfromtxt(filename+'.csv', delimiter=',')
        load_enveloppe = np.genfromtxt(filename + '_enveloppe.csv', delimiter=',')
        self.features = {'magnitude': load_data[0], 'harmonique': load_data[1], 'phase': load_data[2],
                         'magnitude_dB': load_data[3], 'envelop': load_enveloppe}
        print('values loaded from '+filename+'.csv')
        return self.features

    #Selection: 1 original signal over time

    def display_extracted_parameters(self, selection):
        if selection == 1 or selection == 0:
            plt.figure(1)
            plt.plot(np.arange(0, self.data.size, 1)/self.sample_rate, self.data)
            plt.xlabel('Time (s)')
            plt.ylabel('Amplitude')
        if selection == 2 or selection == 0:
            plt.figure(2)
            plt.plot(self.axe_freq, self.magnitude_FFT)
            plt.ylabel('amplitude')
            plt.xlabel('Hz')
        if selection == 3 or selection == 0:
            plt.figure(3)
            plt.plot(self.axe_freq[int(self.data.size/2):], self.magnitude_FFT_dB)
            plt.ylabel('amplitude (dB)')
            plt.xlabel('Hz')
        if selection == 4 or selection == 0:
            plt.figure(4)
            plt.plot(self.axe_freq[int(self.data.size/2):], self.magnitude_FFT_dB)
            plt.plot(self.peak / self.data.size * self.sample_rate, self.magnitude_FFT_dB[self.peak], "x")
            plt.ylabel('amplitude (dB)')
            plt.xlabel('Hz')
        if selection == 5 or selection == 0:
            plt.figure(5)
            plt.plot(self.envelope)
            plt.title("Enveloppe du LA#")
            plt.xlabel("nombre d'échantillons")
            plt.ylabel("Amplitude")
        plt.show()

if __name__ == '__main__':
    guitare = Extractor('note_guitare_LAd.wav')

    sample_rate, data = guitare.get_raw_data()

    envelope = guitare.extract_envelope(885)
    features = guitare.extract_param()
    peaks = guitare.extract_peaks(32, 1)


    #b = guitare.save('test')
    #a = guitare.load('test')
    guitare.display_extracted_parameters(0)
