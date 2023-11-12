#!/usr/bin/python

from pathlib import Path
import numpy as np
import yaml

class ToolsManager(object):
    def __init__(self, datasets):
        self.datasets = datasets
        self.idx = 0

    def crop(self):
        print('CROP')
        self.pathManager.set_file_suffix('_crop')
        box = self.datasets.get_last_coord()
        self.imageManager.crop(box)
        self.datasets.crop_last_name_frame()
        self.editManager.show()


    def set_ImageManager(self, imageManager):
        self.imageManager = imageManager

    def set_PathManager(self, pathManager):
        self.pathManager = pathManager

    def set_EditManager(self, editManager):
        self.editManager = editManager

