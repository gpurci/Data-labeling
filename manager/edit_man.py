#!/usr/bin/python

from tkinter import messagebox


class EditManager :
    def __init__(self) :
        self.__pre_y1 = 0
        self.__pre_x1 = 0
        self.__y1 = 0
        self.__y0 = 0
        self.__x1 = 0
        self.__x0 = 0
        self.__box_edit = (0, 0, 0, 0)
        self.__box_name_edit = 'edit'

        self.__editFrame = None
        self.__showFrame = None
        self.__targetMan = None
        self.__imageMan  = None

        self.set_start_work_coords(0, 0)
        self.set_end_work_coords(0, 0)

        self.__mode_fn         = [self.__cmd_normal_mode,         self.__cmd_edit_mode,         self.__cmd_select_mode]
        self.__mode_release_fn = [self.__cmd_normal_mode_release, self.__cmd_edit_mode_release, self.__cmd_select_mode_release]

        self.NORMAL_MODE = 0
        self.EDIT_MODE   = 1
        self.SELECT_MODE = 2
        self.__work_mode = self.NORMAL_MODE

        self.POINT_00   = 0
        self.POINT_01   = 1
        self.POINT_10   = 2
        self.POINT_11   = 3
        self.ALL_POINTS = 4
        self.NOT_POINTS = 5
        self.__edit_point = self.NOT_POINTS

    def __str__(self) :
        str_ret = """
        EditManager : {}
        """.format('test')
        return str_ret

    def run_last_mode(self):
        self.__mode_fn[self.__work_mode]()

    def run_last_release_mode(self):
        self.__mode_release_fn[self.__work_mode]()

    def set_work_mode(self, work_mode:int):
        self.__work_mode = work_mode

    def __show_edit_mode(self, box:tuple, box_name:str):
        if (self.__targetMan.is_rectangle_mod() == True):
            box = self.__imageMan.calc_coord_from_target(box)
            self.__editFrame.rectangle(box, box_name)
            self.__editFrame.box_4_circle(box)
        elif (self.__targetMan.is_empty_mod() == True):
            self.__editFrame.delete_obj_from_frame()
        elif (self.__targetMan.is_all_mod() == True):
            pass
        else :  # 'do nothing'
            pass

    def __show_normal_mode(self, box:tuple, box_name:str):
        if (self.__targetMan.is_rectangle_mod() == True):
            box = self.__imageMan.calc_coord_from_target(box)
            self.__editFrame.rectangle(box, box_name)
        elif (self.__targetMan.is_empty_mod() == True):
            self.__editFrame.delete_obj_from_frame()
        elif (self.__targetMan.is_all_mod() == True):
            pass
        else :  # 'do nothing'
            pass

    def __set_show_edit_mode(self, box:tuple, box_name:str):
        self.__box_edit = box
        self.__box_name_edit = box_name
        if (self.__showFrame is not None):
            self.__showFrame.set_show_option(self.__showFrame.SHOW_EDIT_MAN)
        
    def show(self):
        img = self.__imageMan.get_image()
        self.__editFrame.img_show(img)
        box = self.__targetMan.get_last_coord()
        if (self.__work_mode == self.EDIT_MODE):
            self.__show_edit_mode(box, self.__targetMan.get_last_name())
        else :
            self.__show_normal_mode(box, self.__targetMan.get_last_name())

    def show_edit(self):
        img = self.__imageMan.get_image()
        self.__editFrame.img_show(img)
        if self.__work_mode == self.EDIT_MODE :
            self.__show_edit_mode(self.__box_edit, self.__box_name_edit)
        else :
            self.__show_normal_mode(self.__box_edit, self.__box_name_edit)

    def set_start_work_coords(self, x0:int, y0:int) :
        self.__x0, self.__y0 = x0, y0
        self.__x1, self.__y1 = x0, y0

    def set_end_work_coords(self, x1:int, y1:int) :
        self.__pre_x1, self.__pre_y1 = self.__x1, self.__y1
        self.__x1,     self.__y1     = x1, y1

    def __cmd_select_mode(self):
        self.__set_show_edit_mode((self.__x0, self.__y0, self.__x1, self.__y1), 'new')


    def __cmd_edit_mode(self) :
        if (self.__targetMan.is_rectangle_mod()):
            box = self.__targetMan.get_last_coord()
            box = self.__imageMan.calc_coord_from_target(box)
            x0, y0, x1, y1 = box
            print('__cmd_edit_mode box {}, type{}'.format(box, type(box)))
            d_x, d_y = self.__x1 - self.__x0, self.__y1 - self.__y0
            step_point = 5    #the tolerance in pixel point to select a peak of box
            if (self.__x0 > x0) and (self.__x0 < x1) and (self.__y0 > y0) and (self.__y0 < y1) :
                self.__edit_point = self.ALL_POINTS
                box = (x0 + d_x, y0 + d_y, x1 + d_x, y1 + d_y)
            elif ((self.__x0 >= (x0 - step_point)) and (self.__x0 <= (x0 + step_point)) and (
                    self.__y0 >= (y0 - step_point)) and (self.__y0 <= (y0 + step_point))) :
                self.__edit_point = self.POINT_00
                box = (x0 + d_x, y0 + d_y, x1, y1)
            elif ((self.__x0 >= (x1 - step_point)) and (self.__x0 <= (x1 + step_point)) and (
                    self.__y0 >= (y0 - step_point)) and (self.__y0 <= (y0 + step_point))) :
                self.__edit_point = self.POINT_01
                box = (x0, y0 + d_y, x1 + d_x, y1)
            elif ((self.__x0 >= (x0 - step_point)) and (self.__x0 <= (x0 + step_point)) and (
                    self.__y0 >= (y1 - step_point)) and (self.__y0 <= (y1 + step_point))) :
                self.__edit_point = self.POINT_10
                box = (x0 + d_x, y0, x1, y1 + d_y)
            elif ((self.__x0 >= (x1 - step_point)) and (self.__x0 <= (x1 + step_point)) and (
                    self.__y0 >= (y1 - step_point)) and (self.__y0 <= (y1 + step_point))) :
                self.__edit_point = self.POINT_11
                box = (x0, y0, x1 + d_x, y1 + d_y)
            else :
                self.__edit_point = self.NOT_POINTS
                pass

            self.__set_show_edit_mode(box, self.__targetMan.get_last_name())
        else :  # 'do nothing'
            pass

    def __cmd_normal_mode(self) :
        x, y = self.__x1 - self.__pre_x1, self.__y1 - self.__pre_y1
        self.__imageMan.move_image(x, y)
        if (self.__showFrame is not None):
            self.__showFrame.set_show_option(self.__showFrame.SHOW_IMAGE)

    def __cmd_select_mode_release(self) :
        self.__editFrame.add_object_frame()

    def __cmd_edit_mode_release(self) :
        d_x, d_y = self.__x1 - self.__x0, self.__y1 - self.__y0
        box = self.__targetMan.get_last_coord()
        box = self.__imageMan.calc_coord_from_target(box)
        x0, y0, x1, y1 = box
        if self.__edit_point == self.ALL_POINTS :
            box = (int(x0 + d_x), int(y0 + d_y), int(x1 + d_x), int(y1 + d_y))
        elif self.__edit_point == self.POINT_00 :
            box = (int(x0 + d_x), int(y0 + d_y), x1, y1)
        elif self.__edit_point == self.POINT_01 :
            box = (x0, int(y0 + d_y), int(x1 + d_x), y1)
        elif self.__edit_point == self.POINT_10 :
            box = (int(x0 + d_x), y0, x1, int(y1 + d_y))
        elif self.__edit_point == self.POINT_11 :
            box = (x0, y0, int(x1 + d_x), int(y1 + d_y))
        else :
            pass

        box = self.__imageMan.calc_coord_to_target(box)
        self.__targetMan.set_last_coord(box)

    def __cmd_normal_mode_release(self) :
        pass

    def add_object_name(self) :
        self.__editFrame.destroy_windows()
        object_name = self.__editFrame.get_object_name()
        print('object_name #{}#'.format(object_name))

        print('datasets {}'.format(self.__targetMan))

        box = (self.__x0, self.__y0, self.__x1, self.__y1)
        box = self.__imageMan.calc_coord_to_target(box)
        d_new_targets = {'names'       : object_name,
                         'description' : object_name,
                         'rating'      : 0,
                         'coord x0' : int(box[0]),
                         'coord y0' : int(box[1]),
                         'coord x1' : int(box[2]),
                         'coord y1' : int(box[3])}
        self.__targetMan.add_object(d_new_targets)
        print('datasets {}'.format(self.__targetMan))

    def mouse_wheel(self, event: object) :
        # respond to Linux or Windows wheel event
        # print('event {}'.format(event))
        if event.num == 5 :
            print(-1)
            self.__imageMan.zoom_image(-1, (event.x, event.y))
        if event.num == 4 :
            print(1)
            self.__imageMan.zoom_image(1, (event.x, event.y))

        if (self.__showFrame is not None):
            self.__showFrame.set_show_option(self.__showFrame.SHOW_IMAGE)

    def set_work_frame(self, filename:str) :
        self.__editFrame.set_work_frame(filename)

    def set_data(self, imageMan: object, targetMan: object) :
        self.__imageMan = imageMan
        self.__targetMan = targetMan

    def set_EditFrame(self, editFrame: object) :
        self.__editFrame = editFrame

    def set_ShowFrame(self, showFrame: object) :
        self.__showFrame = showFrame
