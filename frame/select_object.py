#!/usr/bin/python

from tkinter import *
from tkinter import messagebox

class SelectObjectFrame(object):
    def __init__(self):
        self.last_item = -1

    def init(self):
        self.change_cursor(self.targetMan.get_default_object())

    def set_windows(self, window):
        print('SelectObjectFrame.set_windows')
        self.window = window

    def set_data(self, imageMan, targetMan):
        self.imageMan  = imageMan
        self.targetMan = targetMan

    def none_fn(self):
        pass

    def run(self):
        scrollbar = Scrollbar(self.window)
        scrollbar.pack( side = RIGHT, fill=Y )
        # Create a Listbox with some items
        self.selected_obj_name = Listbox(self.window, height=30, width=40, yscrollcommand = scrollbar.set, bd=5)
        self.selected_obj_name.pack( side = LEFT, fill=None )

        self.show(['no object'])
        self.selected_obj_name.bind("<<ListboxSelect>>", self.on_select_object_name)
        self.selected_obj_name.bind("<ButtonRelease-3>", self.on_click_release)
        scrollbar.config( command = self.selected_obj_name.yview )
        
        self.filemenu = Menu(self.selected_obj_name, tearoff = 0)
        self.filemenu.add_command(label ="Cut", command=self.cut_object_button) 
        self.filemenu.add_separator() 
        self.filemenu.add_command(label ="Rename", command=self.rename_object_button)
        self.filemenu.add_command(label ="Double", command=self.double_object_button)



    def show(self, lst_object):
        # Add items to the Listbox
        for name in lst_object:
            print('object_description {}'.format(name))
            self.selected_obj_name.insert(END, name)

    def update(self, lst_object):
        self.selected_obj_name.delete(0, END)
        self.show(lst_object)

    def cut(self, item):
        self.init()
        self.selected_obj_name.delete(item)

    def add(self, name, cursor):
        self.selected_obj_name.insert(cursor, name)
        self.change_cursor(cursor)

    def on_select_object_name(self, event):
        selected_index = self.selected_obj_name.curselection()
        try:
            print("Selected object index {}, size {}".format(selected_index, self.selected_obj_name.size()))
            if (len(selected_index) != 0):
                print("Selected object index {}, size {}".format(selected_index, self.selected_obj_name.size()))
                self.change_cursor(selected_index[0])
                print("Selected object index {}, size {}".format(selected_index, self.selected_obj_name.size()))
                self.targetMan.select_object(self.last_item)

        except Exception as e:
            # Handle the exception
            print(f"Error SelectObjectFrame selected_index #{selected_index}#", f"An error occurred: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def change_cursor(self, curent_cursor):
        if ((self.last_item != -1) and 
            (self.last_item < self.selected_obj_name.size()) and 
            (str(self.selected_obj_name.get(self.last_item))[0] == '>')):
            selected_obj = str(self.selected_obj_name.get(self.last_item))
            self.selected_obj_name.insert(self.last_item, selected_obj[len('> '):])
            self.selected_obj_name.delete(self.last_item+1)
        
        if (curent_cursor != -1):
            selected_obj = str(self.selected_obj_name.get(curent_cursor))
            self.selected_obj_name.insert(curent_cursor, '> ' + selected_obj)
            self.selected_obj_name.delete(curent_cursor+1)
        
        self.last_item = curent_cursor


    def cut_object_button(self):
        self.targetMan.cut_last_name()

    def double_object_button(self):
        self.targetMan.double_last_name()

    def rename_name_object(self):
        self.targetMan.set_last_object_name(self.obj_name_entry.get())
        self.filewin.withdraw()

    def cancel_name_object(self):
        self.filewin.withdraw()

    def on_key_press_rename_obj(self, event):
        #print('event {}'.format(event.keysym))
        if event.keysym == "Return":
            self.rename_name_object()

    def rename_object_button(self):
        print('rename_object {}'.format(None))
        
        self.filewin = Toplevel(self.window)
        self.filewin.title("Rename object name")
        self.filewin.bind("<KeyPress>", self.on_key_press_rename_obj)

        obj_name_label = Label(self.filewin, text="Object name")
        obj_name_label.pack(side = LEFT)

        self.obj_name_entry = Entry(self.filewin, width = 15, bd = 5)
        self.obj_name_entry.insert (0, '')
        self.obj_name_entry.pack({"side": "left"})

        add_button = Button(self.filewin)
        add_button["text"] = "Rename"
        add_button["command"] = self.rename_name_object
        add_button.pack({"side": "left"})
        
        cancel_button = Button(self.filewin)
        cancel_button["text"] = "Cancel"
        cancel_button["command"] = self.cancel_name_object
        cancel_button.pack({"side": "left"})

    def on_click_release(self, event):
        print('on_click_release {}'.format(event))
        try: 
            self.filemenu.tk_popup(event.x_root, event.y_root) 
        finally: 
            self.filemenu.grab_release()
