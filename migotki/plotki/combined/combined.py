import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from contants import COMBINED
from dao import OTS
from dao import CARERS
from dao import PATIENTS

from migotki.common import first_last_and_independent_data, last_and_sessions, first_and_last_data



TYPE = COMBINED

WIDTH_17_CENTIMERES_IN_INCHES = 6.7
HEIGHT_9_CENTIMERES_IN_INCHES = 3.54

def plot_carer_combined():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(WIDTH_17_CENTIMERES_IN_INCHES, HEIGHT_9_CENTIMERES_IN_INCHES))

    # ------------------------------------------------------------------
    # --------------------plot_carer_workload --------------------------
    # ------------------------------------------------------------------

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

    ax1.scatter(x, y, s=area, c=colors, alpha=0.5)
    ax1.set_xlabel('Mental demand')
    ax1.set_ylabel('Donning')

    # ------------------------------------------------------------------
    # -- plot_patient_and_ot_donning_all_s_1_5_10_14_averaged_no_log ---
    # ------------------------------------------------------------------

    title = 'Donning - OTs and Carers'
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


    ot_color = 'lightgreen'
    patient_color = 'lightblue'
    x_ticks = []
    patient_x_ticks = []
    position = 0
    for pair in data:
        if len(pair) == 2:
            bp = ax2.boxplot(pair, positions=[position +1, position +2], widths=0.6, patch_artist=True)
            bp['boxes'][0].set_facecolor(ot_color)
            bp['boxes'][1].set_facecolor(patient_color)
            patient_x_ticks.append(position + 2)
            x_ticks.append(position + 1.5)
        else:
            bp = ax2.boxplot(pair, positions=[position +1], widths=0.6, patch_artist=True)
            bp['boxes'][0].set_facecolor(patient_color)
            patient_x_ticks.append(position + 1)
            x_ticks.append(position + 1)
        position = position + 3

    ax2.set_ylabel('Donning Time (minutes)')
    ax2.set_title(title)
    ax2.set_xticks(x_ticks)
    ax2.set_xticklabels(('First', 'Last', '10', '14'))

    ot_label = mpatches.Patch(color=ot_color, label="OT")
    patient_label = mpatches.Patch(color=patient_color, label="Carers")

    ax2.set_axisbelow(True)

    # legend
    wilcoxson_text = "p-value={}".format(p_p)
    plt.legend(handles=[ot_label, patient_label])

    ax2.annotate(wilcoxson_text, xy=(0.3, 0.75), xytext=(0.3, 0.90), xycoords='axes fraction',
                 fontsize=10, ha='center', va='bottom',
                 bbox=dict(boxstyle='square', fc='lightblue'),
                 arrowprops=dict(arrowstyle='-[, widthB=2.5, lengthB=1', lw=1.0))

    # ------------------------------------------------------------------
    plt.show()


def plot_patients_fes_threshold_combined():
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(WIDTH_17_CENTIMERES_IN_INCHES, HEIGHT_9_CENTIMERES_IN_INCHES))

    # ------------------------------------------------------------------
    # -------------------- TPR_all_patients_s12345----------------------
    # ------------------------------------------------------------------
    sr = range(1, 6)
    data = {}
    for p in PATIENTS:
        trials = p.data['BCIFES_Trials']
        for t in trials:
            s = t['session']
            if s not in sr:
                continue
            if s not in data:
                data[s] = []
            if p.name == "p4" and t['session'] == 3:
                continue
            tpr = p.get_tpr(t) * 100
            if not np.isnan(tpr):
                data[s].append(tpr)
    print(data)
    tprs = list(data.values())
    labels = [s for s in list(data.keys())]
    ax1.boxplot(tprs, labels=labels)
    ax1.set_xlabel("Session")
    ax1.set_ylabel("True Positives (%)")

    # ------------------------------------------------------------------
    # ------------------------ FES_all_S1_5 ----------------------------
    # ------------------------------------------------------------------

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
    ax2.boxplot(data, labels=labels)
    ax2.set_title('Training Sessions: AM Duration (Before FES)')
    ax2.set_axisbelow(True)
    ax2.set_xlabel('Session')
    ax2.set_ylabel('Time (s)')

    # ------------------------------------------------------------------
    # ----------------- final_threshold_all_patients--------------------
    # ------------------------------------------------------------------

    data = {}
    for p in PATIENTS:
        thresholds = p.data['Threshold']
        tdata = []
        for t in thresholds:
            if t['session'] in [1, 2, 3, 4, 5]:
                last = t['threshold'][-1]
                if not np.isnan(last):
                    tdata.append(last)
        data[p.name] = tdata

    y = list(data.values())
    labels = [k for k in list(data.keys())]
    ax3.boxplot(y, labels=labels)
    ax3.set_title('Training Sessions: Threshold Values')
    ax3.set_axisbelow(True)
    ax3.set_xlabel('Patient')
    ax3.set_ylabel('Threshold (V^2/Hz)')

    # ------------------------------------------------------------------
    plt.show()


def plot_workload_fes_threshold_combined():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(WIDTH_17_CENTIMERES_IN_INCHES, HEIGHT_9_CENTIMERES_IN_INCHES))

    # ------------------------------------------------------------------
    # -------------------------- OTs_workload --------------------------
    # ------------------------------------------------------------------

    FES = []
    BCI = []
    BCIFES1 = []
    BCIFES2 = []

    for ot in OTS:
        nasa = ot.data['NASA_TLX']
        fes = next(n for n in nasa if n['session'] == 1)['total']
        bci = next(n for n in nasa if n['session'] == 2)['total']
        bcifes1 = next(n for n in nasa if n['session'] == 3)['total']
        bcifes2 = next(n for n in nasa if n['session'] == 4)['total']
        if ot.name == 'ot3':
            bcifes1 = next(n for n in nasa if n['session'] == 4)['total']
            bcifes2 = next(n for n in nasa if n['session'] == 5)['total']
        elif ot.name == 'ot4':
            fes = next(n for n in nasa if n['session'] == 2)['total']
        FES.append(fes)
        BCI.append(bci)
        BCIFES1.append(bcifes1)
        BCIFES2.append(bcifes2)

    data = [FES, BCI, BCIFES1, BCIFES2]
    session_str = ['FES', 'BCI', 'BCIFES1', 'BCIFES2']
    ax1.boxplot(data, labels=session_str)
    ax1.set_title("Workload - OTs")
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax1.set_axisbelow(True)
    ax1.set_ylabel('Workload')

    # ------------------------------------------------------------------
    # -------  carer_patient_workload_first_last_and_independent -------
    # ------------------------------------------------------------------

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

    c_color = 'lightblue'
    p_color = 'pink'
    position = 0
    x_ticks = []
    for pair in data:
        bp = ax2.boxplot(pair, positions=[position + 1, position + 2], widths=0.6, patch_artist=True)
        bp['boxes'][0].set_facecolor(p_color)
        bp['boxes'][1].set_facecolor(c_color)
        x_ticks.append(position + 1.5)
        position = position + 3

    ax2.set_ylabel(ylabel)
    ax2.set_title(title)
    ax2.set_xticks(x_ticks)
    ax2.set_xticklabels(('First Training', 'Last Training', 'First Independent', 'Last Independent'))

    p_label = mpatches.Patch(color=p_color, label="Patient")
    c_label = mpatches.Patch(color=c_color, label="Carer")

    plt.legend(handles=[p_label, c_label])

    ax2.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax2.set_axisbelow(True)
    ax2.set_xlabel('Session')

    # ------------------------------------------------------------------
    plt.show()



def plot_satisfaction_combined():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(WIDTH_17_CENTIMERES_IN_INCHES, HEIGHT_9_CENTIMERES_IN_INCHES))

    # ------------------------------------------------------------------
    # ------ carer_patient_satisfaction_first_last_and_independent -----
    # ------------------------------------------------------------------

    title = 'Satisfaction - Patients and Carers'
    ylabel = 'Arbitrary Units'
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

    c_satisfaction_color = 'lightblue'
    p_satisfaction_color = 'pink'
    x_ticks = []
    position = 0
    for pair in data:
        bp = ax1.boxplot(pair, positions=[position + 1, position + 2], widths=0.6, patch_artist=True)
        bp['boxes'][0].set_facecolor(c_satisfaction_color)
        bp['boxes'][1].set_facecolor(p_satisfaction_color)
        x_ticks.append(position + 1.5)
        position = position + 3
        print("\n")

    ax1.set_ylim([-1, 11])
    ax1.set_ylabel(ylabel)
    ax1.set_title(title)
    ax1.set_xticks(x_ticks)
    ax1.set_xticklabels(('First Training', 'Last Training', 'First Independent', 'Last Independent'))

    p_satisfaction_label = mpatches.Patch(color=p_satisfaction_color, label="Patient")
    c_satisfaction_label = mpatches.Patch(color=c_satisfaction_color, label="Carer")
    plt.legend(handles=[p_satisfaction_label, c_satisfaction_label], loc=4)

    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax1.set_axisbelow(True)
    ax1.set_xlabel('Session')

    # ------------------------------------------------------------------
    # -------- carer_patient_stress_first_last_and_independent ---------
    # ------------------------------------------------------------------

    title = 'Stress - Patients and Carers'
    ylabel = 'Arbitrary Units'
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

    c_stress_color = 'lightblue'
    p_stress_color = 'pink'
    x_ticks = []
    position = 0
    for pair in data:
        bp = ax2.boxplot(pair, positions=[position + 1, position + 2], widths=0.6, patch_artist=True)
        bp['boxes'][0].set_facecolor(c_stress_color)
        bp['boxes'][1].set_facecolor(p_stress_color)
        x_ticks.append(position + 1.5)
        position = position + 3

    ax2.set_ylim([-1, 11])
    ax2.set_ylabel(ylabel)
    ax2.set_title(title)
    ax2.set_xticks(x_ticks)
    ax2.set_xticklabels(('First Training', 'Last Training', 'First Independent', 'Last Independent'))

    p_stress_label = mpatches.Patch(color=p_stress_color, label="Patient")
    c_stress_label = mpatches.Patch(color=c_stress_color, label="Carer")
    plt.legend(handles=[p_stress_label, c_stress_label])

    ax2.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax2.set_axisbelow(True)
    ax2.set_xlabel('Session')

    # ------------------------------------------------------------------
    plt.show()

