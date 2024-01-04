#!/usr/bin/python

class ToolsManager:
    def __init__(self):
        self.__pathMan     = None
        self.__notebookMan = None
        self.__targetMan = None
        self.__imageMan  = None
        self.__showFrame = None
        

    def transparency(self):
        print('TRANSPARENCY {}'.format('start'))
        self.__imageMan.transparency((1., 1., 1.3))
        print('TRANSPARENCY {}'.format('end'))
        if (self.__showFrame != None):
            self.__showFrame.set_show_option(self.__showFrame.SHOW_OBJECT)

    def detect(self):
        print('DETECT {}'.format('start'))
        self.__runExtScript.image_detector(self.__imageMan, self.__targetMan)
        print('DETECT {}'.format('end'))

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

    def set_RunExternScript(self, runExtScript: object) :
        self.__runExtScript = runExtScript

    def set_ShowFrame(self, showFrame: object) :
        self.__showFrame = showFrame
