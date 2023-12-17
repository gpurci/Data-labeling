#!/usr/bin/python

from tkinter import *
from frame.add_item import *
import numpy as np


class ToolsFrame:
    def __init__(self, toolsMan: object, notebookMan: object, pathMan: object):
        self.__window       = None
        self.__toolsMan     = toolsMan
        self.__notebookMan  = notebookMan
        self.__pathMan      = pathMan

        frame_title  = 'Add filename'
        search_title = 'Current filename'
        search_item  = ''
        check_similarly_item = True
        self.__addItemFrame = AddItemFrame(frame_title, search_title, search_item, check_similarly_item)
        self.__addItemFrame.set_cancel_fn(lambda : print('CANCEL'))

    def set_windows(self, window: object):
        self.__window = window
        self.__addItemFrame.set_windows(self.__window)


    def __crop(self):
        print('TOOLS CROP')
        self.__new_file()
        self.__addItemFrame.set_add_fn(self.__toolsMan.crop)
        self.__addItemFrame.run()

    def run(self):
        tools_frame = LabelFrame(self.__window, text='Tools')
        tools_frame.pack(fill="both", expand="yes")

        crop_button = Button(tools_frame)
        crop_button["text"] = "Crop",
        crop_button["command"] = self.__crop
        crop_button.pack({"side": "left"})

    def __new_file(self):
        suffixname = self.__notebookMan.targetMan().get_last_name()
        filename   = self.__notebookMan.get_filename()
        print('TOOLS NEW FILE, actual filename {} suffixname {}'.format(filename, suffixname))
        filename   = self.__pathMan.get_filename_with_suffixname('_'+suffixname, filename)
        print('file with suffix {}'.format(filename))
        _tabs_file   = self.__notebookMan.get_tabs()
        _source_file = self.__pathMan.get_source_files()
        _dest_file   = self.__pathMan.get_dest_files()
        _files = np.concatenate((_tabs_file, _source_file, _dest_file), axis=None)
        _files = np.unique(_files, return_index=False, return_inverse=False, return_counts=False, axis=None, equal_nan=False)
        print('_files {}'.format(_files))
        filename     = self.__pathMan.filename_generator(_files, filename)

        self.__addItemFrame.set_search_item(filename)
        self.__addItemFrame.set_items(_files)

