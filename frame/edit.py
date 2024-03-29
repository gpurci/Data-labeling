#!/usr/bin/python

from tkinter import *
from tkinter import messagebox

import numpy as np
from PIL import ImageTk, Image


class EditFrame(object) :
    def __init__(self) :
        self.__edit_frame     = None
        self.__canvas_frame   = None
        self.__workframe_dim  = None
        self.__window         = None
        self.__editMan        = None

        self.__is_canvas_click_release = True
        self.__init_canvas_object()

    def __init_canvas_object(self) :
        self.__cs_image     = None
        self.__cs_rectangle = None
        self.__cs_text      = None

        self.__cs_circle_0 = None
        self.__cs_circle_1 = None
        self.__cs_circle_2 = None
        self.__cs_circle_3 = None

    def set_windows(self, window: object) :
        self.__window = window

    def set_dimension(self, workframe_dim: object) :
        self.__workframe_dim = workframe_dim

    def none_fn(self) :
        print('none_fn {}'.format('test'))
        pass

    def img_show(self, img: object) :
        self.__canvas_frame.itemconfig(self.__cs_image, image=img)
        self.delete_obj_from_frame()

    def rectangle(self, box: tuple, box_name: str) :
        self.__delete_selected_box()
        self.__cs_rectangle = self.__canvas_frame.create_rectangle(box, outline='yellow', width=4)
        x = box[0] + 25
        y = box[1]
        self.__cs_text      = self.__canvas_frame.create_text(x, y, text=box_name, fill="red", 
                                                                font=('Helvetica 15 bold'))

    def box_4_circle(self, box: tuple) :
        self.__delete_box_4_circle()
        x00, y00 = box[0], box[1]
        x01, y01 = box[2], box[1]
        x10, y10 = box[0], box[3]
        x11, y11 = box[2], box[3]

        step_point = 4    #the tolerance in pixel point to select a peak of box
        self.__cs_circle_0 = self.__canvas_frame.create_oval(x00 - step_point, y00 - step_point, 
                                                                x00 + step_point, y00 + step_point, 
                                                                outline='yellow', width=4)
        self.__cs_circle_1 = self.__canvas_frame.create_oval(x01 - step_point, y01 - step_point, 
                                                                x01 + step_point, y01 + step_point, 
                                                                outline='yellow', width=4)
        self.__cs_circle_2 = self.__canvas_frame.create_oval(x10 - step_point, y10 - step_point, 
                                                                x10 + step_point, y10 + step_point, 
                                                                outline='yellow', width=4)
        self.__cs_circle_3 = self.__canvas_frame.create_oval(x11 - step_point, y11 - step_point, 
                                                                x11 + step_point, y11 + step_point, 
                                                                outline='yellow', width=4)

    def move(self, x: int, y: int) :
        self.__canvas_frame.move(self.__cs_image, x, y)

    def coords(self, x: int, y: int) :
        self.__canvas_frame.coords(self.__cs_image, x, y)

    def __delete_selected_box(self) :
        if (self.__cs_rectangle is not None):
            self.__canvas_frame.delete(self.__cs_rectangle)
            self.__canvas_frame.delete(self.__cs_text)
        self.__cs_rectangle = None
        self.__cs_text = None

    def __delete_box_4_circle(self) :
        if (self.__cs_circle_0 is not None):
            self.__canvas_frame.delete(self.__cs_circle_0)
            self.__canvas_frame.delete(self.__cs_circle_1)
            self.__canvas_frame.delete(self.__cs_circle_2)
            self.__canvas_frame.delete(self.__cs_circle_3)
        self.__cs_circle_0 = None
        self.__cs_circle_1 = None
        self.__cs_circle_2 = None
        self.__cs_circle_3 = None

    def delete_obj_from_frame(self):
        self.__delete_selected_box()
        self.__delete_box_4_circle()

    def __on_canvas_click(self, event: object) :
        if (self.__is_canvas_click_release == True):
            self.__is_canvas_click_release = False
            self.__editMan.set_start_work_coords(event.x, event.y)

        self.__editMan.set_end_work_coords(event.x, event.y)
        try :
            self.__editMan.run_last_mode()
        except Exception as e :
            # Handle the exception
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def __on_canvas_click_release(self, event: object) :
        self.__is_canvas_click_release = True
        try :
            self.__editMan.set_end_work_coords(event.x, event.y)
            self.__editMan.run_last_release_mode()
        except Exception as e :
            # Handle the exception
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def __on_mouse_wheel(self, event: object) :
        self.__editMan.mouse_wheel(event)

    def run(self) :
        self.__edit_frame = LabelFrame(self.__window, text='Not file')
        self.__edit_frame.pack(fill="both", expand="yes")

        self.__canvas_frame = Canvas(self.__edit_frame,
                                   width=self.__workframe_dim.get_width(), height=self.__workframe_dim.get_height(),
                                   bd=0, bg='#d1d8e3')  # d1d8e3

        img = Image.new(mode='RGB', size=(4, 4), color=(0xd1, 0xd8, 0xe3))
        self.__cs_image = self.__canvas_frame.create_image(
            (0, 0),
            anchor=NW,
            image=ImageTk.PhotoImage(img))
        self.__canvas_frame.pack()
        self.__canvas_frame.bind("<B1-Motion>", self.__on_canvas_click)
        self.__canvas_frame.bind("<ButtonRelease-1>", self.__on_canvas_click_release)
        self.__canvas_frame.bind("<Button-4>", self.__on_mouse_wheel)
        self.__canvas_frame.bind("<Button-5>", self.__on_mouse_wheel)

        button_frame = LabelFrame(self.__window, text='Work mode')
        button_frame.pack(fill="both", expand="yes")

        select_btn = Button(button_frame, cursor="tcross")
        select_btn["text"] = "Select"
        select_btn["command"] = self.__cmd_select_mode
        select_btn.pack({"side" : "left"})

        edit_btn = Button(button_frame, cursor="plus")
        edit_btn["text"] = "Edit"
        edit_btn["command"] = self.__cmd_edit_mode
        edit_btn.pack({"side" : "left"})

        normal_btn = Button(button_frame, cursor="arrow")
        normal_btn["text"] = "Normal"
        normal_btn["command"] = self.__cmd_normal_mode
        normal_btn.pack({"side" : "left"})

        normal_btn = Button(button_frame, cursor="circle")
        normal_btn["text"] = "Find object"
        normal_btn["command"] = self.__cmd_find_obj_mode
        normal_btn.pack({"side" : "left"})

    def set_work_frame(self, filename: str) :
        self.__edit_frame.config(text=filename)

    def __cmd_select_mode(self) :
        self.__editMan.set_work_mode(self.__editMan.SELECT_MODE)
        self.__canvas_frame.config(cursor="tcross")
        self.__delete_selected_box()
        self.__delete_box_4_circle()

    def __cmd_edit_mode(self) :
        self.__editMan.set_work_mode(self.__editMan.EDIT_MODE)
        self.__canvas_frame.config(cursor="plus")
        self.__editMan.object_edit()

    def __cmd_normal_mode(self) :
        self.__editMan.set_work_mode(self.__editMan.NORMAL_MODE)
        self.__canvas_frame.config(cursor="arrow")
        self.__delete_box_4_circle()

    def __cmd_find_obj_mode(self) :
        self.__editMan.set_work_mode(self.__editMan.FIND_OBJ_MODE)
        self.__canvas_frame.config(cursor="circle")
        self.__delete_selected_box()
        self.__delete_box_4_circle()

    def set_EditManager(self, editManager: object) :
        self.__editMan = editManager
