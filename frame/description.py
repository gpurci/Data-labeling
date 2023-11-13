#!/usr/bin/python

from tkinter import *
from tkinter import messagebox

class DescriptionFrame(object):
    def __init__(self, datasets):
        self.datasets = datasets

    def set_windows(self, window):
        print('DescriptionFrame.set_windows')
        self.window = window

    def set_dimension(self, dataset_dim):
        self.dataset_dim = dataset_dim

    def run(self):
        scrollbar = Scrollbar(self.window)
        scrollbar.pack( side = RIGHT, fill=Y )

        self.labelframe = LabelFrame(self.window, text=self.datasets.get_last_name())
        self.labelframe.pack(fill="both", expand="yes")

        self.text_frame = Text(self.labelframe, bd=5, yscrollcommand=scrollbar.set, 
                                width=int(self.dataset_dim.get_width()/8), height=8)
        self.text_frame.insert(END, self.datasets.get_last_description())
        self.text_frame.pack()

    def get_text_frame(self):
        return self.text_frame.get(1.0, END)[:-1]

    def set_text_frame(self, selected_object, description):
        self.labelframe.config(text=selected_object)
        self.text_frame.delete(1.0, END)
        self.text_frame.insert(END, description)

