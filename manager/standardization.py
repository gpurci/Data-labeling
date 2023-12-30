#!/usr/bin/python

from pathlib import Path
import yaml

from manager.image_man import *
from manager.target_man import *

class Standardization :
    def __init__(self, path_manager: object, resolution_man: object) :
        self.__pathMan       = path_manager
        self.__resolutionMan = resolution_man

    def __call__(self):
        print('\n\n\n\nSTANDARDIZATION {}'.format('run'))
        imageMan  = ImageManager(frame=self.__resolutionMan.get_size())
        targetMan = TargetManager(0)

        for file in self.__pathMan.get_input_files():
            file = str(file)
            print('file {}, type {}'.format(file, type(file)))
            row_input_file = self.__pathMan.get_input_filename(file)
            man_input_file = self.__pathMan.get_man_input_filename(file)
            print('man_input_file {}'.format(man_input_file))
            imageMan.read(row_input_file)
            imageMan.standardization((0, 0, 0))
            imageMan.save(man_input_file, True)

            row_target_file = self.__pathMan.get_target_filename(file)
            man_target_file = self.__pathMan.get_man_target_filename(file)
            print('row_target_file {},\nman_target_file {}'.format(row_target_file, man_target_file))
            targetMan.read(row_target_file)
            targetMan.resize_coord(imageMan.calc_coord_from_target)
            x, y = imageMan.get_size()
            targetMan.set_size(x, y)
            targetMan.save(man_target_file)

        self.__pathMan.set_source_path(self.__pathMan.get_man_input_path())

    def export_image(self, file: str, imageMan: object):
        print('export_image file {}'.format(file))
        row_input_file = self.__pathMan.get_input_filename(file)
        print('row_input_file {}'.format(row_input_file))
        imageMan.read(row_input_file)
        imageMan.standardization((0, 0, 0))


            





