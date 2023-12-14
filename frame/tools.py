#!/usr/bin/python

from tkinter import *


class ToolsFrame:
    def __init__(self, toolsMan: object, notebookMan: object):
        self.__window      = None
        self.__toolsMan    = toolsMan
        self.__notebookMan = notebookMan

    def set_windows(self, window: object):
        self.__window = window

    def __crop(self):
        self.__notebookMan.new_file(self.__notebookMan.targetMan().get_last_name(), self.__toolsMan.crop)
        #self.__toolsMan.crop(filename)

    def run(self):
        tools_frame = LabelFrame(self.__window, text='Tools')
        tools_frame.pack(fill="both", expand="yes")

        crop_button = Button(tools_frame)
        crop_button["text"] = "Crop",
        crop_button["command"] = self.__crop
        crop_button.pack({"side": "left"})

    def not_run(self):
        pass
