import numpy as np
import matplotlib.pyplot as plt

from contants import BOXPLOT
from dao import OTS

TYPE = BOXPLOT


def plot_ots_workload():
    """
        - Plot OT NASA TLX workload as boxplot like this:
            x axis labels FES, BCI, BCIFES1, BCIFES2
            in general session 1=FES, session 2=BCI, session 3= BCIFES1, sess 4= BCIFES2
            BUT since OT1 and OT3 have 5 sessions total..
            For OT1 use session 3 as BCIFES1 and session 4 as BCIFES2
            For OT3 use session 4 as BCIFES1 and session 5 as BCIFES2
            AND
            For OT4 use session 2 as FES, and session 1 as BCI.
    """
    FES = []
    BCI = []
    BCIFES1 = []
    BCIFES2 = []

    for ot in OTS:
        nasa = ot.datap['NASA_TLX']
        if ot.name == 'ot1':
            pass
        elif ot.name == 'ot3':
            pass
        elif ot.name == 'ot4':
            pass

    # session_dict[2].extend(session_dict[3])
    # del session_dict[3]
    # print(session_dict)
    # data = list(session_dict.values())
    # fig, ax = plt.subplots()
    # session_str = ['FES', 'BCI', 'BCIFES1', 'BCIFES2']
    # ax.boxplot(data, labels=session_str)
    # ax.set_title("All OTs - Donning")
    # ticks = np.arange(25, 65, 5)
    # ax.set_yticks(ticks[1:])
    # ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    # ax.set_axisbelow(True)
    # ax.set_xlabel('Sessions')
    # ax.set_ylabel('Donning Time (min)')
    # plt.show()

def plot_ots_donnings_first_last():
    ots = [p.name for p in OTS]
    sessions = [1, 2, 3]
    ots_donnings = [p.data['donning'] for p in OTS if p.name in ots]
    session_dict = {}
    for s in sessions:
        session_dict[s] = []
    for s in session_dict:
        for donnings in ots_donnings:
            minutes = [d['minutes'] for d in donnings if d['session'] == s]
            minutes = [m for m in minutes if not np.isnan(m)]
            session_dict[s].extend(minutes)

    session_dict[2].extend(session_dict[3])
    del session_dict[3]
    print(session_dict)
    data = list(session_dict.values())
    fig, ax = plt.subplots()
    session_str = ['First Training Session', 'Last Training Session']
    ax.boxplot(data, labels=session_str)
    ax.set_title("All OTs - Donning")
    ticks = np.arange(25, 65, 5)
    ax.set_yticks(ticks[1:])
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlabel('Sessions')
    ax.set_ylabel('Donning Time (min)')
    plt.show()


def plot_ots_donning():
    ots = [p.name for p in OTS]
    _donnings(ots, [1, 2, 3], "All OTs - Donning")


def _donnings(ots: list, sessions: list, title: str):
    ots_donnings = [p.data['donning'] for p in OTS if p.name in ots]
    session_dict = {}
    for s in sessions:
        session_dict[s] = []
    for s in session_dict:
        for donnings in ots_donnings:
            minutes = [d['minutes'] for d in donnings if d['session'] == s]
            minutes = [m for m in minutes if not np.isnan(m)]
            session_dict[s].extend(minutes)
    data = list(session_dict.values())
    fig, ax = plt.subplots()
    session_str = [str(k) for k in session_dict.keys()]
    ax.boxplot(data, labels=session_str)
    ax.set_title(title)
    ticks = np.arange(0, 65, 5)
    ax.set_yticks(ticks[1:])
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlabel('Session Number')
    ax.set_ylabel('Donning Time (min)')
    plt.show()
