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

def make_histogram_log(amp, nb_bins = 40):
    bin_width = np.logspace(np.log10(amp.min()), np.log10(amp.max()), nb_bins)
    hist, bin_edges = np.histogram(a = amp, bins = bin_width)
    return hist, bin_edges

def make_histogram(amp, nb_bins = 40):
    bin_width = np.linspace(amp.min(), amp.max(), nb_bins)
    hist, bin_edges = np.histogram(a = amp, bins = bin_width)
    return hist, bin_edges

def add_histogram(hist1, hist2, bin_edges1, bin_edges2):
    avr_bin_edges = (bin_edges1 + bin_edges2)/2
    total_hist = hist1 + hist2
    return total_hist, avr_bin_edges

def coincidence(time1, time2, volt1, volt2, tolerance, bin_edges_time, bin_edges_volt):
    all_event = [0] * len(bin_edges_time)
    non_coincident = [0] * len(bin_edges_time)
    coincident = [0] * len(bin_edges_time)

    i, j = 0, 0
    while i < len(time1) and j < len(time2):
        k = 0
        while volt1[i] > bin_edges_volt[k]:
            k += 1
        delta = time1[i] - time2[j]
        if np.abs(delta) < tolerance:
            coincident[k] += 1
            i += 1
            j += 1
        elif delta < 0:
            i += 1
        elif delta > 0:
            j += 1
        else:
            print('---------------Error---------------')

    i = 0
    while i < len(time1) and j < len(time2):
        k = 0
        while volt1[i] > bin_edges_volt[k]:
            if k < len(bin_edges_volt):
                k += 1
        all_event[k] += 1
        i += 1

    for i in range(len(all_event)):
        non_coincident[i] = all_event[i] - coincident[i]

    print('Nb d\'evenement total : ', np.sum(all_event))
    print('Nb de coincident : ', np.sum(coincident))
    print('Nb de non coincident : ', np.sum(non_coincident))

    total_all = np.sum(all_event)
    all_event = all_event / total_all
    coincident = coincident / total_all
    non_coincident = non_coincident / total_all

    return all_event, non_coincident, coincident


def main():
    data1_file_name = './S2GE_APP3_Problematique_Detecteur_Primaire.csv'
    data2_file_name = './S2GE_APP3_Problematique_Detecteur_Secondaire.csv'

    time1 = get_data_file(data1_file_name, 'TIME')
    time2 = get_data_file(data2_file_name, 'TIME')

    hist1, bin_edges1 = make_histogram(time1)
    hist2, bin_edges2 = make_histogram(time2)
    print(bin_edges1.shape)
    print(bin_edges1)

    all_event, non_coincident, coincident = coincidence(time1, time2,
                                                        0.010, bin_edges1)
    volt1 = get_data_file(data1_file_name, 'VOLT')
    bin_volt1, bin_volt1_edges = make_histogram_log(volt1, nb_bins = 30)

    plt.figure(figsize=(10,10))
    print(len(all_event))
    print(bin_edges1.shape)
    plt.step(bin_edges1, all_event, label="All events", color='blue')
    plt.step(bin_edges1, coincident, label="Coincident", color='red')
    plt.step(bin_edges1, non_coincident, label="Non coincident", color='green')
    #plt.xscale('log')
    plt.legend()
    plt.show()

def main2():
    data1_file_name = './S2GE_APP3_Problematique_Detecteur_Primaire.csv'
    data2_file_name = './S2GE_APP3_Problematique_Detecteur_Secondaire.csv'

    time1 = get_data_file(data1_file_name, 'TIME')
    time2 = get_data_file(data2_file_name, 'TIME')
    volt1 = get_data_file(data1_file_name, 'VOLT')
    volt2 = get_data_file(data2_file_name, 'VOLT')

    hist_time1, edges_time1 = make_histogram_log(time1)
    hist_time2, edges_time2 = make_histogram_log(time2)
    hist_volt1, edges_volt1 = make_histogram_log(volt1)
    hist_volt2, edges_volt2 = make_histogram_log(volt2)

    all_event, non_coincident, coincident = coincidence(time1, time2,
                                                        volt1, volt2, 0.012,
                                                        edges_time1, edges_volt1)

    plt.figure(figsize=(10,10))
    plt.step(edges_volt1, all_event, label="All events", color='blue')
    plt.step(edges_volt1, non_coincident, label="Non coincident", color='green')
    plt.step(edges_volt1, coincident, label="Coincident", color='red')
    plt.xscale('log')
    plt.show()


if __name__ == '__main__':
    main2()
