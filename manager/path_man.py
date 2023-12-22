#!/usr/bin/python

from pathlib import Path
import yaml
import numpy as np
import re


class PathManager :
    def __init__(self, config_file: str) :
        self.__resolutiOnman = None
        self.__showframe     = None

        self.__output_suffix = None # target filename suffix
        self.__input_suffix  = None # input  filename suffix
        self.__description_path = None # all data description
        self.__input_path       = None
        self.__target_path      = None
        self.__man_path    = None
        self.__row_path    = None
        self.__source_path = None
        self.__dest_path   = None
        self.__config_file = config_file
        self.__read_config_yaml_file()

        self.__filename    = None


    def __str__(self) :
        strRet = """
        source_path : {}
        dest_path   : {}
        row_path    : {}
        man_path    : {}
        input_path  : {}
        target_path : {}
        description_path : {}
        input_suffix     : {}
        output_suffix    : {}
        """.format(self.__source_path,  self.__dest_path,
                   self.__row_path,     self.__man_path, 
                   self.__input_path,   self.__target_path, 
                   self.__description_path,
                   self.__input_suffix, self.__output_suffix)
        return strRet

    def __read_config_yaml_file(self) :
        if (Path(self.__config_file).is_file()):
            with open(self.__config_file) as file :
                # The FullLoader parameter handles the conversion from YAML
                # scalar values to Python the dictionary format
                config_list = yaml.load(file, Loader=yaml.FullLoader)

            if ('source_path' in config_list) :
                self.__source_path = config_list['source_path']
            else :
                self.__source_path = '/.'
            if ('dest_path' in config_list) :
                self.__dest_path = config_list['dest_path']
            else :
                self.__dest_path = '/.'
            if ('row_path' in config_list) :
                self.__row_path = config_list['row_path']
            else :
                self.__row_path = 'row'
            if ('man_path' in config_list) :
                self.__man_path = config_list['man_path']
            else :
                self.__man_path = 'man'
            if ('input_path' in config_list) :
                self.__input_path = config_list['input_path']
            else :
                self.__input_path = 'inputs'
            if ('target_path' in config_list) :
                self.__target_path = config_list['target_path']
            else :
                self.__target_path = 'targets'
            if ('description_path' in config_list) :
                self.__description_path = config_list['description_path']
            else :
                self.__description_path = 'description'
            if ('input_suffix' in config_list) :
                self.__input_suffix = config_list['input_suffix']
            else :
                self.__input_suffix = '.png'
            if ('output_suffix' in config_list) :
                self.__output_suffix = config_list['output_suffix']
            else :
                self.__output_suffix = '.csv'
            print(config_list)

        else :
            self.__source_path = '/.'
            self.__dest_path   = '/.'
            self.__row_path = 'row'
            self.__man_path = 'man'
            self.__target_path = 'targets'
            self.__input_path  = 'inputs'
            self.__description_path = 'description'
            self.__input_suffix  = '.png'
            self.__output_suffix = '.csv'
            self.__save_config(self.__config_file)

        self.set_source_path(self.__source_path)
        self.set_dest_path(self.__dest_path)

    def save(self) :
        self.__save_config(self.__config_file)

    def __save_config(self, config_file: str) :
        # create a config file
        Path(config_file).touch(mode=0o666, exist_ok=True)
        # save default rating in yaml file
        names_yaml = """
        source_path : {}
        dest_path   : {}
        row_path    : {}
        man_path    : {}
        input_path  : {}
        target_path : {}
        description_path : {}
        input_suffix     : {}
        output_suffix    : {}
        """.format(self.__source_path,  self.__dest_path,
                   self.__row_path,     self.__man_path, 
                   self.__input_path,   self.__target_path, 
                   self.__description_path,
                   self.__input_suffix, self.__output_suffix)
        names = yaml.safe_load(names_yaml)

        with open(config_file, 'w') as file :
            yaml.dump(names, file)

    def set_source_path(self, _path: str) :
        patern = r"(?P<path>.+/({}|{}))(/({}|{}))?$".format(self.__man_path, self.__row_path, self.__input_path, self.__target_path)
        print('set_source_path regex patern {}'.format(patern))

        match_patern = re.search(patern, _path)
        print('set_source_path match_patern {}'.format(match_patern))

        if (match_patern == None) :
            self.__source_path = _path
        else :
            self.__source_path = _path
            self.set_dest_path(match_patern['path'])
        print('set_source_path {}'.format(self.__source_path))

        if (self.__showframe != None):
            self.__showframe.set_show_option(self.__showframe.SHOW_FILENAMES)

    def set_dest_path(self, _path: str) :
        patern = r"(?P<path>.+/({}|{}))(/({}|{}))?$".format(self.__man_path, self.__row_path, self.__input_path, self.__target_path)
        print('set_dest_path regex patern {}'.format(patern))

        match_patern = re.search(patern, _path)
        print('set_dest_path match_patern {}'.format(match_patern))

        if (match_patern == None) :
            self.__dest_path = Path(_path).joinpath(self.__row_path)
        else :
            self.__dest_path = match_patern['path']

        self.__dest_path = str(self.__dest_path)
        print('set_dest_path {}'.format(self.__dest_path))
        
        if (self.__resolutiOnman != None):
            self.__resolutiOnman.set_path_parent(self.get_description_path())

    def set_filename(self, filename: str) :
        self.__filename = filename

    def is_file(self, filename: str):
        if (Path(self.__source_path).joinpath('name').with_name(filename).is_file() == True):
            retVal = True
        else:
            retVal = False
        return retVal

    def get_source_path(self) :
        return self.__source_path

    def get_source_files(self) :
        files = Path(self.__source_path).glob('*')
        files = list(map(lambda file: str(file.name), files))
        return np.array(files)

    def get_input_files(self) :
        files = Path(self.__dest_path).joinpath(self.__input_path).glob('*')
        files = list(map(lambda file: str(file.name), files))
        return np.array(files)

    def get_dest_path(self) :
        return self.__dest_path

    def get_input_path(self) :
        path = Path(self.__dest_path).joinpath(self.__input_path)
        path.mkdir(parents=True, exist_ok=True)
        return str(path)

    def get_target_path(self) :
        path = Path(self.__dest_path).joinpath(self.__target_path)
        path.mkdir(parents=True, exist_ok=True)
        return str(path)

    def get_man_input_path(self) :
        parent = str(Path(self.__dest_path).parent)
        path = Path(parent).joinpath(self.__man_path, self.__input_path)
        path.mkdir(parents=True, exist_ok=True)
        return str(path)

    def get_man_target_path(self) :
        parent = str(Path(self.__dest_path).parent)
        path = Path(parent).joinpath(self.__man_path, self.__target_path)
        path.mkdir(parents=True, exist_ok=True)
        return str(path)

    def get_filename(self) :
        return self.__filename

    def get_filename_with_suffixname(self, suffixname:str, filename=None) : #filename: str
        if (filename is not None):
            filename = Path(filename)
            filename = filename.with_stem(filename.stem + suffixname)
        elif (self.__filename is not None):
            filename = Path(self.__filename)
            filename = filename.with_stem(filename.stem + suffixname)
        else:
            filename = None
        # print(filename)
        return str(filename)

    def get_source_filename(self, filename=None):
        if (filename is not None):
            file = Path(self.__source_path).joinpath('name').with_name(filename)
        elif (self.__filename is not None):
            file = Path(self.__source_path).joinpath('name').with_name(self.__filename)
        else:
            file = None
        # print(filename)
        return str(file)


    def get_input_filename(self, filename=None): #filename: str
        if (filename is not None) :
            file = Path(self.get_input_path()).joinpath('name').with_name(filename)
        elif (self.__filename is not None) :
            file = Path(self.get_input_path()).joinpath('name').with_name(self.__filename)
        else :
            file = None
        return str(file)

    def get_target_filename(self, filename=None): #filename: str
        if (filename is not None):
            file = Path(self.get_target_path()).joinpath('name').with_name(filename).with_suffix(self.__output_suffix)
            Path(file).parent.mkdir(parents=True, exist_ok=True)
        elif (self.__filename is not None) :
            file = Path(self.get_target_path()).joinpath('name').with_name(self.__filename).with_suffix(self.__output_suffix)
            Path(file).parent.mkdir(parents=True, exist_ok=True)
        else :
            file = None
        return str(file)

    def get_man_input_filename(self, filename=None): #filename: str
        if (filename is not None) :
            file = Path(self.get_man_input_path()).joinpath('name').with_name(filename).with_suffix(self.__input_suffix)
        elif (self.__filename is not None) :
            file = Path(self.get_man_input_path()).joinpath('name').with_name(self.__filename).with_suffix(self.__input_suffix)
        else :
            file = None
        return str(file)

    def get_man_target_filename(self, filename=None): #filename: str
        if (filename is not None) :
            file = Path(self.get_man_target_path()).joinpath('name').with_name(filename).with_suffix(self.__output_suffix)
        elif (self.__filename is not None) :
            file = Path(self.get_man_target_path()).joinpath('name').with_name(self.__filename).with_suffix(self.__output_suffix)
        else :
            file = None
        return str(file)

    def get_object_info_file(self) :
        #print('get_object_info_file {}'.format(self))
        parent = str(Path(self.__dest_path).parent)
        #print('get_object_info_file parent {}'.format(parent))
        file = Path(parent).joinpath(self.__description_path, 'object_info.yaml')
        return str(file)

    def get_description_path(self) :
        parent = str(Path(self.__dest_path).parent)
        path = Path(parent).joinpath(self.__description_path)
        return str(path)

    def exist_filename(self, exist_filenames: 'array', filename: str):
        size_similar_item = np.argwhere(exist_filenames == filename).reshape(-1).shape[0]
        if (size_similar_item > 0):
            retVal = True
        else:
            retVal = False
        return retVal

    def filename_generator(self, exist_filenames: 'array', filename:str):
        printStr = '''START filename_generator exist_filenames {}
        filename   : {}'''.format(exist_filenames, filename)
        print(printStr)

        i = 0
        gen_name = filename
        while (True):
            if (self.exist_filename(exist_filenames, gen_name) == True):
                gen_name = self.get_filename_with_suffixname('_{}'.format(i), filename)
            else:
                break

            print('filename_generator {}'.format(gen_name))
            i += 1
        print('EXIT filename_generator {}'.format(gen_name))
        return gen_name


    def set_ResolutionManager(self, resolutionMan: object) :
        self.__resolutiOnman = resolutionMan

    def set_ShowFrame(self, showFrame: object) :
        self.__showframe = showFrame
