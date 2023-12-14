#!/usr/bin/python

from tkinter import *
from tkinter import messagebox


class SelectObjectFrame :
    def __init__(self) :
        self.__object_menu = None
        self.__selected_obj_name = None
        self.__targetMan = None
        self.__imageMan = None
        self.__window = None
        self.__last_item = -1

    def init(self) :
        self.__set_item(self.__targetMan.get_default_object())

    def set_windows(self, window:object) :
        print('SelectObjectFrame.set_windows')
        self.__window = window

    def set_data(self, imageMan:object, targetMan:object) :
        self.__imageMan = imageMan
        self.__targetMan = targetMan

    def none_fn(self) :
        pass

    def run(self) :
        scrollbar = Scrollbar(self.__window)
        scrollbar.pack(side=RIGHT, fill=Y)
        # Create a Listbox with some items
        self.__selected_obj_name = Listbox(self.__window, height=30, width=40, 
                                            yscrollcommand=scrollbar.set, bd=5, bg='#ffffff')
        self.__selected_obj_name.pack(side=LEFT, fill=None)

        self.__print_object(['no object'])
        self.__selected_obj_name.bind("<<ListboxSelect>>", self.__on_select_object_name)
        self.__selected_obj_name.bind("<ButtonRelease-3>", self.__on_click_release)
        scrollbar.config(command=self.__selected_obj_name.yview)

        self.__object_menu = Menu(self.__selected_obj_name, tearoff=0)
        self.__object_menu.add_command(label="Cut", command=self.__cut_object_button)
        self.__object_menu.add_separator()
        self.__object_menu.add_command(label="Rename", command=self.__rename_object_button)
        self.__object_menu.add_command(label="Double", command=self.__double_object_button)

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

    def __cut_object_button(self) :
        self.__targetMan.cut_last_name()

    def __double_object_button(self) :
        self.__targetMan.double_last_name()

    def __rename_object(self) :
        self.__targetMan.set_last_object_name(self.__obj_name_entry.get())
        self.__rename_frame.withdraw()

    def __cancel_name_object(self) :
        self.__rename_frame.withdraw()

    def __on_key_press_rename_obj(self, event) :
        # print('event {}'.format(event.keysym))
        if event.keysym == "Return" :
            self.__rename_object()

    def __rename_object_button(self) :
        print('rename_object {}'.format(None))

        self.__rename_frame = Toplevel(self.__window)
        self.__rename_frame.title("Rename object name")
        self.__rename_frame.bind("<KeyPress>", self.__on_key_press_rename_obj)

        obj_name_label = Label(self.__rename_frame, text="Object name")
        obj_name_label.pack(side=LEFT)

        self.__obj_name_entry = Entry(self.__rename_frame, width=15, bd=5)
        self.__obj_name_entry.insert(0, '')
        self.__obj_name_entry.pack({"side" : "left"})

        add_button = Button(self.__rename_frame)
        add_button["text"] = "Rename"
        add_button["command"] = self.__rename_object
        add_button.pack({"side" : "left"})

        cancel_button = Button(self.__rename_frame)
        cancel_button["text"] = "Cancel"
        cancel_button["command"] = self.__cancel_name_object
        cancel_button.pack({"side" : "left"})

    def __on_click_release(self, event: object) :
        print('on_click_release {}'.format(event))
        try :
            self.__object_menu.tk_popup(event.x_root, event.y_root)
        finally :
            self.__object_menu.grab_release()
