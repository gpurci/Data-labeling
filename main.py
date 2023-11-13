#!/usr/bin/python

from tkinter import *
from tkinter import messagebox
# import filedialog module
from tkinter import filedialog
import tkinter.ttk as ttk

import time
import datetime

import numpy
import numpy as np
import string
from pathlib import Path
import os
import yaml



from frame.description import *
from frame.select_object import *
from frame.select_filename import *
from frame.path import *
from frame.edit import *
from frame.rating import *
from frame.tools import *
from frame.menu_open import *
from frame.menu_dest import *
from frame.import_frame import *
from frame.notebook import *

from manager.image_man import *
from manager.target_man.target_man import *
from manager.path_man import *
from manager.edit_man import *
from manager.tools_man import *
from manager.hyperparameters_man import *
from manager.open_man import *
from manager.notebook_man import *
from manager.import_man.yolo_v5_format import *


#from yolo_v5_format_manipulation import *

class TimeMonitor(object):
    def __init__(self):
        self.prev_t = self.time()

    def __call__(self):
        t = self.time()
        dt = t - self.prev_t
        self.prev_t = t
        return dt

    def __repr__(self):
        return "TimeMonitor()"

    def __str__(self):
        return 'Delta time {}'.format(self.dt)

    def time(self):
        return time.time()

class FrameManager(object):
    def __init__(self, window):
        
        self.frame_files = Frame(window, height=800, width=50, bd=5)
        self.frame_files.pack( side = LEFT)
        
        self.frame_tools = Frame(window)
        self.frame_tools.pack( side = TOP)
        
        self.frame_image = Frame(window)
        self.frame_image.pack( side = LEFT)
        
        self.frame_select_object = Frame(window)
        self.frame_select_object.pack( side = LEFT)
        
        self.frame_text_description = Frame(self.frame_image)
        self.frame_text_description.pack( side = BOTTOM)
        
        self.frame_edit_button = Frame(window)
        self.frame_edit_button.pack( side = LEFT)
        
        

class WorkFrameDimension(object):
    def __init__(self, config_file):
        self.config_file = config_file
        self.read_config_yaml_file(self.config_file)

    def read_config_yaml_file(self, config_file):
        if (Path(config_file).is_file() == True):
            with open(config_file) as file:
                config_list = yaml.load(file, Loader=yaml.FullLoader)
            self.__width  = config_list['width']
            self.__height = config_list['height']
            print(config_list)
        else:
            self.__width  = 1100
            self.__height = 550

    def get_size(self):
        return (self.__width, self.__height)

    def get_center(self):
        return (int(self.__width/2.), int(self.__height/2.))

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height


class Application(Frame):

    def none_fn(self):
        print('none_fn {}'.format('test'))
        pass

    def menubar_fn(self):
        self.menubar = Menu(self)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command=MenuOpenFrame(self.path_man))
        self.filemenu.add_command(label="Save", command=self.none_fn)
        self.filemenu.add_command(label="Save as...", command=self.none_fn)
        self.filemenu.add_command(label="Destination", command=MenuDestinationFrame(self.path_man))

        self.filemenu.add_separator()

        # add a submenu
        sub_menu_import = Menu(self.filemenu, tearoff=0)
        sub_menu_import.add_command(label='yolo v5 format', command=self.import_frame)
        sub_menu_import.add_command(label='...', command=self.none_fn)


        self.filemenu.add_cascade(label="Import", menu=sub_menu_import)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.editmenu = Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="Cut", command=self.none_fn)
        self.editmenu.add_command(label="Undo", command=self.none_fn)
        self.editmenu.add_command(label="Zoom", command=self.none_fn)
        self.editmenu.add_command(label="Program", command=self.none_fn)
        self.editmenu.add_command(label="Filter Aria", command=self.none_fn)
        self.editmenu.add_command(label="Plot", command=self.none_fn)

        self.editmenu.add_separator()

        self.editmenu.add_command(label="Delete", command=self.quit)

        self.menubar.add_cascade(label="Edit", menu=self.editmenu)
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Help Index", command=self.quit)
        self.helpmenu.add_command(label="About...", command=self.quit)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        root.config(menu=self.menubar)

    def set_windows(self):
        self.description_frame.set_windows(self.frame_man.frame_text_description)
        self.select_object_frame.set_windows(self.frame_man.frame_select_object)
        
        self.select_filename_frame.set_windows(self.frame_man.frame_files)
        
        self.tools_frame.set_windows(self.frame_man.frame_tools)
        
        rank_dataset_frame = Frame(self.frame_man.frame_image)
        rank_dataset_frame.pack( side = TOP )
        self.rating_frame.set_windows(rank_dataset_frame)

        notebook_frame = Frame(self.frame_man.frame_image)
        notebook_frame.pack( side = TOP )
        self.notebook_frame.set_windows(notebook_frame)

        dataset_frame = Frame(self.frame_man.frame_image)
        dataset_frame.pack( side = BOTTOM )
        self.edit_frame.set_windows(dataset_frame)
        
    def config(self):
        self.description_frame.set_dimension(self.dataset_dim)
        
        self.select_filename_frame.set_OpenFilenameMan(self.open_filename_man)
        self.select_filename_frame.set_PathManager(self.path_man)
        self.select_filename_frame.set_NotebookManager(self.notebook_man)

        
        self.open_filename_man.set_SelectFilenameFrame(self.select_filename_frame)
        self.open_filename_man.set_ImageManager(self.image_man)
        self.open_filename_man.set_PathManager(self.path_man)
        self.open_filename_man.set_EditManager(self.edit_man)
        
        self.edit_frame.set_dimension(self.dataset_dim)
        self.edit_frame.set_ImageManager(self.image_man)
        self.edit_frame.set_EditManager(self.edit_man)
        
        self.edit_man.set_EditFrame(self.edit_frame)
        self.edit_man.set_ImageManager(self.image_man)

        self.image_man.set_img_show_fn(self.edit_frame.img_show)
        self.image_man.set_rectangle_img_show_fn(self.edit_frame.rectange_img_show)
        self.image_man.set_move_fn(self.edit_frame.move)
        self.image_man.set_coords_fn(self.edit_frame.coords)
        self.image_man.set_edit_mode_fn(self.edit_frame.edit_mode)


        self.target_man.set_SelectObjectFrame(self.select_object_frame)
        self.target_man.set_DescriptionFrame(self.description_frame)
        self.target_man.set_RatingFrame(self.rating_frame)
        self.target_man.set_EditManager(self.edit_man)

        self.path_man.set_SelectFilenameFrame(self.select_filename_frame)
        self.path_man.set_ResolutionManager(self.resolution_man)
        
        self.resolution_man.set_path_parent(self.path_man.get_description_parent())

        self.tools_man.set_ImageManager(self.image_man)
        self.tools_man.set_PathManager(self.path_man)
        self.tools_man.set_EditManager(self.edit_man)

        self.notebook_frame.set_NotebookManager(self.notebook_man)
        
        self.notebook_man.set_DataDimension(self.dataset_dim)
        self.notebook_man.set_EditFrame(self.edit_frame)
        self.notebook_man.set_DescriptionFrame(self.description_frame)
        self.notebook_man.set_SelectObjectFrame(self.select_object_frame)
        self.notebook_man.set_RatingFrame(self.rating_frame)
        self.notebook_man.set_EditManager(self.edit_man)
        self.notebook_man.set_NotebookFrame(self.notebook_frame)

    def run(self):
        self.description_frame.run()
        self.select_object_frame.run()
        self.select_filename_frame.run()
        self.edit_frame.run()
        self.rating_frame.run()
        self.tools_frame.run()
        self.notebook_frame.run()

    def on_key_press(self, event):
        #print('event {}'.format(event.keysym))
        if event.state == 4 and event.keysym.lower() == "s":
            # Check if Control key (event.state == 4) and "S" key are pressed
            print("Ctrl + S pressed (Save event)")
            self.target_man.save(self.path_man.get_dest_filename())
            self.path_man.save()
            self.resolution_man.save()

        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        
        # Bind the key press event to the windows root
        master.bind("<KeyPress>", self.on_key_press)

        self.filetypes  = (("Type files", "*.png"), ("Type files", "*.jpg"), ("All files", "*.*"))
        self.path_man = PathManager(r'./config/config_path_manager.yaml')
        print(self.path_man)
        self.dataset_dim = WorkFrameDimension(r'./config/config_edit_frame_dim.yaml')
        self.image_man = ImageManager(frame = [self.dataset_dim.get_width(), self.dataset_dim.get_height()])
        self.target_man = TargetManager(1)
        self.notebook_man = NotebookManager(r'./config/config_target_manager.yaml')
        self.frame_man = FrameManager(master)
        self.resolution_man = ResolutionManager(r'./', r'config_resolution.yaml', r'./config/config_resolution.yaml')
        self.tools_man = ToolsManager(self.target_man)
        self.edit_man = EditManager(self.target_man)
        self.open_filename_man = OpenFilenameManager(self.target_man)
        
        self.description_frame = DescriptionFrame(self.target_man)
        self.select_object_frame = SelectObjectFrame(self.target_man)
        self.select_filename_frame = SelectFilenameFrame(self.target_man)
        self.edit_frame = EditFrame(self.target_man)
        self.notebook_frame = NotebookFrame()
        self.rating_frame = RatingFrame(self.target_man)
        self.tools_frame = ToolsFrame(self.tools_man)

        self.import_frame = ImportFrame(self.target_man, master, self.path_man, yolo_v5_format_import_fn)

        self.menubar_fn()
        self.set_windows()
        self.config()
        self.run()
        self.pack()

root = Tk()
root.title("Data labeling")
print("geometry {}x{}".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.geometry("{}x{}".format(root.winfo_screenwidth(), root.winfo_screenheight()))
app = Application(root)
app.mainloop()
