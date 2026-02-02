import numpy as np                  # Gestion de donnees
import matplotlib.pyplot as plt     # Gestion de graphiques
import argparse as ap               # Entree de parametres

data1_file_name = './S2GE_APP3_Problematique_Detecteur_Primaire.csv'
data2_file_name = './S2GE_APP3_Problematique_Detecteur_Secondaire.csv'

data1 = np.loadtxt(data1_file_name, delimiter=',', skiprows=1)
data2 = np.loadtxt(data2_file_name, delimiter=',', skiprows=1)
hist_bins = 20

data1_volt_max = data1[0][2]
data1_volt_min = data1[0][2]

for i in range(len(data1)):
    if data1[i][2] > data1_volt_max:
        data1_volt_max = data1[i][2]
    if data1[i][2] < data1_volt_min:
        data1_volt_min = data1[i][2]
print(data1_volt_max, data1_volt_min)

data1_hist_range = (data1_volt_max - data1_volt_min)/hist_bins
data1_volt = np.zeros(len(data1))
for i in range(len(data1)):
    data1_volt[i] = data1[i][2]

counts, bins = np.histogram(data1_volt)
plt.figure(figsize=(10,10))
plt.stairs(counts, bins)
plt.show()
