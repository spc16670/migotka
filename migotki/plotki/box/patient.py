import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from migotki.common import first_and_last_data, first_last_and_independent_data
from contants import BOXPLOT
from dao import PATIENTS

TYPE = BOXPLOT




def _donnings(patients: list, sessions: list, title: str, linears=False):
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

    width = 0.7 if len(sessions) > 6 else 2
    ax.boxplot(data, labels=session_str, positions=sessions, widths=width)
    ax.set_title(title)
    ax.set_xticks(sessions)
    ticks = np.arange(0, 65, 5)
    ax.set_yticks(ticks[1:])
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlabel('Session Number')
    ax.set_ylabel('Donning Time (min)')

    if linears:
        """
        on r^2: https://uk.mathworks.com/help/matlab/data_analysis/linear-regression.html
        :param patients:
        :param sessions:
        :param title:
        :return:
        """
        y = [np.median(t) for t in data]
        x = sessions
        # linear regression
        coeffs = np.polyfit(x, y, 1)
        lin_a = coeffs[1]
        lin_a_round = round(lin_a, 3)
        lin_b = coeffs[0]
        lin_b_round = round(lin_b, 3)
        p = np.poly1d(coeffs)

        # r2
        # https://stackoverflow.com/questions/893657/how-do-i-calculate-r-squared-using-python-and-numpy
        yhat = p(x)  # or [p(z) for z in x]
        ybar = np.sum(y) / len(y)  # or sum(y)/len(y)
        ssreg = np.sum((yhat - ybar) ** 2)  # or sum([ (yihat - ybar)**2 for yihat in yhat])
        sstot = np.sum((y - ybar) ** 2)  # or sum([ (yi - ybar)**2 for yi in y])
        lin_r_squared = ssreg / sstot
        lin_r_squared_round = round(lin_r_squared, 3)

        plt.plot(x, y, 'yo', x, p(x), '--k')
        # yo is yellow dot, --k is dashed black line (see https://www.mathworks.com/help/matlab/ref/linespec.html)
        plt.xlim(-1, max(x) + 2)
        plt.ylim(5)

        # logarithmic regression
        def func(t, a, b):
            return a + b * np.log(t)

        import scipy.optimize
        popt, pcov = scipy.optimize.curve_fit(func, x, y)
        log_a = popt[0]
        log_a_round = round(log_a, 3)
        log_b = popt[1]
        log_b_round = round(log_b, 3)
        trialX = np.linspace(x[0], x[-1], 20)
        ylog = func(trialX, *popt)

        # r2
        # https://stackoverflow.com/questions/19189362/getting-the-r-squared-value-using-curve-fit
        residuals = y - func(x, *popt)
        ss_res = np.sum(residuals ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        log_r_squared = 1 - (ss_res / ss_tot)
        log_r_squared_round = round(log_r_squared, 3)

        plt.plot(trialX, ylog, 'r-', ls='--')

        # legend
        lin = mpatches.Patch(color='black', label="y=a+bx\na={}, b={}\n$r^2={}$".format(lin_a_round, lin_b_round, lin_r_squared_round))
        log = mpatches.Patch(color='red', label="y=a+bln(x)\na={}, b={}\n$r^2={}$".format(log_a_round, log_b_round, log_r_squared_round))
        plt.legend(handles=[lin, log])

    plt.show()


def plot_patient_donning_first_last_training():
    patients = [p for p in PATIENTS if p.name != 'p9']
    title = [p.name.upper() for p in patients]
    _first_and_last('Patients ' + ", ".join(title), 'Donning', 'Donning', 'total', np.arange(0, 80, 10), True, patients)


def plot_patient_donning_all_s_1_5_10_14():
    patients = [p.name for p in PATIENTS]
    _donnings(patients, [1, 5, 10, 14], "All Patients - Donning At Select Sessions")


def plot_patient_donning_all_s_1_5_10_14_linear_regression():
    # add linear regression
    patients = [p.name for p in PATIENTS]
    _donnings(patients, [1, 5, 10, 14], "All Patients - Donning At Select Sessions", True)


def plot_patient_donning_p2_p5_p8_s_all():
    patients = [p.name for p in PATIENTS if p.name in ['p2', 'p5', 'p8']]
    _donnings(patients, range(1, 16), "P2 P5 P8 - Donning Time", True)


def _first_and_last(title, y_label, key, indicator, ticks=None, with_wilcoxon=False, patients=None):
    firsts, lasts, common, p = first_and_last_data(key, indicator, patients)
    fig, ax = plt.subplots()
    ax.boxplot([firsts, lasts], labels=['First Training', 'Last Training'])
    ax.set_title(title)
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlabel('Session')
    ax.set_ylabel(y_label)
    if ticks is not None:
        ax.set_yticks(ticks)
    if with_wilcoxon:
        wx = mpatches.Patch(color='red', label="Wilcoxon p-value={}".format(p))
        plt.legend(handles=[wx])
    plt.show()


def plot_patient_donning_all_s_first_last_10_14_log_regression():
    title = 'Patient Donning'
    key = 'Donning'
    indicator = 'total'
    sessions = [10, 14]
    firsts, lasts, common, p = first_and_last_data(key, indicator)

    patient_donnings = [p.data[key] for p in PATIENTS]
    session_dict = {}
    for s in sessions:
        session_dict[s] = []
    for s in session_dict:
        for donnings in patient_donnings:
            session_dict[s].extend([d['total'] for d in donnings if d['session'] == s])
    data = [firsts, lasts, session_dict[10], session_dict[14]]

    fig, ax = plt.subplots()

    x = [2, 6, 10, 14]
    ax.set_xticks(x)

    ax.boxplot(data, positions=x, labels=['First Training', 'Last Training', '10', '14'])
    ax.set_title(title)
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlabel('Session')
    ax.set_ylabel('Time (minutes)')
    y_ticks = np.arange(0, 65, 5)
    ax.set_yticks(y_ticks[1:])

    # logarithmic regression
    y = [np.median(t) for t in data]

    def func(t, a, b):
        return a + b * np.log(t)

    import scipy.optimize
    popt, pcov = scipy.optimize.curve_fit(func, x, y)
    log_a = popt[0]
    log_a_round = round(log_a, 3)
    log_b = popt[1]
    log_b_round = round(log_b, 3)
    trialX = np.linspace(x[0], x[-1], 20)
    ylog = func(trialX, *popt)

    # r2
    # https://stackoverflow.com/questions/19189362/getting-the-r-squared-value-using-curve-fit
    residuals = y - func(x, *popt)
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    log_r_squared = 1 - (ss_res / ss_tot)
    log_r_squared_round = round(log_r_squared, 3)

    plt.plot(trialX, ylog, 'r-', ls='--')

    # legend
    wilcoxson_text = "Wilcoxon p-value={}".format(p)
    # wx = mpatches.Patch(color='blue', label=wilcoxson_text)
    log = mpatches.Patch(color='red', label="y=a+bln(x)\na={}, b={}\n$r^2={}$".format(log_a_round, log_b_round, log_r_squared_round))
    plt.legend(handles=[log])

    ax.annotate(wilcoxson_text, xy=(0.2, 0.75), xytext=(0.2, 0.85), xycoords='axes fraction',
                fontsize=10, ha='center', va='bottom',
                bbox=dict(boxstyle='square', fc='white'),
                arrowprops=dict(arrowstyle='-[, widthB=5.5, lengthB=1', lw=1.0))

    plt.show()


def plot_patient_nasa_first_last_training():
    _first_and_last('All Patients - Workload', 'Workload', 'NASA_TLX', 'total', np.arange(0, 130, 10), True)


def plot_patient_stress_first_last_training():
    _first_and_last('All Patients - Stress', 'Stress', 'SAndS', 'stress', np.arange(0, 11, 1), True)


def plot_patient_satisfaction_first_last_training():
    _first_and_last('All Patients - Satisfaction', 'Satisfaction', 'SAndS', 'satisfaction', np.arange(0, 11, 1), True)


def _first_and_last_training_and_independent_bla_bla(title, ylabel, indicator, key, ticks=None):
    patient_ids = ['p2', 'p5', 'p8']
    patients = [p for p in PATIENTS if p.name in patient_ids]
    training_firsts, training_lasts, independent_firsts, independent_lasts = first_last_and_independent_data(
        key, indicator, patients)
    fig, ax = plt.subplots()
    ax.boxplot([training_firsts, training_lasts, independent_firsts, independent_lasts],
               labels=['First Training', 'Last Training', 'First Independent', 'Last Independent'])
    ax.set_title(title)
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlabel('Session')
    ax.set_ylabel(ylabel)
    if ticks is not None:
        ax.set_yticks(ticks)
    plt.show()


def plot_patient_nasa_first_last_training_and_independent():
    _first_and_last_training_and_independent_bla_bla(
        'P2 P5 P8 - Workload', 'Workload', 'NASA_TLX', 'total', np.arange(0, 130, 10))


def plot_patient_stress_first_last_training_and_independent():
    _first_and_last_training_and_independent_bla_bla(
        'P2 P5 P8 - Stress', 'Stress', 'SAndS', 'stress', np.arange(0, 11, 1))


def plot_patient_satisfaction_first_last_training_and_independent():
    _first_and_last_training_and_independent_bla_bla(
        'P2 P5 P8 - Satisfaction', 'Satisfaction', 'SAndS', 'satisfaction', np.arange(0, 11, 1))


def plot_patient_nasa_last_training_and_independent():
    training_lasts = []
    patient_session = {}
    for sid in range(1, 11):
        patient_session[sid] = []
    patient_ids = ['p2', 'p5', 'p8']
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
    ax.set_title('P2 P5 P8 - Workload')
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
                l = p.upper() + k
                labels.append(l)

    fig, ax = plt.subplots()
    ax.boxplot(data, labels=labels)
    ax.set_title("ROMS ({})".format(side))
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlabel('Patients')
    ax.set_ylabel('Degrees')
    plt.show()


def plot_rom_l():
    _rom('L')


def plot_rom_r():
    _rom('R')


def _fes(predicate, names, sort_sessions, arrangement=None):
    feses = {}
    for p in PATIENTS:
        if p.name in names:
            feses[p.name] = {'labels': [], 'data': []}
            fes = p.data['FES_times']
            for f in fes:
                feses[p.name]['labels'].append(str(f['session']))
                d = []
                for v in f['times_for_activation']:
                    if not np.isnan(v):
                        if predicate(v):
                            d .append(v)
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
        labels = [len(d) for d in data] if sort_sessions else v['labels']
        zipped = zip(labels, data)
        srt = sorted(zipped, key=lambda x: x[0]) if sort_sessions else list(zipped)
        srt = [(k, v) for (k, v) in srt if v]
        sorted_labels = [v[0] for v in srt]
        sorted_values = [v[1] for v in srt]
        series.append([sorted_labels, sorted_values])

    if arrangement is None:
        arrangement = {'nrows': 2, 'ncols': 4}
    fig, axes = plt.subplots(**arrangement)
    for ix, ax in enumerate(axes.flat):
        s = series[ix]
        ax.boxplot(s[1], labels=s[0])
        key = keys[ix]
        ax.set_title("Time For Activation ({})".format(key.upper()))
        ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
        ax.set_axisbelow(True)
        ax.set_xlabel('Sessions')
        ax.set_ylabel('Time (s)')
    plt.show()


def plot_fes_all_s1_5():
    patients = [p.name for p in PATIENTS]
    sessions = np.arange(1, 6)
    stats = {}

    for session in sessions:
        data = []
        for p in PATIENTS:
            if p.name in patients:
                p_data = {}
                pf_data = [f['times_for_activation'] for f in p.data['FES_times'] if f['session'] == session]
                pf_data = np.array(pf_data).flatten().tolist()
                pf_data = [t for t in pf_data if not np.isnan(t)]
                p_data[p.name] = pf_data
                data.append(p_data)
        stats[str(session)] = data
    for session, v in stats.items():
        print(session + '\n')
        for pdata in v:
            for patient, data in pdata.items():
                print('  ', patient, len(data))

    fes = [p.data['FES_times'] for p in PATIENTS if p.name in patients]
    fes = np.concatenate(fes).ravel().tolist()
    feses = {}
    for session in sessions:
        tfa = [f['times_for_activation'] for f in fes if f['session'] == session]
        flat = np.concatenate(tfa).ravel().tolist()
        filtered = [t for t in flat if not np.isnan(t)]
        feses[str(session)] = filtered
        print(session, 'plotting', len(filtered), 'values')

    data = list(feses.values())
    labels = [k for k in list(feses.keys())]
    fig, ax = plt.subplots()
    ax.boxplot(data, labels=labels)
    ax.set_title('Times for Activation')
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlabel('Session')
    ax.set_ylabel('Time (s)')
    plt.show()


def plot_fes_all_p2_p3():
    _fes(lambda a: True, ['p2', 'p3'], False, {'nrows': 1, 'ncols': 2})


def plot_fes_all_p4_p5():
    _fes(lambda a: True, ['p4', 'p5'], False, {'nrows': 1, 'ncols': 2})


def plot_fes_all_p6_p7():
    _fes(lambda a: True, ['p6', 'p7'], False, {'nrows': 1, 'ncols': 2})


def plot_fes_all_p8_p9():
    _fes(lambda a: True, ['p8', 'p9'], False, {'nrows': 1, 'ncols': 2})


def plot_fes_all_sorted():
    _fes(lambda a: True, [p.name for p in PATIENTS], True)


def plot_fes_greater_than_1_2_sorted():
    _fes(lambda a: a >= 1.2, [p.name for p in PATIENTS], True)


def plot_fes_greater_than_1_2():
    _fes(lambda a: a >= 1.2, [p.name for p in PATIENTS], False)


def plot_tpr_range_for_each_patient():
    data = {}
    for p in PATIENTS:
        trials = p.data['BCIFES_Trials']
        data[p.name] = []
        for t in trials:
            tpr = p.get_tpr(t)
            if not np.isnan(tpr):
                data[p.name].append(tpr)
    y = list(data.values())
    labels = [k for k in list(data.keys())]
    fig, ax = plt.subplots()
    ax.boxplot(y, labels=labels)
    ax.set_xlabel("Patients")
    ax.set_ylabel("TPR Value")
    plt.title("TPR Values For Each Patient Across Sessions")
    plt.show()


def plot_average_tpr_for_each_patient():
    data = []
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
        data.append((count, pctg))

    srt = sorted(data, key=lambda x: x[0])
    counts, y = zip(*srt)
    fig, ax = plt.subplots()
    ax.boxplot(srt, labels=counts)
    ax.set_xlabel("Number of Sessions")
    ax.set_ylabel("Average True Positive Rate (%)")
    plt.title("Average TPR For All Sessions Of Each Patient")
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

    srt = sorted(data, key=lambda x: x[0])
    counts, y = zip(*srt)
    fig, ax = plt.subplots()
    ax.boxplot(srt, labels=counts)
    ax.set_xlabel("Number of Sessions")
    ax.set_ylabel("Average False Detection Rate (%)")
    plt.title("Average FDR For All Sessions Of Each Patient")
    plt.show()


def plot_final_threshold_all_patients():
    data = {}
    for p in PATIENTS:
        thresholds = p.data['Threshold']
        tdata = []
        for t in thresholds:
            last = t['threshold'][-1]
            if not np.isnan(last):
                tdata.append(last)
        data[p.name] = tdata

    y = list(data.values())
    labels = [k for k in list(data.keys())]
    fig, ax = plt.subplots()
    ax.boxplot(y, labels=labels)
    ax.set_title('Threshold Values Used by Patients')
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlabel('Patient')
    ax.set_ylabel('Threshold (V^2/Hz')
    plt.show()