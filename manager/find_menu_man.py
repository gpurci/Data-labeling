#!/usr/bin/python

from pathlib import Path
import yaml
import pandas as pd
from frame.add_item import *
from manager.target_man import *


class FindFilesMenu(object):
    def __init__(self, path_manager: object, filenameFrame: object) :
        self.__pathMan       = path_manager
        self.__filenameFrame = filenameFrame

        frame_title  = 'Find object name in files'
        search_title = 'Object name'
        search_item  = ''
        check_similarly_item = False
        self.__make_object = AddItemFrame(frame_title, search_title, search_item, check_similarly_item)
        self.__make_object.set_cancel_fn(lambda : print('CANCEL'))
        self.__make_object.set_add_fn(self.__find_object_name)

    def __call__(self):
        self.__make_object.run()

    def __find_object_name(self, name: str):
        targetMan = TargetManager(0)
        filenames = []
        for target_filename in self.__pathMan.get_target_filenames():
            filename = self.__pathMan.get_target_filename(str(target_filename))
            targetMan.read(filename)
            if (targetMan.find_object_by_name(name) != None):
                img_filename = self.__pathMan.get_input_filename_by_target(target_filename)
                if (img_filename != None):
                    filenames.append(img_filename)
        print('find_object_name {}'.format(filenames))
        self.__filenameFrame.set_filenames(filenames)

class MoreThatMenu(object):
    def __init__(self, path_manager: object, filenameFrame: object) :
        self.__pathMan       = path_manager
        self.__filenameFrame = filenameFrame

        frame_title  = 'Find files with more object that ...'
        search_title = 'Value'
        search_item  = ''
        check_similarly_item = False
        self.__make_object = AddItemFrame(frame_title, search_title, search_item, check_similarly_item)
        self.__make_object.set_cancel_fn(lambda : print('CANCEL'))
        self.__make_object.set_add_fn(self.__find_more_that)

    def __call__(self):
        self.__make_object.run()

    def __find_more_that(self, val: str):
        targetMan = TargetManager(0)
        filenames = []
        for target_filename in self.__pathMan.get_target_filenames():
            filename = self.__pathMan.get_target_filename(str(target_filename))
            targetMan.read(filename)
            if (targetMan.get_object_size() >= int(val)):
                img_filename = self.__pathMan.get_input_filename_by_target(target_filename)
                if (img_filename != None):
                    filenames.append(img_filename)
        print('find_object_name {}'.format(filenames))
        self.__filenameFrame.set_filenames(filenames)

class LessThatMenu(object):
    def __init__(self, path_manager: object, filenameFrame: object) :
        self.__pathMan       = path_manager
        self.__filenameFrame = filenameFrame

        frame_title  = 'Find files with less object that ...'
        search_title = 'Value'
        search_item  = ''
        check_similarly_item = False
        self.__make_object = AddItemFrame(frame_title, search_title, search_item, check_similarly_item)
        self.__make_object.set_cancel_fn(lambda : print('CANCEL'))
        self.__make_object.set_add_fn(self.__find_more_that)

    def __call__(self):
        self.__make_object.run()

    def __find_more_that(self, val: str):
        targetMan = TargetManager(0)
        filenames = []
        for target_filename in self.__pathMan.get_target_filenames():
            filename = self.__pathMan.get_target_filename(str(target_filename))
            targetMan.read(filename)
            if (targetMan.get_object_size() < int(val)):
                img_filename = self.__pathMan.get_input_filename_by_target(target_filename)
                if (img_filename != None):
                    filenames.append(img_filename)
        print('find_object_name {}'.format(filenames))
        self.__filenameFrame.set_filenames(filenames)



class ObjectNamesMenu(object):
    def __init__(self, window: object, objectMan:object) :
        self.__frame  = None
        self.__window = window
        self.__objectMan = objectMan

    def run(self):
        # open new window
        if (self.__frame != None):
            self.__frame.withdraw()

        self.__frame = Toplevel(self.__window)
        self.__frame.title('Object names')

        scrollbar = Scrollbar(self.__frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.__text_frame = Text(self.__frame, bd=5, yscrollcommand=scrollbar.set,
                                       width=45, height=40)
        self.__text_frame.pack()

    def __call__(self):
        d_object_names = self.__objectMan.get_user_object_freq()
        pd_object_freq = pd.DataFrame(data={'Name':d_object_names.keys(), 'Freq': d_object_names.values()})
        pd_object_freq = pd_object_freq.sort_values(by=['Freq'])
        print(pd_object_freq)
        self.run()
        self.__text_frame.insert(END, '{:<30}{}\n'.format('Object name', 'Name frequency'))
        for obj_name, freq in pd_object_freq[['Name', 'Freq']].values :
            #obj_name, freq = pd_object_freq[i]
            print('obj_name', obj_name)
            #freq = pd_object_freq[obj_name]
            tmp_ = '{:<30}{}\n'.format(obj_name, freq)
            self.__text_frame.insert(END, tmp_)



