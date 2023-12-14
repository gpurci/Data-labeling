from tkinter import * 
from tkinter import ttk
import numpy as np

from add_name import *

root = Tk()
root.title("Add name")



def __none_fn():
    pass

def __none_add_fn(filename:str):
    pass

def check_fn(filename:str):
    return 'test' == filename

def add_frame():
    add_name_frame.run()

add_button    = Button(root)
add_button["text"]    = "Add"
add_button["command"] = add_frame
add_button.pack({"side" : "left"})


add_name_frame = AddItemFrame()
add_name_frame.set_windows(root)

frame_title = 'Add filename'
label_title = 'Current filename'
entry_text  = ''

add_fn     = __none_add_fn
cancel_fn  = __none_fn



lst_names = ['filename', 'test', 'file', 'filetest', 'file0', 'file1', 'file2']
item = 'test'
print('test ', np.append(lst_names, item))

add_name_frame.set_arg(frame_title, label_title, entry_text, add_fn, cancel_fn)
add_name_frame.set_check_fn(add_name_frame.ask_check_item)
add_name_frame.set_entry_text("filename")
add_name_frame.set_names(lst_names)
#add_name_frame.set_add_fn(self.__add_name_fn)
add_name_frame.run()




root.mainloop()