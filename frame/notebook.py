#!/usr/bin/python

from tkinter import *
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Notebook, Style


class NotebookFrame(object) :
    def __init__(self) :
        self.__notebookMan = None
        self.__note        = None
        self.__window      = None

    def set_windows(self, window: object) :
        self.__window = window

    def __change_tab(self, *args) :
        select_tab_val = self.__note.select()
        if (len(select_tab_val) != 0):
            print('__change_tab  {}'.format(select_tab_val))
            index = self.__note.index(select_tab_val)
            print('__change_tab index {}'.format(index))
            self.__notebookMan.select_tab(index)

    def select_tab(self, index: int):
        self.__note.select(index)


    def run(self) :
        # Create an instance of ttk style
        # style = Style()
        # style.theme_use('default')
        # style.configure('TNotebook.Tab', background="Red")
        # style.map("TNotebook", background= [("selected", "red")])

        # Create a Notebook widget
        self.__note = CustomNotebook(self.__window)
        self.__note.bind('<<NotebookTabChanged>>', self.__change_tab)
        self.__note.pack(expand=True, fill=BOTH, padx=5, pady=5)
        self.__note.set_NotebookManager(self.__notebookMan)

    def add(self, filename: str) :
        # Adding the Tab Name
        self.__note.add(Frame(self.__note, width=400, height=5), text=filename)

    def set_NotebookManager(self, notebookMan: object) :
        self.__notebookMan = notebookMan


class CustomNotebook(ttk.Notebook) :
    """A ttk Notebook with close buttons on each tab"""

    __initialized = False

    def __init__(self, *args, **kwargs) :
        self.__notebookMan = None
        if (self.__initialized == False):
            self.__initialize_custom_style()
            self.__inititialized = True

        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)

        self._active = None

        self.bind("<ButtonPress-1>", self.__on_press, True)
        self.bind("<ButtonRelease-1>", self.__on_release)

    def __on_press(self, event: object) :
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)

        if ("close" in element) :
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index
            return "break"

    def __on_release(self, event: object) :
        """Called when the button is released"""
        if (self.instate(['pressed']) == False):
            return

        element = self.identify(event.x, event.y)
        if ("close" not in element):
            # user moved the mouse off of the close button
            return

        index = self.index("@%d,%d" % (event.x, event.y))

        if self._active == index :
            self.forget(index)
            self.__notebookMan.delete_tab(index)
            self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None

    def __initialize_custom_style(self) :
        style = ttk.Style()
        self.images = (
            tk.PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
            tk.PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            tk.PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                ''')
        )

        style.element_create("close", "image", "img_close",
                             ("active", "pressed", "!disabled", "img_closepressed"),
                             ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky" : "nswe"})])
        style.layout("CustomNotebook.Tab", [
            ("CustomNotebook.tab", {
                "sticky" : "nswe",
                "children" : [
                    ("CustomNotebook.padding", {
                        "side" : "top",
                        "sticky" : "nswe",
                        "children" : [
                            ("CustomNotebook.focus", {
                                "side" : "top",
                                "sticky" : "nswe",
                                "children" : [
                                    ("CustomNotebook.label", {"side" : "left", "sticky" : ''}),
                                    ("CustomNotebook.close", {"side" : "left", "sticky" : ''}),
                                ]
                            })
                        ]
                    })
                ]
            })
        ])

    def set_NotebookManager(self, notebookMan) :
        self.__notebookMan = notebookMan
