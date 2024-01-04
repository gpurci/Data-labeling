#!/usr/bin/python

from pathlib import Path

from manager.image_man import *
from manager.target_man import *
from manager.run_extern_script import *


class RunDetectScript(object) :
    def __init__(self, path_man: object, resolution_man: object, object_man: object, config_file: str) :
        self.__pathMan       = path_man
        self.__resolutionMan = resolution_man
        self.__objectMan     = object_man

        self.__run_extern_script = RunExternScript(config_file, r'./run_script/import_library.py', r'./run_script/run.py')

        self.__imageMan  = ImageManager(frame=self.__resolutionMan.get_size())
        self.__targetMan = TargetManager(0)

    def __str__(self):
        return ''

    def get_imageMan(self):
        return self.__imageMan

    def get_targetMan(self):
        return self.__targetMan

    def folder_detector(self):
        self.__run_extern_script.update()
        print('FOLDER DETECTOR {}'.format(None))
        for file in self.__pathMan.get_input_files():
            self.file_detector(str(file))

    def source_detector(self):
        self.__run_extern_script.update()
        print('SOURCE DETECTOR {}'.format(None))
        for file in self.__pathMan.get_source_files():
            self.source_file_detector(str(file))

    def source_file_detector(self, filename: str):
        print('SOURCE FILE DETECTOR {}'.format(filename))
        source_file = self.__pathMan.get_source_filename(filename)
        print('source_file {}'.format(source_file))
        self.__imageMan.read(source_file)
        self.__imageMan.standardization((0, 0, 0))

        man_image = self.__imageMan.get_man_data()
        im_width, im_height = man_image.size
        self.__targetMan.new(im_width, im_height)

        self.__local['run_detector'](self.__local['detector'], man_image, self.__targetMan, 0.1, None, self.__local)
        self.__targetMan.resize_coord(self.__imageMan.calc_man_coord_to_target)
        self.__objectMan.add_object_names(self.__targetMan.get_names())

        row_input_file = self.__pathMan.get_input_filename(filename)
        self.__imageMan.save(row_input_file)

        row_target_file = self.__pathMan.get_target_filename(filename)
        print('row_target_file {}'.format(row_target_file))

        self.__targetMan.save(row_target_file)

    def file_detector(self, filename: str):
        print('FILE DETECTOR {}'.format(filename))
        row_input_file = self.__pathMan.get_input_filename(file)
        print('row_input_file {}'.format(row_input_file))
        self.__imageMan.read(row_input_file)
        self.__imageMan.standardization((0, 0, 0))

        man_image = self.__imageMan.get_man_data()
        im_width, im_height = man_image.size
        self.__targetMan.new(im_width, im_height)

        self.__local['run_detector'](self.__local['detector'], man_image, self.__targetMan, 0.1, None, self.__local)

        man_input_file = self.__pathMan.get_man_input_filename(filename)
        self.__imageMan.save(man_input_file)
        self.__targetMan.resize_coord(self.__imageMan.calc_man_coord_to_target)
        self.__objectMan.add_object_names(self.__targetMan.get_names())

        man_target_file = self.__pathMan.get_man_target_filename(filename)
        print('man_target_file {}'.format(man_target_file))

        self.__targetMan.save(man_target_file)

    def image_detector(self, imageMan: object, targetMan: object):
        self.__run_extern_script.update()
        self.__local = self.__run_extern_script.get_locals()
        print('IMAGE DETECTOR {}'.format('Start'))
        imageMan.standardization((0, 0, 0))
        man_image = imageMan.get_man_data()
        im_width, im_height = man_image.size
        print('size {}, im_width {}, im_height {}'.format(man_image.size, im_width, im_height))
        self.__targetMan.new(im_width, im_height)

        self.__local['run_detector'](self.__local['detector'], man_image, self.__targetMan, 0.1, None, self.__local)
        print(self.__targetMan)
        self.__targetMan.resize_coord(imageMan.calc_man_coord_to_target)
        self.__objectMan.add_object_names(self.__targetMan.get_names())

        targetMan.concatenate(self.__targetMan)
        print('IMAGE DETECTOR {}'.format('End'))

