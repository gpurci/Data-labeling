#!/usr/bin/python

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import yaml

from pathlib import Path
import shutil


class ImportFrame(object):
    def __init__(self, datasets, windows, pathManager, import_extern_fn):
        self.datasets = datasets
        self.is_save = False
        
        self.pathManager = pathManager
        self.set_windows(windows)
        
        self.import_extern_fn = import_extern_fn
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
        self.import_extern_fn(source_path, dest_path, self.datasets, self.pathManager)


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
