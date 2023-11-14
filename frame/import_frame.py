#!/usr/bin/python

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import yaml

from pathlib import Path
import shutil

from manager.target_man.target_man import *
from manager.import_man.yolo_v5_format import *

class ImportFrame(object):
    def __init__(self, windows, pathManager, config_file):
        self.config_file = config_file
        self.is_save = False
        
        self.pathManager = pathManager
        self.set_windows(windows)
        
        self.source_path = self.pathManager.get_source_path()
        self.dest_path     = self.pathManager.get_dest_path()

    def set_windows(self, windows):
        self.windows = windows

    def __call__(self):
        self.filewin = Toplevel(self.windows)
        self.src_frame = Frame(self.filewin)
        self.src_frame.pack( side = TOP )
        self.dest_frame = Frame(self.filewin)
        self.dest_frame.pack( side = TOP )
        self.button_frame = Frame(self.filewin)
        self.button_frame.pack( side = TOP )
        
        self.source_path_UI(self.src_frame)
        self.destination_path_UI(self.dest_frame)
        self.import_button(self.button_frame)

    def read_config_yaml_file(self):
        if (Path(self.config_file).is_file() == True):
            with open(self.config_file) as file:
                config_list = yaml.load(file, Loader=yaml.FullLoader)
            self.set_default_rating(config_list['default_rating'])
            print(config_list)
        else:
            self.set_default_rating(0)

    def set_default_rating(self, rating:int):
        self.__default_rating = rating

    def open_dir_src(self):
        source_path = filedialog.askdirectory(
                                                                        initialdir=self.source_path,      # Start in the root directory
                                                                        title="Select a Directory",  # Custom title for the dialog
                                                                        mustexist=True,                # Ensure that the selected directory exists
                                                                    )
        self.set_source_path_frame(source_path)

    def set_source_path_frame(self, source_path):
        self.source_path = source_path
        self.src_path_entry.delete(0, END)
        self.src_path_entry.insert(0, source_path)

    def open_dir_dest(self):
        dest_path = filedialog.askdirectory(
                                                                        initialdir=self.dest_path,      # Start in the root directory
                                                                        title="Select a Directory",  # Custom title for the dialog
                                                                        mustexist=True,                # Ensure that the selected directory exists
                                                                    )
        row_path    = str(Path(self.pathManager.get_row_filename(dest_path, 'new.png')).parent)
        self.pathManager.set_source_path(row_path)
        self.pathManager.set_dest_path(dest_path)
        self.set_dest_path_frame(dest_path)

    def set_dest_path_frame(self, dest_path):
        self.dest_path = dest_path
        self.dest_path_entry.delete(0, END)
        self.dest_path_entry.insert(0, dest_path)

    def import_fn(self):
        self.filewin.withdraw()
        source_path = self.source_path
        dest_path     = self.dest_path
        self.read_config_yaml_file()
        datasets = TargetManager(0)
        datasets.set_default_rating(self.__default_rating)
        yolo_v5_format_import_fn(source_path, dest_path, datasets, self.pathManager)


    def source_path_UI(self, window):
        src_path_label = Label(window, text="Source path", width=10)
        src_path_label.pack( side = LEFT)

        self.src_path_entry = Entry(window, width=100, bd = 1)
        self.src_path_entry.insert (0, self.pathManager.get_source_path())
        self.src_path_entry.pack({"side": "left"})

        change_src_path_button = Button(window)
        change_src_path_button["text"] = "Open",
        change_src_path_button["command"] = self.open_dir_src
        change_src_path_button.pack({"side": "left"})

    def destination_path_UI(self, window):
        dest_path_label = Label(window, text="Dest path", width=10)
        dest_path_label.pack( side = LEFT)

        self.dest_path_entry = Entry(window, width=100, bd = 1)
        self.dest_path_entry.insert (0, self.pathManager.get_dest_path())
        self.dest_path_entry.pack({"side": "left"})

        change_dest_path_button = Button(window)
        change_dest_path_button["text"] = "Open",
        change_dest_path_button["command"] = self.open_dir_dest
        change_dest_path_button.pack({"side": "left"})

    def import_button(self, window):
        change_dest_path_button = Button(window)
        change_dest_path_button["text"] = "Import",
        change_dest_path_button["command"] = self.import_fn
        change_dest_path_button.pack({"side": "top"})
