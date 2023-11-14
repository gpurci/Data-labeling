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
            self.pathManager.set_file_suffix('_crop')
            box = self.targetMan.get_last_coord()
            self.imageMan.crop(box)
            self.targetMan.crop_last_name_frame()
        else:
            self.is_data = True

    def set_data(self, imageMan, targetMan):
        self.imageMan  = imageMan
        self.targetMan = targetMan

    def set_PathManager(self, pathManager):
        self.pathManager = pathManager

    def set_EditManager(self, editManager):
        self.editManager = editManager

