'''
Created on Aug 6, 2014

@author: fran_re
'''
from PySide.QtGui import QLineEdit

class SearchField(QLineEdit):    
    def __init__(self, parent=None):
        super(SearchField, self).__init__()
        self.__focus = False
        
    def focusInEvent(self, focusevent):
        self.__focus = True

    def focusOutEvent(self, focusevent):
        self.__focus = False
        
    def isFocused(self):
        return self.__focus