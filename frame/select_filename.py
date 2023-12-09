#!/usr/bin/python

from tkinter import *
from tkinter import messagebox

from pathlib import Path


class SelectFilenameFrame(object) :
    def __init__(self) :
        self.__pathMan     = None
        self.__notebookMan = None

        self.__win_listbox_files = None
        self.__window            = None

        self.__filename  = None
        self.__files     = None
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

        self.__print_filenames()
        self.__win_listbox_files.bind("<<ListboxSelect>>", self.__on_item_select)
        scrollbar.config(command=self.__win_listbox_files.yview)

    def __print_filenames(self) :
        self.__files = self.__pathMan.get_source_files()
        print('print_filenames {}'.format(self.__files))
        # Add items to the Listbox
        for filename in self.__files :
            print('items {}'.format(filename))
            self.__win_listbox_files.insert(END, filename)

    def show(self) :
        print('update {}'.format('SelectFilenameFrame'))
        self.__win_listbox_files.delete(0, END)
        self.__print_filenames()

    def set_filename(self, filename: str):
        try:
            idx = self.__files.index(filename)
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


    '''
    def __save_yes_fn(self) :
        self.__pathMan.set_filename(self.obj_name_entry.get())
        self.openFilenameMan.save()
        print('save_yes_fn open {}'.format(self.__filename))
        self.openFilenameMan.open(self.__filename)
        self.filewin.withdraw()

    def __save_no_fn(self) :
        print('save_no_fn open {}'.format(self.__filename))
        self.openFilenameMan.open(self.__filename)
        self.filewin.withdraw()

    def save_frame(self) :
        self.filewin = Toplevel(self.__window)
        self.filewin.title("Save")

        obj_name_label = Label(self.filewin, text="Save file")
        obj_name_label.pack(side=LEFT)

        self.obj_name_entry = Entry(self.filewin, width=70, bd=5)
        self.obj_name_entry.insert(50, self.__pathMan.get_source_filename())
        self.obj_name_entry.pack({"side" : "left"})

        save_button = Button(self.filewin)
        save_button["text"] = "Yes"
        save_button["command"] = self.__save_yes_fn
        save_button.pack({"side" : "left"})

        no_button = Button(self.filewin)
        no_button["text"] = "No"
        no_button["command"] = self.__save_no_fn
        no_button.pack({"side" : "left"})

    def set_OpenFilenameMan(self, openFilenameMan) :
        self.openFilenameMan = openFilenameMan
    '''

    def set_PathManager(self, pathManager) :
        self.__pathMan = pathManager

    def set_NotebookManager(self, notebookMan) :
        self.__notebookMan = notebookMan
