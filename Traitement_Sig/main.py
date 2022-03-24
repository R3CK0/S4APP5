import numpy as np
from extraction import Extractor as extract
from filter import Filter
from generation import generation as gen
import matplotlib.pyplot as plt

if __name__ == '__main__':
    fichier_guitare = 'note_guitare_LAd.wav'
    fichier_basson = 'note_basson_plus_sinus_1000_Hz.wav'

    #extract data from guitare
    guitare = extract(fichier_guitare)
    f = Filter()

    #process data for the features of the sound file
    sample_rate_g, data_g = guitare.get_raw_data()
    envelope_g = guitare.extract_envelope(f.FIR_order())
    features_g = guitare.extract_param()
    peaks_g = guitare.extract_peaks(32, 1)

    #save and load the main features
    features_saved = guitare.save('guitare')
    features_loaded = guitare.load('guitare')

    #display features
    guitare.display_extracted_parameters(0)
    guitare.display_extracted_parameters(6)

    #generate sounds
    guitare_gen = gen(sample_rate_g, features_loaded['magnitude'], features_loaded['harmonique'],
                              features_loaded['phase'], features_loaded['envelop'])


    note = guitare_gen.generate('la')
    la = extract()
    la.update_data(sample_rate_g, note)
    envelope_la = la.extract_envelope(f.FIR_order())
    features_la = la.extract_param()
    peaks_la = la.extract_peaks(32, 1)
    la.display_extracted_parameters(0)

    beethoven_sound = guitare_gen.beethoven()

    #save notes
    guitare_gen.save_wav('beethoven', beethoven_sound)

    #play sounds(why you no work)
    #guitare_gen.play_wav(fichier_guitare)

    #Cleaning du Basson
    filter_order = 1024
    filter_bandwith = 40

    basson = extract(fichier_basson)
    sample_rate, pre_data = basson.get_raw_data()

    basson_filter = Filter(sample_rate, filter_order)
    H_coupe_bande = basson_filter.coupe_bande(filter_bandwith)



    filtered_basson = np.convolve(pre_data, H_coupe_bande)
    for _ in range(2):
        filtered_basson = np.convolve(filtered_basson, H_coupe_bande)

    #extract data
    basson.update_data(sample_rate, filtered_basson)
    envelope_basson = basson.extract_envelope(f.FIR_order())
    features_basson = basson.extract_param()
    peaks_basson = basson.extract_peaks(32, 1)

    # display features
    basson.display_extracted_parameters(3)

    #save extracted data
    features_saved_b = basson.save('basson')
    features_loaded_b = basson.load('basson')

    #save sound
    basson_gen = gen(sample_rate)
    basson_gen.save_wav('basson_fitre', filtered_basson)

    #filter prints
    basson_filter.print_filter(1)
    basson_filter.print_filter(2)
    basson_filter.print_filter(3)
    basson_filter.print_filter(4)
