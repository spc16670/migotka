import numpy as np
import matplotlib.pyplot as plt

from dao import PATIENTS


def plot_average_tpr_for_each_patient():
    data = []
    for p in PATIENTS:
        trials = p.data['BCIFES_Trials']
        avg = 0
        count = len(trials)
        for t in trials:
            tpr = p.get_tpr(t)
            if not np.isnan(tpr):
                avg += tpr
            else:
                count -= 1
        pctg = avg / count * 100
        data.append((count, pctg))

    x, y = zip(*data)
    print(data)
    plt.xticks(range(len(x)), x)
    plt.bar(x, y, color='green')
    #ax.set_xticklabels([str(l) for l in x])
    #ax.set_xlabel("Number of Sessions")
    plt.ylabel("Average True Positive Rate (%)")
    plt.title("Average TPR for  Each patient")
    plt.show()
