#!/usr/bin/python

from pathlib import Path
import yaml
from tkinter import messagebox

from manager.image_man import *
from manager.target_man import *

class RunExternScript(object) :
    def __init__(self, path_manager: object, resolution_man: object, config_file: str) :
        self.__pathMan       = path_manager
        self.__resolutionMan = resolution_man
        self.__config_file   = config_file

        self.__script_file    = None
        self.__import_file    = None

        self.__import_library = None
        self.__script_code    = None

    def __str__(self):
        return self.__script_code

    def run(self):
        print('\n\n\n\nRUN_EXTERN_SCRIPT {}'.format('run'))
        imageMan  = ImageManager(frame=self.__resolutionMan.get_size())
        targetMan = TargetManager(0)

        for file in self.__pathMan.get_input_files():
            file = str(file)
            print('file {}, type {}'.format(file, type(file)))
            row_input_file = self.__pathMan.get_input_filename(file)
            print('row_input_file {}'.format(row_input_file))
            imageMan.read_standardization(row_input_file, (0, 0, 0))

            man_target_file = self.__pathMan.get_man_target_filename(file)
            print('man_target_file {}'.format(man_target_file))
            x, y = imageMan.get_size()
            targetMan.set_size(x, y)
            targetMan.save(man_target_file)

        self.__pathMan.set_source_path(self.__pathMan.get_man_input_path())

    def test_run(self):
        g = dict()
        l = dict()
        #exec(self.__import_library, g, l)
        print(f'\n\n\nGLOBAL {g}')
        print(f'\n\n\nLOCAL {l}')
        exec(self.__script_code, g, l)
        print(f'\n\n\nGLOBAL {g}')
        print(f'\n\n\nLOCAL {l}')


    def read_script(self):
        self.__read_config_file()
        if (Path(self.__import_file).is_file() == True):
            self.__import_library = Path(self.__import_file).read_text()
        else:
            #script file does not exist
            error = r'Import file does not exist'
            messagebox.showerror("Error", f"An error occurred: {error}")
        if (Path(self.__script_file).is_file() == True):
            self.__script_code = Path(self.__script_file).read_text()
        else:
            #script file does not exist
            error = r'Script file does not exist'
            messagebox.showerror("Error", f"An error occurred: {error}")

    def __read_config_file(self):
        if (Path(self.__config_file).is_file()):
            with open(self.__config_file) as file :
                config_list = yaml.load(file, Loader=yaml.FullLoader)

            if ('script_file' in config_list) :
                self.__script_file = config_list['script_file']
            else :
                self.__script_file = './run_script/run.py'
            if ('import_file' in config_list) :
                self.__import_file = config_list['import_file']
            else :
                self.__import_file = './run_script/import_library.py'
            print(config_list)
        else :
            self.__source_path = './run_script/run.py'
            self.__import_file = './run_script/import_library.py'
            self.__save_config()

    def __save_config(self):
        # save name of script file in yaml file
        config_data = """script_file : {}
        import_file : {}
        """.format(self.__script_file, self.__import_file)
        config_data_yaml = yaml.safe_load(config_data)

        with open(self.__config_file, 'w') as file :
            yaml.dump(config_data_yaml, file)
        print('script_file {}, read {}'.format(self.__script_file, open(self.__config_file).read()))

