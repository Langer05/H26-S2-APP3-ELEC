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

def make_histogram_log(amp, nb_bins):
    bin_width = np.logspace(np.log10(amp.min()), np.log10(amp.max()), nb_bins)
    hist, bin_edges = np.histogram(a = amp, bins = bin_width)
    return hist, bin_edges

def make_histogram(amp, nb_bins):
    bin_width = np.linspace(amp.min(), amp.max(), nb_bins)
    hist, bin_edges = np.histogram(a = amp, bins = bin_width)
    return hist, bin_edges

def coincidence(time1, time2, volt1, volt2, tolerance, bin_edges_time, bin_edges_volt, temps_mort):
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
            print('Erreur coincidence')

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

    input_temps_mort = input("Voulez-vous les temps morts ? [y/N] : ")
    if input_temps_mort == 'y' or input_temps_mort == 'Y':
        delta_t = (time1[-1] - 0) - np.sum(temps_mort)
        Avr_muons_temps = np.sum(coincident) / delta_t
        Avr_temps_morts = np.sum(temps_mort) / len(temps_mort)
        Avr_rate_muons = Avr_muons_temps * Avr_temps_morts
        for i in range(len(coincident)):
            coincident[i] = coincident[i] + (coincident[i] * Avr_rate_muons)

    print('Nb d\'evenement total : ', np.sum(all_event))
    print('Nb de coincident : ', np.sum(coincident))
    print('Nb de non coincident : ', np.sum(non_coincident))

    total_all = np.sum(all_event)
    coincident_err = np.sqrt(coincident) / total_all
    all_event = all_event / total_all
    coincident = coincident / total_all
    non_coincident = non_coincident / total_all

    return all_event, non_coincident, coincident, coincident_err, input_temps_mort

def main():
    data1_file_name = './S2GE_APP3_Problematique_Detecteur_Primaire.csv'
    data2_file_name = './S2GE_APP3_Problematique_Detecteur_Secondaire.csv'

    time1 = get_data_file(data1_file_name, 'TIME')
    time2 = get_data_file(data2_file_name, 'TIME')
    volt1 = get_data_file(data1_file_name, 'VOLT')
    volt2 = get_data_file(data2_file_name, 'VOLT')
    temps_morts = get_data_file(data1_file_name, 'TEMP')

    nb_bins = int(input("Nombre de classe (N) : "))
    hist_time1, edges_time1 = make_histogram_log(time1, nb_bins)
    hist_time2, edges_time2 = make_histogram_log(time2, nb_bins)
    hist_volt1, edges_volt1 = make_histogram_log(volt1, nb_bins)
    hist_volt2, edges_volt2 = make_histogram_log(volt2, nb_bins)

    all_event, non_coincident, coincident, coincident_err, input_temps_mort =   (coincidence(time1, time2,
                                                                                volt1, volt2, 0.012,
                                                                                edges_time1, edges_volt1,
                                                                                temps_morts))

    edges_err = np.zeros(len(edges_volt1))
    for i in range(len(edges_volt1) - 1):
        edges_err[i+1] = (edges_volt1[i + 1] + edges_volt1[i]) / 2

    plt.figure(figsize=(10,10))
    plt.step(edges_volt1, all_event, label="Événements capteur primaire", color='grey')
    plt.step(edges_volt1, non_coincident, label="Événement autres", color='green')
    plt.step(edges_volt1, coincident, label="Événements captés simultanément", color='red')
    plt.errorbar(edges_err, coincident, yerr=coincident_err, fmt='none', color='red')
    plt.legend()
    plt.xlabel('Tension [mV]')
    plt.ylabel('Taux / classe [s^-1]')
    plt.xscale('log')
    plt.grid(which='both', linestyle='--', linewidth=0.2, color='grey')
    plt.ylim(0, 0.14)

    if input_temps_mort == 'y' or input_temps_mort == 'Y':
        plt.title('Nombre de muons détectés par niveau de tension (Rectification pour les temps morts)')
    else:
        plt.title('Nombre de muons détectés par niveau de tension')

    input_is_fichier = input("Créer un fichier ? [y/N]")
    if input_is_fichier == "y" or input_is_fichier == "Y":
        plt.savefig("app3_fig.png")
    else:
        plt.show()


if __name__ == '__main__':
    main()
