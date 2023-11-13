#!/usr/bin/python

from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Notebook, Style


class NotebookFrame(object):
    def __init__(self):
        pass

    def set_windows(self, windows):
        self.windows = windows

    def select_tab(self, *args):
        #t_nos=str(my_tabs.index())
        select_tab_val = self.note.select()
        if (len(select_tab_val) != 0):
            self.notebookManager.select_tab(select_tab_val[0])
    
    def run(self):
        # Create an instance of ttk style
        style = Style()
        style.theme_use('default')
        style.configure('TNotebook.Tab', background="Red")
        style.map("TNotebook", background= [("selected", "red")])

        # Create a Notebook widget
        self.note = Notebook(self.windows)
        self.note.bind('<<NotebookTabChanged>>', self.select_tab)
        self.note.pack(expand=True, fill=BOTH, padx=5, pady=5)
        self.frame = Frame(self.note, width=400, height=5)

    def add(self, filename):
        # Adding the Tab Name
        self.note.add(self.frame, text=filename)

    def set_NotebookManager(self, notebookManager):
        self.notebookManager = notebookManager