#!/usr/bin/python

from pathlib import Path
import yaml

class PathManager(object):
    def __init__(self, config_file):
        self.config_file = config_file
        self.read_config_yaml_file(self.config_file)
        self.filename = None
        self.file_suffix = None

    def __str__(self):
        strRet = """
        source_path : {}
        dest_path : {}
        input_parent_row : {}
        input_parent_man : {}
        output_parent : {}
        description_parent : {}
        input_suffix : {}
        output_suffix : {}
        """.format(self.source_path, self.dest_path, 
                        self.input_parent_row, self.input_parent_man, self.output_parent, self.description_parent,
                        self.input_suffix, self.output_suffix)
        return (strRet)

    def read_config_yaml_file(self, config_file):
        if (Path(config_file).is_file() == True):
            with open(config_file) as file:
                # The FullLoader parameter handles the conversion from YAML
                # scalar values to Python the dictionary format
                config_list = yaml.load(file, Loader=yaml.FullLoader)
            
            if ('source_path' in config_list):
                self.source_path = config_list['source_path']
            else:
                self.source_path = '/.'
            if ('dest_path' in config_list):
                self.dest_path = config_list['dest_path']
            else:
                self.dest_path = '/.'
            if ('input_parent_row' in config_list):
                self.input_parent_row = config_list['input_parent_row']
            else:
                self.input_parent_row = 'row'
            if ('input_parent_man' in config_list):
                self.input_parent_man = config_list['input_parent_man']
            else:
                self.input_parent_man = 'man'
            if ('output_parent' in config_list):
                self.output_parent = config_list['output_parent']
            else:
                self.output_parent = 'targets'
            if ('description_parent' in config_list):
                self.description_parent = config_list['description_parent']
            else:
                self.description_parent = 'description'
            if ('input_suffix' in config_list):
                self.input_suffix = config_list['input_suffix']
            else:
                self.input_suffix = '.png'
            if ('output_suffix' in config_list):
                self.output_suffix = config_list['output_suffix']
            else:
                self.output_suffix = '.csv'
            print(config_list)
        else:
            self.source_path = '/.'
            self.dest_path = '/.'
            self.input_parent_row = 'row'
            self.input_parent_man = 'man'
            self.output_parent = 'targets'
            self.description_parent = 'description'
            self.input_suffix = '.png'
            self.output_suffix = '.csv'
            self.save_config(config_file)

    def save(self):
        self.save_config(self.config_file)

    def save_config(self, config_file):
        #create a config file
        Path(config_file).touch(mode=0o666, exist_ok=True)
        #save default rating in yaml file
        names_yaml = """
        source_path : {}
        dest_path : {}
        input_parent_row : {}
        input_parent_man : {}
        output_parent : {}
        description_parent : {}
        input_suffix : {}
        output_suffix : {}
        """.format(self.source_path, self.dest_path, 
                        self.input_parent_row, self.input_parent_man, self.output_parent, self.description_parent,
                        self.input_suffix, self.output_suffix)
        names = yaml.safe_load(names_yaml)

        with open(config_file, 'w') as file:
            yaml.dump(names, file)

    def set_source_path(self, source_path):
        self.source_path = source_path
        self.selectFilenameFrame.update()

    def set_dest_path(self, dest_path):
        self.dest_path = dest_path
        self.resolutionMan.set_path_parent(self.get_description_parent())

    def set_filename(self, filename):
        self.filename = filename

    def set_file_suffix(self, file_suffix):
        self.file_suffix = file_suffix

    def get_source_path(self):
        return self.source_path

    def get_dest_path(self):
        return self.dest_path

    def get_filename(self):
        return self.filename

    def get_file_suffix(self):
        return self.file_suffix

    def get_filename_with_suffixname(self, suffix):
        filename = Path(self.filename)
        filename = filename.with_stem(filename.stem + suffix)
        #print(filename)
        return str(filename)

    def get_saved_source_filename(self):
        if (self.filename != None):
            source_file = Path(self.source_path).joinpath(self.input_parent, 'name').with_name(self.filename).with_suffix(self.input_suffix)
        else:
            source_file = None
        return str(source_file)

    def get_source_filename(self):
        if (self.filename != None):
            if (self.file_suffix != None):
                filename = Path(self.filename)
                filename = filename.with_stem(filename.stem + self.file_suffix)
                self.file_suffix = None
            else:
                filename = self.filename
            source_file = Path(self.source_path).joinpath('name').with_name(filename)
        else:
            source_file = None
        return str(source_file)

    def get_row_filename(self, path, filename):
        file = Path(path).joinpath(self.input_parent_row, 'name').with_name(filename)
        return str(file)

    def get_row_filename(self):
        file = Path(self.dest_path).joinpath(self.input_parent_row, 'name').with_name(self.filename)
        return str(file)

    def get_dest_filename(self):
        if (self.filename != None):
            dest_file = Path(self.dest_path).joinpath(self.output_parent, 'name').with_name(self.filename).with_suffix(self.output_suffix)
            dest_file.parent.mkdir(parents=True, exist_ok=True)
        else:
            dest_file = None
        return str(dest_file)

    def get_target_filename(self, path, filename):
        file = Path(path).joinpath(self.output_parent, 'name').with_name(filename).with_suffix(self.output_suffix)
        return str(file)

    def get_description_parent(self):
        tmp_description_parent = str(Path(self.dest_path).joinpath(self.description_parent))
        return tmp_description_parent


    def set_ResolutionManager(self, resolutionManager):
        self.resolutionMan = resolutionManager

    def set_SelectFilenameFrame(self, selectFilenameFrame):
        self.selectFilenameFrame = selectFilenameFrame
