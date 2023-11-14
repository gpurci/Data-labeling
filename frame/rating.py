#!/usr/bin/python

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

#from pathlib import Path

class RatingFrame(object):
    def __init__(self, notebookMan):
        self.notebookMan = notebookMan

    def set_windows(self, window):
        self.window = window

    def set_data(self, imageMan, targetMan):
        self.imageMan  = imageMan
        self.targetMan = targetMan

    def set_rating(self, name, rating):
        self.label.config(text = "Select oject @{}@ with rating {}".format(name, rating))

    def set_rating_frame(self, rating):
        self.window.setvar(name='rating', value=rating)
        self.update_rating_frame()

    def update_rating_frame(self):
        self.set_rating(self.targetMan.get_last_name(), self.rating.get())

    def select_rating(self):
        self.update_rating_frame()
        self.targetMan.set_last_rating(self.rating.get())

    def set_default_rating(self, *arg):
        print('ratind frame default_rating {}'.format(self.default_rating_combo.current()))
        self.targetMan.set_default_rating(self.default_rating_combo.current())

    def run(self):
        self.rating = IntVar(self.window, value=self.notebookMan.get_default_rating(), name='rating')
        self.label = Label(self.window)
        self.label.pack()
        self.set_rating('not object', self.notebookMan.get_default_rating())
        
        rank_frame = Frame(self.window)
        rank_frame.pack( side = LEFT )
        
        Rm1 = Radiobutton(rank_frame, text="like -1", variable=self.rating, value=-1, command=self.select_rating)
        Rm1.pack( side = LEFT )
        R0 = Radiobutton(rank_frame, text="like 0", variable=self.rating, value=0, command=self.select_rating)
        R0.pack( side = LEFT )
        R1 = Radiobutton(rank_frame, text="like 1", variable=self.rating, value=1, command=self.select_rating)
        R1.pack( side = LEFT )
        R2 = Radiobutton(rank_frame, text="like 2", variable=self.rating, value=2, command=self.select_rating)
        R2.pack( side = LEFT )
        R3 = Radiobutton(rank_frame, text="like 3", variable=self.rating, value=3, command=self.select_rating)
        R3.pack( side = LEFT )

        values = ["Default rating {}".format(i) for i in [-1, 0, 1, 2, 3]]
           
        # Create a Combobox widget 
        self.default_rating_combo = ttk.Combobox(self.window)
        self.default_rating_combo['values'] = values 
        self.default_rating_combo['state'] = 'readonly'
        self.default_rating_combo.set("Default rating {}".format(self.notebookMan.get_default_rating()))
        #combo.pack( side = LEFT)
        self.default_rating_combo.pack(padx = 5, pady = 5)
        
        self.default_rating_combo.bind("<<ComboboxSelected>>", self.set_default_rating)


