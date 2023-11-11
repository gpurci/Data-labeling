#!/usr/bin/python

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

from pathlib import Path

class PathFrame(object):
    def __init__(self, path_manager):
        self.pathManager = path_manager

    def set_windows(self, src_frame, dest_frame):
        self.src_frame   = src_frame
        self.dest_frame = dest_frame

    def open_dir_src(self):
        source_path = filedialog.askdirectory(
                                                                        initialdir=self.pathManager.get_source_path(),      # Start in the root directory
                                                                        title="Select a Directory",  # Custom title for the dialog
                                                                        mustexist=True,                # Ensure that the selected directory exists
                                                                    )
        self.pathManager.set_source_path(source_path)

    def set_source_path_frame(self, source_path):
        self.src_path_entry.delete(0, END)
        self.src_path_entry.insert(0, source_path)

    def open_dir_dest(self):
        dest_path = filedialog.askdirectory(
                                                                        initialdir=self.pathManager.get_dest_path(),      # Start in the root directory
                                                                        title="Select a Directory",  # Custom title for the dialog
                                                                        mustexist=True,                # Ensure that the selected directory exists
                                                                    )
        self.pathManager.set_dest_path(dest_path)

    def set_dest_path_frame(self, dest_path):
        self.dest_path_entry.delete(0, END)
        self.dest_path_entry.insert(0, dest_path)

    def run(self):
        self.source_path_UI(self.src_frame)
        self.destination_path_UI(self.dest_frame)

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

