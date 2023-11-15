#!/usr/bin/python

from pathlib import Path
import pandas as pd
import numpy as np

class ShowFrame(object):
    def __init__(self):
        self.SHOW_NO = -1
        self.SHOW_ALL = 0
        self.SHOW_IMAGE = 1
        self.SHOW_NEW_TAB = 2
        self.__show_option = self.SHOW_NO

    def __str__(self):
        strRet = 'Labels:\n{}'.format(self.df_targets)
        return strRet

    def set_data(self, imageMan, targetMan):
        self.imageMan  = imageMan
        self.targetMan = targetMan

    def show(self):
        if(self.__show_option == self.SHOW_ALL):
            img = self.imageMan.get_image()
            self.editFrame.img_show(img)
            self.__show_option = self.SHOW_NO
        elif (self.__show_option == self.SHOW_IMAGE):
            img = self.imageMan.get_image()
            self.editFrame.img_show(img)
            self.__show_option = self.SHOW_NO
        elif (self.__show_option == self.SHOW_NEW_TAB):
            img = self.imageMan.get_image()
            self.editFrame.img_show(img)

            self.editFrame.set_work_frame(self.__filename)
            self.__show_option = self.SHOW_NO


    def set_target_object(self, target_object:dict):
        print('target_object', target_object)
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

    def add_object_frame(self, d_new_target:dict):
        d_new_target['rating'] = self.__default_rating
        self.add_object(d_new_target, self.get_object_size())
        
        self.selectObjectFrame.add(self.get_last_name(), self.get_object_size())
        self.descriptionFrame.set_text_frame(self.get_last_name(), self.get_last_description())
        self.ratingFrame.set_rating_frame(self.get_last_rating())

    def select_object_frame(self, item:int):
        self.save_description_frame()
        self.set_selected_object(item)
        self.update_last_name()
        
        self.descriptionFrame.set_text_frame(self.get_last_name(), self.get_last_description())
        self.ratingFrame.set_rating_frame(self.get_last_rating())
        self.editManager.show()

    def read_frame(self, filename:str):
        self.read(filename)

        self.update_description_frame()
        self.selectObjectFrame.init()

    def crop_last_name_frame(self):
        self.crop_last_name()

        self.update_description_frame()
        self.selectObjectFrame.init()
        self.editManager.show()

    def save_frame(self, filename):
        self.save_description_frame()
        #save target data to csv file
        self.save_targets(filename)

    def save_description_frame(self):
        text_description = self.descriptionFrame.get_text_frame()
        self.set_last_description(text_description)

    def cut_last_name_frame(self):
        self.cut_last_name()
        self.selectObjectFrame.cut(self.__selected_object)

    def double_last_name_frame(self):
        self.double_last_name()
        
        self.selectObjectFrame.add(self.last_name, self.__selected_object)
        self.descriptionFrame.set_text_frame(self.get_last_name(), self.get_last_description())
        self.ratingFrame.set_rating_frame(self.get_last_rating())


    def update_description_frame(self):
        self.selectObjectFrame.update()
        self.descriptionFrame.set_text_frame(self.get_last_name(), self.get_last_description())
        self.ratingFrame.set_rating_frame(self.get_last_rating())

    def update_object_frame(self):
        self.selectObjectFrame.update()
        self.descriptionFrame.set_text_frame(self.get_last_name(), self.get_last_description())
        self.ratingFrame.set_rating_frame(self.get_last_rating())


    def set_DescriptionFrame(self, descriptionFrame):
        self.descriptionFrame = descriptionFrame

    def set_SelectObjectFrame(self, selectObjectFrame):
        self.selectObjectFrame = selectObjectFrame

    def set_RatingFrame(self, ratingFrame):
        self.ratingFrame = ratingFrame

    def set_EditManager(self, editManager):
        self.editManager = editManager

    def set_EditFrame(self, editFrame):
        self.editFrame = editFrame
