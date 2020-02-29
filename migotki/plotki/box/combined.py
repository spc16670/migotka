import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from migotki.common import first_last_and_independent_data, last_and_sessions

from contants import BOXPLOT
from dao import CARERS, PATIENTS

TYPE = BOXPLOT


def plot_carer_patient_stress_and_satisfaction_first_last_and_independent():
    title = 'Patients and Carers Stress and Satisfaction C2, C5, C8, P2, P5, P8'
    ylabel = 'Level'
    key_stress = 'stress'
    key_satisfaction = 'satisfaction'
    indicator = 'SAndS'
    carer_ids = ['c2', 'c5', 'c8']
    carers = [p for p in CARERS if p.name in carer_ids]
    patient_ids = ['p2', 'p5', 'p8']
    patients = [p for p in PATIENTS if p.name in patient_ids]
    c_stress_t_firsts, c_stress_t_lasts, c_stress_i_firsts, c_stress_i_lasts = first_last_and_independent_data(
        key_stress, indicator, carers)
    p_stress_t_firsts, p_stress_t_lasts, p_stress_i_firsts, p_stress_i_lasts = first_last_and_independent_data(
        key_stress, indicator, patients)
    c_satisfaction_t_firsts, c_satisfaction_t_lasts, c_satisfaction_i_firsts, c_satisfaction_i_lasts = first_last_and_independent_data(
        key_satisfaction, indicator, carers)
    p_satisfaction_t_firsts, p_satisfaction_t_lasts, p_satisfaction_i_firsts, p_satisfaction_i_lasts = first_last_and_independent_data(
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
        bp['boxes'][1].set_facecolor(c_satisfaction_color)
        bp['boxes'][2].set_facecolor(p_stress_color)
        bp['boxes'][3].set_facecolor(p_satisfaction_color)
        x_ticks.append(position + 2.5)
        position = position + 6

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
    title = 'Workload - Patients and Carers C2, C5, C8, P2, P5, P8'
    ylabel = 'Workload'
    indicator = 'NASA_TLX'
    key = 'total'

    carer_ids = ['c2', 'c5', 'c8']
    carers = [p for p in CARERS if p.name in carer_ids]
    c_training_firsts, c_training_lasts, c_independent_firsts, c_independent_lasts = first_last_and_independent_data(
        key, indicator, carers)
    patient_ids = ['p2', 'p5', 'p8']
    patients = [p for p in PATIENTS if p.name in patient_ids]
    p_training_firsts, p_training_lasts, p_independent_firsts, p_independent_lasts = first_last_and_independent_data(
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

