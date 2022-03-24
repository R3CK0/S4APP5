import numpy as np
from numpy.fft import ifft, fft
import matplotlib.pyplot as plt
from scipy.signal import unit_impulse


class Filter:

    def __init__(self, sample_rate=None, order=None):
        self.sample_rate = sample_rate
        self.order = order
        pass

    def FIR_order(self):

        index = np.array([])
        res = 0
        for n in range(1, 1000):
        # En utilisant la méthode des fenêtres
            hn = np.power(np.e, (-1j * n * np.pi / 1000))
            res += hn
            Hw = 1 / n * res
            index = np.append(index, Hw)

        ordre = (np.abs(np.abs(index) - 1 / np.sqrt(2))).argmin()
        # Prend la valeur la plus près de 0.707 --> -3dB

        return ordre

    def passe_bas(self, bandwidth):
        N = self.order  # Ordre du coupe-bande
        fe = self.sample_rate
        f_range = bandwidth

        self.hlp = []

        n = np.arange((-N / 2) + 1, (N / 2) + 1, 1)  # Sommation de -N/2 à N/2
        K = (f_range / fe) * N * 2 + 1  # Largeur du filtre

        #Conception du passe bas
        for index in n:
            if index == 0:
                self.hlp.append(K / N)  # Division par zéro
            else:
                self.hlp.append((1 / N) * (np.sin(((np.pi * index * K) / N)) / (np.sin(((np.pi * index) / N)))))  # réponse impulsionnelle lp
        return self.hlp




    def coupe_bande(self, bandwidth):

        hlp = self.passe_bas(bandwidth)

        fe = self.sample_rate
        N = self.order
        n = np.arange((-N / 2) + 1, (N / 2) + 1, 1)

        w0 = 2 * np.pi * 1000 / fe

        # Coupe-bande à partir du passe bas
        delta = np.zeros(N)
        delta[int(N / 2)] = 1  # 1 si N=0 et 0 reste
        self.hbs = []
        for i in range(0, N):
            self.hbs.append(delta[i] - (2 * hlp[i] * np.cos(w0 * n[i])))  # réponse impulsionnelle bandstop avec eq donnée

        return self.hbs

    def print_filter(self, graph_type = None):

        if graph_type == 1:
            hbs = np.array(self.hbs)
            dirac = unit_impulse(hbs.size)
            dirac_f = fft(dirac)
            x = np.arange(960, 1040, (1040-960)/2047)
            response_f = np.convolve(dirac_f, hbs)
            plt.figure()
            plt.plot(x, response_f)
            plt.title('Reponse a impulsion coupe-bande')
            plt.show()

        if graph_type == 2:
            hbs = np.array(self.hbs)
            length = np.arange(0, hbs.size)
            sinus = np.sin(2*np.pi*length*1000/44100)
            hbs_t = ifft(hbs)
            response_t = sinus*hbs_t
            plt.figure()
            plt.plot(length, sinus, color='blue')
            plt.plot(length, response_t, color='orange')
            plt.ylabel('Amplitude')
            plt.xlabel('echantillons')
            plt.title('sinus filtrer')
            plt.show()

        if graph_type == 3:
            hbs = np.array(self.hbs)
            freq = np.arange(960, 1040, 80/hbs.size)
            plt.figure()
            plt.plot(freq, hbs)
            plt.title('amplitude filtre coupe_bande')
            plt.xlabel('frequence (Hz)')
            plt.ylabel('amplitude')
            plt.show()

        if graph_type == 4:
            hbs = np.array(self.hbs)
            freq = np.arange(960, 1040, 80/hbs.size)
            plt.figure()
            plt.plot(freq, np.angle(hbs))
            plt.title('angle filtre coupe_bande')
            plt.xlabel('frequence (Hz)')
            plt.ylabel('angle')
            plt.show()

