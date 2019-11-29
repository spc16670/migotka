import inspect
import tkinter as tk
from tkinter import Tk, Frame, Listbox

import dao
from contants import BARCHART, BOXPLOT, SCATTERPLOT
import migotki.plotki.box.ot as boxplots_ots
import migotki.plotki.box.carer as boxplots_carers
import migotki.plotki.box.patient as boxplots_patients
import migotki.plotki.bar.patient as barchart_patients
import migotki.plotki.scatter.patient as scatterplots_patients


class App:

    WIDTH = 600
    HEIGHT = 600

    def __init__(self, root, funcs):
        self.root = root
        self.root.title("Plotki Migotki")
        self.root.geometry("%dx%d%+d%+d" % (App.WIDTH, App.HEIGHT, 0, 0))
        self.main_frame = Frame(root, width=App.WIDTH, height=App.HEIGHT)
        self.main_frame.pack_propagate(0)
        self.main_frame.pack()
        self.list_map = funcs
        self.listbox = Listbox(self.main_frame, height=4, width=15, selectbackground="orange")
        for ix, (entry, _f) in enumerate(self.list_map):
            plot_type, title = entry
            self.listbox.insert(ix, title)
            if plot_type == BARCHART:
                self.listbox.itemconfig(ix, bg='green')
            elif plot_type == BOXPLOT:
                self.listbox.itemconfig(ix, bg='yellow')
            elif plot_type == SCATTERPLOT:
                self.listbox.itemconfig(ix, bg='grey')
        self.listbox.bind("<Double-Button-1>", self.call_back)
        self.listbox.bind("<Return>", self.call_back)
        self.listbox.pack(expand=1, fill=tk.BOTH)

    def call_back(self, event):
        zones = self.listbox.curselection()
        assert len(zones) == 1
        ix = zones[0]
        ix, cb = self.list_map[ix]
        cb()


def get_plotting_functions(modules):
    funcs = []
    for m in modules:
        for name, fnc in inspect.getmembers(m, inspect.isfunction):
            if name.startswith("plot_"):
                name = name[5:]
                name = name.replace("_", " ")
                name = name.upper()
                name = m.TYPE.ljust(13) + "   | " + name
                funcs.append(((m.TYPE, name), fnc))
    return funcs


def main():
    dao.print_ots()
    root = Tk()
    funcs = get_plotting_functions([
        boxplots_ots,
        boxplots_carers,
        boxplots_patients,
        barchart_patients,
        scatterplots_patients
    ])
    App(root, funcs)
    root.bind("<Escape>", lambda q: root.destroy())
    root.mainloop()


if __name__ == "__main__":
    main()
