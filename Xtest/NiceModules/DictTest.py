'''
Created on Nov 3, 2014

@author: fran_re
'''
class ItemData(dict):
    def __init__(self, uID, nodeType, lib):
        self['uID'] = uID
        self['nodeType'] = nodeType
        self['lib'] = lib
    


bla = ItemData(123, "testnode", None)
print bla