'''
Created on Aug 13, 2014

@author: fran_re
'''
'''
Created on Aug 5, 2014

@author: fran_re
'''
import sys
from PySide.QtGui import QTextDocument, QMainWindow, QTextEdit, QApplication
#from cpacsPy.tixi import tixiwrapper
import tixiwrapper
from config import Config
import re

class CPACS_Handler():
    
    def __init__ (self):
        self.tixi = tixiwrapper.Tixi()
        
    def loadFile(self, xmlFilename, cpacs_schema):
        try:
            self.tixi.openDocument(xmlFilename) 
            self.tixi.schemaValidateFromFile(cpacs_schema)
            
            return self.tixi.exportDocumentAsString()
        except tixiwrapper.TixiException, e:  
            raise e

    def getVectorX(self, prof_uid):
        xpath = self.tixi.uIDGetXPath(prof_uid)
        return self.tixi.getFloatVector(xpath + "/pointList/x",100)

    def getVectorY(self, prof_uid):
        xpath = self.tixi.uIDGetXPath(prof_uid)
        return self.tixi.getFloatVector(xpath + "/pointList/y",100)
    
    def getVectorZ(self, prof_uid):
        xpath = self.tixi.uIDGetXPath(prof_uid)
            
    def updatedictionary(self,path_dict, path_schema):
        dict_file = open(path_dict)
        schema_file = open(path_schema, 'r')
        flag = False
        res = ""
        with open(path_dict, "a") as mydict :
            for line in schema_file :
                res = re.search("(?<=\<xsd:complexType name=\").*(?=\"\>)", line)
                if res != None :
                    for tmp in dict_file : 
                        if tmp == res.group(0) +"\n" :
                            flag = True
                            break
                    if(not flag) :
                        mydict.write(res.group(0)+"\n")
            
        dict_file.close()
        mydict.close()
        schema_file.close()            
        
    def __del__(self):
        self.tixi.close()
        self.tixi.cleanup() 

class EditorWindow(QMainWindow):
    """initialize editor"""
    def __init__(self):
        super(EditorWindow, self).__init__()

        self.editor = QTextEdit()      
        config = Config()
        self.temp = CPACS_Handler()  
        self.temp.loadFile(config.path_cpacs_A320_Wing, config.path_cpacs_21_schema)
        
        directory = self.temp.tixi.exportDocumentAsString()
        #version = self.temp.tixi.getTextElement('/cpacs/vehicles/aircraft/model/name')
        #attributeValue = self.temp.tixi.getTextAttribute(config.path_element2, config.attrName2)
        
        self.temp.tixi.close()
        
        #print version
        #print attributeValue
        self.editor.setText(directory)
        
        self.statusBar()
        self.setWindowTitle('Simple XML editor')
        self.setCentralWidget(self.editor)
        self.resize(800, 800)

    def find(self, word) :
        self.editor.find(self.searchbox.text(), QTextDocument.FindBackward)      

    def search(self, xpath):
        print "test"

def main():
    app = QApplication(sys.argv)
    w = EditorWindow()
    w.show()
    w.temp.updatedictionary(Config.path_code_completion_dict, Config.path_cpacs_21_schema)
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
