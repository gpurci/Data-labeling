#!/usr/bin/python

import re
import numpy as np
from pathlib import Path

from manager.image_man import *
from manager.target_man import *


class YoloV5Format(object) :
    def __init__(self, object_man: object, import_frame: object) :
        self.__objectMan = object_man
        self.__import_frame = import_frame

    def __call__(self):
        pass

    def import_frame(self) :
        self.__import_frame.set_import_fn(self.__import_fn)
        self.__import_frame()

    def __import_fn(self, _pathMan, _default_rating) :
        print('YoloV5Format import method {}'.format('START'))
        imageMan  = ImageManager(frame=(0, 0))
        targetMan = TargetManager(0)
        filenames = Path(_pathMan.get_source_path()).glob('*/images/*.*')
        all_object_names = get_object_names(source_path)
        print('all_object_names : {}'.format(all_object_names))
        # filenames = list(map(lambda s: str(s), filenames))
        for filename in filenames :
            print('filename {}'.format(filename))
            imageMan.read(filename, False)
            if (imageMan.is_image()):
                to_file_F = _pathMan.get_input_filename(str(filename.name))
                imageMan.save(to_file_F)
                width, height = imageMan.get_size()

                from_file_T = filename.with_suffix('.txt')
                from_file_T = rename_dir(from_file_T, 'images', 'labels')
                np_label, np_center_x, np_center_y, np_w, np_h = readLabelsYoloV5Format(from_file_T)
                coord = (np_center_x, np_center_y, np_w, np_h)
                object_names = all_object_names[np_label]
                yolo_v5_format_file_import(targetMan, object_names, coord, img.size)

                to_file_T = _pathMan.get_target_filename(str(filename.name))
                targetMan.save(to_file_T)

                print('filename {}'.format(filename))
                print('to file {}'.format(to_file_F))
                print('targetMan {}'.format(targetMan))

    def export_fn(self, _pathMan):
        pass



def rename_dir(path, src, dst) :
    # convert to list so that we can change elements
    parts = list(path.parts)

    # replace part that matches src with dst
    parts[parts.index(src)] = dst

    return Path(*parts)


# read a file Yolo v5 format and get array of labels, centers, width and height
def readLabelsYoloV5Format(filename: str) :
    # filename - a txt file yolo v5 format
    # can use pandas: pd.read_csv(filename, sep=' ', names=['label', 'center_x', 'center_y', 'w', 'h'])

    # pathern of Yolo v5 format
    reObjLabel = re.compile(r"(?P<label>\S+) (?P<center_x>\S+) (?P<center_y>\S+) (?P<w>\S+) (?P<h>\S+)")

    lst_label = []
    lst_center_x = []
    lst_center_y = []
    lst_w = []
    lst_h = []
    try :
        f = open(filename, "r")
        for line in f :
            # interpretation of yolo v5 format
            reLabel = reObjLabel.match(line)

            label = int(reLabel.group('label'))
            center_x = float(reLabel.group('center_x'))
            center_y = float(reLabel.group('center_y'))
            w = float(reLabel.group('w'))
            h = float(reLabel.group('h'))

            # add to list all class
            lst_label.append(label)
            lst_center_x.append(center_x)
            lst_center_y.append(center_y)
            lst_w.append(w)
            lst_h.append(h)
    except OSError as e :
        print(e.errno)
    finally :
        f.close()

    # cast list to numpy
    np_label = np.array(lst_label)
    np_center_x, np_center_y = np.array(lst_center_x), np.array(lst_center_y)
    np_w, np_h = np.array(lst_w), np.array(lst_h)

    # get
    # label - object class
    # center_x - percent of center of object X (width ) axis 
    # center_y - percent of center of object Y (height) axis 
    # w - percent of width  of located object
    # h - percent of height of located object
    # height - height of row image
    # width  - width  of row image
    return np_label, np_center_x, np_center_y, np_w, np_h


# write a file Yolo v5 format and put labels, centers, width and height
def writeLabelsYoloV5Format(filename: str, zip_elements) :
    # filename     - a txt file yolo v5 format
    # zip_elements - labels, centers, width and height
    # label - object class
    # center_x - percent of center of object X (width ) axis 
    # center_y - percent of center of object Y (height) axis 
    # w - percent of width  of located object
    # h - percent of height of located object
    # if use pandas: df.to_string(filename, index=False, header=False)
    try :
        f = open(filename, "w")
        for l, c_x, c_y, w, h in zip_elements :
            data = '{} {} {} {} {}\n'.format(l, c_x, c_y, w, h)
            f.write(data)
    except OSError as e :
        print(e.errno)
    finally :
        f.close()


# transform yolo v5 format to cartesian coordinate
def transformCenter2Cartesian(center_x, center_y, w, h, height, width) :
    # center_x - percent of center of object X (width ) axis
    # center_y - percent of center of object Y (height) axis
    # w - percent of width  of located object
    # h - percent of height of located object
    # height - height of row image
    # width  - width  of row image

    tmp_center_x = np.array(center_x * width)
    tmp_center_y = np.array(center_y * height)
    tmp_w = np.array(w * width)
    tmp_h = np.array(h * height)
    x0 = np.array((tmp_center_x - tmp_w / 2.), dtype=np.uint32)
    y0 = np.array((tmp_center_y - tmp_h / 2.), dtype=np.uint32)
    x1 = np.array((x0 + tmp_w), dtype=np.uint32)
    y1 = np.array((y0 + tmp_h), dtype=np.uint32)

    # get
    # x0, y0 - coordinate of leftmost X, topmost Y point of object
    # x1, y1 - coordinate of rightmost X, bottommost Y point of object
    return x0, y0, x1, y1


# transform cartesian coordinate to yolo v5 format
def transformCartesian2Center(x0, y0, x1, y1, height, width) :
    # x0, y0 - coordinate of leftmost X, topmost Y point of object
    # x1, y1 - coordinate of rightmost X, bottommost Y point of object
    # height - height of row image
    # width  - width  of row image

    # calculate width and height of object
    tmp_w = x1 - x0
    tmp_h = y1 - y0

    # calculate center of object
    tmp_center_x = x0 + tmp_w / 2.
    tmp_center_y = y0 + tmp_h / 2.

    # calculate percent of center of object
    center_x = tmp_center_x / width
    center_y = tmp_center_y / height

    # calculate percent of width and height of object
    w, h = tmp_w / width, tmp_h / height

    np_center_x, np_center_y = np.array(center_x), np.array(center_y)
    np_w, np_h = np.array(w), np.array(h)

    # get
    # center_x - percent of center of object X (width ) axis 
    # center_y - percent of center of object Y (height) axis 
    # w - percent of width  of located object
    # h - percent of height of located object
    return np_center_x, np_center_y, np_w, np_h


def yolo_v5_format_file_import(targets, object_names, coord, size):
    width, height = size
    np_center_x, np_center_y, np_w, np_h = coord
    targets.new(width, height)
    x0s, y0s, x1s, y1s = transformCenter2Cartesian(np_center_x, np_center_y, np_w, np_h, height, width)
    for obj_name, x0, y0, x1, y1 in zip(object_names, x0s, y0s, x1s, y1s) :
        d_new_targets = {'names'    :    obj_name,
                         'description' : obj_name,
                         'rating'   : targets.get_default_rating(),
                         'coord x0' : x0,
                         'coord x1' : x1,
                         'coord y0' : y0,
                         'coord y1' : y1}
        targets.add_object(d_new_targets)


def get_object_names(config_file: str) :
    _config_file = Path(config_file).joinpath('name').with_name('data.yaml')
    if (Path(_config_file).is_file()) :
        with open(_config_file) as file :
            _config_list = yaml.load(file, Loader=yaml.FullLoader)
        _object_names = _config_list['names']
        print(_config_list)
    else :
        _object_names = []
    return np.array(_object_names)
