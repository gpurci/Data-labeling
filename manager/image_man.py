#!/usr/local/bin/python

from PIL import Image, ImageTk, ImageDraw
import numpy
import numpy as np
import time
import datetime
from MyStr import *

class ImageManager:
    """
    y = numarul de linii
    x = nunarul de coloane
    data = imaginea
    """
    def __init__(self, frame = (600, 600)):
        self.y = 0
        self.x = 0
        self.size_frame = np.array(frame, dtype=np.float32)
        self.zoom = 1
        self.zoom_normal = 1
        self.zoom_step = 0.05
        self.prev_cursor = np.array((0, 0), dtype=np.float32)
        self.data = None
        self.flag = 0

    def __str__(self):
        returnStr = "ImageManager\n linii:  " + str(self.y)
        returnStr += "\n coloane:  " + str(self.x)
        returnStr += "\n" + str(self.data)
        return returnStr

    def __do_calc_zoom(self):
        fX, fY = self.size_frame / self.image_size
        print('do_calc_zoom size_frame {} WH format'.format(self.size_frame))
        print('do_calc_zoom image_size {} WH format'.format(self.image_size))
        print('do_calc_zoom zoom W {} H {}'.format(fX, fY))
        if (fY >= 1 and fX >= 1):
            if fY > fX:
                self.zoom = fY
            else:
                self.zoom = fX

        if (fY < 1 or fX < 1):
            if fY < fX:
                self.zoom = fY
            else:
                self.zoom = fX
        self.zoom_normal = self.zoom
        print('do_calc_zoom zoom {}'.format(self.zoom))

    def get_zoom(self):
        return self.zoom

    def get_start_cursor(self):
        img_size = np.array(self.image_size * self.zoom, dtype=np.int32)
        print("W {}, H {}".format(*img_size))
        img_width, img_height = img_size
        fr_width, fr_height         = self.size_frame
        cursor_x, cursor_y = (fr_width - img_width) / 2., (fr_height - img_height) / 2.
        cursor_x, cursor_y = int(cursor_x), int(cursor_y)
        self.prev_cursor = np.array((cursor_x, cursor_y), dtype=np.float32)
        print('cursor_x {}, cursor_y {}'.format(cursor_x, cursor_y))
        return cursor_x, cursor_y

    def read(self, name):
        self.data = Image.open(name)
        self.image_size = np.array(self.data.size, dtype=np.float32)
        print("image_size W {}, H {}".format(*self.image_size))
        self.__do_calc_zoom()
        self.prev_cursor = np.array((0, 0), dtype=np.float32)
        img_size = np.array(self.image_size * self.zoom, dtype=np.int32)
        
        cursor_x, cursor_y = self.get_start_cursor()
        self.coords_fn(cursor_x, cursor_y)

        self.show_data = ImageTk.PhotoImage(self.data.resize(img_size))

    def zoom_image(self, zoom_out, cursor):
        print('zoom_image zoom_out {}, cursor {}'.format(zoom_out, cursor))
        cursor = np.array(cursor, dtype=np.float32)
        cursor_x, cursor_y = cursor
        prev_zoom = self.zoom
        img_0 = cursor - self.prev_cursor
        x0, y0 = img_0
        print("x0 {}, y0 {}".format(x0, y0))
        
        self.zoom += (zoom_out * self.zoom_normal * self.zoom_step)
        x1, y1 = img_0 * (self.zoom / prev_zoom)
        print("x1 {}, y1 {}".format(x1, y1))
        
        x, y = x0 - x1, y0 - y1
        print("x {}, y {}".format(x, y))
        print('zoom {}'.format(self.zoom / self.zoom_normal))
        # Size of the image in pixels (size of original image)
        # (This is not mandatory)
        self.move_image(x, y)

    def move_image(self, x, y):
        print('move_image x {}, y {}'.format(x, y))
        # Size of the image in pixels (size of original image)
        # (This is not mandatory)
        self.prev_cursor += (x, y)
        cursor_x, cursor_y = self.prev_cursor
        self.coords_fn(cursor_x, cursor_y)
        img_size = np.array(self.image_size * self.zoom, dtype=np.int32)
        print("W {}, H {}".format(*img_size))
        img = self.data.resize(img_size)

        self.show_data = ImageTk.PhotoImage(img)

    def get_image(self):
        return self.show_data

    def get_image_size(self):
        return self.data.size

    def get_image_size(self):
        return np.array(self.image_size * self.zoom, dtype=np.int32)

    def calc_coord_from_target(self, box):
        print('calc_coord_from_target (x0 {}, y0 {}, x1 {}, y1 {})'.format(*box))
        dW, dH = self.prev_cursor
        print('dW {}, dH {}'.format(dW, dH))
        (x0, y0, x1, y1) = np.array(box, dtype=np.float32) * self.get_zoom() 
        x0, x1 = x0 + dW, x1 + dW
        y0, y1 = y0 + dH, y1 + dH
        
        print('(x0 {}, y0 {}, x1 {}, y1 {})'.format(x0, y0, x1, y1))
        return (x0, y0, x1, y1)

    def calc_coord_to_target(self, box):
        print('calc_coord_to_target (x0 {}, y0 {}, x1 {}, y1 {})'.format(*box))
        dW, dH = self.prev_cursor
        print('dW {}, dH {}'.format(dW, dH))
        (x0, y0, x1, y1) = box
        x0, x1 = x0 - dW, x1 - dW
        y0, y1 = y0 - dH, y1 - dH
        
        box = np.array((x0, y0, x1, y1), dtype=np.float32) / self.get_zoom()
        print('return (x0 {}, y0 {}, x1 {}, y1 {})'.format(*box))
        return box

    def crop(self, box):
        print('crop (x0 {}, y0 {}, x1 {}, y1 {})'.format(*box))
        # Cropped image of above dimension
        # (It will not change original image)
        img = self.data.crop(box)
        
        self.image_size = np.array(img.size, dtype=np.float32)
        print("image_size W {}, H {}".format(*self.image_size))
        self.data = img
        self.__do_calc_zoom()
        self.prev_cursor = np.array((0, 0), dtype=np.float32)
        img_size = np.array(self.image_size * self.zoom, dtype=np.int32)
        
        cursor_x, cursor_y = self.get_start_cursor()
        self.coords_fn(cursor_x, cursor_y)
            
        self.show_data = ImageTk.PhotoImage(self.data.resize(img_size))

    def save(self, filename):
        self.data.save(filename)




    def set_img_show_fn(self, fn):
        self.img_show_fn = fn

    def set_move_fn(self, fn):
        self.move_fn = fn

    def set_coords_fn(self, fn):
        self.coords_fn = fn

    def set_edit_mode_fn(self, fn):
        self.edit_mode_fn = fn

    def set_rectangle_img_show_fn(self, fn):
        self.rectangle_img_show_fn = fn

    def img_show(self):
        self.img_show_fn(self.show_data)

    def rectangle_img_show(self, box, text):
        box = self.calc_coord_from_target(box)
        self.rectangle_img_show_fn(box, text)

    def edit_mode(self, box):
        box = self.calc_coord_from_target(box)
        self.edit_mode_fn(box)

    def set_EditFrame(self, editFrame):
        self.editFrame = editFrame