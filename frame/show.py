#!/usr/bin/python

class ShowFrame :
    def __init__(self) :
        self.__editMan = None
        self.editFrame = None
        self.notebookFrame = None
        self.ratingFrame   = None
        self.selectFilenameFrame = None
        self.selectObjectFrame   = None
        self.descriptionFrame    = None
        self.__filename  = None
        self.__name      = None
        self.__item      = None
        self.__targetMan = None
        self.__imageMan  = None

        self.SHOW_NO        = -1
        self.SHOW_OBJECT    = 0
        self.SHOW_IMAGE     = 1
        self.SHOW_SET_TAB   = 2
        self.SHOW_FILENAMES = 3
        self.SHOW_SET_USER  = 4

        self.__show_option = self.SHOW_NO

    def __str__(self) :
        strRet = 'Labels:\n{}'.format(self.__targetMan)
        return strRet

    def set_data(self, imageMan: object, targetMan: object) :
        self.__imageMan  = imageMan
        self.__targetMan = targetMan

    def show(self) :
        if (self.__show_option == self.SHOW_NO):
            pass
        elif (self.__show_option == self.SHOW_OBJECT):
            print('SHOW_OBJECT')
            self.__editMan.show()
            self.selectObjectFrame.show()
            self.descriptionFrame.set_text_frame(self.__targetMan.get_last_name(), self.__targetMan.get_last_description())
            self.ratingFrame.set_rating(self.__targetMan.get_last_rating())
            pass
        elif (self.__show_option == self.SHOW_IMAGE):
            print('SHOW_IMAGE')
            self.__editMan.show()
            pass
        elif (self.__show_option == self.SHOW_SET_TAB) :
            print('SHOW_SET_TAB')
            self.__editMan.show()
            self.editFrame.set_work_frame(self.__filename)
            self.selectFilenameFrame.set_filename(self.__filename)
            self.selectObjectFrame.show()
            self.descriptionFrame.set_text_frame(self.__targetMan.get_last_name(), self.__targetMan.get_last_description())
            self.ratingFrame.set_rating(self.__targetMan.get_last_rating())
            pass
        elif (self.__show_option == self.SHOW_FILENAMES) :
            print('SHOW_FILENAMES')
            self.selectFilenameFrame.show()
            pass
        elif (self.__show_option == self.SHOW_SET_USER) :
            print('SHOW_SET_USER')
            self.selectObjectFrame.set_user_name(self.__pathMan.get_user_name())
            if (self.__filename != None):
                self.__editMan.show()
                self.selectObjectFrame.show()
                self.descriptionFrame.set_text_frame(self.__targetMan.get_last_name(), self.__targetMan.get_last_description())
                self.ratingFrame.set_rating(self.__targetMan.get_last_rating())
            pass
            pass

        self.__show_option = self.SHOW_NO

    def set_item(self, item: int) :
        self.__item = item

    def set_name(self, name: int) :
        self.__name = name

    def set_show_option(self, show_option: int) :
        self.__show_option = show_option

    def set_filename(self, filename: str) :
        self.__filename = filename



    def set_DescriptionFrame(self, obj: object) :
        self.descriptionFrame = obj

    def set_SelectObjectFrame(self, obj: object) :
        self.selectObjectFrame = obj

    def set_SelectFilenameFrame(self, obj: object) :
        self.selectFilenameFrame = obj

    def set_RatingFrame(self, obj: object) :
        self.ratingFrame = obj

    def set_EditManager(self, obj: object) :
        self.__editMan = obj

    def set_PathManager(self, obj: object) :
        self.__pathMan = obj

    def set_EditFrame(self, obj: object) :
        self.editFrame = obj

    def set_NotebookFrame(self, obj: object) :
        self.notebookFrame = obj
