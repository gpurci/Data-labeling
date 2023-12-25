#!/usr/bin/python

from pathlib import Path
import yaml
from tkinter import messagebox

from manager.image_man import *
from manager.target_man import *
from manager.standardization import *

from manager.import_man.yolo_v5_format import *



class RunExternScript(object) :
    def __init__(self, path_manager: object, resolution_man: object, config_file: str) :
        self.__pathMan       = path_manager
        self.__resolutionMan = resolution_man
        self.__config_file   = config_file

        self.__script_file    = None
        self.__import_file    = None

        self.__import_library = None
        self.__script_code    = None
        self.__standardization = Standardization(path_manager, resolution_man)

        self.__imageMan  = ImageManager(frame=self.__resolutionMan.get_size())
        self.__targetMan = TargetManager(0)


    def update(self):
        self.__read_config_file()
        self.__read_script()
        self.__exec_script()
        
    def __str__(self):
        return self.__script_code

    def get_imageMan(self):
        return self.__imageMan

    def get_targetMan(self):
        return self.__targetMan

    def folder_detector(self):
        print('FOLDER DETECTOR {}'.format(None))
        for file in self.__pathMan.get_input_files():
            self.file_detector(str(file))

    def source_detector(self):
        self.update()
        print('SOURCE DETECTOR {}'.format(None))
        for file in self.__pathMan.get_source_files():
            self.source_file_detector(str(file))

    def source_file_detector(self, filename: str):
        print('SOURCE FILE DETECTOR {}'.format(filename))

        source_file = self.__pathMan.get_source_filename(filename)
        print('source_file {}'.format(source_file))
        self.__imageMan.read_standardization(source_file, (0, 0, 0))

        man_image = self.__imageMan.get_man_data()

        self.__local['run_detector'](self.__local['detector'], man_image, self.__targetMan, 0.1, None, self.__local)

        row_input_file = self.__pathMan.get_input_filename(filename)
        self.__imageMan.save(row_input_file)
        x, y = self.__imageMan.get_size()
        self.__targetMan.set_size(x, y)
        self.__targetMan.resize_coord(self.__imageMan.calc_coord_to_target)

        row_target_file = self.__pathMan.get_target_filename(filename)
        print('row_target_file {}'.format(row_target_file))

        self.__targetMan.save(row_target_file)

    def file_detector(self, filename: str):
        print('FILE DETECTOR {}'.format(filename))
        self.__standardization.export_image(filename, self.__imageMan)
        man_image = self.__imageMan.get_man_data()

        self.__local['run_detector'](self.__local['detector'], man_image, self.__targetMan, 0.1, None, self.__local)

        man_input_file = self.__pathMan.get_man_input_filename(filename)
        self.__imageMan.save(man_input_file)
        x, y = self.__imageMan.get_size()
        self.__targetMan.set_size(x, y)
        self.__targetMan.resize_coord(self.__imageMan.calc_coord_to_target)

        man_target_file = self.__pathMan.get_man_target_filename(filename)
        print('man_target_file {}'.format(man_target_file))

        self.__targetMan.save(man_target_file)

    def image_detector(self, imageMan: object):
        print('IMAGE DETECTOR {}'.format('Start'))
        self.__imageMan = imageMan
        self.__standardization.export_image(filename, self.__imageMan)
        man_image = self.__imageMan.get_man_data()

        self.__local['run_detector'](self.__local['detector'], man_image, self.__targetMan, 0.1, None, self.__local)

        x, y = self.__imageMan.get_size()
        self.__targetMan.set_size(x, y)
        self.__targetMan.resize_coord(self.__imageMan.calc_coord_to_target)
        print('IMAGE DETECTOR {}'.format('End'))


    def __exec_script(self):
        self.__global = dict()
        self.__local  = dict()
        exec(self.__import_library, self.__global, self.__local)
        exec(self.__script_code,    self.__global, self.__local)
        #print(f'\n\n\nGLOBAL {self.__global}')
        #print(f'\n\n\nLOCAL {self.__local}')



    def __read_script(self):
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
                if (Path(self.__script_file).is_file() != True):
                    self.__script_file = './run_script/run.py'
            else :
                self.__script_file = './run_script/run.py'
            if ('import_file' in config_list) :
                self.__import_file = config_list['import_file']
                if (Path(self.__import_file).is_file() != True):

                    self.__import_file = './run_script/import_library.py'
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
