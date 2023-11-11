#!/usr/bin/python

from pathlib import Path
import pandas as pd
import numpy as np
import yaml

class TargetManager(object):
    def __init__(self, config_file):
        self.config_file = config_file
        self.DEFAULT_OBJECT = 1
        self.read_config_yaml_file(self.config_file)
        self.init()

    def read_config_yaml_file(self, config_file:str):
        if (Path(config_file).is_file() == True):
            with open(config_file) as file:
                config_list = yaml.load(file, Loader=yaml.FullLoader)
            self.default_rating = config_list['default_rating']
            print(config_list)
        else:
            self.default_rating = 0

    def delete(self):
        del self.df_targets
        
    def __str__(self):
        strRet = 'Labels:\n{}'.format(self.df_targets)
        return strRet

    def is_rectangle_mod(self):
        return self.get_last_name() not in ['all_within', 'all_without']

    def is_empty_mod(self):
        return self.get_last_name() == 'all_without'

    def is_all_mod(self):
        return self.get_last_name() == 'all_within'

    def init_last_name(self):
        self.update_last_name()

    def init_selected_object(self):
        self.set_selected_object(self.DEFAULT_OBJECT)

    def init(self):
        df_new_targets = {
                                        'names':['all_within', 'all_without'],
                                        'description':['', ''], 
                                        'rating':[self.default_rating, self.default_rating], 
                                        'coord x0':[0, 0], 
                                        'coord x1':[-1, -1], 
                                        'coord y0':[0, 0], 
                                        'coord y1':[-1, -1]}
        print(' {}'.format('init'))
        self.df_targets = pd.DataFrame( df_new_targets, 
                                        index=[0, 1])
        print('df_targets types {}'.format(self.df_targets.dtypes))
        self.init_selected_object()
        self.init_last_name()
        
    def set_selected_object(self, item:int):
        if (item < len(self.df_targets)):
            self.selected_object = item
        else:
            self.selected_object = self.DEFAULT_OBJECT

    def set_default_rating(self, rating:int):
        self.default_rating = rating

    def set_description(self, key:int, text:str):
        self.df_targets.at[key, 'description'] = text

    def set_rating(self, key:int, rating:int):
        self.df_targets.at[key, 'rating']  = rating

    def set_coord(self, key:int, coord:tuple):
        x0, y0, x1, y1 = coord
        self.df_targets.at[key, 'coord x0'] = int(x0)
        self.df_targets.at[key, 'coord x1'] = int(x1)
        self.df_targets.at[key, 'coord y0'] = int(y0)
        self.df_targets.at[key, 'coord y1'] = int(y1)

    def update_last_name(self):
        self.last_name = self.df_targets['names'][self.selected_object]

    def set_last_description(self, text:str):
        self.set_description(self.selected_object, text)

    def set_last_rating(self, rating:int):
        self.set_rating(self.selected_object, rating)

    def set_last_coord(self, coord:tuple):
        self.set_coord(self.selected_object, coord)
    
    def set_size(self, x:int, y:int):
        self.df_targets.at[self.DEFAULT_OBJECT, 'coord x1'] = x
        self.df_targets.at[self.DEFAULT_OBJECT, 'coord y1'] = y

    def get_selected_object(self):
        return self.selected_object

    def get_default_rating(self):
        return self.default_rating 

    def get_last_name(self):
        return str(self.last_name)

    def get_names(self):
        return list(self.df_targets['names'])

    def get_default_object(self):
        return self.DEFAULT_OBJECT

    def get_description(self, key:int):
        return str(self.df_targets['description'][key])

    def get_rating(self, key:int):
        return int(self.df_targets['rating'][key])

    def get_coord(self, key:int):
        x0 = self.df_targets['coord x0'][key]
        x1 = self.df_targets['coord x1'][key]
        y0 = self.df_targets['coord y0'][key]
        y1 = self.df_targets['coord y1'][key]
        return x0, y0, x1, y1

    def get_all_coords(self):
        x0 = self.df_targets['coord x0']
        x1 = self.df_targets['coord x1']
        y0 = self.df_targets['coord y0']
        y1 = self.df_targets['coord y1']
        return x0, y0, x1, y1

    def get_size(self):
        x = self.df_targets['coord x1'][self.DEFAULT_OBJECT]
        y = self.df_targets['coord y1'][self.DEFAULT_OBJECT]
        return (x, y)

    def get_last_description(self):
        return self.get_description(self.selected_object)

    def get_last_rating(self):
        return self.get_rating(self.selected_object)

    def get_last_coord(self):
        return self.get_coord(self.selected_object)


    def read(self, filename:str):
        self.df_targets = pd.read_csv(filename, 
                                        sep=',', 
                                        dtype={
                                            'names':       'str',
                                            'description': 'str',
                                            'rating':      'int',
                                            'coord x0':    'int',
                                            'coord x1':    'int',
                                            'coord y0':    'int',
                                            'coord y1':    'int'
                                            })
        print('columns {}'.format(self.df_targets.columns))

        self.init_selected_object()
        self.init_last_name()

    def save_targets(self, filename:str):
        #save target data to csv file
        Path(filename).touch(mode=0o666, exist_ok=True)
        self.df_targets.to_csv(filename, sep=',', index=False)

    def cut(self, indexes):
        tolerance = np.arange(self.DEFAULT_OBJECT+1)
        tolerance_index = np.argwhere(list(map(lambda t: t in indexes, tolerance))).reshape(-1)
        #print('tolerance_index', tolerance_index)
        invalid_idx = np.delete(arr=indexes, obj=tolerance_index)
        print('invalid_idx', invalid_idx)

        self.df_targets.drop(index=invalid_idx, inplace=True)
        #print('index {}', self.df_targets.index)
        self.df_targets.index = np.arange(len(self.df_targets))

    def cut_last_name(self):
        print('cut_last_name {}'.format(self.df_targets))
        print('get_last_name {}, ittem {}, len {}'.format(self.get_last_name(), self.selected_object, len(self.df_targets)))
        if (self.selected_object > self.DEFAULT_OBJECT):
            self.cut([self.selected_object])
            self.set_selected_object(self.DEFAULT_OBJECT)
        print('cut_last_name {}'.format(self.df_targets))
        print('get_last_name {}, ittem {}, len {}'.format(self.get_last_name(), self.selected_object, len(self.df_targets)))

    def crop_last_targets(self):
        print('crop_targets {} item {}'.format(self.get_last_name(), self.get_selected_object()))
        cx0, cy0, cx1, cy1 = self.get_last_coord()
        print('x0 {}, y0 {}, x1 {}, y1 {}'.format(cx0, cy0, cx1, cy1))
        self.set_size(cx1 - cx0, cy1 - cy0)
        print('size {}', self.get_size())

        invalid_index = self.get_invalid_obj_man((cx0, cy0, cx1, cy1))
        self.cut(invalid_index)
        for idx in range(self.DEFAULT_OBJECT+1, len(self.df_targets)):
            print(idx)
            x0, y0, x1, y1 = self.get_coord(idx)
            x0, x1 = x0 - cx0, x1 - cx0
            y0, y1 = y0 - cy0, y1 - cy0
            self.set_coord(idx, (x0, y0, x1, y1))


    def get_invalid_obj_man(self, box:tuple):
        x0, y0, x1, y1 = box
        l_x0, l_y0, l_x1, l_y1 = self.get_all_coords()

        idxs_not_valid_x0 = np.argwhere(list(map(lambda x: (x < x0) or (x > x1), l_x0))).reshape(-1)
        idxs_not_valid_x1 = np.argwhere(list(map(lambda x: (x < x0) or (x > x1), l_x1))).reshape(-1)
        idxs_not_valid_y0 = np.argwhere(list(map(lambda y: (y < y0) or (y > y1), l_y0))).reshape(-1)
        idxs_not_valid_y1 = np.argwhere(list(map(lambda y: (y < y0) or (y > y1), l_y1))).reshape(-1)

        tmp_idx = np.concatenate([  idxs_not_valid_x0, 
                                    idxs_not_valid_x1,
                                    idxs_not_valid_y0,
                                    idxs_not_valid_y1], 
                                  axis=0)
        invalid_idx = np.unique(tmp_idx)
        print('invalid_idx', invalid_idx)
        return invalid_idx

    def get_valid_obj_man(self, box:tuple):
        nbr_object = len(self.df_targets)
        invalid_idx = self.get_invalid_obj_man(box)
        valid_idx = np.array([i for i in range(nbr_object) if i not in invalid_idx])
        print('valid_idx', valid_idx)
        return 

    def new(self, x1:int, y1:int):
        self.delete()
        self.init()
        self.set_last_coord((0, 0, x1, y1))

    def new_import(self, x1:int, y1:int):
        self.new(x1, y1)

    def add_object(self, d_new_target:dict, idx:int):
        self.set_selected_object(idx)
        self.df_targets.loc[self.selected_object] = d_new_target
        self.update_last_name()

    def add_object_import(self, d_new_target:dict, idx:int):
        self.add_object(d_new_target, idx + self.DEFAULT_OBJECT + 1)

    def set_object_name_frame(self, name:str):
        self.df_targets.at[self.selected_object, 'names'] = name
        self.update_last_name()

        self.selectObjectFrame.update()
        
        shape_rectangle = self.get_last_coord()
        print('shape_rectangle {}, type{}'.format(shape_rectangle, type(shape_rectangle)))
        self.imageManager.rectangle_img_show(shape_rectangle, self.get_last_name())

    def new_frame(self, x1:int, y1:int):
        self.new(x1, y1)

        self.update_description_frame()
        self.selectObjectFrame.init()

    def add_object_frame(self, d_new_target:dict):
        d_new_target['rating'] = self.default_rating
        self.add_object(d_new_target, len(self.get_names()))
        
        self.selectObjectFrame.add(self.get_last_name(), len(self.get_names()))
        self.descriptionFrame.set_text_frame(self.get_last_name(), self.get_last_description())
        self.ratingFrame.set_rating_frame(self.get_last_rating())

    def select_object_frame(self, item:int):
        self.save_description()
        self.set_selected_object(item)
        self.update_last_name()
        
        self.descriptionFrame.set_text_frame(self.get_last_name(), self.get_last_description())
        self.ratingFrame.set_rating_frame(self.get_last_rating())
        self.editManager.show()

    def read_frame(self, filename:str):
        self.read(filename)

        self.update_description_frame()
        self.selectObjectFrame.init()

    def crop_targets_frame(self, index, box):
        print('crop_targets', index)
        self.df_targets = self.df_targets.iloc[index]
        print('crop_targets', self.df_targets)
        for idx in range(self.DEFAULT_OBJECT, len(self.df_targets)):
            print(idx)
            x0, y0, x1, y1 = self.get_coord(idx)
            x0, x1 = x0 - box[0], x1 - box[0]
            y0, y1 = y0 - box[1], y1 - box[1]
            self.set_coord(idx, (x0, y0, x1, y1))
        print('crop_targets', self.df_targets)

        self.update_description_frame()
        self.selectObjectFrame.init()

    def save(self, filename):
        self.save_description()
        #save target data to csv file
        self.save_targets(filename)
        #save default rating in yaml file
        names_yaml = """default_rating : {}""".format(self.get_default_rating())
        names = yaml.safe_load(names_yaml)

        with open(self.config_file, 'w') as file:
            yaml.dump(names, file)
        print('default_rating {}, read {}'.format(self.get_default_rating(), open(self.config_file).read()))

    def save_description(self):
        text_description = self.descriptionFrame.get_text_frame()
        self.set_last_description(text_description)

    def cut_last_name_frame(self):
        self.cut_last_name()
        self.selectObjectFrame.cut(self.selected_object)

    def double_last_name(self):
        print('double_last_name {}'.format(self.df_targets))
        print('get_last_name {}, ittem {}, len {}'.format(self.get_last_name(), self.selected_object, len(self.df_targets)))
        d_new_target = self.df_targets.loc[self.selected_object]
        print('double_last_name selected_object {}, data'.format(self.selected_object, d_new_target))
        self.set_selected_object(len(self.get_names()))
        
        self.df_targets.loc[self.selected_object] = d_new_target
        self.update_last_name()
        
        self.selectObjectFrame.add(self.last_name, self.selected_object)
        self.descriptionFrame.set_text_frame(self.get_last_name(), self.get_last_description())
        self.ratingFrame.set_rating_frame(self.get_last_rating())
        print('double_last_name {}'.format(self.df_targets))


    def update_description_frame(self):
        self.selectObjectFrame.update()
        self.descriptionFrame.set_text_frame(self.get_last_name(), self.get_last_description())
        self.ratingFrame.set_rating_frame(self.get_last_rating())

    def update_object_frame(self):
        self.selectObjectFrame.update()
        self.descriptionFrame.set_text_frame(self.get_last_name(), self.get_last_description())
        self.ratingFrame.set_rating_frame(self.get_last_rating())


    def set_DescriptionFrame(self, descriptionFrame):
        self.descriptionFrame = descriptionFrame

    def set_SelectObjectFrame(self, selectObjectFrame):
        self.selectObjectFrame = selectObjectFrame

    def set_RatingFrame(self, ratingFrame):
        self.ratingFrame = ratingFrame

    def set_ImageManager(self, imageManager):
        self.imageManager = imageManager

    def set_EditManager(self, editManager):
        self.editManager = editManager

    def set_EditFrame(self, editFrame):
        self.editFrame = editFrame