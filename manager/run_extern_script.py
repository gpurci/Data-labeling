#!/usr/bin/python

from pathlib import Path
import yaml
from tkinter import messagebox
import os


class RunExternScript(object) :
    def __init__(self, config_file: str, def_import_filename:str, def_script_filename:str) :
        self.__config_file   = config_file
        self.__def_import_filename = def_import_filename
        self.__def_script_filename = def_script_filename

        self.__prev_mod_time_import = 0
        self.__prev_mod_time_script = 0

        self.__import_filename = None
        self.__script_filename = None

        self.__import_library  = None
        self.__script_code     = None

        self.__global = None
        self.__local  = None

    def __is_modified(self):
        if ((self.__script_filename == None) or (self.__import_filename == None)):
            bVal = True
        else:
            ti_mod_import = os.path.getmtime(self.__import_filename)
            ti_mod_script = os.path.getmtime(self.__script_filename)
            bVal = ((self.__prev_mod_time_import != ti_mod_import) or (self.__prev_mod_time_script != ti_mod_script))
        return bVal

    def update(self):
        if (self.__is_modified() == True):
            self.__read_config_filename()
            self.__read_script()
            self.__exec_script()
            self.__prev_mod_time_import = os.path.getmtime(self.__import_filename)
            self.__prev_mod_time_script = os.path.getmtime(self.__script_filename)
        
    def __str__(self):
        return self.__script_code

    def set_import_filename(self, filename: str):
        self.__import_filename = filename
        self.__prev_mod_time_import = 0

    def set_script_filename(self, filename: str):
        self.__script_filename = filename
        self.__prev_mod_time_script = 0

    def get_globals(self):
        return self.__global

    def get_locals(self):
        return self.__local

    def __read_config_filename(self):
        def check_filename(config_list, key, default_filename):
            if (key in config_list) :
                retFilename = config_list[key]
            else :
                retFilename = default_filename

            if (Path(retFilename).is_file() == False):
                retFilename = Path(retFilename)
                retFilename.parent.mkdir(mode=0o777, parents=True, exist_ok=True)
                retFilename.touch(mode=0o666, exist_ok=True)
            return str(retFilename)

        if (Path(self.__config_file).is_file()):
            with open(self.__config_file) as file :
                config_list = yaml.load(file, Loader=yaml.FullLoader)
        else :
            config_list = {'RunExternScript config_not_exist': self.__config_file}
        print(config_list)
        self.__script_filename = check_filename(config_list, 'script_filename', self.__def_script_filename)
        self.__import_filename = check_filename(config_list, 'import_filename', self.__def_import_filename)
        self.__save_config()

    def __read_script(self):
        if (Path(self.__import_filename).is_file() == True):
            self.__import_library = Path(self.__import_filename).read_text()
        else:
            # import filename does not exist
            error = 'Import file @{}@ does not exist!'.format(self.__import_filename)
            messagebox.showerror("Error", f"An error occurred: {error}")
        if (Path(self.__script_filename).is_file() == True):
            self.__script_code = Path(self.__script_filename).read_text()
        else:
            # script filename does not exist
            error = 'Script file @{}@ does not exist!'.format(self.__script_filename)
            messagebox.showerror("Error", f"An error occurred: {error}")

    def __exec_script(self):
        if (self.__global != None):
            del self.__global
        if (self.__local != None):
            del self.__local

        self.__global = dict()
        self.__local  = dict()
        exec(self.__import_library, self.__global, self.__local)
        exec(self.__script_code,    self.__global, self.__local)
        #print(f'\n\n\nGLOBAL {self.__global}')
        #print(f'\n\n\nLOCAL {self.__local}')

    def __save_config(self):
        # save name of script file in yaml file
        config_data = """script_filename: {}
import_filename: {}
        """.format(self.__script_filename, self.__import_filename)
        print(config_data)
        config_data_yaml = yaml.safe_load(config_data)

        with open(self.__config_file, 'w') as file :
            yaml.dump(config_data_yaml, file)
        print('read {}'.format(open(self.__config_file).read()))
