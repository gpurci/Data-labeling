#!/usr/bin/python

from tkinter import *
from tkinter import messagebox
import numpy as np


class AddNameFrame :
    def __init__(self) :
        self.__frame_title = None
        self.__label_title = None
        self.__entry_text  = None
        self.__prev_value  = ''
        self.__names       = []
        self._is_check_item = True

        self.__add_fn     = None
        self.__check_fn   = None
        self.__cancel_fn  = None

        self.__window = None

    def set_arg(self, frame_title: str, label_title: str, entry_text: str, add_fn: 'function', cancel_fn: 'function') :
        self.__frame_title = frame_title
        self.__label_title = label_title
        self.__entry_text  = entry_text

        self.__add_fn     = add_fn
        self.__cancel_fn  = cancel_fn

    def set_entry_text(self, entry_text: str):
        self.__entry_text = entry_text

    def set_add_fn(self, add_fn: 'function'):
        self.__add_fn = add_fn

    def set_names(self, names):
        self.__names = np.array(names)

    def set_check_fn(self, check_fn):
        self.__check_fn = check_fn

    def set_windows(self, window: object) :
        print('AddNameFrame.set_window')
        self.__window = window



    def run(self) :
        print('AddNameFrame run'.format(None))
        # open new window
        self.__add_name_frame = Toplevel(self.__window)
        self.__add_name_frame.title(self.__frame_title)
        self.__add_name_frame.bind("<KeyPress>", self.__on_key_press_save)
        # window to put name
        add_frame      = Frame(self.__add_name_frame)
        add_frame.pack(side=TOP)
        # name of title
        obj_name_label = Label(add_frame, text=self.__label_title)
        obj_name_label.pack(side=LEFT)
        # frame to write name
        self.__w_name_entry = Entry(add_frame, width=35, bd=5)
        self.__w_name_entry.bind("<KeyRelease>", self.__on_name_modification)
        self.__w_name_entry.insert(0, self.__entry_text)
        self.__w_name_entry.pack({"side" : "left"})
        # add name button
        add_button    = Button(add_frame)
        add_button["text"]    = "Add"
        add_button["command"] = self.__cmd_add_item
        add_button.pack({"side" : "left"})
        # cancel operation
        cancel_button = Button(add_frame)
        cancel_button["text"]    = "Cancel"
        cancel_button["command"] = self.__cmd_cancel_add_item
        cancel_button.pack({"side" : "left"})

        # window to print predicted name
        listbox_frame = Frame(self.__add_name_frame)
        listbox_frame.pack(side=TOP)
        # scrool of frame where you put predicted name
        scrollbar = Scrollbar(listbox_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        # Create a Listbox with predicted name
        self.__w_similar_item = Listbox(listbox_frame, height=10, width=35, 
                                            yscrollcommand=scrollbar.set, bd=5, bg='#ffffff')
        self.__w_similar_item.pack(side=BOTTOM, fill=None)

        #self.__print_object(['no object'])
        self.__w_similar_item.bind("<<ListboxSelect>>", self.__on_select_item)
        scrollbar.config(command=self.__w_similar_item.yview)
        # print similarity names
        self.__name_modification()


    def __get_similary_names(self, name: str):
        is_name_idx = np.array(list(map(lambda val: name in val, self.__names)))
        similary_names = self.__names[is_name_idx]
        print('similary_names {}'.format(similary_names))
        return similary_names

    def __set_entry_name(self, name: str):
        self.__w_name_entry.delete(0, END)
        self.__w_name_entry.insert(0, name)
        self.__entry_text = name

    def __print_names(self, lst_object: list) :
        self.__w_similar_item.delete(0, END)
        # Add items to the Listbox
        for name in lst_object :
            print('AddNameFrame name {}'.format(name))
            self.__w_similar_item.insert(END, name)

    def __on_select_item(self, event: object):
        selected_index = self.__w_similar_item.curselection()
        try :
            if (len(selected_index) != 0) :
                str_item = self.__w_similar_item.get(selected_index[0])
                print("Selected item {}, text {}".format(selected_index, str_item))
                self.__set_entry_name(str_item)
                self.__name_modification()

        except Exception as e :
            # Handle the exception
            print(f"Error AddNameFrame selected_index #{selected_index}#", f"An error occurred: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def __on_name_modification(self, event: object):
        self.__name_modification()

    def __name_modification(self):
        value = str(self.__w_name_entry.get())
        if (self.__prev_value != value):
            names = self.__get_similary_names(value)
            self.__print_names(names)
        else:
            pass
        self.__prev_value = value


    def get_name(self):
        return str(self.__w_name_entry.get())

    def __cmd_add_item(self) :
        print('ADD_item')
        str_item = str(self.__w_name_entry.get())
        if (self.__check_fn(str_item) == True):
            self.__ask_window_frame(str_item)
        else:
            self.__add_fn(str_item)
            self.__add_name_frame.withdraw()
        self._is_check_item = True

    def __cmd_cancel_add_item(self) :
        print('cancel_add_object')
        self.__cancel_fn()
        self.__add_name_frame.withdraw()

    def __on_key_press_save(self, event: object) :
        # print('event {}'.format(event.keysym))
        if event.keysym == "Return" :
            self.__cmd_add_item()


    def ask_check_name(self, name: str):
        print('ask_check_name run'.format(None))
        if (self._is_check_item == True):
            size_similar_item = np.argwhere(self.__names == name).reshape(-1).shape[0]
            print('size_similar_item {}'.format(size_similar_item))
            self._is_check_item = (size_similar_item > 0)
        return self._is_check_item

    def not_ask_check_name(self, name: str):
        return False
        

    def __ask_window_frame(self, name: str):
        # open new window
        self.__ask_check_frame = Toplevel(self.__window)
        self.__ask_check_frame.title('Error')
        self.__ask_check_frame.bind("<KeyPress>", self.__on_key_press_yes)
        # name of title
        ask_check_label       = Label(self.__ask_check_frame, text='The @{}@ item exist,\nSave?'.format(name))
        ask_check_label.pack(side=LEFT)
        # add name button
        add_button            = Button(self.__ask_check_frame)
        add_button["text"]    = "Yes"
        add_button["command"] = self.__cmd_save_name
        add_button.pack({"side" : "left"})
        # cancel operation
        cancel_button            = Button(self.__ask_check_frame)
        cancel_button["text"]    = "No"
        cancel_button["command"] = self.__cmd_not_save_name
        cancel_button.pack({"side" : "left"})

    def __on_key_press_yes(self, event: object) :
        # print('event {}'.format(event.keysym))
        if event.keysym == "Return" :
            self.__cmd_save_name()

    def __cmd_save_name(self):
        self._is_check_item = False # if the item is find in list of items, the name will be save
        self.__ask_check_frame.withdraw()

    def __cmd_not_save_name(self):
        self._is_check_item = True  # if the item is find in list of items, write another name
        self.__ask_check_frame.withdraw()

