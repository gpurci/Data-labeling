#!/usr/bin/python

from tkinter import filedialog


class MenuOpenFrame :
    def __init__(self, pathMan: object) :
        self.__pathMan = pathMan

    def __call__(self) :
        path = filedialog.askdirectory(
            initialdir=self.__pathMan.get_source_path(),  # Start in the root directory
            title="Select a Directory",                   # Custom title for the dialog
            mustexist=True,                               # Ensure that the selected directory exists
        )
        self.__pathMan.set_source_path(path)
