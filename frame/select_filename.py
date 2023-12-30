#!/usr/bin/python

from tkinter import *
from tkinter import messagebox

from pathlib import Path


class SelectFilenameFrame(object) :
    def __init__(self) :
        self.__pathMan     = None
        self.__notebookMan = None
        self.__showFrame   = None

        self.__win_listbox_files = None
        self.__window            = None

        self.__filename  = None
        self.__filenames = []
        self.__last_item = -1

    def set_windows(self, window:object) :
        self.__window = window

    def run(self) :
        scrollbar = Scrollbar(self.__window)
        scrollbar.pack(side=RIGHT, fill=Y)
        # Create a Listbox with some items
        self.__win_listbox_files = Listbox(self.__window, height=30, width=40, 
                                                yscrollcommand=scrollbar.set, bd=5)
        self.__win_listbox_files.pack(side=LEFT, fill=None)

        self.__print_filenames(self.__filenames)
        self.__win_listbox_files.bind("<<ListboxSelect>>", self.__on_item_select)
        scrollbar.config(command=self.__win_listbox_files.yview)

    def __print_filenames(self, filenames) :
        #print('print_filenames {}'.format(filenames))
        # Add items to the Listbox
        for filename in filenames :
            print('items {}'.format(filename))
            self.__win_listbox_files.insert(END, filename)

    def show(self) :
        print('update {}'.format('SelectFilenameFrame'))
        self.__win_listbox_files.delete(0, END)
        self.__print_filenames(self.__filenames)

    def set_filenames(self, filenames: list):
        self.__filenames = filenames
        if (self.__showFrame != None):
            self.__showFrame.set_show_option(self.__showFrame.SHOW_FILENAMES)


    def set_filename(self, filename: str):
        try:
            idx = self.__filenames.index(filename)
            self.__set_item(idx)
        except:
            pass


    def __on_item_select(self, event: object) :
        try :
            selected_index = self.__win_listbox_files.curselection()
            if (len(selected_index) != 0 ):
                self.__set_item(selected_index[0])
                self.__filename = self.__win_listbox_files.get(self.__last_item)
                print('__on_item_select {}'.format(self.__filename))
                self.__notebookMan.add(self.__filename)
            else :
                pass

        except Exception as e :
            # Handle the exception
            print("Error SelectFilenameFrame", f"An error occurred: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def __set_item(self, item: int) :
        if ((self.__last_item >= 0) and
                (self.__last_item < self.__win_listbox_files.size())) :
            self.__win_listbox_files.itemconfig(self.__last_item, bg='#ffffff')

        if ((item >= 0) and
                (item < self.__win_listbox_files.size())) :
            self.__win_listbox_files.itemconfig(item, bg='OrangeRed3')
            self.__last_item = item

    def set_PathManager(self, pathMan: object):
        self.__pathMan = pathMan
        self.set_filenames(self.__pathMan.get_source_files())

    def set_NotebookManager(self, notebookMan: object) :
        self.__notebookMan = notebookMan

    def set_ShowFrame(self, showFrame: object) :
        self.__showFrame = showFrame
