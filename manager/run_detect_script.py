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

        self.__imageMan  = ImageManager(frame=self.__resolutionMan.get_det_size())
        self.__targetMan = TargetManager(0)

    def __str__(self):
        return ''

    def folder_detector(self):
        self.__run_extern_script.update()
        print('FOLDER DETECTOR {}'.format(None))
        imageMan  = ImageManager(frame=self.__resolutionMan.get_det_size())
        targetMan = TargetManager(0)

        for filename in self.__pathMan.get_input_files():
            filename = str(filename)
            input_filename  = self.__pathMan.get_input_filename(filename)
            target_filename = self.__pathMan.get_target_filename(filename)
            print('input_filename {}'.format(input_filename))
            imageMan.read(input_filename, False)
            if (imageMan.is_image()):
                if (Path(target_filename).is_file() == True) :
                    targetMan.read(target_filename)
                else :
                    x, y = imageMan.get_size()
                    targetMan.new(x, y)
                self.__detect(imageMan, targetMan)
                print('target_filename {}'.format(target_filename))

                targetMan.save(target_filename)

    def image_detector(self, imageMan: object, targetMan: object):
        self.__run_extern_script.update()
        self.__local = self.__run_extern_script.get_locals()
        imageMan.set_size_standard(self.__resolutionMan.get_det_size())
        self.__detect(imageMan, targetMan)

    def __detect(self, imageMan: object, targetMan: object):
        print('IMAGE DETECTOR {}'.format('Start'))
        imageMan.standardization((0, 0, 0))
        man_image = imageMan.get_man_data()
        im_width, im_height = man_image.size
        print('size {}, im_width {}, im_height {}'.format(man_image.size, im_width, im_height))
        self.__targetMan.new(im_width, im_height)

        self.__local['run_detector'](self.__local['detector'], man_image, self.__targetMan, 0.1, None, self.__local)
        print(self.__targetMan)
        x, y = imageMan.get_size()
        self.__targetMan.set_size(x, y)
        self.__targetMan.resize_coord(imageMan.calc_man_coord_to_target)
        self.__objectMan.add_object_names(self.__targetMan.get_names())

        targetMan.concatenate(self.__targetMan)
        print('IMAGE DETECTOR {}'.format('End'))

