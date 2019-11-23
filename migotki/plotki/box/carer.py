import numpy as np
import matplotlib.pyplot as plt

from dao import CARERS


def plot_carer_nasa_first_last_training():
    firsts = []
    lasts = []
    for c in CARERS:
        patients_trainings = c.get_training_sessions('NASA_TLX')
        first = patients_trainings[0]
        first_total = first['total']
        if not np.isnan(first_total):
            firsts.append(first_total)
        last = patients_trainings[-1]
        last_total = last['total']
        if not np.isnan(last_total):
            lasts.append(last_total)
    fig, ax = plt.subplots()
    ax.boxplot([firsts, lasts], labels=['First Training', 'Last Training'])
    ax.set_title("NASA TLX Total Workload")
    ticks = np.arange(0, 140, 20)
    ax.set_yticks(ticks[1:])
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlabel('Session')
    ax.set_ylabel('Workload')
    plt.show()


def plot_carer_nasa_first_last_training_and_independent():
    training_firsts = []
    independent_firsts = []
    training_lasts = []
    independent_lasts = []
    carer_ids = ['c2', 'c5', 'c8']
    carers = [p for p in CARERS if p.name in carer_ids]
    for c in carers:
        # training
        carer_trainings = c.get_training_sessions('NASA_TLX')
        first = carer_trainings[0]
        first_total = first['total']
        if not np.isnan(first_total):
            training_firsts.append(first_total)
        last = carer_trainings[-1]
        last_total = last['total']
        if not np.isnan(last_total):
            training_lasts.append(last_total)
        # independent
        nasa = c.data['NASA_TLX']
        s_ix = c.data['Training_sessions']
        independent = nasa[s_ix:]
        first_independent = independent[0]
        first_independent_total = first_independent['total']
        if not np.isnan(first_independent_total):
            independent_firsts.append(first_independent_total)
        last_independent = independent[-1]
        last_independent_total = last_independent['total']
        if not np.isnan(last_independent_total):
            independent_lasts.append(last_independent_total)

    fig, ax = plt.subplots()
    ax.boxplot([training_firsts, training_lasts, independent_firsts, independent_lasts],
               labels=['First Training', 'Last Training', 'First Independent', 'Last Independent'])
    ax.set_title("NASA TLX Total Workload " + ",".join(carer_ids))
    ticks = np.arange(0, 140, 20)
    ax.set_yticks(ticks[1:])
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlabel('Session')
    ax.set_ylabel('Workload')
    plt.show()


def plot_carer_nasa_last_training_and_independent():
    carer_ids = ['c2', 'c5', 'c8']
    training_lasts = []
    carer_session = {}
    for sid in range(1, 11):
        carer_session[sid] = []
    carers = [p for p in CARERS if p.name in carer_ids]
    for p in carers:
        nasa = p.data['NASA_TLX']
        s_ix = p.data['Training_sessions']
        last_training_session = nasa[s_ix-1]
        last_total = last_training_session['total']
        if not np.isnan(last_total):
            training_lasts.append(last_total)
        independent_sessions = nasa[s_ix:]
        for ix, s in enumerate(independent_sessions):
            s_independent_total = s['total']
            if not np.isnan(s_independent_total):
                carer_session[ix+1].append(s_independent_total)

    data = [training_lasts] + list(carer_session.values())
    labels = ['Last Training'] + [str(k) for k in list(carer_session.keys())]
    fig, ax = plt.subplots()
    ax.boxplot(data, labels=labels)
    ax.set_title("NASA TLX Total Workload " + ",".join(carer_ids))
    ticks = np.arange(0, 140, 20)
    ax.set_yticks(ticks[1:])
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlabel('Session')
    ax.set_ylabel('Workload')
    plt.show()
