import numpy as np

from dao import PATIENTS


def first_last_and_independent_data(key, indicator, data, s_label='Training_sessions'):
    training_firsts = []
    independent_firsts = []
    training_lasts = []
    independent_lasts = []
    for c in data:
        # training
        trainings = c.get_training_sessions(indicator)
        first = trainings[0]
        first_total = first[key]
        if not np.isnan(first_total):
            training_firsts.append(first_total)
        last = trainings[-1]
        last_total = last[key]
        if not np.isnan(last_total):
            training_lasts.append(last_total)
        # independent
        nasa = c.data[indicator]
        s_ix = c.data[s_label]
        independent = nasa[s_ix:]
        if not independent:
            continue
        first_independent = independent[0]
        first_independent_total = first_independent[key]
        if not np.isnan(first_independent_total):
            independent_firsts.append(first_independent_total)
        last_independent = independent[-1]
        last_independent_total = last_independent[key]
        if not np.isnan(last_independent_total):
            independent_lasts.append(last_independent_total)
    return training_firsts, training_lasts, independent_firsts, independent_lasts


def first_and_last_data(key, indicator, data=None):
    if not data:
        data = PATIENTS
    firsts = []
    lasts = []
    common = []
    for p in data:
        patients_trainings = p.get_training_sessions(key)

        # firsts
        first = patients_trainings[0]
        first_total = first[indicator]
        if not np.isnan(first_total):
            firsts.append(first_total)
        # lasts
        last = patients_trainings[-1]
        last_total = last[indicator]
        if p.name == 'p9':
            continue
        if not np.isnan(last_total):
            lasts.append(last_total)
        if not np.isnan(first_total) and not np.isnan(last_total):
            common.append([first_total, last_total])
    # wilcoxson
    common_a = [c[0] for c in common]
    common_b = [c[1] for c in common]

    # from scipy.stats import ranksums
    # p = ranksums(common_a, common_b)
    # p_round = round(p.pvalue, 3)

    from scipy.stats import wilcoxon
    stat, p = wilcoxon(common_a, common_b)
    p_round = round(p, 3)

    return firsts, lasts, common, p_round


def last_and_sessions(data, indicator='NASA_TLX', key='total', count_key='Training_sessions'):
    lasts = []
    session = {}
    for sid in range(1, 11):
        session[sid] = []
    for p in data:
        nasa = p.data[indicator]
        s_ix = p.data[count_key]
        last_training_session = nasa[s_ix-1]
        last_total = last_training_session[key]
        if not np.isnan(last_total):
            lasts.append(last_total)
        independent_sessions = nasa[s_ix:]
        for ix, s in enumerate(independent_sessions):
            s_independent_total = s[key]
            if not np.isnan(s_independent_total):
                session[ix+1].append(s_independent_total)
    return lasts, session