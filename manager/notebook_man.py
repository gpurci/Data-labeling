#!/usr/bin/python

from pathlib import Path
import yaml
from manager.image_man import *
from manager.target_man.target_man import *

class NotebookManager(object):
    def __init__(self, config_file):
        self.config_file = config_file + '/default_rating.yaml'
        self.default_target_file = config_file + '/default_target.csv'
        self.__images = []
        self.__targets = []
        self.__filenames = []
        self.__idx_tab = -1
        self.__read_config_yaml_file()

    def run(self):
        self.__default_data()

    def __read_config_yaml_file(self):
        if (Path(self.config_file).is_file() == True):
            with open(self.config_file) as file:
                config_list = yaml.load(file, Loader=yaml.FullLoader)
            self.set_default_rating(config_list['default_rating'])
            print(config_list)
        else:
            self.set_default_rating(0)

    def __default_data(self):
        self.__def_imageMan = ImageManager(frame=[self.dataDimension.get_width(), self.dataDimension.get_height()])

        self.__def_targetMan = TargetManager(self.__default_rating)
        self.__config(self.__def_imageMan, self.__def_targetMan)
        self.__def_imageMan.false_image()
        self.__def_targetMan.read(self.default_target_file)


    def set_default_rating(self, rating:int):
        self.__default_rating = rating
        for idx in range(self.get_tab_size()):
            self.__images[idx].set_default_rating(self.__default_rating)

    def get_default_rating(self):
        return self.__default_rating

    def save_configs(self):
        #save default rating in yaml file
        names_yaml = """default_rating : {}""".format(self.__default_rating)
        names = yaml.safe_load(names_yaml)

        with open(self.config_file, 'w') as file:
            yaml.dump(names, file)
        print('default_rating {}, read {}'.format(self.__default_rating, open(self.config_file).read()))

    def get_tab_size(self):
        return int(len(self.__images))

    def __str__(self):
        strRet = """
        filename : {}
        tabs     : {}
        """.format(self.get_filename(), self.get_tab_size())
        return (strRet)

    def select_tab(self, idx:int):
        print('select_tab', type(idx))
        if ((idx >= 0) and (idx < self.get_tab_size())):
            self.__idx_tab = idx
            self.__set_data(self.imageMan(), self.targetMan())
            self.showFrame.set_filename(self.get_filename())
            self.showFrame.set_show_option(self.showFrame.SHOW_SET_TAB)
        else:
            self.__idx_tab = -1

    def add(self, filename:str):
        self.__filenames.append(filename)
        self.pathManager.set_filename(filename)
        imageMan = ImageManager(frame=[self.dataDimension.get_width(), self.dataDimension.get_height()])
        targetMan = TargetManager(self.__default_rating)
        self.__images.append(imageMan)
        self.__targets.append(targetMan)
        self.__config(imageMan, targetMan)
        self.__open(imageMan, targetMan)
        print('add tab {}'.format(filename))
        self.select_tab(self.get_tab_size()-1)

        self.showFrame.set_filename(self.get_filename())
        self.showFrame.set_show_option(self.showFrame.SHOW_NEW_TAB)

    def imageMan(self):
        if (self.__idx_tab >= 0):
            retVal = self.__images[self.__idx_tab]
        else:
            retVal = self.__def_imageMan
        return retVal

    def targetMan(self):
        if (self.__idx_tab >= 0):
            retVal = self.__targets[self.__idx_tab]
        else:
            retVal = self.__def_targetMan
        return retVal

    def get_filename(self):
        if (self.__idx_tab >= 0):
            retVal = self.__filenames[self.__idx_tab]
        else:
            retVal = None
        return retVal

    def __config(self, imageMan:object, targetMan:object):
        imageMan.set_img_show_fn(self.editFrame.img_show)
        imageMan.set_rectangle_img_show_fn(self.editFrame.rectange_img_show)
        imageMan.set_move_fn(self.editFrame.move)
        imageMan.set_coords_fn(self.editFrame.coords)
        imageMan.set_edit_mode_fn(self.editFrame.edit_mode)

        targetMan.set_ShowFrame(self.showFrame)


    def __open(self, imageMan:object, targetMan:object):
        source_file = self.pathManager.get_source_filename()
        imageMan.read(source_file)

        dest_file      = self.pathManager.get_dest_filename()
        if (Path(dest_file).is_file() == True):
            print('True  -> dest_file {}'.format(dest_file))
            targetMan.read(dest_file)
        else:
            print('False -> dest_file {}'.format(dest_file))
            x, y = imageMan.get_image_size()
            targetMan.new_frame(x, y)
        print('datasets {}'.format(targetMan))


    def __set_data(self, imageMan:object, targetMan:object):
        self.toolsManager.set_data(imageMan, targetMan)
        self.editManager.set_data(imageMan, targetMan)

        self.selectObjectFrame.set_data(imageMan, targetMan)
        self.ratingFrame.set_data(imageMan, targetMan)
        self.descriptionFrame.set_data(imageMan, targetMan)
        self.showFrame.set_data(imageMan, targetMan)

    def delete_tab(self, idx:int):
        if ((idx >= 0) and (idx < self.get_tab_size())):
            del self.__images[idx]
            del self.__targets[idx]
            del self.__filenames[idx]
        elif (self.get_tab_size() == 0):
            self.__idx_tab = -1
        else:
            pass




    def set_DataDimension(self, dataDimension):
        self.dataDimension = dataDimension

    def set_ToolsManager(self, toolsManager):
        self.toolsManager = toolsManager

    def set_EditManager(self, editManager):
        self.editManager = editManager

    def set_PathManager(self, pathManager):
        self.pathManager = pathManager

    def set_EditFrame(self, editFrame):
        self.editFrame = editFrame

    def set_DescriptionFrame(self, descriptionFrame):
        self.descriptionFrame = descriptionFrame

    def set_SelectObjectFrame(self, selectObjectFrame):
        self.selectObjectFrame = selectObjectFrame

    def set_RatingFrame(self, ratingFrame):
        self.ratingFrame = ratingFrame

    def set_NotebookFrame(self, notebookFrame):
        self.notebookFrame = notebookFrame

    def set_ShowFrame(self, showFrame:object):
        self.showFrame = showFrame
