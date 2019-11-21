import numpy as np
import matplotlib.pyplot as plt

from dao import PATIENTS


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
    ax.set_xlabel('Session')
    ax.set_ylabel('Donning Time (min)')
    plt.show()


def plot_patient_donning_all_s_1_5_10_14():
    patients = [p.name for p in PATIENTS]
    _donnings(patients, [1, 5, 10, 14])


def plot_patient_donning_p2_p5_p8_s_all():
    patients = [p.name for p in PATIENTS if p.name in ['p2', 'p5', 'p8']]
    _donnings(patients, range(1, 16))


def plot_patient_nasa_first_last_training():
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
    ax.boxplot([firsts, lasts], labels=['First Training', 'Last Training'])
    ax.set_title("NASA TLX Total Workload")
    ticks = np.arange(0, 140, 20)
    ax.set_yticks(ticks[1:])
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlabel('Session')
    ax.set_ylabel('Workload')
    plt.show()


def plot_patient_nasa_first_last_training_and_independent():
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
    ax.set_title("NASA TLX Total Workload " + ",".join(patient_ids))
    ticks = np.arange(0, 140, 20)
    ax.set_yticks(ticks[1:])
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlabel('Session')
    ax.set_ylabel('Workload')
    plt.show()


def plot_patient_nasa_last_training_and_independent():
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
    ax.set_title("NASA TLX Total Workload " + ",".join(patient_ids))
    ticks = np.arange(0, 140, 20)
    ax.set_yticks(ticks[1:])
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlabel('Session')
    ax.set_ylabel('Workload')
    plt.show()


def _rom(side):
    roms = dict()
    for p in PATIENTS:
        roms[p.name] = {'i': [], 'f': []}
        for t in p.data['ROM_initial']:
            if t['type'] == side:
                rom = t['flexion'] - t['extension']
                if not np.isnan(rom):
                    roms[p.name]['i'].append(rom)
        for t in p.data['ROM_final']:
            if t['type'] == side:
                rom = t['flexion'] - t['extension']
                if not np.isnan(rom):
                    roms[p.name]['f'].append(rom)
    data = []
    labels = []
    for p, d in roms.items():
        for k in d.keys():
            if d[k]:
                data.append(d[k])
                l = p + k
                labels.append(l)

    fig, ax = plt.subplots()
    ax.boxplot(data, labels=labels)
    ax.set_title("Range of Motion ({})".format(side))
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlabel('Patients')
    ax.set_ylabel('Degrees')
    plt.show()


def plot_rom_l():
    _rom('L')


def plot_rom_r():
    _rom('R')


def _fes(predicate):
    feses = {}
    for p in PATIENTS:
        feses[p.name] = {'labels': [], 'data': []}
        fes = p.data['FES_times']
        for f in fes:
            feses[p.name]['labels'].append(str(f['session']))
            d = [v for v in f['times_for_activation'] if predicate(v)]
            feses[p.name]['data'].append(d)

    keys = list(feses.keys())
    # Turn
    # { 'p2': {'labels': [], 'data': []} }
    # to
    # [ p[ l[], d[] ], p[ ... ]... ]
    series = []
    for k, v in feses.items():
        data = v['data']
        # instead of session labels use trial counts
        labels = [len(d) for d in data]
        zipped = zip(labels, data)
        srt = sorted(zipped, key=lambda x: x[0])
        sorted_labels = [v[0] for v in srt]
        sorted_values = [v[1] for v in srt]
        series.append([sorted_labels, sorted_values])

    fig, axes = plt.subplots(2, 4)
    for ix, ax in enumerate(axes.flat):
        s = series[ix]
        ax.boxplot(s[1], labels=s[0])
        key = keys[ix]
        ax.set_title("Time per activation ({})".format(key))
        ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
        ax.set_axisbelow(True)
        ax.set_xlabel('Sessions')
        ax.set_ylabel('Time (s)')
    plt.show()


def plot_times_for_activation_all():
    _fes(lambda a: True)


def plot_times_for_activation_greater_than_1_2():
    _fes(lambda a: a >= 1.2)

