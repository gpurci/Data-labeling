#!/usr/bin/python

from tkinter import filedialog

class MenuDestinationFrame(object):
    def __init__(self, pathManager):
        self.pathManager = pathManager

    def __call__(self):
        path = filedialog.askdirectory(
                                                        initialdir=self.pathManager.get_dest_path(),      # Start in the root directory
                                                        title="Select a Directory",  # Custom title for the dialog
                                                        mustexist=True,                # Ensure that the selected directory exists
                                                    )
        self.pathManager.set_dest_path(path)