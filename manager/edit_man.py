#!/usr/bin/python

from tkinter import messagebox


class EditManager :
    def __init__(self) :
        self.pre_y1 = None
        self.pre_x1 = None
        self.y1 = None
        self.y0 = None
        self.edit_point = None
        self.editFrame = None
        self.targetMan = None
        self.imageMan = None
        self.x1 = None
        self.x0 = None
        self.work_mode = 0

        self.set_start_work_coords(0, 0)
        self.set_end_work_coords(0, 0)

        self.mode_fn = [self.object_normal, self.object_edit, self.object_select]
        self.mode_release_fn = [self.object_normal_release, self.object_edit_release, self.object_select_release]

        self.NORMAL_MODE = 0
        self.EDIT_MODE = 1
        self.SELECT_MODE = 2

        self.POINT_00 = 0
        self.POINT_01 = 1
        self.POINT_10 = 2
        self.POINT_11 = 3
        self.ALL_POINTS = 4
        self.NOT_POINTS = 5

    def __str__(self) :
        str_ret = """
        EditManager : {}
        """.format('test')
        return str_ret

    def run_last_mode(self) :
        self.mode_fn[self.work_mode]()

    def run_last_release_mode(self) :
        self.mode_release_fn[self.work_mode]()

    def set_work_mode(self, work_mode) :
        self.work_mode = work_mode

    def show_edit_mode(self) :
        image = self.imageMan
        self.imageMan.img_show()
        if self.targetMan.is_rectangle_mod() :
            shape_rectangle = self.targetMan.get_last_coord()
            print('object_edit shape_rectangle {}, type{}'.format(shape_rectangle, type(shape_rectangle)))
            self.imageMan.edit_mode(shape_rectangle)
            self.imageMan.rectangle_img_show(shape_rectangle, self.targetMan.get_last_name())
        elif self.targetMan.is_empty_mod() :
            self.editFrame.delete_edit_mode()
            self.editFrame.delete_selected_box()
        elif self.targetMan.is_all_mod() :
            pass
        else :  # 'do nothing'
            pass

    def show_normal_mode(self) :
        if self.targetMan.is_rectangle_mod() :
            shape_rectangle = self.targetMan.get_last_coord()
            print('object_edit shape_rectangle {}, type{}'.format(shape_rectangle, type(shape_rectangle)))
            self.imageMan.rectangle_img_show(shape_rectangle, self.targetMan.get_last_name())
        elif self.targetMan.is_empty_mod() :
            self.editFrame.delete_edit_mode()
            self.editFrame.delete_selected_box()
        elif self.targetMan.is_all_mod() :
            pass
        else :  # 'do nothing'
            pass

    def show(self) :
        if self.work_mode == self.EDIT_MODE :
            self.show_edit_mode()
        else :
            self.show_normal_mode()

    def set_start_work_coords(self, x0, y0) :
        self.x0, self.y0 = x0, y0
        self.x1, self.y1 = x0, y0

    def set_end_work_coords(self, x1, y1) :
        self.pre_x1, self.pre_y1 = self.x1, self.y1
        self.x1, self.y1 = x1, y1

    def object_select(self) :
        shape_rectangle = self.imageMan.calc_coord_to_target((self.x0, self.y0, self.x1, self.y1))
        self.imageMan.rectangle_img_show(shape_rectangle, 'new')

    def object_edit(self) :
        if self.targetMan.is_rectangle_mod() :
            shape_rectangle = self.targetMan.get_last_coord()
            shape_rectangle = self.imageMan.calc_coord_from_target(shape_rectangle)
            x0, y0, x1, y1 = shape_rectangle
            print('object_edit shape_rectangle {}, type{}'.format(shape_rectangle, type(shape_rectangle)))
            d_x, d_y = self.x1 - self.x0, self.y1 - self.y0
            step_point = 5
            if (self.x0 > x0) and (self.x0 < x1) and (self.y0 > y0) and (self.y0 < y1) :
                self.edit_point = self.ALL_POINTS
                shape_rectangle = (x0 + d_x, y0 + d_y, x1 + d_x, y1 + d_y)
            elif ((self.x0 >= (x0 - step_point)) and (self.x0 <= (x0 + step_point)) and (
                    self.y0 >= (y0 - step_point)) and (self.y0 <= (y0 + step_point))) :
                self.edit_point = self.POINT_00
                shape_rectangle = (x0 + d_x, y0 + d_y, x1, y1)
            elif ((self.x0 >= (x1 - step_point)) and (self.x0 <= (x1 + step_point)) and (
                    self.y0 >= (y0 - step_point)) and (self.y0 <= (y0 + step_point))) :
                self.edit_point = self.POINT_01
                shape_rectangle = (x0, y0 + d_y, x1 + d_x, y1)
            elif ((self.x0 >= (x0 - step_point)) and (self.x0 <= (x0 + step_point)) and (
                    self.y0 >= (y1 - step_point)) and (self.y0 <= (y1 + step_point))) :
                self.edit_point = self.POINT_10
                shape_rectangle = (x0 + d_x, y0, x1, y1 + d_y)
            elif ((self.x0 >= (x1 - step_point)) and (self.x0 <= (x1 + step_point)) and (
                    self.y0 >= (y1 - step_point)) and (self.y0 <= (y1 + step_point))) :
                self.edit_point = self.POINT_11
                shape_rectangle = (x0, y0, x1 + d_x, y1 + d_y)
            else :
                self.edit_point = self.NOT_POINTS
                pass
            shape_rectangle = self.imageMan.calc_coord_to_target(shape_rectangle)
            print('object_edit shape_rectangle {}, type{}'.format(shape_rectangle, type(shape_rectangle)))
            self.imageMan.edit_mode(shape_rectangle)
            self.imageMan.rectangle_img_show(shape_rectangle, self.targetMan.get_last_name())
        else :  # 'do nothing'
            pass

    def object_normal(self) :
        x, y = self.x1 - self.pre_x1, self.y1 - self.pre_y1
        self.imageMan.move_image(x, y)
        self.show_normal_mode()

    def object_select_release(self) :
        self.editFrame.select_object_frame()

    def object_edit_release(self) :
        d_x, d_y = self.x1 - self.x0, self.y1 - self.y0
        shape_rectangle = self.targetMan.get_last_coord()
        shape_rectangle = self.imageMan.calc_coord_from_target(shape_rectangle)
        x0, y0, x1, y1 = shape_rectangle
        if self.edit_point == self.ALL_POINTS :
            shape_rectangle = (int(x0 + d_x), int(y0 + d_y), int(x1 + d_x), int(y1 + d_y))
        elif self.edit_point == self.POINT_00 :
            shape_rectangle = (int(x0 + d_x), int(y0 + d_y), x1, y1)
        elif self.edit_point == self.POINT_01 :
            shape_rectangle = (x0, int(y0 + d_y), int(x1 + d_x), y1)
        elif self.edit_point == self.POINT_10 :
            shape_rectangle = (int(x0 + d_x), y0, x1, int(y1 + d_y))
        elif self.edit_point == self.POINT_11 :
            shape_rectangle = (x0, y0, int(x1 + d_x), int(y1 + d_y))
        else :
            pass

        shape_rectangle = self.imageMan.calc_coord_to_target(shape_rectangle)
        self.targetMan.set_last_coord(shape_rectangle)

    def object_normal_release(self) :
        pass

    def add_object_name(self) :
        self.editFrame.destroy_select_object_frame()
        object_name = self.editFrame.get_object_name()
        print('object_name #{}#'.format(object_name))

        print('datasets {}'.format(self.targetMan))

        shape_rectangle = self.imageMan.calc_coord_to_target((self.x0, self.y0, self.x1, self.y1))
        d_new_targets = {'names' : object_name,
                         'description' : object_name,
                         'rating' : 0,
                         'coord x0' : int(shape_rectangle[0]),
                         'coord y0' : int(shape_rectangle[1]),
                         'coord x1' : int(shape_rectangle[2]),
                         'coord y1' : int(shape_rectangle[3])}
        self.targetMan.add_object(d_new_targets)
        print('datasets {}'.format(self.targetMan))

    def mouse_wheel(self, event) :
        # respond to Linux or Windows wheel event
        # print('event {}'.format(event))
        if event.num == 5 :
            print(-1)
            self.imageMan.zoom_image(-1, (event.x, event.y))
        if event.num == 4 :
            print(1)
            self.imageMan.zoom_image(1, (event.x, event.y))

        self.show()
        self.editFrame.plus()

    def set_work_frame(self, filename) :
        self.editFrame.set_work_frame(filename)

    def set_data(self, imageMan, targetMan) :
        self.imageMan = imageMan
        self.targetMan = targetMan

    def set_EditFrame(self, editFrame) :
        self.editFrame = editFrame
