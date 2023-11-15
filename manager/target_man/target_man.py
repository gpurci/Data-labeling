#!/usr/bin/python

from pathlib import Path
import pandas as pd
import numpy as np

class TargetManager(object):
    def __init__(self, default_rating:int):
        self.__DEFAULT_OBJECT = 1
        self.__default_rating = default_rating
        self.__init()

    def __delete(self):
        del self.__df_targets
        
    def __str__(self):
        strRet = 'Labels:\n{}'.format(self.__df_targets)
        return strRet

    def is_rectangle_mod(self):
        return self.get_last_name() not in ['all_within', 'all_without']

    def is_empty_mod(self):
        return self.get_last_name() == 'all_without'

    def is_all_mod(self):
        return self.get_last_name() == 'all_within'

    def __init_last_name(self):
        self.update_last_name()

    def __init_selected_object(self):
        self.set_selected_object(self.__DEFAULT_OBJECT)

    def __init(self):
        df_new_targets = {
                                        'names':['all_within', 'all_without'],
                                        'description':['', ''], 
                                        'rating':[self.__default_rating, self.__default_rating], 
                                        'coord x0':[0, 0], 
                                        'coord x1':[-1, -1], 
                                        'coord y0':[0, 0], 
                                        'coord y1':[-1, -1]}
        print(' {}'.format('init'))
        self.__df_targets = pd.DataFrame( df_new_targets, 
                                          index=[0, 1])
        print('df_targets types {}'.format(self.__df_targets.dtypes))
        self.__init_selected_object()
        self.__init_last_name()

    def set_selected_object(self, item:int):
        if ((item >= 0) and (item < self.get_object_size())):
            self.__selected_object = item
        else:
            self.__selected_object = self.__DEFAULT_OBJECT

    def set_default_rating(self, rating:int):
        self.__default_rating = rating

    def set_description(self, key:int, text:str):
        self.__df_targets.at[key, 'description'] = text

    def set_rating(self, key:int, rating:int):
        self.__df_targets.at[key, 'rating']  = rating

    def set_coord(self, key:int, coord:tuple):
        x0, y0, x1, y1 = coord
        self.__df_targets.at[key, 'coord x0'] = int(x0)
        self.__df_targets.at[key, 'coord x1'] = int(x1)
        self.__df_targets.at[key, 'coord y0'] = int(y0)
        self.__df_targets.at[key, 'coord y1'] = int(y1)

    def update_last_name(self):
        self.__last_name = self.__df_targets['names'][self.__selected_object]

    def set_last_description(self, text:str):
        self.set_description(self.__selected_object, text)

    def set_last_rating(self, rating:int):
        self.set_rating(self.__selected_object, rating)

    def set_last_coord(self, coord:tuple):
        self.set_coord(self.__selected_object, coord)
    
    def set_size(self, x:int, y:int):
        self.__df_targets.at[self.__DEFAULT_OBJECT, 'coord x1'] = x
        self.__df_targets.at[self.__DEFAULT_OBJECT, 'coord y1'] = y

    def get_selected_object(self):
        return self.__selected_object

    def get_default_rating(self):
        return self.__default_rating 

    def get_last_name(self):
        return str(self.__last_name)

    def get_names(self):
        return list(self.__df_targets['names'])

    def get_default_object(self):
        return self.__DEFAULT_OBJECT

    def get_description(self, key:int):
        return str(self.__df_targets['description'][key])

    def get_rating(self, key:int):
        return int(self.__df_targets['rating'][key])

    def get_coord(self, key:int):
        x0 = self.__df_targets['coord x0'][key]
        x1 = self.__df_targets['coord x1'][key]
        y0 = self.__df_targets['coord y0'][key]
        y1 = self.__df_targets['coord y1'][key]
        return x0, y0, x1, y1

    def get_all_coords(self):
        x0 = self.__df_targets['coord x0']
        x1 = self.__df_targets['coord x1']
        y0 = self.__df_targets['coord y0']
        y1 = self.__df_targets['coord y1']
        return x0, y0, x1, y1

    def get_size(self):
        x = self.__df_targets['coord x1'][self.__DEFAULT_OBJECT]
        y = self.__df_targets['coord y1'][self.__DEFAULT_OBJECT]
        return (x, y)

    def get_object_size(self):
        return len(self.get_names())

    def get_last_description(self):
        return self.get_description(self.__selected_object)

    def get_last_rating(self):
        return self.get_rating(self.__selected_object)

    def get_last_coord(self):
        return self.get_coord(self.__selected_object)

    def get_last_object(self):
        return self.__df_targets.loc[self.__selected_object]

    def save_targets(self, filename:str):
        #save target data to csv file
        Path(filename).touch(mode=0o666, exist_ok=True)
        self.__df_targets.to_csv(filename, sep=',', index=False)

    def __cut(self, indexes:"array_int"):
        tolerance = np.arange(self.__DEFAULT_OBJECT+1)
        tolerance_index = np.argwhere(list(map(lambda t: t in indexes, tolerance))).reshape(-1)
        #print('tolerance_index', tolerance_index)
        invalid_idx = np.delete(arr=indexes, obj=tolerance_index)
        print('invalid_idx', invalid_idx)

        self.__df_targets.drop(index=invalid_idx, inplace=True)
        #print('index {}', self.__df_targets.index)
        self.__df_targets.index = np.arange(self.get_object_size())
        self.set_selected_object(self.__DEFAULT_OBJECT)

    def __get_invalid_obj_man(self, box:tuple):
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

    def __get_valid_obj_man(self, box:tuple):
        nbr_object = self.get_object_size()
        invalid_idx = self.__get_invalid_obj_man(box)
        valid_idx = np.array([i for i in range(nbr_object) if i not in invalid_idx])
        print('valid_idx', valid_idx)
        return valid_idx


    def read(self, filename:str):
        self.__df_targets = pd.read_csv(filename, 
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
        print('columns {}'.format(self.__df_targets.columns))

        self.__init_selected_object()
        self.__init_last_name()

    def cut_last_name(self):
        print('cut_last_name {}'.format(self.__df_targets))
        print('get_last_name {}, ittem {}, len {}'.format(self.get_last_name(), self.__selected_object, self.get_object_size()))
        if (self.__selected_object > self.__DEFAULT_OBJECT):
            self.__cut([self.__selected_object])
            self.set_selected_object(self.__DEFAULT_OBJECT)
        print('cut_last_name {}'.format(self.__df_targets))
        print('get_last_name {}, ittem {}, len {}'.format(self.get_last_name(), self.__selected_object, self.get_object_size()))
        self.showFrame.set_show_option(self.showFrame.SHOW_IMAGE)

    def crop_last_name(self):
        print('crop_last_name {} item {}'.format(self.get_last_name(), self.get_selected_object()))
        cx0, cy0, cx1, cy1 = self.get_last_coord()

        invalid_index = self.__get_invalid_obj_man((cx0, cy0, cx1, cy1))
        invalid_index = np.concatenate((invalid_index, [self.__selected_object]), axis=None)
        self.__cut(invalid_index)
        print('x0 {}, y0 {}, x1 {}, y1 {}'.format(cx0, cy0, cx1, cy1))
        self.set_size(cx1 - cx0, cy1 - cy0)
        print('size {}, object size {}'.format(self.get_size(), self.get_object_size()))
        for idx in range(self.__DEFAULT_OBJECT+1, self.get_object_size()):
            print(idx)
            x0, y0, x1, y1 = self.get_coord(idx)
            x0, x1 = x0 - cx0, x1 - cx0
            y0, y1 = y0 - cy0, y1 - cy0
            self.set_coord(idx, (x0, y0, x1, y1))
        print('crop_last_name end')
        self.set_selected_object(self.__DEFAULT_OBJECT)
        self.showFrame.set_show_option(self.showFrame.SHOW_IMAGE)

    def double_last_name(self):
        print('double_last_name {}'.format(self.__df_targets))
        print('get_last_name {}, ittem {}, len {}'.format(self.get_last_name(), self.__selected_object, self.get_object_size()))
        d_new_target = self.__df_targets.loc[self.__selected_object]
        print('double_last_name selected_object {}, data'.format(self.__selected_object, d_new_target))
        self.set_selected_object(self.get_object_size())
        
        self.__df_targets.loc[self.__selected_object] = d_new_target
        self.update_last_name()

        self.showFrame.set_target_object(self.get_last_object())
        self.showFrame.set_show_option(self.showFrame.SHOW_ALL)

    def new(self, x1:int, y1:int):
        self.__delete()
        self.__init()
        self.set_last_coord((0, 0, x1, y1))

    def add_object(self, d_new_target:dict):
        self.set_selected_object(self.get_object_size())
        self.__df_targets.loc[self.__selected_object] = d_new_target
        self.update_last_name()

        self.showFrame.set_target_object(self.get_last_object())
        self.showFrame.set_show_option(self.showFrame.SHOW_ALL)

    def set_last_object_name(self, name:str):
        self.__df_targets.at[self.__selected_object, 'names'] = name
        self.update_last_name()

        self.showFrame.set_target_object(self.get_last_object())
        self.showFrame.set_show_option(self.showFrame.SHOW_OBJECTS)

    def select_object(self, item:int):
        self.__save_description_frame()
        self.set_selected_object(item)
        self.update_last_name()
        
        self.showFrame.set_target_object(self.get_last_object())
        self.showFrame.set_show_option(self.showFrame.SHOW_ALL)


    def save(self, filename:str):
        self.__save_description_frame()
        #save target data to csv file
        self.save_targets(filename)

    def __save_description_frame(self):
        text_description = self.descriptionFrame.get_text_frame()
        self.set_last_description(text_description)


    def set_ShowFrame(self, showFrame:object):
        self.showFrame = showFrame


    def set_DescriptionFrame(self, descriptionFrame:object):
        self.descriptionFrame = descriptionFrame
