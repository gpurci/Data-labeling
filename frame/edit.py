#!/usr/bin/python

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

from pathlib import Path
import numpy as np
from PIL import ImageTk, Image

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


class EditFrame(object):
    def __init__(self):
        self.is_canvas_dataset_click_release = True
        self.init_canvas_object()

    def init_canvas_object(self):
        self.canvas_obj_image = None
        self.canvas_obj_rectangle = None
        self.canvas_obj_text = None
        
        self.canvas_obj_line_0 = None
        self.canvas_obj_line_1 = None
        
        self.canvas_obj_circle_0 = None
        self.canvas_obj_circle_1 = None
        self.canvas_obj_circle_2 = None
        self.canvas_obj_circle_3 = None

    def set_windows(self, windows:object):
        self.windows = windows

    def set_dimension(self, dataset_dim:object):
        self.dataset_dim = dataset_dim

    def none_fn(self):
        print('none_fn {}'.format('test'))
        pass

    def img_show(self, img:object):
        self.input_canvas.itemconfig(self.canvas_obj_image, image=img)
            
        self.delete_selected_box()

    def move(self, x:int, y:int):
        self.input_canvas.move(self.canvas_obj_image, x, y)

    def coords(self, x:int, y:int):
        self.input_canvas.coords(self.canvas_obj_image, x, y)

    def delete_selected_box(self):
        if (self.canvas_obj_rectangle != None):
            self.input_canvas.delete(self.canvas_obj_rectangle)
            self.input_canvas.delete(self.canvas_obj_text)
        self.canvas_obj_rectangle = None
        self.canvas_obj_text           = None

    def delete_edit_mode(self):
        if (self.canvas_obj_circle_0 != None):
            self.input_canvas.delete(self.canvas_obj_circle_0)
            self.input_canvas.delete(self.canvas_obj_circle_1)
            self.input_canvas.delete(self.canvas_obj_circle_2)
            self.input_canvas.delete(self.canvas_obj_circle_3)
        self.canvas_obj_circle_0 = None
        self.canvas_obj_circle_1 = None
        self.canvas_obj_circle_2 = None
        self.canvas_obj_circle_3 = None

    def rectange_img_show(self, box:tuple, text:str):
        self.delete_selected_box()
        self.canvas_obj_rectangle = self.input_canvas.create_rectangle(box, outline= 'yellow', width=4)
        x = box[0]+25
        y = box[1]
        self.canvas_obj_text          = self.input_canvas.create_text(x, y, text=text, fill="red", font=('Helvetica 15 bold'))

    def edit_mode(self, box:tuple):
        self.delete_edit_mode()
        x00, y00 = box[0], box[1]
        x01, y01 = box[2], box[1]
        x10, y10 = box[0], box[3]
        x11, y11 = box[2], box[3]
        self.canvas_obj_circle_0 = self.input_canvas.create_oval(x00-4, y00-4, x00+4, y00+4, outline= 'yellow', width=4)
        self.canvas_obj_circle_1 = self.input_canvas.create_oval(x01-4, y01-4, x01+4, y01+4, outline= 'yellow', width=4)
        self.canvas_obj_circle_2 = self.input_canvas.create_oval(x10-4, y10-4, x10+4, y10+4, outline= 'yellow', width=4)
        self.canvas_obj_circle_3 = self.input_canvas.create_oval(x11-4, y11-4, x11+4, y11+4, outline= 'yellow', width=4)

    def plus(self):
        if (self.canvas_obj_line_0 != None):
            self.input_canvas.delete(self.canvas_obj_line_0)
            self.input_canvas.delete(self.canvas_obj_line_1)
            del self.canvas_obj_line_0
            del self.canvas_obj_line_1
        # Add a line in canvas widget
        self.canvas_obj_line_0 = self.input_canvas.create_line((int(self.dataset_dim.width/2), 0, int(self.dataset_dim.width/2), int(self.dataset_dim.height)), 
                                                                                                        fill="green", width=2)
        self.canvas_obj_line_1 = self.input_canvas.create_line((0, int(self.dataset_dim.height/2), int(self.dataset_dim.width), int(self.dataset_dim.height/2)), 
                                                                                                        fill="green", width=2)

    def on_canvas_dataset_click(self, event:object):
        if (self.is_canvas_dataset_click_release):
            self.is_canvas_dataset_click_release = False
            self.editManager.set_start_work_coords(event.x, event.y)

        self.editManager.set_end_work_coords(event.x, event.y)
        try:
            self.editManager.run_last_mode()
        except Exception as e:
            # Handle the exception
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def on_canvas_dataset_click_release(self, event:object):
        self.is_canvas_dataset_click_release = True
        try:
            self.editManager.run_last_release_mode()
        except Exception as e:
            # Handle the exception
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def on_key_press_select_obj(self, event:object):
        #print('event {}'.format(event.keysym))
        if event.keysym == "Return":
            self.editManager.add_object_name()

    def mouse_wheel(self, event:object):
        self.editManager.mouse_wheel(event)

    def get_object_name(self):
        return self.obj_name_entry.get()

    def destroy_select_object_frame(self):
        self.filewin.withdraw()

    def cancel_object_name(self):
        self.destroy_select_object_frame()
        self.delete_selected_box()

    def select_object_frame(self):
        self.filewin = Toplevel(self.windows)
        self.filewin.title("Object name")
        self.filewin.bind("<KeyPress>", self.on_key_press_select_obj)

        obj_name_label = Label(self.filewin, text="Object name")
        obj_name_label.pack(side = LEFT)

        self.obj_name_entry = Entry(self.filewin, width = 15, bd = 5)
        self.obj_name_entry.insert (0, '')
        self.obj_name_entry.pack({"side": "left"})

        add_button = Button(self.filewin)
        add_button["text"] = "Add"
        add_button["command"] = self.editManager.add_object_name
        add_button.pack({"side": "left"})
        
        cancel_button = Button(self.filewin)
        cancel_button["text"] = "Cancel"
        cancel_button["command"] = self.cancel_object_name
        cancel_button.pack({"side": "left"})

    def run(self):
        self.canvas_frame = LabelFrame(self.windows, text='Not file')
        self.canvas_frame.pack(fill="both", expand="yes")

        self.input_canvas = Canvas(self.canvas_frame, 
                                    width=self.dataset_dim.get_width(), height=self.dataset_dim.get_height(), 
                                    bd=0, bg='#d1d8e3')#d1d8e3

        img = np.ones((10, 10, 3))#d1d8e3
        img = Image.fromarray(img, mode='RGB')
        self.canvas_obj_image = self.input_canvas.create_image(
                                                                (0, 0), 
                                                                anchor=NW, 
                                                                image=ImageTk.PhotoImage(img))
        self.input_canvas.pack()
        self.input_canvas.bind("<B1-Motion>", self.on_canvas_dataset_click)
        self.input_canvas.bind("<ButtonRelease-1>", self.on_canvas_dataset_click_release)
        self.input_canvas.bind("<Button-4>", self.mouse_wheel)
        self.input_canvas.bind("<Button-5>", self.mouse_wheel)
        
        button_frame = LabelFrame(self.windows, text='Work mode')
        button_frame.pack(fill="both", expand="yes")

        select_button = Button(button_frame, cursor="tcross")
        select_button["text"] = "Select"
        select_button["command"] = self.select_button
        select_button.pack({"side": "left"})

        edit_button = Button(button_frame, cursor="plus")
        edit_button["text"] = "Edit"
        edit_button["command"] = self.edit_button
        edit_button.pack({"side": "left"})

        normal_button = Button(button_frame, cursor="arrow")
        normal_button["text"] = "Normal"
        normal_button["command"] = self.normal_button
        normal_button.pack({"side": "left"})

    def set_work_frame(self, filename:str):
        self.canvas_frame.config(text=filename)


    def select_button(self):
        self.editManager.set_work_mode(self.editManager.SELECT_MODE)
        self.input_canvas.config(cursor="tcross")
        self.delete_selected_box()
        self.delete_edit_mode()

    def edit_button(self):
        self.editManager.set_work_mode(self.editManager.EDIT_MODE)
        self.input_canvas.config(cursor="plus")
        self.delete_selected_box()
        self.editManager.object_edit()

    def normal_button(self):
        self.editManager.set_work_mode(self.editManager.NORMAL_MODE)
        self.input_canvas.config(cursor="arrow")
        self.delete_edit_mode()


    def set_EditManager(self, editManager:object):
        self.editManager = editManager
