#!/usr/bin/python

import yaml

from pathlib import Path
import numpy as np

from manager.image_man import *
from manager.target_man import *


class TabManager(object):
    def __init__(self) :
        self.__tabs = {}
        self.__names = []
        self.__feature = {'image':0, 'target':1}

    def __call__(self, name: str, feature: str):
        tab = self.get_tab(name)
        if (tab != None):
            retFeature = tab[self.__feature[feature]]
        else:
            retFeature = None
        return retFeature

    def get_tab(self, name: str):
        return self.__tabs.get(name, None)

    def get_tab_feature(self, name: str, feature: str):
        tab = self.get_tab(name)
        if (tab != None):
            retFeature = tab[self.__feature[feature]]
        else:
            retFeature = None
        return retFeature

    def get_name(self, idx: int):
        if ((idx >= 0) and (idx < self.get_size())):
            retVal = self.__names[idx]
        else:
            retVal = None
        return retVal

    def get_index(self, name: str):
        try:
            idx = self.__names.index(name)
        except:
            idx = -1
        return idx

    def get_names(self):
        return self.__names

    def get_size(self):
        return len(self.__names)

    def delete_tab(self, name: str):
        idx = self.get_index(name)
        if (idx >= 0):
            del self.__names[idx]
            del self.__tabs[name]


    def set_tab(self, name: str, imageMan: object, targetMan: object):
        self.__names.append(name)
        self.__tabs[name] = (imageMan, targetMan)



class NotebookManager :
    def __init__(self, config_file: str) :
        self.toolsManager = None
        self.editManager  = None
        self.__pathMan    = None
        self.__editFrame  = None
        self.descriptionFrame  = None
        self.selectObjectFrame = None
        self.ratingFrame     = None
        self.__notebookFrame = None
        self.__showFrame     = None
        self.__addNameFrame  = None
        self.dataDimension   = None
        self.__default_rating = None

        self.config_file         = config_file + '/default_rating.yaml'
        self.default_target_file = config_file + '/default_target.csv'

        self.__tabMan    = TabManager()
        self.__tab_name  = None
        self.__read_config_yaml_file()

    def run(self) :
        self.__default_data()

    def __default_data(self) :
        self.__def_imageMan  = ImageManager(frame=self.dataDimension.get_size())

        self.__def_targetMan = TargetManager(self.__default_rating)
        self.__config(self.__def_imageMan, self.__def_targetMan)
        self.__def_imageMan.new((4, 4), (255, 255, 255))
        self.__def_targetMan.read(self.default_target_file)

    def set_default_rating(self, rating: int) :
        self.__default_rating = rating
        for name in self.__tabMan.get_names():
            self.__tabMan(name, 'target').set_default_rating(self.__default_rating)

    def get_default_rating(self) :
        return self.__default_rating

    def get_tab_name(self, idx=None) : #idx: int
        if (idx == None):
            retVal = self.__tab_name
        else:
            retVal = self.__tabMan.get_name(idx)
        return retVal

    def get_tabs(self) :
        return np.array(self.__tabMan.get_names())

    def get_tab_size(self) :
        return self.__tabMan.get_size()

    def __str__(self) :
        strRet = """
        filename : {}
        tabs     : {}
        size     : {}
        """.format(self.__tab_name, self.__tabMan.get_names(), self.__tabMan.get_size())
        return strRet

    def select_tab(self, name: str) :
        print('select_tab {}'.format(name))
        idx = self.__tabMan.get_index(name)
        if (idx >= 0):
            self.__tab_name = name
            self.__set_data(self.imageMan(), self.targetMan())
            self.__showFrame.set_filename(self.__tab_name)
            self.__showFrame.set_show_option(self.__showFrame.SHOW_SET_TAB)
            self.__notebookFrame.select_tab(idx)

    def add(self, filename: str) :
        print('ADD filename {}'.format(filename))
        if (self.__pathMan.is_file(filename) == True):
            # file exist
            self.__pathMan.set_filename(filename)
            print('ADD tab {}'.format(filename))
            if (self.__tabMan.get_index(filename) == -1): 
                # make new tab
                print('ADD make new tab {}'.format(filename))
                imageMan  = ImageManager(frame=self.dataDimension.get_size())
                targetMan = TargetManager(self.__default_rating)
                self.__tabMan.set_tab(filename, imageMan, targetMan)
                self.__config(imageMan, targetMan)
                self.__open(imageMan, targetMan)
                self.__notebookFrame.add(filename)
            else: 
                #tab exist
                pass
            # select tab
            self.select_tab(filename)
        else:
            # is not a file
            #do nothing
            pass


    def imageMan(self, tab_name=None) : #tab_name: str
        if (tab_name == None):
            tab_name = self.__tab_name
        retVal = self.__tabMan(tab_name, 'image')

        if (retVal == None) :
            retVal = self.__def_imageMan
        return retVal

    def targetMan(self, tab_name=None) : #tab_name: str
        if (tab_name == None):
            tab_name = self.__tab_name
        retVal = self.__tabMan(tab_name, 'target')

        if (retVal == None) :
            retVal = self.__def_targetMan
        return retVal

    def __config(self, imageMan: object, targetMan: object) :
        imageMan.set_EditFrame(self.__editFrame)
        targetMan.set_ShowFrame(self.__showFrame)

    def __open(self, imageMan: object, targetMan: object) :
        print('NotebookManager OPEN')
        image_file = self.__pathMan.get_source_filename()
        print('image_file {}'.format(image_file))
        imageMan.read(image_file)
        imageMan.vDoImageTK()

        target_file = self.__pathMan.get_target_filename()
        if (Path(target_file).is_file() == True) :
            print('True  -> target_file {}'.format(target_file))
            targetMan.read(target_file)
        else :
            print('False -> target_file {}'.format(target_file))
            x, y = imageMan.get_size()
            targetMan.new(x, y)
        print('datasets {}'.format(targetMan))

    def __set_data(self, imageMan: object, targetMan: object) :
        self.toolsManager.set_data(imageMan, targetMan)
        self.editManager.set_data(imageMan, targetMan)

        self.selectObjectFrame.set_data(imageMan, targetMan)
        self.ratingFrame.set_data(imageMan, targetMan)
        self.descriptionFrame.set_data(imageMan, targetMan)
        
        self.__showFrame.set_data(imageMan, targetMan)

    def delete_tab(self, tab_name: str) :
        self.__save_dataset(tab_name)
        self.__tabMan.delete_tab(tab_name)
        

    def double(self, filename: str):
        print('DOUBLE {}'.format(filename))
        imageMan  = self.imageMan().copy()
        targetMan = self.targetMan().copy()

        self.__tabMan.set_tab(filename, imageMan, targetMan)

        self.__notebookFrame.add(filename)
        self.select_tab(filename)

    def __read_config_yaml_file(self) :
        if (Path(self.config_file).is_file()):
            with open(self.config_file) as file :
                config_list = yaml.load(file, Loader=yaml.FullLoader)
            self.set_default_rating(config_list['default_rating'])
            print(config_list)
        else :
            self.set_default_rating(0)

    def __save_configs(self):
        # save default rating in yaml file
        config_data = """default_rating : {}""".format(self.__default_rating)
        config_data_yaml = yaml.safe_load(config_data)

        with open(self.config_file, 'w') as file :
            yaml.dump(config_data_yaml, file)
        print('default_rating {}, read {}'.format(self.__default_rating, open(self.config_file).read()))

    def __save_dataset(self, tab_name=None): # tab_name: str
        if (tab_name == None):
            tab_name = self.__tab_name

        if (tab_name != None) :
            file = self.__pathMan.get_target_filename(tab_name)
            print('target_filename {}'.format(file))
            self.targetMan(tab_name).save(file)
            file = self.__pathMan.get_input_filename(tab_name)
            print('image_filename {}'.format(file))
            if (Path(file).is_file() == False):
                print('Save filename {}'.format(file))
                self.imageMan(tab_name).save(file)
        else:
            # not open tab
            pass

    def save(self):
        self.__save_configs()
        self.__save_dataset()





    def set_DataDimension(self, dataDimension) :
        self.dataDimension = dataDimension

    def set_ToolsManager(self, toolsManager) :
        self.toolsManager = toolsManager

    def set_EditManager(self, editManager) :
        self.editManager = editManager

    def set_PathManager(self, pathManager) :
        self.__pathMan = pathManager

    def set_EditFrame(self, editFrame) :
        self.__editFrame = editFrame

    def set_DescriptionFrame(self, descriptionFrame) :
        self.descriptionFrame = descriptionFrame

    def set_SelectObjectFrame(self, selectObjectFrame) :
        self.selectObjectFrame = selectObjectFrame

    def set_RatingFrame(self, ratingFrame) :
        self.ratingFrame = ratingFrame

    def set_NotebookFrame(self, notebookFrame) :
        self.__notebookFrame = notebookFrame

    def set_ShowFrame(self, showFrame: object) :
        self.__showFrame = showFrame

