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
        #self.datasets.cut_last_name()
        self.imageManager.crop(box)
        #self.manualCrop(box)
        self.datasets.crop_targets()
        self.imageManager.img_show()


    # crop a box from image of all classes
    def manualCrop(self, crop):
        # crop - dict of labels name, keys name, elements index of name

        #select cartesian coordinate by object from image
        obj_x0, obj_y0, obj_x1, obj_y1 = crop

        #select cartesian coordinate to crop image
        #c_x0, c_y0, c_x1, c_y1 = 
        '''
        #recalculate the coordinate by new coordinate
        for x0, y0, x1, y1 in zip(c_x0, c_y0, c_x1, c_y1):
            if ((obj_x0 > x0) and (obj_x0 > x1)):
            
            new_x0, new_y0, new_x1, new_y1 = obj_x0 - x0, obj_y0 - y0, obj_x1 - x0, obj_y1 - y0
        '''


    def set_ImageManager(self, imageManager):
        self.imageManager = imageManager

    def set_PathManager(self, pathManager):
        self.pathManager = pathManager

    def set_EditManager(self, editManager):
        self.editManager = editManager

