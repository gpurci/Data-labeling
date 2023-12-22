#!/usr/bin/python

from tkinter import *
from tkinter import filedialog

from manager.import_man.yolo_v5_format import *


class ImportFrame :
    def __init__(self, windows, pathManager, config_file) :
        self.__default_rating = None
        self.__import_fn = None
        self.__windows = None
        self.__config_file = config_file

        self.__pathMan = pathManager
        self.set_windows(windows)

        self.__source_path = self.__pathMan.get_source_path()
        self.__dest_path = self.__pathMan.get_dest_path()

    def set_windows(self, windows: object) :
        self.__windows = windows

    def set_import_fn(self, fn: 'import_function') :
        self.__import_fn = fn

    def __call__(self) :
        self.__import_frame = Toplevel(self.__windows)
        source_frame = Frame(self.__import_frame)
        source_frame.pack(side=TOP)
        dest_frame = Frame(self.__import_frame)
        dest_frame.pack(side=TOP)
        import_button_frame = Frame(self.__import_frame)
        import_button_frame.pack(side=TOP)

        self.__source_path_UI(source_frame)
        self.__destination_path_UI(dest_frame)
        self.__import_button(import_button_frame)

    def __read_config_yaml_file(self) :
        if Path(self.__config_file).is_file() :
            with open(self.__config_file) as file :
                config_list = yaml.load(file, Loader=yaml.FullLoader)
            self.set_default_rating(config_list['default_rating'])
            print(config_list)
        else :
            self.set_default_rating(0)

    def set_default_rating(self, rating: int) :
        self.__default_rating = rating

    def __open_dir_source(self) :
        source_path = filedialog.askdirectory(
            initialdir=self.__source_path,  # Start in the root directory
            title="Select a Directory",  # Custom title for the dialog
            mustexist=True,  # Ensure that the selected directory exists
        )
        self.__set_source_path_frame(source_path)

    def __set_source_path_frame(self, source_path: str) :
        self.__src_path_entry.delete(0, END)
        self.__src_path_entry.insert(0, source_path)

    def __open_dir_dest(self) :
        dest_path = filedialog.askdirectory(
            initialdir=self.__dest_path,  # Start in the root directory
            title="Select a Directory",  # Custom title for the dialog
            mustexist=True,  # Ensure that the selected directory exists
        )
        self.__set_dest_path_frame(dest_path)

    def __set_dest_path_frame(self, dest_path: str) :
        self.__dest_path_entry.delete(0, END)
        self.__dest_path_entry.insert(0, dest_path)

    def __do_import(self) :
        self.__import_frame.withdraw()
        self.__read_config_yaml_file()
        self.__source_path = str(self.__src_path_entry.get())
        self.__dest_path = str(self.__dest_path_entry.get())
        self.__pathMan.set_dest_path(self.__dest_path)
        self.__pathMan.set_source_path(self.__pathMan.get_input_path())

        datasets = TargetManager(self.__default_rating)
        self.__import_fn(self.__source_path, self.__dest_path, datasets, self.__pathMan)

    def __source_path_UI(self, window: object) :
        src_path_label = Label(window, text="Source path", width=10)
        src_path_label.pack(side=LEFT)

        self.__src_path_entry = Entry(window, width=100, bd=1)
        self.__src_path_entry.insert(0, self.__pathMan.get_source_path())
        self.__src_path_entry.pack({"side" : "left"})

        change_src_path_button = Button(window)
        change_src_path_button["text"] = "Open",
        change_src_path_button["command"] = self.__open_dir_source
        change_src_path_button.pack({"side" : "left"})

    def __destination_path_UI(self, window: object) :
        dest_path_label = Label(window, text="Dest path", width=10)
        dest_path_label.pack(side=LEFT)

        self.__dest_path_entry = Entry(window, width=100, bd=1)
        self.__dest_path_entry.insert(0, self.__pathMan.get_dest_path())
        self.__dest_path_entry.pack({"side" : "left"})

        change_dest_path_button = Button(window)
        change_dest_path_button["text"] = "Open",
        change_dest_path_button["command"] = self.__open_dir_dest
        change_dest_path_button.pack({"side" : "left"})

    def __import_button(self, window: object) :
        change_dest_path_button = Button(window)
        change_dest_path_button["text"] = "Import",
        change_dest_path_button["command"] = self.__do_import
        change_dest_path_button.pack({"side" : "top"})
