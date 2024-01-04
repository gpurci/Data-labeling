#!/usr/bin/python

from pathlib import Path
import yaml
import numpy as np
import re


class PathManager :
    def __init__(self, config_file: str) :
        self.__resolutionMan = None
        self.__filenameFrame = None

        self.__output_suffix = None # target filename suffix
        self.__input_suffix  = None # input  filename suffix
        self.__description_path = None # all data description
        self.__input_path       = None
        self.__target_path      = None
        self.__man_path    = None
        self.__row_path    = None
        self.__source_path = None
        self.__dest_path   = None
        self.__user_name   = None
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
        user             : {}
        """.format(self.__source_path,  self.__dest_path,
                   self.__row_path,     self.__man_path, 
                   self.__input_path,   self.__target_path, 
                   self.__description_path,
                   self.__input_suffix, self.__output_suffix,
                   self.__user_name)
        return strRet

    def __read_config_yaml_file(self) :
        def check_key(config_list, key, default):
            if (key in config_list) :
                retVal = config_list[key]
            else :
                retVal = default
            return retVal

        if (Path(self.__config_file).is_file()):
            with open(self.__config_file) as file :
                # The FullLoader parameter handles the conversion from YAML
                # scalar values to Python the dictionary format
                config_list = yaml.load(file, Loader=yaml.FullLoader)

            print(config_list)

        else :
            config_list = {'NotConfigFile':0}

        self.__source_path = check_key(config_list, 'source_path', '/.')
        self.__dest_path   = check_key(config_list, 'dest_path',   '/.')
        self.__row_path    = check_key(config_list, 'row_path',    'row')
        self.__man_path    = check_key(config_list, 'man_path',    'man')
        self.__input_path  = check_key(config_list, 'input_path',  'inputs')
        self.__target_path = check_key(config_list, 'target_path', 'targets')
        self.__user_name   = check_key(config_list, 'user',        'user')
        self.__description_path = check_key(config_list, 'description_path', 'description')
        self.__input_suffix     = check_key(config_list, 'input_suffix',     '.png')
        self.__output_suffix    = check_key(config_list, 'output_suffix',    '.csv')

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
        user             : {}
        """.format(self.__source_path,  self.__dest_path,
                   self.__row_path,     self.__man_path, 
                   self.__input_path,   self.__target_path, 
                   self.__description_path,
                   self.__input_suffix, self.__output_suffix,
                   self.__user_name)
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

        if (self.__filenameFrame != None):
            self.__filenameFrame.set_filenames(self.get_source_files())

    def set_dest_path(self, _path: str) :
        patern = r"(?P<path>.+/({}|{}))(/({}|{})(?P<user>(/(\w+)))?)?$".format(self.__man_path, self.__row_path, self.__input_path, self.__target_path)
        print('set_dest_path regex patern {}'.format(patern))

        match_patern = re.search(patern, _path)
        print('set_dest_path match_patern {}'.format(match_patern))

        if (match_patern == None) :
            self.__dest_path = Path(_path).joinpath(self.__row_path)
        else :
            self.__dest_path = match_patern['path']
            if (match_patern['user']):
                print('user ', match_patern['user'])
                self.set_user_name(match_patern['user'][1:])

        self.__dest_path = str(self.__dest_path)
        self.__makedir()


        print('set_dest_path {}'.format(self.__dest_path))
        
        if (self.__resolutionMan != None):
            self.__resolutionMan.set_path_parent(self.get_description_path())

    def set_user_name(self, user: str) :
        self.__user_name = user
        self.__makedir()

    def set_filename(self, filename: str) :
        self.__filename = filename

    def is_file(self, filename: str):
        if (Path(self.__source_path).joinpath('name').with_name(filename).is_file() == True):
            retVal = True
        else:
            retVal = False
        return retVal

    def get_user_name(self) :
        return self.__user_name

    def get_source_path(self) :
        return self.__source_path

    def get_source_files(self) :
        files = Path(self.__source_path).glob('*')
        new_files = []
        for file in files:
            if (file.is_file()):
                new_files.append(str(file.name))
        return np.array(new_files)

    def get_input_files(self) :
        files = Path(self.__dest_path).joinpath(self.__input_path).glob('*')
        files = list(map(lambda file: str(file.name), files))
        return np.array(files)

    def get_target_filenames(self) :
        files = Path(self.get_target_path()).glob('*')
        files = list(map(lambda file: str(file.name), files))
        return np.array(files)

    def get_dest_path(self) :
        return self.__dest_path

    def get_input_path(self) :
        path = Path(self.__dest_path).joinpath(self.__input_path)
        return str(path)

    def get_target_path(self) :
        path = Path(self.__dest_path).joinpath(self.__target_path, self.__user_name)
        return str(path)

    def get_man_input_path(self) :
        parent = str(Path(self.__dest_path).parent)
        path = Path(parent).joinpath(self.__man_path, self.__input_path)
        return str(path)

    def get_man_target_path(self) :
        parent = str(Path(self.__dest_path).parent)
        path = Path(parent).joinpath(self.__man_path, self.__target_path, self.__user_name)
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
        elif (self.__filename is not None) :
            file = Path(self.get_target_path()).joinpath('name').with_name(self.__filename).with_suffix(self.__output_suffix)
        else :
            file = None
        return str(file)

    def get_input_filename_by_target(self, filename=None): #filename: str
        if (filename is not None):
            match = str(Path(filename).stem) + '*'
            file = list(Path(self.get_input_path()).glob(match))
            if (len(file) != 0):
                file = str(file[0].name)
            else:
                file = None
        else :
            file = None
        return file

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

    def get_user_info_file(self) :
        #print('get_object_info_file {}'.format(self))
        parent = str(Path(self.__dest_path).parent)
        #print('get_object_info_file parent {}'.format(parent))
        file = Path(parent).joinpath(self.__description_path, 'user_info.yaml')
        return str(file)

    def get_description_path(self) :
        parent = str(Path(self.__dest_path).parent)
        path = Path(parent).joinpath(self.__description_path)
        return str(path)

    def __makedir(self):
        Path(self.get_input_path()).mkdir(parents=True, exist_ok=True)
        Path(self.get_target_path()).mkdir(parents=True, exist_ok=True)
        Path(self.get_man_input_path()).mkdir(parents=True, exist_ok=True)
        Path(self.get_man_target_path()).mkdir(parents=True, exist_ok=True)

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
        self.__resolutionMan = resolutionMan

    def set_FilenameFrame(self, obj: object) :
        self.__filenameFrame = obj
