
import numpy as np
import matplotlib.pyplot as plt

# https://matplotlib.org/3.1.1/gallery/pyplots/boxplot_demo_pyplot.html#sphx-glr-gallery-pyplots-boxplot-demo-pyplot-py
# https://matplotlib.org/examples/pylab_examples/boxplot_demo2.html

from models.patient import load as load_patients
from models.carer import load as load_carers



def donning():
    p2 = load_patients()[0]
    data = [d['total'] for d in p2.data['Donning']]
    fig7, ax7 = plt.subplots()
    ax7.boxplot(data, labels=['p2'])
    ax7.set_title("Donning total across {} sessions".format(len(data)))
    ax7.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax7.set_axisbelow(True)
    ax7.set_xlabel('Patients')
    ax7.set_ylabel('Donning total')
    plt.show()


def plot():
    carers = load_carers()
    print("\n----------------------\n" + str(carers))


def plot2():
    #patients = load_patients()
    np.random.seed(19680801)
    spread = np.random.rand(50) * 100
    print("Spread is {}\n".format(str(spread)))
    center = np.ones(25) * 50
    print("Center is {}\n".format(str(center)))
    flier_high = np.random.rand(10) * 100 + 100
    print("flier_high is {}\n".format(str(flier_high)))
    flier_low = np.random.rand(10) * -100
    print("flier_low is {}\n".format(str(flier_low)))
    p1 = np.concatenate((spread, center, flier_high, flier_low))
    p1.shape = (-1, 1)


    spread = np.random.rand(50) * 100
    print("spread2 is {}\n".format(str(spread)))
    center = np.ones(25) * 40
    print("center2 is {}\n".format(str(center)))
    flier_high = np.random.rand(10) * 100 + 100
    print("flier_high2 is {}\n".format(str(flier_high)))
    flier_low = np.random.rand(10) * -100
    print("flier_low2 is {}\n".format(str(flier_low)))
    p2 = np.concatenate((spread, center, flier_high, flier_low))
    p2.shape = (-1, 1)


    p3 = p2[::2, 0]
    boxplot_data = [p1, p2, p3]
    fig7, ax7 = plt.subplots()
    ax7.set_title('Multiple Samples with Different sizes')
    ax7.boxplot(boxplot_data)
    plt.show()


plot()
