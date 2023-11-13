#!/usr/bin/python

from tkinter import *
from tkinter import messagebox

from pathlib import Path

class SelectFilenameFrame(object):
    def __init__(self, datasets):
        self.datasets = datasets
        self.last_item = -1

    def set_windows(self, windows):
        self.windows = windows

    def run(self):
        scrollbar = Scrollbar(self.windows)
        scrollbar.pack( side = RIGHT, fill=Y )
        # Create a Listbox with some items
        self.listbox_files_dataset = Listbox(self.windows, height=30, width=40, yscrollcommand = scrollbar.set, bd=5)
        self.listbox_files_dataset.pack( side = LEFT, fill=None )

        self.show()
        self.listbox_files_dataset.bind("<<ListboxSelect>>", self.on_item_select)
        scrollbar.config( command = self.listbox_files_dataset.yview )

    def show(self):
        filenames = Path(self.pathManager.get_source_path()).glob('*')
        print('print_filenames {}'.format(filenames))
        # Add items to the Listbox
        for filename in filenames:
            new_filename = filename.name
            print('items {}'.format(new_filename))
            self.listbox_files_dataset.insert(END, new_filename)
    
    def update(self):
        print('update {}'.format('SelectFilenameFrame'))
        self.listbox_files_dataset.delete(0, END)
        self.show()

    def on_item_select(self, event):
        try:
            selected_index = self.listbox_files_dataset.curselection()
            if (len(selected_index) != 0):
                self.filename = self.listbox_files_dataset.get(selected_index[0])
                self.change_cursor(selected_index[0])
                
                self.openFilenameMan.save()
                self.openFilenameMan.open(self.filename)
                self.notebookMan.add_frame(self.filename)
            else:
                pass

        except Exception as e:
            # Handle the exception
            print("Error SelectFilenameFrame", f"An error occurred: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def change_cursor(self, curent_cursor):
        if ((self.last_item != -1) and 
            (self.last_item < self.listbox_files_dataset.size()) and 
            (str(self.listbox_files_dataset.get(self.last_item)[0]) == '>')):
            selected_file = str(self.listbox_files_dataset.get(self.last_item))
            self.listbox_files_dataset.insert(self.last_item, selected_file[len('> '):])
            self.listbox_files_dataset.delete(self.last_item+1)
            
        if (curent_cursor != -1):
            selected_file = str(self.listbox_files_dataset.get(curent_cursor))
            self.listbox_files_dataset.insert(curent_cursor, '> ' + selected_file)
            self.listbox_files_dataset.delete(curent_cursor+1)
        self.last_item = curent_cursor
    

    def save_yes_fn(self):
        self.pathManager.set_filename(self.obj_name_entry.get())
        self.openFilenameMan.save()
        print('save_yes_fn open {}'.format(self.filename))
        self.openFilenameMan.open(self.filename)
        self.filewin.withdraw()

    def save_no_fn(self):
        print('save_no_fn open {}'.format(self.filename))
        self.openFilenameMan.open(self.filename)
        self.filewin.withdraw()

    def save_frame(self):
        self.filewin = Toplevel(self.windows)
        self.filewin.title("Save")

        obj_name_label = Label(self.filewin, text="Save file")
        obj_name_label.pack(side = LEFT)

        self.obj_name_entry = Entry(self.filewin, width = 70, bd = 5)
        self.obj_name_entry.insert (50, self.pathManager.get_source_filename())
        self.obj_name_entry.pack({"side": "left"})

        save_button = Button(self.filewin)
        save_button["text"] = "Yes"
        save_button["command"] = self.save_yes_fn
        save_button.pack({"side": "left"})

        no_button = Button(self.filewin)
        no_button["text"] = "No"
        no_button["command"] = self.save_no_fn
        no_button.pack({"side": "left"})



    def set_OpenFilenameMan(self, openFilenameMan):
        self.openFilenameMan = openFilenameMan

    def set_PathManager(self, pathManager):
        self.pathManager = pathManager

    def set_NotebookManager(self, notebookMan):
        self.notebookMan = notebookMan

