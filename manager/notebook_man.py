#!/usr/bin/python

from pathlib import Path
import yaml
from manager.image_man import *
from manager.target_man.target_man import *

class NotebookManager(object):
    def __init__(self, config_file):
        self.config_file = config_file
        self.__images = []
        self.__targets = []
        self.__filenames = []
        self.__idx_tab = -1
        self.read_config_yaml_file(self.config_file)

    def read_config_yaml_file(self, config_file:str):
        if (Path(config_file).is_file() == True):
            with open(config_file) as file:
                config_list = yaml.load(file, Loader=yaml.FullLoader)
            self.set_default_rating(config_list['default_rating'])
            print(config_list)
        else:
            self.set_default_rating(0)

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
        else:
            self.__idx_tab = -1

    def select_tab_frame(self, idx:int):
        print('select_tab', type(idx))
        if ((idx >= 0) and (idx < self.get_tab_size())):
            self.__idx_tab = idx
            self.set_data(self.image(), self.target())

            filename = self.get_filename()
            self.editManager.set_work_frame(filename)
            self.editManager.show()
        else:
            self.__idx_tab = -1

    def add(self, filename):
        self.__filenames.append(filename)
        self.pathManager.set_filename(filename)
        image_man = ImageManager(frame=[self.dataDimension.get_width(), self.dataDimension.get_height()])
        source_file = self.pathManager.get_source_filename()
        image_man.read(source_file)


        target_man = TargetManager(self.__default_rating)
        dest_file      = self.pathManager.get_dest_filename()
        if (Path(dest_file).is_file() == True):
            print('True  -> dest_file {}'.format(dest_file))
            target_man.read_frame(dest_file)
        else:
            print('False -> dest_file {}'.format(dest_file))
            x, y = image_man.get_image_size()
            target_man.new_frame(x, y)
        print('datasets {}'.format(target_man))
                                
        self.__images.append(image_man)
        self.__targets.append(target_man)
        self.config()
        print('add tab {}'.format(filename))
        self.select_tab_frame(self.get_tab_size()-1)

    def image(self):
        if (self.__idx_tab >= 0):
            retVal = self.__images[self.__idx_tab]
        else:
            retVal = None
        return retVal

    def target(self):
        if (self.__idx_tab >= 0):
            retVal = self.__targets[self.__idx_tab]
        else:
            retVal = None
        return retVal

    def get_filename(self):
        if (self.__idx_tab >= 0):
            retVal = self.__filenames[self.__idx_tab]
        else:
            retVal = None
        return retVal

    def config(self):
        image = self.__images[self.get_tab_size()-1]
        image.set_img_show_fn(self.editFrame.img_show)
        image.set_rectangle_img_show_fn(self.editFrame.rectange_img_show)
        image.set_move_fn(self.editFrame.move)
        image.set_coords_fn(self.editFrame.coords)
        image.set_edit_mode_fn(self.editFrame.edit_mode)

        target = self.__targets[self.get_tab_size()-1]
        target.set_SelectObjectFrame(self.selectObjectFrame)
        target.set_DescriptionFrame(self.descriptionFrame)
        target.set_RatingFrame(self.ratingFrame)
        target.set_EditManager(self.editManager)

    def set_data(self, imageMan, targetMan):
        self.toolsManager.set_data(imageMan, targetMan)
        self.editManager.set_data(imageMan, targetMan)

        self.selectObjectFrame.set_data(imageMan, targetMan)
        self.ratingFrame.set_data(imageMan, targetMan)

    def add_frame(self, filename):
        self.add(filename)
        self.notebookFrame.add(filename)

    def delete_tab(self, index):
        del self.__images[index]
        del self.__targets[index]
        del self.__filenames[index]



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
