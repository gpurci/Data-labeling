#!/usr/bin/python

from pathlib import Path
import yaml


class ResolutionManager :
    def __init__(self, path_parent, filename, config_file) :
        self.resolution = None
        self.height = None
        self.width = None
        self.path_parent = path_parent
        self.filename = filename
        self.config_file = config_file
        self.read_config_yaml_file()

    def read_config_yaml_file(self) :
        if Path(self.config_file).is_file() :
            with open(self.config_file) as file :
                config_list = yaml.load(file, Loader=yaml.FullLoader)
            self.width = config_list['width']
            self.height = config_list['height']
            self.resolution = config_list['resolution']
            print(config_list)
        else :
            self.width = 512
            self.height = 384
            self.resolution = self.width / self.height
            self.save_config(self.config_file)

    def get_config_filename(self) :
        return str(Path(self.path_parent).joinpath('name').with_name(self.filename))

    def set_path_parent(self, path_parent) :
        self.path_parent = path_parent

    def set_width(self, width) :
        self.width = width

    def set_height(self, height) :
        self.height = height

    def set_resolution(self, resolution) :
        self.resolution = resolution

    def save(self) :
        tmp_config_file = self.get_config_filename()
        self.save_config(tmp_config_file)

    def save_config(self, config_file) :
        # create a config file
        Path(self.path_parent).mkdir(mode=0o777, parents=True, exist_ok=True)
        Path(config_file).touch(mode=0o666, exist_ok=True)
        # save default rating in yaml file
        names_yaml = """
        width : {}
        height : {}
        resolution : {}
        """.format(self.width, self.height, self.resolution)
        names = yaml.safe_load(names_yaml)

        with open(config_file, 'w') as file :
            yaml.dump(names, file)
