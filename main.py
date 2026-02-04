import numpy as np                  # Gestion de donnees
import matplotlib.pyplot as plt     # Gestion de graphiques
import argparse as ap               # Entree de parametres
from scipy.ndimage import label
from sympy import true


#data1_file_name = './S2GE_APP3_Problematique_Detecteur_Primaire.csv'
#data2_file_name = './S2GE_APP3_Problematique_Detecteur_Secondaire.csv'

def get_data_file(file_name, column = 'ALL', delimiter=',', skip_header=1):
    data = np.loadtxt(file_name, delimiter=delimiter, skiprows=skip_header)
    index = data[:,0]
    time = data[:,1]
    volt = data[:,2]
    dead_time = data[:,3]
    temps = data[:,4]
    if column == 'ALL':
        return index, time, volt, dead_time, temps
    if column == 'INDEX':
        return index
    if column == 'TIME':
        return time
    if column == 'VOLT':
        return volt
    if column == 'DEAD_TIME':
        return dead_time
    if column == 'TEMP':
        return temps
    return None

def make_histogram_log(amp, nb_bins = 30):
    bin_width = np.logspace(np.log10(amp.min()), np.log10(amp.max()), nb_bins)
    hist, bin_edges = np.histogram(a = amp, bins = bin_width)
    return hist, bin_edges

def make_histogram(amp, nb_bins = 30):
    bin_width = np.linspace(amp.min(), amp.max(), nb_bins)
    hist, bin_edges = np.histogram(a = amp, bins = bin_width)
    return hist, bin_edges

def add_histogram(hist1, hist2, bin_edges1, bin_edges2):
    avr_bin_edges = (bin_edges1 + bin_edges2)/2
    total_hist = hist1 + hist2
    return total_hist, avr_bin_edges

def coincidence(arr1, arr2, tolerance, bin_edges):
    all_event = [0] * len(bin_edges)
    non_coincident = [0] * len(bin_edges)
    coincident = [0] * len(bin_edges)

    k = 1
    for i in range(len(arr1)):
        delta = (arr1[i] - arr2[i])
        avr = (arr1[i] + arr2[i]) / 2

        # What bin
        if avr > bin_edges[k]:
            while avr > bin_edges[k]:
                print(i)
                if k >= 29:
                    break
                k = k + 1
        # Coincidence
        if delta < tolerance:
            coincident[k - 1] = coincident[k - 1] + 1
        # Non-coincidence
        else:
            non_coincident[k - 1] = non_coincident[k - 1] + 1

        all_event[k - 1] = all_event[k - 1] + 1

    return all_event, non_coincident, coincident


def main():
    data1_file_name = './S2GE_APP3_Problematique_Detecteur_Primaire.csv'
    data2_file_name = './S2GE_APP3_Problematique_Detecteur_Secondaire.csv'

    time1 = get_data_file(data1_file_name, 'TIME')
    time2 = get_data_file(data2_file_name, 'TIME')

    hist1, bin_edges1 = make_histogram_log(time1)
    hist2, bin_edges2 = make_histogram_log(time2)
    print(bin_edges1.shape)
    print(bin_edges1)

    all_event, non_coincident, coincident = coincidence(time1, time2,
                                                        0.010, bin_edges1)

    plt.figure(figsize=(10,10))
    print(len(all_event))
    print(bin_edges1.shape)
    plt.step(bin_edges1, all_event, label="All events")
    plt.step(bin_edges1, coincident, label="Coincident")
    plt.step(bin_edges1, non_coincident, label="Non coincident")
    plt.xscale('log')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()