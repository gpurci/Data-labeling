from pathlib import Path

# importing sys
import sys

# adding Folder_2/subfolder to the system path
sys.path.insert(0, '/home/gheorghe/Desktop/Data_labeling/Data-labeling')
from manager.run_extern_script import *


print(Path('./').cwd())


runObj = RunExternScript(None, None, r'../config/config_run_script.yaml')


runObj.read_script()
#print(runObj)

runObj.test_run()
