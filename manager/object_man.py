#!/usr/bin/python

from pathlib import Path
import yaml


class ObjectManager :
    def __init__(self, path_manager: object) :
        self.__pathMan = path_manager
        self.__object_names = self.__get_object_names()
        #to do
        #save only names that exist, the names that does not exist remove

    def set_object_names(self, names: 'array'):
        print('ObjectManager {}'.format(names))
        self.__object_names = names

    def get_object_names(self):
        return self.__object_names

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
