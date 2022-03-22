import numpy as np


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

        hlp = []

        n = np.arange((-N / 2) + 1, (N / 2) + 1, 1)  # Sommation de -N/2 à N/2
        K = (f_range / fe) * N * 2 + 1  # Largeur du filtre

        #Conception du passe bas
        for index in n:
            if index == 0:
                hlp.append(K / N)  # Division par zéro
            else:
                hlp.append((1 / N) * (np.sin(((np.pi * index * K) / N)) / (np.sin(((np.pi * index) / N)))))  # réponse impulsionnelle lp
        return hlp


    def coupe_bande(self, bandwidth):

        hlp = self.passe_bas(bandwidth)

        fe = self.sample_rate
        N = self.order
        n = np.arange((-N / 2) + 1, (N / 2) + 1, 1)

        w0 = 2 * np.pi * 1000 / fe

        # Coupe-bande à partir du passe bas
        delta = np.zeros(N)
        delta[int(N / 2)] = 1  # 1 si N=0 et 0 reste
        hbs = []
        for i in range(0, N):
            hbs.append(delta[i] - (2 * hlp[i] * np.cos(w0 * n[i])))  # réponse impulsionnelle bandstop avec eq donnée

        return hbs