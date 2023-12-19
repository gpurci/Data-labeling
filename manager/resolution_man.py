#!/usr/bin/python

from pathlib import Path
import yaml


class ResolutionManager :
    def __init__(self, path_parent: str, filename: str, config_file: str):
        self.__resolution  = None
        self.__height      = None
        self.__width       = None
        self.__path_parent = path_parent
        self.__filename    = filename
        self.__config_file = config_file
        self.__read_config_yaml_file()

    def __read_config_yaml_file(self):
        if (Path(self.__config_file).is_file()):
            with open(self.__config_file) as file :
                config_list = yaml.load(file, Loader=yaml.FullLoader)

            self.__width      = config_list['width']
            self.__height     = config_list['height']
            self.__resolution = config_list['resolution']
            print(config_list)
        else :
            self.__width      = 512
            self.__height     = 384
            self.__resolution = self.__width / self.__height
            self.save_config(self.__config_file)

    def __get_config_filename(self) :
        return str(Path(self.__path_parent).joinpath('name').with_name(self.__filename))

    def set_path_parent(self, path_parent: str) :
        self.__path_parent = path_parent

    def set_width(self, width: int) :
        self.__width  = width

    def set_height(self, height: int) :
        self.__height = height

    def set_resolution(self, resolution: int) :
        self.__resolution = resolution

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_size(self):
        return (self.__width, self.__height)

    def save(self) :
        tmp_config_file = self.__get_config_filename()
        self.__save_config(tmp_config_file)

    def __save_config(self, config_file: str) :
        # create a config file
        Path(self.__path_parent).mkdir(mode=0o777, parents=True, exist_ok=True)
        Path(config_file).touch(mode=0o666, exist_ok=True)
        # save default rating in yaml file
        names_yaml = """
        width      : {}
        height     : {}
        resolution : {}
        """.format(self.__width, self.__height, self.__resolution)
        names = yaml.safe_load(names_yaml)

        with open(config_file, 'w') as file :
            yaml.dump(names, file)
