#!/usr/bin/python

from pathlib import Path
import yaml
import numpy as np
from manager.target_man import *


class ObjectManager :
    def __init__(self, path_manager: object) :
        self.__pathMan = path_manager
        self.__object_names = self.__get_object_names()
        #to do
        #save only names that exist, the names that does not exist remove

    def set_object_names(self, names: 'array'):
        print('ObjectManager {}'.format(names))
        self.__object_names = names

    def add_object_names(self, names: 'array'):
        print('ObjectManager {}'.format(names))
        for name in names:
            self.__add_item_to_items(name)

    def add_object_name(self, name: str):
        print('ObjectManager {}'.format(name))
        self.__add_item_to_items(name)

    def get_object_names(self):
        return self.__object_names

    def get_user_object_freq(self):
        targetMan = TargetManager(0)
        d_object_names = {}
        for target_filename in self.__pathMan.get_target_filenames():
            filename = self.__pathMan.get_target_filename(str(target_filename))
            targetMan.read(filename)
            object_names = targetMan.get_names()
            for name in object_names:
                if (name in d_object_names) :
                    d_object_names[name] += 1
                else :
                    d_object_names[name]  = 1
        return d_object_names

    def __add_item_to_items(self, item: str):
        item = item.lower()
        if (self.__is_item_in_items(item) == False):
            print('__add_item_to_items {}'.format(item))
            self.__object_names = np.append(self.__object_names, item)

    def __is_item_in_items(self, item: str):
        size_similar_item = np.argwhere(self.__object_names == item).reshape(-1).shape[0]
        #print('size_similar_item {}'.format(size_similar_item))
        return (size_similar_item > 0)

    def __get_object_names(self):
        if (Path(self.__pathMan.get_object_info_file()).is_file()) :
            with open(self.__pathMan.get_object_info_file()) as file :
                config_list = yaml.load(file, Loader=yaml.FullLoader)
            retVal = config_list['object_names']
            print('get_object_names {}'.format(config_list))
        else :
            retVal = []
        return retVal

    def save(self) :
        # save default rating in yaml file
        names_yaml = """object_names : {}""".format(list(self.__object_names))
        print(names_yaml)
        names = yaml.safe_load(names_yaml)

        with open(self.__pathMan.get_object_info_file(), 'w') as file :
            yaml.dump(names, file)

