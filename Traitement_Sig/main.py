import math
import matplotlib.pyplot as plt
import numpy as np
import winsound
from extraction import Extractor as extract
from filter import Filter
from generation import generation as gen

if __name__ == '__main__':
    fichier_guitare = 'note_guitare_LAd.wav'
    fichier_basson = 'note_basson_plus_sinus_1000_Hz'

    #extract data from guitare
    guitare = extract(fichier_guitare)
    f = Filter()
    gen = gen()

    sample_rate, data = guitare.get_raw_data()

    #process data for the features of the sound file
    envelope = guitare.extract_envelope(f.FIR_order())
    features = guitare.extract_param()
    peaks = guitare.extract_peaks(32, 1)

    #save and load the main features
    features_saved = guitare.save('test')
    features_loaded = guitare.load('test')

    #display features
    #guitare.display_extracted_parameters(0)

    #play sounds
    note, sinus, envelope = gen.generate('fa', features_loaded['magnitude'], features_loaded['harmonique'],
                              features_loaded['phase'], features_loaded['envelop'], sample_rate)

    gen.play_wav(fichier_guitare)

    plt.figure()
    plt.plot(np.arange(0, sinus.size, 1), sinus)
    plt.show()