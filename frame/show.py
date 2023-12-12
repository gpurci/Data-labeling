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
        self.SHOW_EDIT_MAN  = 4

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
        elif (self.__show_option == self.SHOW_IMAGE):
            print('SHOW_IMAGE')
            self.__editMan.show()
        elif (self.__show_option == self.SHOW_EDIT_MAN) :
            print('SHOW_EDIT_MAN')
            self.__editMan.show_edit()
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

        self.__show_option = self.SHOW_NO

    def set_item(self, item: int) :
        self.__item = item

    def set_name(self, name: int) :
        self.__name = name

    def set_show_option(self, show_option: int) :
        self.__show_option = show_option

    def set_filename(self, filename: str) :
        self.__filename = filename



    def set_DescriptionFrame(self, descriptionFrame: object) :
        self.descriptionFrame = descriptionFrame

    def set_SelectObjectFrame(self, selectObjectFrame: object) :
        self.selectObjectFrame = selectObjectFrame

    def set_SelectFilenameFrame(self, selectFilenameFrame: object) :
        self.selectFilenameFrame = selectFilenameFrame

    def set_RatingFrame(self, ratingFrame: object) :
        self.ratingFrame = ratingFrame

    def set_EditManager(self, editManager: object) :
        self.__editMan = editManager

    def set_EditFrame(self, editFrame: object) :
        self.editFrame = editFrame

    def set_NotebookFrame(self, notebookFrame: object) :
        self.notebookFrame = notebookFrame
