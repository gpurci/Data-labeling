#!/usr/bin/python

from pathlib import Path
from manager.image_man import *
from manager.target_man import *

class FolderStructure(object) :
    def __init__(self, object_man: object, import_frame: object) :
        self.__objectMan = object_man
        self.__import_frame = import_frame

    def __call__(self):
        pass

    def import_frame(self) :
        self.__import_frame.set_import_fn(self.__import_fn)
        self.__import_frame()

    def __import_fn(self, _pathMan, _default_rating):
        print('FolderStructure import method {}'.format('START'))
        imageMan  = ImageManager(frame=(0, 0))
        targetMan = TargetManager(0)
        filenames = list(Path(_pathMan.get_source_path()).rglob("*.*"))
        print('path {}, size filenames {}'.format(_pathMan.get_source_path(), len(filenames)))
        for filename in filenames:
            print('filename {}'.format(filename))
            imageMan.read(filename, False)
            if (imageMan.is_image()):
                to_file_F = _pathMan.get_input_filename(str(filename.name))
                imageMan.save(to_file_F)
                width, height = imageMan.get_size()

                targetMan.new(width, height)
                obj_name = str(filename.parts[-2])
                d_new_targets = {'names'       : obj_name,
                                 'description' : obj_name,
                                 'rating'   : _default_rating,
                                 'coord x0' : 0,
                                 'coord x1' : width,
                                 'coord y0' : 0,
                                 'coord y1' : height}
                targetMan.add_object(d_new_targets)
                to_file_T = _pathMan.get_target_filename(str(filename.name))
                targetMan.save(to_file_T)

                self.__objectMan.add_object_name(obj_name)

        print('FolderStructure import method {}'.format('END'))

    def export_fn(self, _pathMan):
        pass



