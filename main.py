import dao
import inspect
import tkinter as tk
from tkinter import Tk, Frame, Listbox
import ania.boxplots.patients as p_plots
import ania.boxplots.carers as c_plots


class App:

    WIDTH = 300
    HEIGHT = 500

    def __init__(self, root, funcs):
        self.root = root
        self.root.title("Boxploty Migotki :****")
        self.root.geometry("%dx%d%+d%+d" % (App.WIDTH, App.HEIGHT, 0, 0))
        self.main_frame = Frame(root, width=App.WIDTH, height=App.HEIGHT)
        self.main_frame.pack_propagate(0)
        self.main_frame.pack()
        self.list_map = funcs
        self.listbox = Listbox(self.main_frame, height=4, width=15, selectbackground="orange")
        for ix, e in enumerate(self.list_map):
            self.listbox.insert(ix, e[0])
        self.listbox.bind("<Double-Button-1>", self.call_back)
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
                funcs.append((name, fnc))
    return funcs


def main():
    #dao.print_patients()
    root = Tk()
    funcs = get_plotting_functions([p_plots, c_plots])
    App(root, funcs)
    root.mainloop()


if __name__ == "__main__":
    main()
