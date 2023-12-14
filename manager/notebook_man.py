#!/usr/bin/python

import yaml

from pathlib import Path
from manager.image_man import *
from manager.target_man.target_man import *


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
        self.__images    = []
        self.__targets   = []
        self.__filenames = []
        self.__idx_tab   = -1
        self.__read_config_yaml_file()

    def run(self) :
        self.__default_data()

    def __read_config_yaml_file(self) :
        if Path(self.config_file).is_file() :
            with open(self.config_file) as file :
                config_list = yaml.load(file, Loader=yaml.FullLoader)
            self.set_default_rating(config_list['default_rating'])
            print(config_list)
        else :
            self.set_default_rating(0)

    def __default_data(self) :
        self.__def_imageMan = ImageManager(frame=[self.dataDimension.get_width(), self.dataDimension.get_height()])

        self.__def_targetMan = TargetManager(self.__default_rating)
        self.__config(self.__def_imageMan, self.__def_targetMan)
        self.__def_imageMan.do_RGB_image((10, 10), (255, 255, 255))#to do
        self.__def_targetMan.read(self.default_target_file)

    def get_idx_filename(self, filename: str) :
        try:
            idx = self.__filenames.index(filename)
        except:
            idx = -1
            pass
        return idx

    def set_default_rating(self, rating: int) :
        self.__default_rating = rating
        for idx in range(self.get_tab_size()) :
            self.__images[idx].set_default_rating(self.__default_rating)

    def get_default_rating(self) :
        return self.__default_rating

    def save_configs(self) :
        # save default rating in yaml file
        names_yaml = """default_rating : {}""".format(self.__default_rating)
        names = yaml.safe_load(names_yaml)

        with open(self.config_file, 'w') as file :
            yaml.dump(names, file)
        print('default_rating {}, read {}'.format(self.__default_rating, open(self.config_file).read()))

    def get_tab_size(self) :
        return int(len(self.__images))

    def __str__(self) :
        strRet = """
        filename : {}
        tabs     : {}
        """.format(self.get_filename(), self.get_tab_size())
        return strRet

    def select_tab(self, idx: int) :
        print('select_tab {}'.format(idx))
        if (idx >= 0) and (idx < self.get_tab_size()) :
            self.__idx_tab = idx
            self.__set_data(self.imageMan(), self.targetMan())
            self.__showFrame.set_filename(self.get_filename())
            self.__showFrame.set_show_option(self.__showFrame.SHOW_SET_TAB)
            self.__notebookFrame.select_tab(self.__idx_tab)
        else :
            self.__idx_tab = -1

    def add(self, filename: str) :
        if (self.__pathMan.is_file(filename) == True):
            print('ADD tab {}'.format(filename))
            idx_filename = self.get_idx_filename(filename)
        else:
            if (self.__idx_tab == -1):
                idx_filename = -2
            else:
                idx_filename = self.__idx_tab
        if (idx_filename == -1):
            print('ADD idx_filename == -1 {}'.format(filename))
            self.__filenames.append(filename)
            imageMan = ImageManager(frame=[self.dataDimension.get_width(), self.dataDimension.get_height()])
            targetMan = TargetManager(self.__default_rating)
            self.__images.append(imageMan)
            self.__targets.append(targetMan)
            self.__config(imageMan, targetMan)
            self.__open(imageMan, targetMan)
            self.__notebookFrame.add(filename)
            self.select_tab(self.get_tab_size() - 1)
        else:
            self.select_tab(idx_filename)


    def imageMan(self) :
        if self.__idx_tab >= 0 :
            retVal = self.__images[self.__idx_tab]
        else :
            retVal = self.__def_imageMan
        return retVal

    def targetMan(self) :
        if self.__idx_tab >= 0 :
            retVal = self.__targets[self.__idx_tab]
        else :
            retVal = self.__def_targetMan
        return retVal

    def get_filename(self) :
        if self.__idx_tab >= 0 :
            retVal = self.__filenames[self.__idx_tab]
        else :
            retVal = 'Not files'
        return retVal

    def __config(self, imageMan: object, targetMan: object) :
        imageMan.set_EditFrame(self.__editFrame)

        targetMan.set_ShowFrame(self.__showFrame)

    def __open(self, imageMan: object, targetMan: object) :
        source_file = self.__pathMan.get_source_filename()
        print('source_file {}'.format(source_file))
        imageMan.read(source_file)

        dest_file = self.__pathMan.get_dest_filename()
        if Path(dest_file).is_file() :
            print('True  -> dest_file {}'.format(dest_file))
            targetMan.read(dest_file)
        else :
            print('False -> dest_file {}'.format(dest_file))
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

    def delete_tab(self, idx: int) :
        if (idx >= 0) and (idx < self.get_tab_size()) :
            del self.__images[idx]
            del self.__targets[idx]
            del self.__filenames[idx]
        elif self.get_tab_size() == 0 :
            self.__idx_tab = -1
        else :
            pass

    def double(self, filename: str):
        print('DOUBLE {}'.format(filename))
        imageMan  = self.imageMan().copy()
        targetMan = self.targetMan().copy()

        self.__filenames.append(filename)
        self.__images.append(imageMan)
        self.__targets.append(targetMan)

        self.__notebookFrame.add(filename)
        self.select_tab(self.get_tab_size() - 1)

    def save(self):
        filename = self.__pathMan.get_target_filename(self.get_filename())
        print('target_filename {}'.format(filename))
        self.targetMan().save(filename)
        filename = self.__pathMan.get_row_filename(self.get_filename())
        print('row_filename {}'.format(filename))
        if (Path(filename).is_file() == False):
            print('Save row_filename {}'.format(filename))
            self.imageMan().save(filename)




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

