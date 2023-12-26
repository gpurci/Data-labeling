#!/usr/bin/python

# importing sys
import sys

# adding Folder_2/subfolder to the system path
sys.path.insert(0, '/home/gheorghe/Desktop/Data_labeling/Data-labeling')
from manager.target_man import *



target_man = TargetManager(1)
target_man.read(r't_target_man_crop.csv')

print(target_man)


def crop_last_targets() :
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

    # assert factorial(0) == 1


def double_last_name() :
    """
    """
    target_man.double_last_name()
    print(target_man)

    # assert factorial(0) == 1


def crop_last_targets() :
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

    # assert factorial(0) == 1


def crop_last_targets() :
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

    # assert factorial(0) == 1

def get_all():
    retVal = target_man.get_all()
    print('dataframe:\n {}\ntype {}'.format(retVal, type(retVal)))

def concatenate():
    print('concatenate '.format(None))
    target_man.concatenate(target_man)
    print(target_man)


#crop_last_targets()
#double_last_name()
get_all()
concatenate()

