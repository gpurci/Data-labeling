#!/usr/bin/python

import sys

# adding Folder_2/subfolder to the system path
sys.path.insert(0, '/home/gheorghe/Desktop/Data_labeling/Data-labeling/manager')

from path_man import *

path_man = PathManager(r'../config/config_path_manager.yaml')

#print(path_man.get_input_filename('test.png'))

#print(path_man.get_source_files())


print(path_man.get_source_files())
print('test ', path_man.get_input_filename_by_target('istockphoto-1483553289-612x612.csv'))