#!/usr/bin/python

from tkinter import *
from add_item import *


class ToolsFrame:
    def __init__(self, toolsMan: object, notebookMan: object):
        self.__window       = None
        self.__toolsMan     = toolsMan
        self.__notebookMan  = notebookMan

        frame_title  = 'Add filename'
        search_title = 'Current filename'
        search_item  = ''
        self.__addItemFrame = AddItemFrame(frame_title, search_title, search_item, True)

        add_name_frame.set_search_item("filename")
        add_name_frame.set_items(lst_names)

    def set_windows(self, window: object):
        self.__window = window
        self.__addItemFrame.set_windows(self.__window)

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
