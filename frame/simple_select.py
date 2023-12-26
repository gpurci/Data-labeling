#!/usr/bin/python

from tkinter import *
from tkinter import messagebox

class SelectFrame :
    def __init__(self) :
        self.__object_menu       = None
        self.__selected_obj_name = None
        self.__targetMan = None
        self.__imageMan  = None
        self.__window    = None
        self.__last_item = -1


    def init(self) :
        self.__set_item(self.__targetMan.get_default_object())

    def set_windows(self, window:object) :
        print('SelectObjectFrame.set_windows')
        self.__window = window

    def none_fn(self) :
        pass

    def run(self) :
        scrollbar = Scrollbar(self.__window)
        scrollbar.pack(side=RIGHT, fill=Y)
        # Create a Listbox with some items
        self.__selected_obj_name = Listbox(self.__window, height=20, width=5, 
                                            yscrollcommand=scrollbar.set, bd=5, bg='#ffffff')
        self.__selected_obj_name.pack(side=LEFT, fill=None)

        self.__print_object(['no object'])
        self.__selected_obj_name.bind("<<ListboxSelect>>", self.__on_select_object_name)
        scrollbar.config(command=self.__selected_obj_name.yview)



    def __print_object(self, lst_object: list) :
        # Add items to the Listbox
        for name in lst_object :
            print('object_description {}'.format(name))
            self.__selected_obj_name.insert(END, name)

    def show(self) :
        self.__selected_obj_name.config(bg='#ffffff')
        self.__selected_obj_name.delete(0, END)
        self.__print_object(self.__targetMan.get_names())
        self.__selected_obj_name.itemconfig(self.__targetMan.get_selected_object(), bg='OrangeRed3')

    def cut(self, item: int) :
        self.init()
        self.__selected_obj_name.delete(item)

    def add(self, name: str, item: int) :
        self.__selected_obj_name.insert(item, name)
        self.__set_item(cursor)

    def __on_select_object_name(self, event: object) :
        self.__object_menu.pack_forget()

        selected_index = self.__selected_obj_name.curselection()
        try :
            print("Selected object index {}, size {}".format(selected_index, self.__selected_obj_name.size()))
            if (len(selected_index) != 0) :
                print("Selected object index {}, size {}".format(selected_index, self.__selected_obj_name.size()))
                self.__set_item(selected_index[0])
                print("Selected object index {}, size {}".format(selected_index, self.__selected_obj_name.size()))
                self.__targetMan.select_object(self.__last_item)

        except Exception as e :
            # Handle the exception
            print(f"Error SelectObjectFrame selected_index #{selected_index}#", f"An error occurred: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def __set_item(self, item: int) :
        if ((self.__last_item >= 0) and
                (self.__last_item < self.__selected_obj_name.size())) :
            self.__selected_obj_name.itemconfig(self.__last_item, bg='#ffffff')

        if ((item >= 0) and
                (item < self.__selected_obj_name.size())) :
            self.__selected_obj_name.itemconfig(item, bg='OrangeRed3')
            self.__last_item = item
