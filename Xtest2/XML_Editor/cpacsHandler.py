'''
Created on Aug 13, 2014

@author: fran_re
'''
'''
Created on Aug 5, 2014

@author: fran_re
'''
import sys
from lxml import etree
from PySide.QtGui import QTextDocument, QMainWindow, QGridLayout, QWidget, QPushButton, QMenu, QFont, QTextEdit, qApp, QApplication
from PySide.QtCore import QFile
from cpacsPy.tixi import tixiwrapper
from xml.etree.ElementTree import ParseError
from config import Config
import re

class CPACS_Handler():
    
    def __init__ (self):
        self.tixi = tixiwrapper.Tixi()
     #   self.elementPath = conf.path_element2
      #  self.attributeName = conf.attrName2
        
    def loadFile(self, xmlFilename, cpacs_schema):
        try:
            self.tixi.openDocument(xmlFilename) 
            self.tixi.schemaValidateFromFile(cpacs_schema)
 #       print attributeValue
            #version = self.tixi.getTextElement('/cpacs/header/version')
            version = self.tixi.getTextElement('/cpacs/vehicles/aircraft/model/name')
            
            print "dsfdsf"
            print version             
            return self.tixi.exportDocumentAsString()
        except tixiwrapper.TixiException, e:  
          #  print e.error
           ()
           raise e
            
            
        
            
 #       attributeValue = self.tixi.getTextAttribute(self.elementPath, self.attributeName)
        version = self.tixi.getTextElement('/cpacs/header/version')
 
 #       print attributeValue
        print "dsfdsf"
        print version 

    def __del__(self):
        self.tixi.close()
        self.tixi.cleanup() 

class EditorWindow(QMainWindow):
    """initialize editor"""
    def __init__(self):
        super(EditorWindow, self).__init__()

        self.editor = QTextEdit()      
        config = Config()
        temp = CPACS_Handler()  
        temp.loadFile(config.path_cpacs_A380_Fuse, config.path_cpacs_21_schema)
        
        dir = temp.tixi.exportDocumentAsString()
        
        temp.tixi.close()
        
        self.editor.setText(dir)
        
        self.statusBar()
        self.setWindowTitle('Simple XML editor')
        self.setCentralWidget(self.editor)
        self.resize(800, 800)

    def find(self, word) :
        self.editor.find(self.searchbox.text(), QTextDocument.FindBackward)      

    def search(self, xpath):
        print "test"
 
    def updatedictionary(self,path_dict, path_schema):
        dict_file = open(path_dict)
        schema_file = open(path_schema, 'r')
        flag = False
        res = ""
        with open(path_dict, "a") as dict :
            for line in schema_file :
                res = re.search("(?<=\<xsd:complexType name=\").*(?=\"\>)", line)
                if res != None :
                    for tmp in dict_file : 
                        if tmp == res.group(0) +"\n" :
                            flag = True
                            break
                    if(not flag) :
                        #print res.group(0)
                        dict.write(res.group(0)+"\n")
            
        dict_file.close()
        dict.close()
        schema_file.close()
 
def main():
    app = QApplication(sys.argv)
    w = EditorWindow()
    w.show()
    w.updatedictionary(Config.path_code_completion_dict, Config.path_cpacs_21_schema)
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
