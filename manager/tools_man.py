#!/usr/bin/python

from pathlib import Path
import numpy as np
import yaml

class ToolsManager(object):
    def __init__(self):
        self.idx = 0
        self.is_data = False

    def crop(self):
        print('CROP is_data {}'.format(self.is_data))
        if (self.is_data == True):
            self.__pathManager.set_file_suffix('_crop')
            box = self.__targetMan.get_last_coord()
            self.__imageMan.crop(box)
            self.__targetMan.crop_last_name()
        else:
            self.is_data = True

    def set_data(self, imageMan, targetMan):
        self.__imageMan  = imageMan
        self.__targetMan = targetMan

    def set_PathManager(self, pathManager):
        self.__pathManager = pathManager

