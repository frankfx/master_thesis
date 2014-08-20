'''
Created on Aug 6, 2014

@author: fran_re
'''
from PySide.QtGui import QLineEdit

class SearchField(QLineEdit):    
    '''This is a docstring'''
    def __init__(self):
        super(SearchField, self).__init__()
        self.__focus = False
        
    def focusInEvent(self, focusevent):
        self.__focus = True
        super(SearchField, self).focusInEvent(focusevent)

    def focusOutEvent(self, focusevent):
        self.__focus = False
        super(SearchField, self).focusInEvent(focusevent)

    def isFocused(self):
        '''returns true if focus is on text field'''
        return self.__focus