#!/usr/bin/python

from pathlib import Path
import yaml


class Standardization :
    def __init__(self, path_manager: object, resolution_man: object) :
        self.__pathMan       = path_manager
        self.__resolutionMan = resolution_man

    def __call__(self):
        print('Standardization {}'.format('run'))
        imageMan  = ImageManager(frame=self.__resolutionMan.get_size())
        targetMan = TargetManager(0)

        for file in self.__pathMan.get_row_files():
            row_input_file = self.__pathMan.get_row_input_filename(file)
            man_input_file = self.__pathMan.get_man_input_filename(file)
            imageMan.read_standardization(row_input_file, (0, 0, 0))
            imageMan.save(man_input_file)

            row_target_file = self.__pathMan.get_row_target_filename(file)
            man_target_file = self.__pathMan.get_man_target_filename(file)
            targetMan.read(row_target_file)
            targetMan.resize_coord(imageMan.get_zoom())
            targetMan.save(man_target_file)
            





