from tkinter import * 
from tkinter import ttk
import numpy as np
# importing sys
import sys

# adding Folder_2/subfolder to the system path
sys.path.insert(0, '/home/gheorghe/Desktop/Data_labeling/Data-labeling/frame')
from add_item import *

root = Tk()
root.title("Add name")



def __none_fn():
    print('CANCEL test {}'.format(None))
    pass

def __none_add_fn(filename:str):
    print('ADD test {}'.format(filename))
    pass

def add_frame_check_no():
    add_name_frame.ask_is_item(False)

def add_frame_check_yes():
    add_name_frame.ask_is_item(True)

def add_frame():
    add_name_frame.run()

add_button    = Button(root)
add_button["text"]    = "Check filename"
add_button["command"] = add_frame_check_yes
add_button.pack({"side" : "left"})

add_button    = Button(root)
add_button["text"]    = "Not check filename"
add_button["command"] = add_frame_check_no
add_button.pack({"side" : "left"})

add_button    = Button(root)
add_button["text"]    = "Add filename"
add_button["command"] = add_frame
add_button.pack({"side" : "left"})


frame_title = 'Add filename'
label_title = 'Current filename'
search_item = ''

add_name_frame = AddItemFrame(frame_title, label_title, search_item, True)
add_name_frame.set_windows(root)

lst_names = ['filename', 'test', 'file', 'filetest', 'file0', 'file1', 'file2']

#add_name_frame.set_search_item("filename")
add_name_frame.set_items(lst_names)
add_name_frame.set_add_fn(__none_add_fn)
add_name_frame.set_cancel_fn(__none_fn)
add_name_frame.run()




root.mainloop()