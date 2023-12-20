#!/usr/bin/python

import sys

# adding Folder_2/subfolder to the system path
sys.path.insert(0, '/home/gheorghe/Desktop/Data_labeling/Data-labeling/manager')

from path_man import *

path_man = PathManager(r'./config/config_path_manager.yaml')

print(path_man.get_input_filename('test.png'))


