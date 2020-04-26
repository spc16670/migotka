import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from migotki.common import first_last_and_independent_data, last_and_sessions, first_and_last_data

from contants import BOXPLOT
from dao import CARERS, PATIENTS, OTS

TYPE = BOXPLOT


def plot_patient_and_ot_donning_all_s_1_5_10_14_averaged():
    title = 'Patient and OT Donning'
    p_key = 'Donning'
    p_indicator = 'total'
    sessions = [10, 14]
    p_firsts, p_lasts, _p_common, p_p = first_and_last_data(p_key, p_indicator)
    ot_key = 'donning'
    ot_indicator = 'minutes'
    ot_firsts, ot_lasts, _ot_common, _ot_p = first_and_last_data(ot_key, ot_indicator, OTS)

    patient_donnings = [p.data[p_key] for p in PATIENTS]
    session_dict = {}
    for s in sessions:
        session_dict[s] = []
    for s in session_dict:
        for donnings in patient_donnings:
            session_dict[s].extend([d['total'] for d in donnings if d['session'] == s])

    data = [[ot_firsts, p_firsts], [ot_lasts, p_lasts],  [session_dict[10]], [session_dict[14]]]
    print(data)
    fig, ax = plt.subplots()

    ot_color = 'red'
    patient_color = 'blue'
    x_ticks = []
    patient_x_ticks = []
    patient_x_values = [1, 4.43, 10, 14]
    position = 0
    for pair in data:
        if len(pair) == 2:
            bp = ax.boxplot(pair, positions=[position+1, position+2], widths=0.6, patch_artist=True)
            bp['boxes'][0].set_facecolor(ot_color)
            bp['boxes'][1].set_facecolor(patient_color)
            patient_x_ticks.append(position + 2)
            x_ticks.append(position + 1.5)
        else:
            bp = ax.boxplot(pair, positions=[position+1], widths=0.6, patch_artist=True)
            bp['boxes'][0].set_facecolor(patient_color)
            patient_x_ticks.append(position + 1)
            x_ticks.append(position + 1)
        position = position + 3

    ax.set_ylabel('Time (minutes)')
    ax.set_title(title)
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(('First Training', 'Last Training', '10', '14'))

    ot_label = mpatches.Patch(color=ot_color, label="OT")
    patient_label = mpatches.Patch(color=patient_color, label="Patient")

    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_axisbelow(True)

    # logarithmic regression
    x = patient_x_ticks
    patient_data = [p_firsts, p_lasts, session_dict[10], session_dict[14]]
    y = [np.median(t) for t in patient_data]

    def func(t, a, b):
        return a + b * np.log(t)

    import scipy.optimize
    popt, pcov = scipy.optimize.curve_fit(func, patient_x_values, y)
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
    plt.plot(trialX, ylog, 'y-', ls='--')

    # legend
    wilcoxson_text = "Wilcoxon p-value={}".format(p_p)
    log = mpatches.Patch(linestyle='--', facecolor='yellow',
                         label="y=a+bln(x)\na={}, b={}\n$r^2={}$".format(log_a_round, log_b_round, log_r_squared_round))
    plt.legend(handles=[log, ot_label, patient_label])

    ax.annotate(wilcoxson_text, xy=(0.3, 0.75), xytext=(0.3, 0.90), xycoords='axes fraction',
                fontsize=10, ha='center', va='bottom',
                bbox=dict(boxstyle='square', fc='white'),
                arrowprops=dict(arrowstyle='-[, widthB=5.5, lengthB=1', lw=1.0))

    plt.show()



def plot_patient_and_ot_donning_all_s_1_5_10_14():
    title = 'Patient and OT Donning'
    p_key = 'Donning'
    p_indicator = 'total'
    sessions = [10, 14]
    p_firsts, p_lasts, _p_common, p_p = first_and_last_data(p_key, p_indicator)
    ot_key = 'donning'
    ot_indicator = 'minutes'
    ot_firsts, ot_lasts, _ot_common, _ot_p = first_and_last_data(ot_key, ot_indicator, OTS)

    patient_donnings = [p.data[p_key] for p in PATIENTS]
    session_dict = {}
    for s in sessions:
        session_dict[s] = []
    for s in session_dict:
        for donnings in patient_donnings:
            session_dict[s].extend([d['total'] for d in donnings if d['session'] == s])

    data = [[ot_firsts, p_firsts], [ot_lasts, p_lasts],  [session_dict[10]], [session_dict[14]]]

    fig, ax = plt.subplots()

    ot_color = 'red'
    patient_color = 'blue'
    x_ticks = []
    patient_x_ticks = []
    position = 0
    for pair in data:
        if len(pair) == 2:
            bp = ax.boxplot(pair, positions=[position+1, position+2], widths=0.6, patch_artist=True)
            bp['boxes'][0].set_facecolor(ot_color)
            bp['boxes'][1].set_facecolor(patient_color)
            patient_x_ticks.append(position + 2)
            x_ticks.append(position + 1.5)
        else:
            bp = ax.boxplot(pair, positions=[position+1], widths=0.6, patch_artist=True)
            bp['boxes'][0].set_facecolor(patient_color)
            patient_x_ticks.append(position + 1)
            x_ticks.append(position + 1)
        position = position + 3

    ax.set_ylabel('Time (minutes)')
    ax.set_title(title)
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(('First Training', 'Last Training', '10', '14'))

    ot_label = mpatches.Patch(color=ot_color, label="OT")
    patient_label = mpatches.Patch(color=patient_color, label="Patient")

    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_axisbelow(True)


    # logarithmic regression
    x = patient_x_ticks
    patient_data = [p_firsts, p_lasts, session_dict[10], session_dict[14]]
    y = [np.median(t) for t in patient_data]

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

    plt.plot(trialX, ylog, 'y-', ls='--')

    # legend
    wilcoxson_text = "Wilcoxon p-value={}".format(p_p)
    log = mpatches.Patch(linestyle='--', facecolor='yellow',
                         label="y=a+bln(x)\na={}, b={}\n$r^2={}$".format(log_a_round, log_b_round, log_r_squared_round))
    plt.legend(handles=[log, ot_label, patient_label])

    ax.annotate(wilcoxson_text, xy=(0.3, 0.75), xytext=(0.3, 0.90), xycoords='axes fraction',
                fontsize=10, ha='center', va='bottom',
                bbox=dict(boxstyle='square', fc='white'),
                arrowprops=dict(arrowstyle='-[, widthB=5.5, lengthB=1', lw=1.0))

    plt.show()


def plot_carer_patient_stress_and_satisfaction_first_last_and_independent():
    title = 'Patients and Carers Stress and Satisfaction'
    ylabel = 'Level'
    key_stress = 'stress'
    key_satisfaction = 'satisfaction'
    indicator = 'SAndS'

    # Harvest first adn last training session data for all carers/patients
    c_stress_t_firsts, c_stress_t_lasts, _, _ = first_last_and_independent_data(
        key_stress, indicator, CARERS)
    p_stress_t_firsts, p_stress_t_lasts, _, _ = first_last_and_independent_data(
        key_stress, indicator, PATIENTS)
    c_satisfaction_t_firsts, c_satisfaction_t_lasts, _, _ = first_last_and_independent_data(
        key_satisfaction, indicator, CARERS)
    p_satisfaction_t_firsts, p_satisfaction_t_lasts, _, _ = first_last_and_independent_data(
        key_satisfaction, indicator, PATIENTS)

    # Harvest independent session data for selected carers/patients
    carer_ids = ['c2', 'c5', 'c8']
    carers = [p for p in CARERS if p.name in carer_ids]
    patient_ids = ['p2', 'p5', 'p8']
    patients = [p for p in PATIENTS if p.name in patient_ids]

    _, _, c_stress_i_firsts, c_stress_i_lasts = first_last_and_independent_data(
        key_stress, indicator, carers)
    _, _, p_stress_i_firsts, p_stress_i_lasts = first_last_and_independent_data(
        key_stress, indicator, patients)
    _, _, c_satisfaction_i_firsts, c_satisfaction_i_lasts = first_last_and_independent_data(
        key_satisfaction, indicator, carers)
    _, _, p_satisfaction_i_firsts, p_satisfaction_i_lasts = first_last_and_independent_data(
        key_satisfaction, indicator, patients)

    data = [
        [c_stress_t_firsts, c_satisfaction_t_firsts, p_stress_t_firsts, p_satisfaction_t_firsts],
        [c_stress_t_lasts, c_satisfaction_t_lasts, p_stress_t_lasts, p_satisfaction_t_lasts],
        [c_stress_i_firsts, c_satisfaction_i_firsts, p_stress_i_firsts, p_satisfaction_i_firsts],
        [c_stress_i_lasts, c_satisfaction_i_lasts, p_stress_i_lasts, p_satisfaction_i_lasts],
    ]

    fig, ax = plt.subplots()

    c_stress_color = 'red'
    c_satisfaction_color = 'blue'
    p_stress_color = 'pink'
    p_satisfaction_color = 'purple'
    x_ticks = []
    position = 0
    for pair in data:
        bp = ax.boxplot(pair, positions=[position+1, position+2, position+3, position+4], widths=0.6, patch_artist=True)
        bp['boxes'][0].set_facecolor(c_stress_color)
        #print("Carer Stress", pair[0])
        bp['boxes'][1].set_facecolor(c_satisfaction_color)
        #print("Carer Satisfaction", pair[1])
        bp['boxes'][2].set_facecolor(p_stress_color)
        #print("Patient Stress", pair[2])
        bp['boxes'][3].set_facecolor(p_satisfaction_color)
        #print("Patient Satisfaction", pair[3])
        x_ticks.append(position + 2.5)
        position = position + 6
        print("\n")


    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(('First Training', 'Last Training', 'First Independent', 'Last Independent'))

    p_stress_label = mpatches.Patch(color=p_stress_color, label="Patient Stress")
    p_satisfaction_label = mpatches.Patch(color=p_satisfaction_color, label="Patient Satisfaction")
    c_stress_label = mpatches.Patch(color=c_stress_color, label="Carer Stress")
    c_satisfaction_label = mpatches.Patch(color=c_satisfaction_color, label="Carer Satisfaction")
    plt.legend(handles=[c_stress_label, c_satisfaction_label, p_stress_label, p_satisfaction_label])

    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlabel('Session')

    plt.show()


def plot_carer_patient_workload_first_last_and_independent():
    title = 'Workload - Patients and Carers'
    ylabel = 'Workload'
    indicator = 'NASA_TLX'
    key = 'total'

    c_training_firsts, c_training_lasts, _, _ = first_last_and_independent_data(
        key, indicator, CARERS)
    p_training_firsts, p_training_lasts, _, _ = first_last_and_independent_data(
        key, indicator, PATIENTS)

    carer_ids = ['c2', 'c5', 'c8']
    carers = [p for p in CARERS if p.name in carer_ids]
    _, _, c_independent_firsts, c_independent_lasts = first_last_and_independent_data(
        key, indicator, carers)
    patient_ids = ['p2', 'p5', 'p8']
    patients = [p for p in PATIENTS if p.name in patient_ids]
    _, _, p_independent_firsts, p_independent_lasts = first_last_and_independent_data(
        key, indicator, patients)

    data = [
        [p_training_firsts, c_training_firsts],
        [p_training_lasts, c_training_lasts],
        [p_independent_firsts, c_independent_firsts],
        [p_independent_lasts, c_independent_lasts]
    ]

    fig, ax = plt.subplots()

    c_color = 'lightblue'
    p_color = 'pink'
    position = 0
    x_ticks = []
    for pair in data:
        bp = ax.boxplot(pair, positions=[position+1, position+2], widths=0.6, patch_artist=True)
        bp['boxes'][0].set_facecolor(p_color)
        bp['boxes'][1].set_facecolor(c_color)
        x_ticks.append(position + 1.5)
        position = position + 3

    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(('First Training', 'Last Training', 'First Independent', 'Last Independent'))

    p_label = mpatches.Patch(color=p_color, label="Patient")
    c_label = mpatches.Patch(color=c_color, label="Carer")

    plt.legend(handles=[p_label, c_label])

    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlabel('Session')

    plt.show()


def plot_carer_workload_last_training_and_independent():
    carer_ids = ['c2', 'c5', 'c8']
    carers = [p for p in CARERS if p.name in carer_ids]
    c_lasts, c_session = last_and_sessions(carers, 'NASA_TLX', 'total', 'Training_sessions')
    c_data = [c_lasts] + list(c_session.values())

    patient_ids = ['p2', 'p5', 'p8']
    patients = [p for p in PATIENTS if p.name in patient_ids]
    p_lasts, p_session = last_and_sessions(patients, 'NASA_TLX', 'total', 'Training_sessions')
    p_data = [p_lasts] + list(p_session.values())
    data = zip(c_data, p_data)

    fig, ax = plt.subplots()
    c_color = 'cyan'
    p_color = 'blue'
    position = 0
    x_ticks = []
    for pair in data:
        bp = ax.boxplot(pair, positions=[position+1, position+2], widths=0.6, patch_artist=True)
        bp['boxes'][0].set_facecolor(p_color)
        bp['boxes'][1].set_facecolor(c_color)
        x_ticks.append(position + 1.5)
        position = position + 3

    ax.set_ylabel('Workload')
    ax.set_title('Workload C2, C5, C8, P2, P5, P8')
    ax.set_xticks(x_ticks)
    labels = ['Last Training'] + [str(k) for k in list(c_session.keys())]
    ax.set_xticklabels(labels)

    p_label = mpatches.Patch(color=p_color, label="Patient")
    c_label = mpatches.Patch(color=c_color, label="Carer")
    plt.legend(handles=[p_label, c_label])

    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlabel('Sessions')

    plt.show()

















def plot_carer_patient_stress_first_last_and_independent():
    title = 'Patients and Carers Stress'
    ylabel = 'Level'
    key_stress = 'stress'
    indicator = 'SAndS'

    # Harvest first adn last training session data for all carers/patients
    c_stress_t_firsts, c_stress_t_lasts, _, _ = first_last_and_independent_data(
        key_stress, indicator, CARERS)
    p_stress_t_firsts, p_stress_t_lasts, _, _ = first_last_and_independent_data(
        key_stress, indicator, PATIENTS)

    # Harvest independent session data for selected carers/patients
    carer_ids = ['c2', 'c5', 'c8']
    carers = [p for p in CARERS if p.name in carer_ids]
    patient_ids = ['p2', 'p5', 'p8']
    patients = [p for p in PATIENTS if p.name in patient_ids]

    _, _, c_stress_i_firsts, c_stress_i_lasts = first_last_and_independent_data(
        key_stress, indicator, carers)
    _, _, p_stress_i_firsts, p_stress_i_lasts = first_last_and_independent_data(
        key_stress, indicator, patients)

    data = [
        [c_stress_t_firsts, p_stress_t_firsts],
        [c_stress_t_lasts, p_stress_t_lasts],
        [c_stress_i_firsts, p_stress_i_firsts],
        [c_stress_i_lasts, p_stress_i_lasts],
    ]

    fig, ax = plt.subplots()

    c_stress_color = 'cyan'
    p_stress_color = 'blue'
    x_ticks = []
    position = 0
    for pair in data:
        bp = ax.boxplot(pair, positions=[position+1, position+2], widths=0.6, patch_artist=True)
        bp['boxes'][0].set_facecolor(c_stress_color)
        bp['boxes'][1].set_facecolor(p_stress_color)
        x_ticks.append(position + 1.5)
        position = position + 3
        print("\n")

    ax.set_ylim([-1, 11])
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(('First Training', 'Last Training', 'First Independent', 'Last Independent'))

    p_stress_label = mpatches.Patch(color=p_stress_color, label="Patient Stress")
    c_stress_label = mpatches.Patch(color=c_stress_color, label="Carer Stress")
    plt.legend(handles=[c_stress_label, p_stress_label])

    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlabel('Session')

    plt.show()


def plot_carer_patient_satisfaction_first_last_and_independent():
    title = 'Patients and Carers Satisfaction'
    ylabel = 'Level'
    key_satisfaction = 'satisfaction'
    indicator = 'SAndS'

    # Harvest first adn last training session data for all carers/patients
    c_satisfaction_t_firsts, c_satisfaction_t_lasts, _, _ = first_last_and_independent_data(
        key_satisfaction, indicator, CARERS)
    p_satisfaction_t_firsts, p_satisfaction_t_lasts, _, _ = first_last_and_independent_data(
        key_satisfaction, indicator, PATIENTS)

    # Harvest independent session data for selected carers/patients
    carer_ids = ['c2', 'c5', 'c8']
    carers = [p for p in CARERS if p.name in carer_ids]
    patient_ids = ['p2', 'p5', 'p8']
    patients = [p for p in PATIENTS if p.name in patient_ids]

    _, _, c_satisfaction_i_firsts, c_satisfaction_i_lasts = first_last_and_independent_data(
        key_satisfaction, indicator, carers)
    _, _, p_satisfaction_i_firsts, p_satisfaction_i_lasts = first_last_and_independent_data(
        key_satisfaction, indicator, patients)

    data = [
        [c_satisfaction_t_firsts, p_satisfaction_t_firsts],
        [c_satisfaction_t_lasts, p_satisfaction_t_lasts],
        [c_satisfaction_i_firsts, p_satisfaction_i_firsts],
        [c_satisfaction_i_lasts, p_satisfaction_i_lasts],
    ]

    fig, ax = plt.subplots()

    c_satisfaction_color = 'cyan'
    p_satisfaction_color = 'blue'
    x_ticks = []
    position = 0
    for pair in data:
        bp = ax.boxplot(pair, positions=[position+1, position+2], widths=0.6, patch_artist=True)
        bp['boxes'][0].set_facecolor(c_satisfaction_color)
        bp['boxes'][1].set_facecolor(p_satisfaction_color)
        x_ticks.append(position + 1.5)
        position = position + 3
        print("\n")

    ax.set_ylim([-1, 11])
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(('First Training', 'Last Training', 'First Independent', 'Last Independent'))

    p_satisfaction_label = mpatches.Patch(color=p_satisfaction_color, label="Patient Satisfaction")
    c_satisfaction_label = mpatches.Patch(color=c_satisfaction_color, label="Carer Satisfaction")
    plt.legend(handles=[c_satisfaction_label, p_satisfaction_label])

    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlabel('Session')

    plt.show()
