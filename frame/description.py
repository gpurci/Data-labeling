#!/usr/bin/python

from tkinter import *
import tkinter as tk
from tkinter import messagebox

class DescriptionFrame(object):
    def __init__(self):
        pass

    def set_windows(self, window:object):
        print('DescriptionFrame.set_windows')
        self.__window = window

    def set_data(self, imageMan:object, targetMan:object):
        self.__imageMan  = imageMan
        self.__targetMan = targetMan

    def set_dimension(self, dataset_dim:object):
        self.__dataset_dim = dataset_dim

    def run(self):
        scrollbar = Scrollbar(self.__window)
        scrollbar.pack( side = RIGHT, fill=Y )

        self.__labelframe = LabelFrame(self.__window, text='not expected object')
        self.__labelframe.pack(fill="both", expand="yes")

        self.__text_frame = CustomText(self.__labelframe, bd=5, yscrollcommand=scrollbar.set, 
                                width=int(self.__dataset_dim.get_width()/8), height=8)
        self.__text_frame.insert(END, 'no description')
        self.__text_frame.pack()
        self.__text_frame.bind("<<TextModified>>", self.__onModification)

    def __onModification(self, event:object):
        self.__targetMan.set_last_description(self.__get_text_frame())

    def __get_text_frame(self):
        return self.__text_frame.get(1.0, END)[:-1]

    def set_text_frame(self, object_image:str, object_description:str):
        self.__labelframe.config(text=object_image)
        self.__text_frame.delete(1.0, END)
        self.__text_frame.insert(END, object_description)


class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        """A text widget that report on internal widget commands"""
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")

        return result