# -*- coding: utf-8 -*-

import re

from PIL import Image

from manager.path_man import *
from manager.target_man import *


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


def yolo_v5_format_import_fn(source_path, dest_path, targets, path_man) :
    filenames = Path(source_path).glob('*/images/*.*')
    # dest_path = Path(dest_path)
    row_file_path = Path(path_man.get_row_path())
    target_file_path = Path(path_man.get_target_path())
    print('row_file_path {}/ntarget_file_path {}'.format(row_file_path, target_file_path))
    row_file_path.mkdir(parents=True, exist_ok=True)
    target_file_path.mkdir(parents=True, exist_ok=True)
    object_names = get_object_names(source_path)
    print('object_names : {}'.format(object_names))
    # filenames = list(map(lambda s: str(s), filenames))
    for filename in filenames :
        to_file_F = row_file_path.joinpath('name').with_name(filename.name)
        # shutil.copy(str(filename), str(to_file))
        # to_file.parent.mkdir(parents=True, exist_ok=True)
        # to_file_F.touch(mode=0o666, exist_ok=True)
        to_file_F.write_bytes(filename.read_bytes())
        from_file_T = filename.with_suffix('.txt')
        from_file_T = rename_dir(from_file_T, 'images', 'labels')
        np_label, np_center_x, np_center_y, np_w, np_h = readLabelsYoloV5Format(from_file_T)
        img = Image.open(str(filename))
        width, height = img.size
        targets.new(height, width)
        del img
        x0s, y0s, x1s, y1s = transformCenter2Cartesian(np_center_x, np_center_y, np_w, np_h, height, width)
        for label, x0, y0, x1, y1 in zip(np_label, x0s, y0s, x1s, y1s) :
            d_new_targets = {'names' : object_names[label],
                             'description' : object_names[label],
                             'rating' : targets.get_default_rating(),
                             'coord x0' : x0,
                             'coord x1' : x1,
                             'coord y0' : y0,
                             'coord y1' : y1}
            targets.add_object(d_new_targets)
            print('targets {}'.format(targets.get_object_size()))
        to_file_T = path_man.get_target_filename(str(filename.name))
        targets.save(to_file_T)

        print('filename {}'.format(filename))
        print('to file {}'.format(to_file_F))
        print('targets {}'.format(targets))
    # print('import_fn {}'.format(filenames))


def get_object_names(config_file) :
    config_file = Path(config_file).joinpath('name').with_name('data.yaml')
    if Path(config_file).is_file() :
        with open(config_file) as file :
            config_list = yaml.load(file, Loader=yaml.FullLoader)
        object_names = config_list['names']
        print(config_list)
    else :
        object_names = []
    return object_names
