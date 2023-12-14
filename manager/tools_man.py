#!/usr/bin/python

class ToolsManager:
    def __init__(self):
        self.__pathMan     = None
        self.__notebookMan = None
        self.__targetMan = None
        self.__imageMan  = None
        

    def crop(self, filename: str):
        print('CROP filename {}'.format(filename))
        self.__notebookMan.double(filename)
        box = self.__targetMan.get_last_coord()
        self.__imageMan.crop(box)
        self.__targetMan.crop_last_name()

    def set_data(self, imageMan: object, targetMan: object):
        self.__imageMan  = imageMan
        self.__targetMan = targetMan

    def set_PathManager(self, pathMan: object):
        self.__pathMan = pathMan

    def set_NotebookManager(self, notebookMan: object) :
        self.__notebookMan = notebookMan
