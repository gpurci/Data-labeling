#!/usr/bin/python

from pathlib import Path
from manager.image_man import *
from manager.target_man import *

class FolderStructure(object) :
    def __init__(self, pathMan: object) :
        self.__pathMan = pathMan
        self.__path    = Path(self.__pathMan.get_source_path())

    def __call__(self):
        pass

    def import_fn(self):
        imageMan  = ImageManager(frame=(0, 0))
        targetMan = TargetManager(0)
        filenames = self.__path.rglob("*.*")
        row_file_path    = Path(self.__pathMan.get_input_path())
        target_file_path = Path(self.__pathMan.get_target_path())
        for filename in filenames:
            to_file_F = self.__pathMan.get_input_filename(str(filename.name))
            imageMan.read(filename)
            imageMan.save(to_file_F)
            width, height = imageMan.get_size()

            targetMan.new(width, height)
            obj_name = str(filename.parent)
            d_new_targets = {'names'       : obj_name,
                             'description' : obj_name,
                             'rating'   : 0,
                             'coord x0' : 0,
                             'coord x1' : width,
                             'coord y0' : 0,
                             'coord y1' : height}
            targetMan.add_object(d_new_targets)
            to_file_T = self.__pathMan.get_target_filename(str(filename.name))
            targetMan.save(to_file_T)

    def export_fn(self):
        pass



