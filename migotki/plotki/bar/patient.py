import numpy as np
import matplotlib.pyplot as plt

from contants import BARCHART
from dao import PATIENTS

TYPE = BARCHART


def plot_average_tpr_for_each_patient():
    data = []
    error = []
    for p in PATIENTS:
        trials = p.data['BCIFES_Trials']
        sum = 0
        tprs = []
        count = len(trials)
        for t in trials:
            tpr = p.get_tpr(t)
            if not np.isnan(tpr):
                sum += tpr
                tprs.append(tpr)
            else:
                count -= 1
        pctg = sum / count * 100
        err = np.std(tprs) * 100
        error.append(err)
        data.append((count, pctg))

    counts, y = zip(*data)
    fig, ax = plt.subplots()
    x = range(len(counts))
    ax.bar(x, y, color='green', yerr=error, align="center", alpha=.5)
    ax.set_xticks(x)
    ax.set_xticklabels(counts)
    ax.set_xlabel("Number of Sessions")
    ax.set_ylabel("Average True Positive Rate (%)")
    plt.title("Average TPR for  Each patient")
    plt.show()


def plot_average_fdr_for_each_patient():
    data = []
    error = []
    for p in PATIENTS:
        trials = p.data['BCIFES_Trials']
        sum = 0
        tprs = []
        count = len(trials)
        for t in trials:
            tpr = p.get_fdr(t)
            if not np.isnan(tpr):
                sum += tpr
                tprs.append(tpr)
            else:
                count -= 1
        pctg = sum / count * 100
        err = np.std(tprs) * 100
        error.append(err)
        data.append((count, pctg))

    counts, y = zip(*data)
    fig, ax = plt.subplots()
    x = range(len(counts))
    ax.bar(x, y, color='green', yerr=error, align="center", alpha=.5)
    ax.set_xticks(x)
    ax.set_xticklabels(counts)
    ax.set_xlabel("Number of Sessions")
    ax.set_ylabel("Average True Positive Rate (%)")
    plt.title("Average FDR for  Each patient")
    plt.show()