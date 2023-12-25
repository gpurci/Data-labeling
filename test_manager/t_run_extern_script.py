from pathlib import Path

# importing sys
import sys

# adding Folder_2/subfolder to the system path
sys.path.insert(0, '/home/gheorghe/Desktop/Data_labeling/Data-labeling')
from manager.run_extern_script import *
from manager.path_man import *
from manager.resolution_man import *


print(Path('./').cwd())


path_man  = PathManager(r'../config/config_path_manager.yaml')
resolution_man = ResolutionManager(r'../', r'config_resolution.yaml', r'../config/config_resolution.yaml')
runObj = RunExternScript(path_man, resolution_man, r'../config/config_run_script.yaml')


runObj.read_script()
runObj.exec_script()
#print(runObj)

runObj.test_file()
