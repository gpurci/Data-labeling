#!/usr/bin/python

from target_manager import *

target_man = TargetManager(r'./config/config_target_manager.yaml')
def crop_last_targets():
    """
    """
    target_man.read(r'test_crop.csv')

    print(target_man)
    target_man.set_selected_object(11)
    target_man.update_last_name()


    target_man.crop_last_targets()

    print(target_man)
    target_man.set_selected_object(9)
    target_man.update_last_name()


    target_man.crop_last_targets()
    print(target_man)

    #assert factorial(0) == 1

crop_last_targets()