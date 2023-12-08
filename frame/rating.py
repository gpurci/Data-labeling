#!/usr/bin/python

from tkinter import *
from tkinter import ttk


# from pathlib import Path

class RatingFrame :
    def __init__(self, notebookMan: object) :
        self.__notebookMan = notebookMan
        self.__targetMan = None
        self.__imageMan  = None
        self.__window    = None

        self.__w_default_rating = None
        self.__w_info_text      = None
        self.__w_rating         = None

    def set_windows(self, window) :
        self.__window = window

    def set_data(self, imageMan, targetMan) :
        self.__imageMan = imageMan
        self.__targetMan = targetMan

    def __config_rating(self, name: str, rating: int):
        self.__w_info_text.config(text="Select object @{}@ with rating {}".format(name, rating))

    def __update(self) :
        self.__config_rating(self.__targetMan.get_last_name(), self.__w_rating.get())

    def __select_rating(self) :
        self.__update()
        self.__targetMan.set_last_rating(self.__w_rating.get())

    def __set_default_rating(self, *arg) :
        print('ratind frame default_rating {}'.format(self.__w_default_rating.current()))
        self.__notebookMan.set_default_rating(self.__w_default_rating.current())

    def set_rating(self, rating: int) :
        self.__window.setvar(name='rating', value=rating)
        self.__update()

    def run(self) :
        self.__w_rating    = IntVar(self.__window, value=self.__notebookMan.get_default_rating(), name='rating')
        self.__w_info_text = Label(self.__window)
        self.__w_info_text.pack()
        self.__config_rating('not object', self.__notebookMan.get_default_rating())

        rank_frame = Frame(self.__window)
        rank_frame.pack(side=LEFT)

        Rm1 = Radiobutton(rank_frame, text="like -1", variable=self.__w_rating, value=-1, command=self.__select_rating)
        Rm1.pack(side=LEFT)
        R0 = Radiobutton(rank_frame, text="like 0", variable=self.__w_rating, value=0, command=self.__select_rating)
        R0.pack(side=LEFT)
        R1 = Radiobutton(rank_frame, text="like 1", variable=self.__w_rating, value=1, command=self.__select_rating)
        R1.pack(side=LEFT)
        R2 = Radiobutton(rank_frame, text="like 2", variable=self.__w_rating, value=2, command=self.__select_rating)
        R2.pack(side=LEFT)
        R3 = Radiobutton(rank_frame, text="like 3", variable=self.__w_rating, value=3, command=self.__select_rating)
        R3.pack(side=LEFT)

        values = ["Default rating {}".format(i) for i in [-1, 0, 1, 2, 3]]

        # Create a Combobox widget 
        self.__w_default_rating = ttk.Combobox(self.__window)
        self.__w_default_rating['values'] = values
        self.__w_default_rating['state'] = 'readonly'
        self.__w_default_rating.set("Default rating {}".format(self.__notebookMan.get_default_rating()))
        # combo.pack( side = LEFT)
        self.__w_default_rating.pack(padx=5, pady=5)

        self.__w_default_rating.bind("<<ComboboxSelected>>", self.__set_default_rating)
