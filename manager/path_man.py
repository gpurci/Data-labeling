#!/usr/bin/python

from pathlib import Path
import yaml


class PathManager :
    def __init__(self, config_file) :
        self.output_suffix = None
        self.input_suffix  = None
        self.description_parent = None
        self.output_parent    = None
        self.input_parent_man = None
        self.input_parent_row = None
        self.source_path   = None
        self.dest_path     = None
        self.config_file   = config_file
        self.read_config_yaml_file(self.config_file)
        self.filename    = None
        self.file_suffix = None

        self.resolutionMan = None
        self.showFrame = None

    def __str__(self) :
        strRet = """
        source_path : {}
        dest_path   : {}
        input_parent_row : {}
        input_parent_man : {}
        output_parent    : {}
        description_parent : {}
        input_suffix     : {}
        output_suffix    : {}
        """.format(self.source_path, self.dest_path,
                   self.input_parent_row, self.input_parent_man, self.output_parent, self.description_parent,
                   self.input_suffix, self.output_suffix)
        return strRet

    def read_config_yaml_file(self, config_file: str) :
        if (Path(config_file).is_file()) :
            with open(config_file) as file :
                # The FullLoader parameter handles the conversion from YAML
                # scalar values to Python the dictionary format
                config_list = yaml.load(file, Loader=yaml.FullLoader)

            if ('source_path' in config_list) :
                self.source_path = config_list['source_path']
            else :
                self.source_path = '/.'
            if ('dest_path' in config_list) :
                self.dest_path = config_list['dest_path']
            else :
                self.dest_path = '/.'
            if ('input_parent_row' in config_list) :
                self.input_parent_row = config_list['input_parent_row']
            else :
                self.input_parent_row = 'row'
            if ('input_parent_man' in config_list) :
                self.input_parent_man = config_list['input_parent_man']
            else :
                self.input_parent_man = 'man'
            if ('output_parent' in config_list) :
                self.output_parent = config_list['output_parent']
            else :
                self.output_parent = 'targets'
            if ('description_parent' in config_list) :
                self.description_parent = config_list['description_parent']
            else :
                self.description_parent = 'description'
            if ('input_suffix' in config_list) :
                self.input_suffix = config_list['input_suffix']
            else :
                self.input_suffix = '.png'
            if ('output_suffix' in config_list) :
                self.output_suffix = config_list['output_suffix']
            else :
                self.output_suffix = '.csv'
            print(config_list)
        else :
            self.source_path = '/.'
            self.dest_path   = '/.'
            self.input_parent_row = 'row'
            self.input_parent_man = 'man'
            self.output_parent      = 'targets'
            self.description_parent = 'description'
            self.input_suffix  = '.png'
            self.output_suffix = '.csv'
            self.save_config(config_file)

    def save(self) :
        self.save_config(self.config_file)

    def save_config(self, config_file: str) :
        # create a config file
        Path(config_file).touch(mode=0o666, exist_ok=True)
        # save default rating in yaml file
        names_yaml = """
        source_path : {}
        dest_path   : {}
        input_parent_row : {}
        input_parent_man : {}
        output_parent      : {}
        description_parent : {}
        input_suffix  : {}
        output_suffix : {}
        """.format(self.source_path, self.dest_path,
                   self.input_parent_row, self.input_parent_man, self.output_parent, self.description_parent,
                   self.input_suffix, self.output_suffix)
        names = yaml.safe_load(names_yaml)

        with open(config_file, 'w') as file :
            yaml.dump(names, file)

    def set_source_path(self, source_path: str) :
        self.source_path = source_path
        self.showFrame.set_show_option(self.showFrame.SHOW_FILENAMES)

    def set_dest_path(self, dest_path: str) :
        tmp_path = Path(dest_path)
        if tmp_path.parents[0] != self.output_parent :
            self.dest_path = dest_path
        else :
            self.dest_path = str(tmp_path.root)
        print('set_dest_path {}'.format(self.dest_path))
        self.resolutionMan.set_path_parent(self.get_description_parent())

    def set_filename(self, filename: str) :
        self.filename = filename

    def is_file(self, filename: str) :
        if (Path(self.source_path).joinpath('name').with_name(filename).is_file() == True):
            self.filename = filename
            retVal = True
        else:
            retVal = False
        return retVal

    def set_file_suffix(self, file_suffix: str) :
        self.file_suffix = file_suffix

    def get_source_path(self) :
        return self.source_path

    def get_source_files(self) :
        files = Path(self.source_path).glob('*')
        files = list(map(lambda file: str(file.name), files))
        return files

    def get_dest_path(self) :
        return self.dest_path

    def get_row_path(self) :
        return str(Path(self.dest_path).joinpath(self.input_parent_row))

    def get_target_path(self) :
        return str(Path(self.dest_path).joinpath(self.output_parent))

    def get_filename(self) :
        return self.filename

    def get_file_suffix(self) :
        return self.file_suffix

    def get_filename_with_suffixname(self, suffix:str, filename=None) : #filename: str
        if (filename is not None):
            filename = Path(filename)
            filename = filename.with_stem(filename.stem + suffix)
        elif (self.filename is not None):
            filename = Path(self.filename)
            filename = filename.with_stem(filename.stem + suffix)
        else:
            filename = 'NONE'
        # print(filename)
        return str(filename)

    def get_saved_source_filename(self) :
        if (self.filename is not None):
            source_file = Path(self.source_path).joinpath(self.input_parent, 'name').with_name(
                self.filename).with_suffix(self.input_suffix)
        else :
            source_file = None
        return str(source_file)

    def get_source_filename(self) :
        if (self.filename is not None) :
            if (self.file_suffix is not None) :
                filename = Path(self.filename)
                filename = filename.with_stem(filename.stem + self.file_suffix)
                self.file_suffix = None
            else :
                filename = self.filename
            source_file = Path(self.source_path).joinpath('name').with_name(filename)
        else :
            source_file = None
        return str(source_file)

    def get_row_filename(self, filename=None): #filename: str
        if (filename is not None) :
            file = Path(self.dest_path).joinpath(self.input_parent_row, 'name').with_name(filename)
        elif (self.filename is not None) :
            file = Path(self.dest_path).joinpath(self.input_parent_row, 'name').with_name(self.filename)
        else :
            file = None
        return str(file)

    def get_target_filename(self, filename=None): #filename: str
        if (filename is not None) :
            file = Path(self.dest_path).joinpath(self.output_parent, 'name').with_name(filename).with_suffix(self.output_suffix)
            Path(file).parent.mkdir(parents=True, exist_ok=True)
        elif (self.filename is not None) :
            file = Path(self.dest_path).joinpath(self.output_parent, 'name').with_name(self.filename).with_suffix(self.output_suffix)
            Path(file).parent.mkdir(parents=True, exist_ok=True)
        else :
            file = None
        return str(file)

    def get_dest_filename(self) :
        if (self.filename is not None) :
            file = Path(self.dest_path).joinpath(self.output_parent, 'name').with_name(self.filename).with_suffix(self.output_suffix)
            Path(file).parent.mkdir(parents=True, exist_ok=True)
        else :
            file = None
        return str(file)

    def get_description_parent(self) :
        tmp_description_parent = str(Path(self.dest_path).joinpath(self.description_parent))
        return tmp_description_parent

    def get_idx_list(self, exist_filenames: list, filename: str) :
        try:
            idx = exist_filenames.index(filename)
        except:
            idx = -1
            pass
        return idx

    def exist_filename(self, exist_filenames: list, filename:str):
        if ((self.get_idx_list(exist_filenames, filename) != -1) or 
            (self.is_file(filename) == True)):
            retVal = True
        else:
            retVal = False
        return retVal

    def filename_generator(self, exist_filenames: list, filename:str):
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
        self.resolutionMan = resolutionMan

    def set_ShowFrame(self, showFrame: object) :
        self.showFrame = showFrame
