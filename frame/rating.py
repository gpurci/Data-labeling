#!/usr/bin/python

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

#from pathlib import Path

class RatingFrame(object):
    def __init__(self, datasets):
        self.datasets = datasets

    def set_windows(self, window):
        self.window = window

    def set_rating_frame(self, rating):
        self.window.setvar(name='rating', value=rating)
        self.update_rating_frame()

    def update_rating_frame(self):
        self.label.config(text = "Select oject @{}@ with rating {}".format(self.datasets.get_last_name(), self.rating.get()))

    def select_rating(self):
        self.update_rating_frame()
        self.datasets.set_last_rating(self.rating.get())

    def set_default_rating(self, *arg):
        print('ratind frame default_rating {}'.format(self.default_rating_combo.current()))
        self.datasets.set_default_rating(self.default_rating_combo.current())

    def run(self):
        self.rating = IntVar(self.window, value=self.datasets.get_last_rating(), name='rating')
        self.label = Label(self.window)
        self.label.pack()
        self.update_rating_frame()
        
        rank_frame = Frame(self.window)
        rank_frame.pack( side = LEFT )
        
        R1 = Radiobutton(rank_frame, text="like 1", variable=self.rating, value=1, command=self.select_rating)
        R1.pack( side = LEFT )
        R2 = Radiobutton(rank_frame, text="like 2", variable=self.rating, value=2, command=self.select_rating)
        R2.pack( side = LEFT )
        R3 = Radiobutton(rank_frame, text="like 3", variable=self.rating, value=3, command=self.select_rating)
        R3.pack( side = LEFT)
        R4 = Radiobutton(rank_frame, text="like 4", variable=self.rating, value=4, command=self.select_rating)
        R4.pack( side = LEFT)
        R5 = Radiobutton(rank_frame, text="like 5", variable=self.rating, value=5, command=self.select_rating)
        R5.pack( side = LEFT)

        values = ["Default rating {}".format(i) for i in [0, 1, 2, 3, 4, 5]]
           
        # Create a Combobox widget 
        self.default_rating_combo = ttk.Combobox(self.window)
        self.default_rating_combo['values'] = values 
        self.default_rating_combo['state'] = 'readonly'
        self.default_rating_combo.set("Default rating {}".format(self.datasets.get_default_rating()))
        #combo.pack( side = LEFT)
        self.default_rating_combo.pack(padx = 5, pady = 5)
        
        self.default_rating_combo.bind("<<ComboboxSelected>>", self.set_default_rating)


