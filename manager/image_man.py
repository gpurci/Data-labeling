#!/usr/local/bin/python

import numpy as np
from PIL import Image, ImageTk


class ImageManager :
    """
    y = numarul de linii
    x = nunarul de coloane
    data = imaginea
    """

    def __init__(self, frame=(600, 600)) :
        self.__editFrame = None
        self.__show_data = None
        self.__size = None
        self.__size_frame = np.array(frame, dtype=np.float32)
        self.__zoom = 1
        self.__zoom_normal = 1
        self.__zoom_step = 0.05
        self.__prev_cursor = np.array((0, 0), dtype=np.float32)
        self.__data = None

    def copy(self):
        imageMan = ImageManager(self.get_frame_size())
        imageMan.set_local_data(self.get_local_data())
        return imageMan

    def set_local_data(self, data: tuple):
        self.__editFrame, self.__zoom_step, self.__data = data

    def get_local_data(self):
        return self.__editFrame, self.__zoom_step, self.__data.copy()

    def __str__(self) :
        returnStr = "ImageManager"
        return returnStr

    def get_image(self) :
        cursor_x, cursor_y = self.__prev_cursor
        self.__editFrame.coords(cursor_x, cursor_y)
        return self.__show_data

    def get_zoom(self) :
        return self.__zoom

    def get_frame_size(self) :
        return self.__size_frame

    def get_size(self) :
        return self.__data.size

    def __do_calc_zoom(self) :
        fX, fY = self.__size_frame / self.__size
        print('do_calc_zoom size_frame {} WH format'.format(self.__size_frame))
        print('do_calc_zoom image_size {} WH format'.format(self.__size))
        print('do_calc_zoom zoom W {} H {}'.format(fX, fY))
        if fY >= 1 and fX >= 1 :
            if fY > fX :
                self.__zoom = fY
            else :
                self.__zoom = fX

        if fY < 1 or fX < 1 :
            if fY < fX :
                self.__zoom = fY
            else :
                self.__zoom = fX
        self.__zoom_normal = self.__zoom
        print('do_calc_zoom zoom {}'.format(self.__zoom))

    def get_start_cursor(self) :
        img_size = np.array(self.__size * self.__zoom, dtype=np.int32)
        print("W {}, H {}".format(*img_size))
        img_width, img_height = img_size
        fr_width, fr_height = self.__size_frame
        cursor_x, cursor_y = (fr_width - img_width) / 2., (fr_height - img_height) / 2.
        cursor_x, cursor_y = int(cursor_x), int(cursor_y)
        self.__prev_cursor = np.array((cursor_x, cursor_y), dtype=np.float32)
        print('cursor_x {}, cursor_y {}'.format(cursor_x, cursor_y))
        return cursor_x, cursor_y

    def __do_for_tkinter(self):
        img_size = np.array(self.__size * self.__zoom, dtype=np.int32)
        print("W {}, H {}".format(*img_size))
        img = self.__data.resize(img_size)
        self.__show_data = ImageTk.PhotoImage(img)


    def read(self, filename: str) :
        self.__data = Image.open(filename)
        self.__size = np.array(self.__data.size, dtype=np.float32)
        print("image_size W {}, H {}".format(*self.__size))
        self.__do_calc_zoom()

        cursor_x, cursor_y = self.get_start_cursor()
        self.__editFrame.coords(cursor_x, cursor_y)
        self.__do_for_tkinter()

    def do_RGB_image(self, shape: tuple, color: tuple) :
        #to do
        img = np.ones((10, 10, 3))  # d1d8e3
        img = Image.fromarray(img, mode='RGB')
        self.__show_data = ImageTk.PhotoImage(img)

    def __move_on_edit_frame(self, x: int, y: int) :
        print('__move_on_edit_frame x {}, y {}'.format(x, y))
        self.__prev_cursor += (x, y)
        cursor_x, cursor_y = self.__prev_cursor
        self.__editFrame.coords(cursor_x, cursor_y)

    def zoom(self, zoom_out: int, cursor: tuple) :
        # zoom_out is zoom in (-1) or zoom out (1)
        # cursor is the point from where do you do the zoom
        print('zoom zoom_out {}, cursor {}'.format(zoom_out, cursor))
        cursor = np.array(cursor, dtype=np.float32)
        cursor_x, cursor_y = cursor
        prev_zoom = self.__zoom
        img_0 = cursor - self.__prev_cursor
        x0, y0 = img_0
        print("x0 {}, y0 {}".format(x0, y0))

        self.__zoom += (zoom_out * self.__zoom_normal * self.__zoom_step)
        x1, y1 = img_0 * (self.__zoom / prev_zoom)
        print("x1 {}, y1 {}".format(x1, y1))

        x, y = x0 - x1, y0 - y1
        print("x {}, y {}".format(x, y))
        print('zoom {}'.format(self.__zoom / self.__zoom_normal))
        
        self.__move_on_edit_frame(x, y)
        self.__do_for_tkinter()

    def move(self, x: int, y: int) :
        self.__move_on_edit_frame(x, y)

    def calc_coord_from_target(self, box: tuple) :
        print('calc_coord_from_target (x0 {}, y0 {}, x1 {}, y1 {})'.format(*box))
        dW, dH = self.__prev_cursor
        print('dW {}, dH {}'.format(dW, dH))
        (x0, y0, x1, y1) = np.array(box, dtype=np.float32) * self.__zoom
        x0, x1 = x0 + dW, x1 + dW
        y0, y1 = y0 + dH, y1 + dH

        print('(x0 {}, y0 {}, x1 {}, y1 {})'.format(x0, y0, x1, y1))
        return x0, y0, x1, y1

    def calc_coord_to_target(self, box: tuple) :
        print('calc_coord_to_target (x0 {}, y0 {}, x1 {}, y1 {})'.format(*box))
        dW, dH = self.__prev_cursor
        print('dW {}, dH {}'.format(dW, dH))
        (x0, y0, x1, y1) = box
        x0, x1 = x0 - dW, x1 - dW
        y0, y1 = y0 - dH, y1 - dH

        box = np.array((x0, y0, x1, y1), dtype=np.float32) / self.__zoom
        print('return (x0 {}, y0 {}, x1 {}, y1 {})'.format(*box))
        return box

    def crop(self, box: tuple) :
        print('crop (x0 {}, y0 {}, x1 {}, y1 {})'.format(*box))
        # Cropped image of above dimension
        # (It will not change original image)
        img = self.__data.crop(box)

        self.__size = np.array(img.size, dtype=np.float32)
        print("image_size W {}, H {}".format(*self.__size))
        self.__data = img
        self.__do_calc_zoom()

        cursor_x, cursor_y = self.get_start_cursor()
        self.__editFrame.coords(cursor_x, cursor_y)
        self.__do_for_tkinter()

    def save(self, filename: str) :
        if (self.__data != None):
            self.__data.save(filename)

    def set_EditFrame(self, editFrame: object) :
        self.__editFrame = editFrame
