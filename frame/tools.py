#!/usr/bin/python

from tkinter import *


class ToolsFrame:
    def __init__(self, toolsManager):
        self.windows = None
        self.toolsManager = toolsManager

    def set_windows(self, windows):
        self.windows = windows

    def run(self):
        tools_frame = LabelFrame(self.windows, text='Tools')
        tools_frame.pack(fill="both", expand="yes")

        crop_button = Button(tools_frame)
        crop_button["text"] = "Crop",
        crop_button["command"] = self.toolsManager.crop
        crop_button.pack({"side": "left"})

    def not_run(self):
        pass
