import numpy as np
import matplotlib.pyplot as plt

from contants import HISTOGRAM
from dao import PATIENTS

TYPE = HISTOGRAM


def _rom(side):
    max_roms = dict()
    for p in PATIENTS:
        initial_side_flexion = max([t['flexion'] for t in p.data['ROM_initial'] if t['type'] == side], default=None)
        initial_side_extension = min([t['extension'] for t in p.data['ROM_initial'] if t['type'] == side], default=None)
        pinitial = [initial_side_flexion, initial_side_extension]
        final_side_flexion = max([t['flexion'] for t in p.data['ROM_final'] if t['type'] == side], default=None)
        final_side_extension = min([t['extension'] for t in p.data['ROM_final'] if t['type'] == side], default=None)
        pfinal = [final_side_flexion, final_side_extension]

        if all(pinitial) or all(pfinal):
            max_roms[p.name] = {}
        if all(pinitial) and not np.all(np.isnan(pinitial)):
            max_roms[p.name]['initial'] = pinitial
        if all(pfinal) and not np.all(np.isnan(pfinal)):
            max_roms[p.name]['final'] = pfinal


    fig, ax = plt.subplots()
    labels = [p for p, v in max_roms.items()]
    x = np.arange(len(labels))
    width = 0.6
    for i, (patient, data) in enumerate(max_roms.items()):
        initial = data['initial'] if 'initial' in data else []
        if initial:
            ax.bar(i-0.3, initial[1], width=width/2, align='edge', color='r')
            ax.bar(i-0.3, initial[0], width=width/2, align='edge', color='b')
        final = data['final'] if 'final' in data else []
        if final:
            ax.bar(i+0.05, final[1], width=width/2, align='edge', color='g', alpha=0.5)
            ax.bar(i+0.05, final[0], width=width/2, align='edge', color='y', alpha=0.5)
    print(max_roms)

    # for ix, rect in enumerate(ax.patches):
    #     y_value = rect.get_height()
    #     x_value = rect.get_x() + rect.get_width() / 2
    #
    #     space = 5
    #     # If value of bar is negative: Place label below bar
    #     if y_value < 0:
    #         # Invert space to place label below
    #         space *= -1
    #         # Vertically align label at top
    #         va = 'top'
    #
    #     ax.annotate(
    #         'initial',  # Use `label` as label
    #         (x_value, y_value),  # Place label at end of the bar
    #         xytext=(0, space),  # Vertically shift label by `space`
    #         textcoords="offset points",  # Interpret `xytext` as offset in points
    #         ha='center',  # Horizontally center label
    #         va='top')  # Vertically align label differently  positive

    ax.set_ylabel('Scores')
    ax.set_title('Roms')

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    plt.show()


def plot_rom_l():
    _rom('L')


def plot_rom_r():
    _rom('R')