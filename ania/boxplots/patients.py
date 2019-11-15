import numpy as np
import matplotlib.pyplot as plt

from dao import PATIENTS


def donning_all_s_1_5_10_14():
    patients = [p.name for p in PATIENTS]
    _donnings(patients, [1, 5, 10, 14])


def donning_p2_p5_p8_s_all():
    patients = [p.name for p in PATIENTS if p.name in ['p2', 'p5', 'p8']]
    _donnings(patients, range(1, 16))


def _donnings(patients: list, sessions: list):
    patient_donnings = [p.data['Donning'] for p in PATIENTS if p.name in patients]
    session_dict = {}
    for s in sessions:
        session_dict[s] = []
    for s in session_dict:
        for donnings in patient_donnings:
            session_dict[s].extend([d['total'] for d in donnings if d['session'] == s])
    data = list(session_dict.values())
    fig, ax = plt.subplots()
    session_str = [str(k) for k in session_dict.keys()]
    ax.boxplot(data, labels=session_str)
    ax.set_title("P-all-S-{}".format(",".join(session_str)))
    ticks = np.arange(0, 65, 5)
    ax.set_yticks(ticks[1:])
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlabel('Session number')
    ax.set_ylabel('Donning time(min)')
    plt.show()


def nasa_first_last_training():
    firsts = []
    lasts = []
    for p in PATIENTS:
        patients_trainings = p.get_training_sessions('NASA_TLX')
        # firsts
        first = patients_trainings[0]
        first_total = first['total']
        if not np.isnan(first_total):
            firsts.append(first_total)
        # lasts
        last = patients_trainings[-1]
        last_total = last['total']
        if not np.isnan(last_total):
            lasts.append(last_total)
    fig, ax = plt.subplots()
    ax.boxplot([firsts, lasts], labels=['First', 'Last'])
    ax.set_title("NasaX sessions")
    ticks = np.arange(0, 140, 20)
    ax.set_yticks(ticks[1:])
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlabel('Session')
    ax.set_ylabel('Total')
    plt.show()


def nasa_first_last_training_and_independent():
    training_firsts = []
    independent_firsts = []
    training_lasts = []
    independent_lasts = []
    patient_ids = ['p2', 'p5', 'p8']
    patients = [p for p in PATIENTS if p.name in patient_ids]
    for p in patients:
        # training
        patients_trainings = p.get_training_sessions('NASA_TLX')
        first = patients_trainings[0]
        first_total = first['total']
        if not np.isnan(first_total):
            training_firsts.append(first_total)
        last = patients_trainings[-1]
        last_total = last['total']
        if not np.isnan(last_total):
            training_lasts.append(last_total)
        # independent
        nasa = p.data['NASA_TLX']
        s_ix = p.data['Training_sessions']
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
    ax.set_title("NasaX sessions " + ",".join(patient_ids))
    ticks = np.arange(0, 140, 20)
    ax.set_yticks(ticks[1:])
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlabel('Session')
    ax.set_ylabel('Total')
    plt.show()


def nasa_last_training_and_independent():
    patient_ids = ['p2', 'p5', 'p8']
    training_lasts = []
    patient_session = {}
    for sid in range(1, 11):
        patient_session[sid] = []
    patients = [p for p in PATIENTS if p.name in patient_ids]
    for p in patients:
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
                patient_session[ix+1].append(s_independent_total)

    data = [training_lasts] + list(patient_session.values())
    labels = ['Last Training'] + [str(k) for k in list(patient_session.keys())]
    fig, ax = plt.subplots()
    ax.boxplot(data, labels=labels)
    ax.set_title("NasaX sessions " + ",".join(patient_ids))
    ticks = np.arange(0, 140, 20)
    ax.set_yticks(ticks[1:])
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlabel('Session')
    ax.set_ylabel('Total')
    plt.show()