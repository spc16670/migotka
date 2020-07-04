import numpy as np
import matplotlib.pyplot as plt

from contants import SCATTERPLOT
from dao import CARERS
from dao import PATIENTS

TYPE = SCATTERPLOT

def plot_carer_workload():

    x = []
    y = []
    for id in range(2, 10):
        c_name = "c" + str(id)
        carer = [c for c in CARERS if c.name == c_name][0]
        carer_data = carer.data['NASA_TLX']
        p_name = "p" + str(id)
        patient = [p for p in PATIENTS if p.name == p_name][0]
        patient_data = patient.data['Donning']
        for c_ix, c_session in enumerate(carer_data):
            p_session = patient_data[c_ix]
            donning = p_session['total']
            demand = c_session['mental_demand']
            if np.isnan(donning) or np.isnan(demand):
                continue
            else:
                y.append(donning)
                x.append(demand)

    colors = (0, 0, 0)
    area = np.pi * 3

    plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    plt.xlabel('Mental demand')
    plt.ylabel('Donning')
    plt.show()
