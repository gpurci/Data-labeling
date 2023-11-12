#!/usr/bin/python

from pathlib import Path

class OpenFilenameManager(object):
    def __init__(self, datasets):
        self.datasets = datasets

    def save(self):
        if (self.pathManager.get_file_suffix() != None):
            self.selectFilenameFrame.save_frame()
        
        if (self.pathManager.get_filename() != None):
            dest_file = self.pathManager.get_dest_filename()
            Path(dest_file).parent.mkdir(parents=True, exist_ok=True)
            print('dest_file {}'.format(dest_file))
            self.datasets.save_frame(dest_file)
            row_filename = self.pathManager.get_row_filename()
            if (Path(row_filename).is_file() == False):
                self.imageManager.save(row_filename)
            print('datasets {}'.format(self.datasets))

    def open(self, filename):
        print("Selected file: {}".format(filename))
        self.pathManager.set_filename(filename)
        self.editManager.set_work_frame(filename)
        
        dest_file      = self.pathManager.get_dest_filename()
        if (Path(dest_file).is_file() == True):
            print('True  -> dest_file {}'.format(dest_file))
            self.datasets.read_frame(dest_file)
        else:
            print('False -> dest_file {}'.format(dest_file))
            self.datasets.new_frame()
        print('datasets {}'.format(self.datasets))
        source_file = self.pathManager.get_source_filename()
        self.imageManager.read(source_file)
        self.editManager.show()



    def set_SelectFilenameFrame(self, selectFilenameFrame):
        self.selectFilenameFrame = selectFilenameFrame

    def set_ImageManager(self, imageManager):
        self.imageManager = imageManager

    def set_PathManager(self, pathManager):
        self.pathManager = pathManager

    def set_EditManager(self, editManager):
        self.editManager = editManager
