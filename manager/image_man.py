#!/usr/local/bin/python

import numpy as np
from pathlib import Path
from PIL import Image, ImageTk


class ImageManager :
    """
    y = numarul de linii
    x = nunarul de coloane
    data = imaginea
    """

    def __init__(self, frame=(600, 600)) :
        self.__editFrame  = None
        self.__show_data  = None
        self.__size       = None
        self.__size_frame = np.array(frame, dtype=np.float32)
        self.__size_standard = np.array(frame, dtype=np.float32)
        self.__zoom        = 1
        self.__zoom_normal = 1
        self.__zoom_step   = 0.05
        self.__zoom_man    = 1
        self.__prev_cursor = np.array((0, 0), dtype=np.float32)
        self.__data        = None
        self.__man_data    = None
        self.__pad_color   = (0, 0, 0)
        self.__dilatation  = (0, 0)
        self.__is_man      = False
        self.__is_image    = True

    def copy(self):
        imageMan = ImageManager(self.get_frame_size())
        imageMan.set_local_data(self.get_local_data())
        return imageMan

    def set_local_data(self, data: tuple):
        self.__editFrame, self.__zoom_step, self.__data = data

    def get_local_data(self):
        return self.__editFrame, self.__zoom_step, self.__data.copy()

    def set_pad_color(self, color: tuple):
        self.__pad_color = color

    def set_size_standard(self, size: tuple):
        self.__size_standard = np.array(size, dtype=np.float32)

    def set_dilatation(self, size: tuple):
        self.__dilatation = np.array(size, dtype=np.int32)

    def is_image(self):
        return self.__is_image

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

    def get_data(self) :
        return self.__data

    def get_man_data(self) :
        return self.__man_data

    def __fDoClcZoom(self, _size_frame) :
        fX, fY = _size_frame / self.__size
        print('do_calc_zoom size_frame {} WH format'.format(_size_frame))
        print('do_calc_zoom image_size {} WH format'.format(self.__size))
        print('do_calc_zoom zoom W {} H {}'.format(fX, fY))
        _zoom = 1.
        if ((fY >= 1) and (fX >= 1)) :
            if (fY < fX) :
                _zoom = fY
            else :
                _zoom = fX

        if ((fY < 1) or (fX < 1)) :
            if (fY < fX) :
                _zoom = fY
            else :
                _zoom = fX
        print('do_calc_zoom zoom {}'.format(_zoom))
        return _zoom

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

    def get_man_cursor(self) :
        img_size = np.array(self.__size * self.__zoom_man, dtype=np.int32)
        print("W {}, H {}".format(*img_size))
        img_width, img_height = img_size
        fr_width, fr_height = self.__size_standard
        cursor_x, cursor_y = (fr_width - img_width) / 2., (fr_height - img_height) / 2.
        cursor_x, cursor_y = int(cursor_x), int(cursor_y)
        print('cursor_x {}, cursor_y {}'.format(cursor_x, cursor_y))
        return cursor_x, cursor_y

    def __vDoTkinterImage(self, _data: 'pil_image', _size: tuple, _zoom: float):
        img_size = np.array(_size * _zoom, dtype=np.int32)
        print("W {}, H {}".format(*img_size))
        img = _data.resize(img_size, resample=None, box=None, reducing_gap=None)
        self.__show_data = ImageTk.PhotoImage(img)


    def read(self, filename: str, is_user=True) :
        try:
            self.__data = Image.open(filename).convert('RGB')
            self.__size = np.array(self.__data.size, dtype=np.float32)
            self.__is_image = True
        except:
            self.__is_image = False
            error = 'Filename @{}@ does not exist!'.format(filename)
            if (is_user == True):
                # filename does not exist
                messagebox.showerror("Error", f"An error occurred: {error}")
            else:
                print('---------ERROR-------\n---{}'.format(error))

    def vDoImageTK(self):
        print("image_size W {}, H {}".format(*self.__size))
        self.__zoom = self.__fDoClcZoom(self.__size_frame)
        self.__zoom_normal = self.__zoom

        cursor_x, cursor_y = self.get_start_cursor()
        self.__editFrame.coords(cursor_x, cursor_y)
        if (self.__is_man == True):
            print('MAN_DATA')
            _data = self.__man_data
        else:
            print('DATA')
            _data = self.__data
        self.__vDoTkinterImage(_data, self.__size, self.__zoom)

    def standardization(self, color: tuple) :
        self.__zoom_man = self.__fDoClcZoom(self.__size_standard)

        cursor_x, cursor_y = self.get_man_cursor()

        new_size    = np.array(self.__size * self.__zoom_man, dtype=np.int32)
        print("W {}, H {}".format(*new_size))

        fr_width, fr_height = self.__size_standard
        fr_width, fr_height = int(fr_width), int(fr_height)

        self.__man_data = Image.new(self.__data.mode, (fr_width, fr_height), color) 
        
        self.__man_data.paste(self.__data.resize(new_size), (cursor_x, cursor_y))
        print('standardization W {}, H {}'.format(*self.__man_data.size))



    def new(self, shape: tuple, color: tuple) :
        img = Image.new(mode='RGB', size=shape, color=color)
        return img

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
        self.__vDoTkinterImage(self.__data, self.__size, self.__zoom)

    def move(self, x: int, y: int) :
        self.__move_on_edit_frame(x, y)

    def transparency(self, alfa: tuple) :
        print('transparency mode  {}, pixel {}'.format(self.__data.mode, self.__data.getpixel((0, 0))))
        _data = np.asarray(self.__data, dtype=np.int8)
        print('original data shape {} {}, {}'.format(self.__data.size, _data.shape, _data[0][0]))
        _alfa = np.array(alfa, dtype=np.float32)
        print('alfa  {}'.format(_alfa))
        _data = np.array(_data * _alfa, dtype=np.int8)
        print('alfa data shape {}, {} {}'.format(_data.shape, _data[0][0], type(_data[0][0][0])))

        self.__man_data = Image.fromarray(_data, mode=self.__data.mode)
        print('size man_data {}, data {}'.format(self.__man_data.size, self.__data.size))

        self.__is_man      = True
        self.__vDoTkinterImage(self.__man_data, self.__size, self.__zoom)



    def calc_coord_from_target(self, box: tuple) :
        print('calc_coord_from_target (x0 {}, y0 {}, x1 {}, y1 {})'.format(*box))
        dW, dH = self.__prev_cursor
        print('dW {}, dH {}, zoom {}'.format(dW, dH, self.__zoom))
        (x0, y0, x1, y1) = np.array(box, dtype=np.float32) * self.__zoom
        x0, x1 = x0 + dW, x1 + dW
        y0, y1 = y0 + dH, y1 + dH

        print('(x0 {}, y0 {}, x1 {}, y1 {})'.format(x0, y0, x1, y1))
        return (x0, y0, x1, y1)

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

    def calc_man_coord_to_target(self, box: tuple) :
        print('calc_coord_to_target (x0 {}, y0 {}, x1 {}, y1 {})'.format(*box))
        dW, dH = self.get_man_cursor()
        print('dW {}, dH {}'.format(dW, dH))
        (x0, y0, x1, y1) = box
        x0, x1 = x0 - dW, x1 - dW
        y0, y1 = y0 - dH, y1 - dH

        box = np.array((x0, y0, x1, y1), dtype=np.float32) / self.__zoom_man
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
        self.__zoom = self.__fDoClcZoom(self.__size_frame)
        self.__zoom_normal = self.__zoom

        cursor_x, cursor_y = self.get_start_cursor()
        self.__editFrame.coords(cursor_x, cursor_y)
        self.__vDoTkinterImage(self.__data, self.__size, self.__zoom)

    def save(self, filename: str, is_man_data=False) :# is_man_data: bool
        if ((is_man_data == False) and (self.__data != None)):
            Path(filename).touch(mode=0o666, exist_ok=True)
            print('save image data size {}'.format(self.__data.size))
            self.__data.save(filename)
        elif((is_man_data == True) and (self.__man_data != None)):
            Path(filename).touch(mode=0o666, exist_ok=True)
            print('save image man data size {}'.format(self.__man_data.size))
            self.__man_data.save(filename)
        else:
            pass


    def set_EditFrame(self, editFrame: object) :
        self.__editFrame = editFrame
