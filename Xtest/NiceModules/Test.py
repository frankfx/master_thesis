'''
Created on Oct 9, 2014

@author: rene
'''
class Test:
    def __init__(self):
        self.__x = 3
        self._y = 2
        
class Bla:
    def __init__(self):
        t = Test()
        print t._y
        print t.__x
        
xx = Bla()
