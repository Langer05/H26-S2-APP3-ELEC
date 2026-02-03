import numpy as np                  # Gestion de donnees
import matplotlib.pyplot as plt     # Gestion de graphiques
import argparse as ap               # Entree de parametres

from scipy.ndimage import label
print('---------- Étape 1 & 2 ----------')

data1_file_name = './S2GE_APP3_Problematique_Detecteur_Primaire.csv'
data2_file_name = './S2GE_APP3_Problematique_Detecteur_Secondaire.csv'

data1 = np.loadtxt(data1_file_name, delimiter=',', skiprows=1) # Load les donnees primaires dans une matrice
data2 = np.loadtxt(data2_file_name, delimiter=',', skiprows=1) # Load les donnees secondaires dans une matrice

data1_volt_max = data1[0][2]
data1_volt_min = data1[0][2]
data2_volt_max = data2[0][2]
data2_volt_min = data2[0][2]

data1_volt = np.zeros(len(data1))
for i in range(len(data1)):
    data1_volt[i] = data1[i][2]

data2_volt = np.zeros(len(data2))
for i in range(len(data2)):
    data2_volt[i] = data2[i][2]

data1_volt_max = data1_volt.max()
data1_volt_min = data1_volt.min()
data2_volt_max = data2_volt.max()
data2_volt_min = data2_volt.min()


nb_hist_bins = 500 # Valeur nombre de bins dans l'histogramme
width_bins_volt1 = np.logspace(start = 0, stop = data1_volt_max,
                               num = nb_hist_bins, base = 10)
width_bins_volt2 = np.logspace(start = 0, stop = data2_volt_max,
                               num = nb_hist_bins, base = 10)

print(data1_volt.shape, '\t\t', width_bins_volt1.shape)

hist_volt1, edge_bins_volt1 = np.histogram(a = data1_volt, bins = nb_hist_bins)


plt.figure(figsize=(10,10))
plt.stairs(values = hist_volt1, edges = edge_bins_volt1)
#plt.hist(data1_volt, bins=nb_hist_bins, histtype='step', color='blue', alpha=1, label='CSV1')
#plt.hist(data2_volt, bins=nb_hist_bins, histtype='step', color='red', alpha=1, label='CSV2')
print('Nombre de conetenant : ', nb_hist_bins)
plt.xscale('log')
plt.ylabel('Quantité / conetenant')
plt.xlabel('Tension (mV)')
plt.title('Quantité de tension détecté')
plt.grid()
#plt.legend()
plt.show()

print('Valeur maximale : ', data1_volt_max, '\tValeur minimale', data1_volt_min)

print('---------- Étape ----------')

