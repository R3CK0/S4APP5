import math
import matplotlib.pyplot as plt
import numpy as np
import winsound
from extraction import Extractor as extract
import filter

if __name__ == '__main__':
    fichier_guitare = 'note_guitare_LAd.wav'
    fichier_basson = 'note_basson_plus_sinus_1000_Hz'

    #extract data from guitare
    guitare = extract(fichier_guitare)

    #sample_rate, data = guitare.get_raw_data()

    #process data for the features of the sound file
    features = guitare.extract_param()
    envelope = guitare.extract_envelope(885)

    #save and load the main features
    #b = guitare.save('test')
    #a = guitare.load('test')

    #display features
    guitare.display_extracted_parameters()