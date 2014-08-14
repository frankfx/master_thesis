'''
Created on Aug 5, 2014

@author: fran_re
'''
import sys
from lxml import etree
from PySide.QtGui import QMainWindow, QGridLayout, QWidget, QPushButton, QMenu, QFont, QTextEdit, qApp, QApplication
from PySide.QtCore import QFile
from cpacsPy.tixi import tixiwrapper
from xml.etree.ElementTree import ParseError

class Config():
    path_cpacs_schema = "CPACS_21_Schema.xsd"
    path_cpacs_file1  = "D150_CPACS2.0_valid.xml"
    path_cpacs_file2  = "Test_File.xml"
    path_cpacs_file3  = "A320_Fuse.xml"
    
    path_element1     = "/plane/wings/wing[1]"
    path_element2     = "/cpacs/vehicles/aircraft/model/fuselages/fuselage[1]"
    
    attrName1    = "position"
    attrName2    = "uID"
        

conf = Config()

class FileLoader():
    
    def __init__ (self):
        self.tixi = tixiwrapper.Tixi()
        self.elementPath = conf.path_element2
        self.attributeName = conf.attrName2
        
    def loadFile(self, xmlFilename, cpacs_schema):
        try:
            self.tixi.openDocument(xmlFilename) 
            self.tixi.schemaValidateFromFile(cpacs_schema)
        except tixiwrapper.TixiException, e:  
            print e.error
            raise e  
            
        attributeValue = self.tixi.getTextAttribute(self.elementPath, self.attributeName)
        version = self.tixi.getTextElement('/cpacs/header/version')
 
        print attributeValue
        print version 
 

class EditorWindow(QMainWindow):
    """initialize editor"""
    def __init__(self):
        super(EditorWindow, self).__init__()

        self.editor = QTextEdit()      
        config = Config()
        temp = FileLoader()  
        temp.loadFile(config.path_cpacs_file2, config.path_cpacs_schema)
        
        dir = temp.tixi.exportDocumentAsString()
        
        temp.tixi.close()
        
        self.editor.setText(dir)
        
        self.statusBar()
        self.setWindowTitle('Simple XML editor')
        self.setCentralWidget(self.editor)
        self.resize(800, 800)
 
def main():
    app = QApplication(sys.argv)
    w = EditorWindow()
    w.show()
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
