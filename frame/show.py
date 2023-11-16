#!/usr/bin/python

from pathlib import Path
import pandas as pd
import numpy as np

class ShowFrame(object):
    def __init__(self):
        self.SHOW_NO = -1
        self.SHOW_OBJECT = 0
        self.SHOW_IMAGE = 1
        self.SHOW_SET_TAB = 2
        self.SHOW_NEW_TAB = 3
        self.SHOW_FILENAMES = 4
        self.__show_option = self.SHOW_NO

    def __str__(self):
        strRet = 'Labels:\n{}'.format(self.df_targets)
        return strRet

    def set_data(self, imageMan, targetMan):
        self.imageMan  = imageMan
        self.targetMan = targetMan

    def show(self):
        if(self.__show_option == self.SHOW_NO):
            pass
        elif(self.__show_option == self.SHOW_OBJECT):
            img = self.imageMan.get_image()
            self.editFrame.img_show(img)
            box = (self.__target_object['coord x0'], self.__target_object['coord y0'], self.__target_object['coord x1'], self.__target_object['coord y1'])
            box = self.imageMan.calc_coord_from_target(box)
            self.editFrame.rectange_img_show(box, self.__target_object['names'])
            self.selectObjectFrame.show()
            self.descriptionFrame.set_text_frame(self.__target_object['names'], self.__target_object['description'])
            self.ratingFrame.set_rating_frame(self.__target_object['rating'])
            pass
        elif (self.__show_option == self.SHOW_IMAGE):
            print('SHOW_IMAGE')
            img = self.imageMan.get_image()
            self.editFrame.img_show(img)
            pass
        elif (self.__show_option == self.SHOW_SET_TAB):
            print('SHOW_SET_TAB')
            img = self.imageMan.get_image()
            self.editFrame.img_show(img)
            self.editFrame.set_work_frame(self.__filename)
            self.selectObjectFrame.show()
            pass
        elif (self.__show_option == self.SHOW_NEW_TAB):
            print('SHOW_NEW_TAB')
            self.notebookFrame.add(self.__filename)
            img = self.imageMan.get_image()
            self.editFrame.img_show(img)
            self.editFrame.set_work_frame(self.__filename)
            self.selectObjectFrame.show()
            pass
        elif (self.__show_option == self.SHOW_FILENAMES):
            print('SHOW_FILENAMES')
            self.selectFilenameFrame.show()
            pass
        
        self.__show_option = self.SHOW_NO


    def set_target_object(self, target_object:dict):
        print('target_object \n@{}@'.format(target_object))
        self.__target_object = target_object

    def set_item(self, item):
        self.__item = item

    def set_name(self, name):
        self.__name = name

    def set_show_option(self, show_option):
        self.__show_option = show_option

    def set_filename(self, filename):
        self.__filename = filename

    def set_rectangle(self, box):
        self.__box = box




    def set_DescriptionFrame(self, descriptionFrame):
        self.descriptionFrame = descriptionFrame

    def set_SelectObjectFrame(self, selectObjectFrame):
        self.selectObjectFrame = selectObjectFrame

    def set_SelectFilenameFrame(self, selectFilenameFrame):
        self.selectFilenameFrame = selectFilenameFrame

    def set_RatingFrame(self, ratingFrame):
        self.ratingFrame = ratingFrame

    def set_EditManager(self, editManager):
        self.editManager = editManager

    def set_EditFrame(self, editFrame):
        self.editFrame = editFrame

    def set_NotebookFrame(self, notebookFrame):
        self.notebookFrame = notebookFrame
