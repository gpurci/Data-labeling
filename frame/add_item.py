#!/usr/bin/python

from tkinter import *
import numpy as np


class AddItemFrame :
    def __init__(self, frame_title: str, search_title: str, search_item: str, is_item=False) :
        self.__s_frame_title  = frame_title
        self.__s_search_title = search_title
        self.__s_search_item  = search_item

        self.__s_prev_item   = ''
        self.__as_items      = []
        self.__ask_is_item   = is_item
        self.__CHECK_SIMILARLY_ITEM = is_item

        self.__add_fn     = None
        self.__cancel_fn  = None

        self.__window         = None
        self.__add_item_frame = None

    def ask_is_item(self, is_item: bool):
        print('ask_is_item {}'.format(is_item))
        self.__ask_is_item = is_item
        self.__CHECK_SIMILARLY_ITEM = is_item

    def set_search_item(self, item: str):
        self.__s_search_item = item

    def set_add_fn(self, _fn: 'function'):
        self.__add_fn = _fn

    def set_cancel_fn(self, _fn: 'function'):
        self.__cancel_fn = _fn

    def set_items(self, items: 'array'):
        self.__as_items = np.array(items)

    def set_windows(self, window: object) :
        print('AddItemFrame.set_window')
        self.__window = window

    def get_items(self):
        return self.__as_items

    def get_item(self):
        return self.__s_search_item



    def run(self) :
        print('AddItemFrame run'.format(None))
        # open new window
        if (self.__add_item_frame != None):
            self.__add_item_frame.withdraw()

        self.__add_item_frame = Toplevel(self.__window)
        self.__add_item_frame.title(self.__s_frame_title)
        self.__add_item_frame.bind("<KeyPress>", self.__on_key_press_save_item)
        # window to put item
        add_frame      = Frame(self.__add_item_frame)
        add_frame.pack(side=TOP)
        # item of title
        _label_item = Label(add_frame, text=self.__s_search_title)
        _label_item.pack(side=LEFT)
        # frame to write item
        self.__w_search_item = Entry(add_frame, width=35, bd=5)
        self.__w_search_item.bind("<KeyRelease>", self.__on_item_change)
        self.__w_search_item.insert(0, self.__s_search_item)
        self.__w_search_item.pack({"side" : "left"})
        # add item button
        add_button    = Button(add_frame)
        add_button["text"]    = "Add"
        add_button["command"] = self.__cmd_add_item
        add_button.pack({"side" : "left"})
        # cancel operation
        cancel_button = Button(add_frame)
        cancel_button["text"]    = "Cancel"
        cancel_button["command"] = self.__cmd_cancel_add_item
        cancel_button.pack({"side" : "left"})

        # window to print predicted item
        listbox_frame = Frame(self.__add_item_frame)
        listbox_frame.pack(side=TOP)
        # scrool of frame where you put predicted item
        scrollbar = Scrollbar(listbox_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        # Create a Listbox with predicted item
        self.__w_similar_item = Listbox(listbox_frame, height=10, width=35, 
                                            yscrollcommand=scrollbar.set, bd=5, bg='#ffffff')
        self.__w_similar_item.pack(side=BOTTOM, fill=None)
        self.__w_similar_item.bind("<<ListboxSelect>>", self.__on_select_item)
        scrollbar.config(command=self.__w_similar_item.yview)
        # print similarity items
        _items = self.__get_similarly_items(self.__s_search_item)
        self.__print_items(_items)



    def __get_similarly_items(self, item: str):
        items_idx = np.array(list(map(lambda val: item in val, self.__as_items)))
        similarly_items = self.__as_items[items_idx]
        print('similarly_items {}'.format(similarly_items))
        return similarly_items

    def __set_search_item(self, item: str):
        self.__w_search_item.delete(0, END)
        self.__w_search_item.insert(0, item)
        self.__s_search_item = item

    def __print_items(self, items: list) :
        self.__w_similar_item.delete(0, END)
        # Add items to the Listbox
        for item in items :
            print('AddItemFrame item {}'.format(item))
            self.__w_similar_item.insert(END, item)

    def __on_select_item(self, event: object):
        selected_index = self.__w_similar_item.curselection()
        try :
            if (len(selected_index) != 0) :
                str_item = self.__w_similar_item.get(selected_index[0])
                print("Selected item {}, text {}".format(selected_index, str_item))
                self.__set_search_item(str_item)
                self.__item_change()

        except Exception as e :
            # Handle the exception
            print(f"Error AddItemFrame selected_index #{selected_index}#", f"An error occurred: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def __on_item_change(self, event: object):
        self.__item_change()

    def __item_change(self):
        _item = str(self.__w_search_item.get())
        if (self.__s_prev_item != _item):
            _items = self.__get_similarly_items(_item)
            self.__print_items(_items)
        else:
            pass
        self.__s_prev_item = _item


    def __add_item_to_items(self, item: str):
        if (self.__is_item_in_items(item) == False):
            self.__as_items = np.append(self.__as_items, item)

    def __cmd_add_item(self) :
        print('ADD_item ask_check_item {}'.format(self.__ask_is_item))
        _item = str(self.__w_search_item.get())
        if (self.__ask_check_item(_item) == True):
            self.__ask_window_frame(_item)
        else:
            self.__add_item_to_items(_item)
            self.set_search_item(_item)
            self.__add_fn(_item)
            self.__add_item_frame.withdraw()
        self.__ask_is_item = self.__CHECK_SIMILARLY_ITEM

    def __cmd_cancel_add_item(self) :
        print('cancel_add_object')
        self.__cancel_fn()
        self.__add_item_frame.withdraw()

    def __on_key_press_save_item(self, event: object) :
        # print('event {}'.format(event.keysym))
        if event.keysym == "Return" :
            self.__cmd_add_item()


    def __is_item_in_items(self, item: str):
        size_similar_item = np.argwhere(self.__as_items == item).reshape(-1).shape[0]
        print('size_similar_item {}'.format(size_similar_item))
        return (size_similar_item > 0)

    def __ask_check_item(self, item: str):
        print('ask_check_item {}'.format(self.__ask_is_item))
        if (self.__ask_is_item == True):
            self.__ask_is_item = self.__is_item_in_items(item)
        return self.__ask_is_item

    def __ask_window_frame(self, item: str):
        # open new window
        self.__ask_check_frame = Toplevel(self.__window)
        self.__ask_check_frame.title('Error')
        self.__ask_check_frame.bind("<KeyPress>", self.__on_key_press_yes)
        # item of title
        ask_check_label       = Label(self.__ask_check_frame, text='The @{}@ item exist,\nSave?'.format(item))
        ask_check_label.pack(side=LEFT)
        # add item button
        add_button            = Button(self.__ask_check_frame)
        add_button["text"]    = "Yes"
        add_button["command"] = self.__cmd_save_item
        add_button.pack({"side" : "left"})
        # cancel operation
        cancel_button            = Button(self.__ask_check_frame)
        cancel_button["text"]    = "No"
        cancel_button["command"] = self.__cmd_not_save_item
        cancel_button.pack({"side" : "left"})

    def __on_key_press_yes(self, event: object) :
        # print('event {}'.format(event.keysym))
        if event.keysym == "Return" :
            self.__cmd_save_item()

    def __cmd_save_item(self):
        self.__ask_check_frame.withdraw()
        print('START cmd_save_item {}'.format(self.__ask_is_item))
        self.__ask_is_item = False # if the item is find in list of items, the item will be save
        self.__cmd_add_item()
        print('END cmd_save_item {}'.format(self.__ask_is_item))

    def __cmd_not_save_item(self):
        self.__ask_check_frame.withdraw()
        self.__ask_is_item = True  # if the item is find in list of items, write another item

