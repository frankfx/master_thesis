'''
Created on Aug 5, 2014

@author: fran_re
'''
import sys
from PySide.QtGui import QTextDocument, QMainWindow, QTextEdit, QApplication
#from cpacsPy.tixi import tixiwrapper
#from cpacsPy.tigl import tiglwrapper
import tiglwrapper
import tixiwrapper
from config import Config
import re

class CPACS_Handler():
    
    def __init__ (self):
        self.tixi = tixiwrapper.Tixi()
        self.tigl = tiglwrapper.Tigl()
        
    def loadFile(self, xmlFilename, cpacs_schema):
        try:
            self.tixi.openDocument(xmlFilename) 
            self.tixi.schemaValidateFromFile(cpacs_schema)
            #print self.tixi._handle.value
            #self.tigl.openCPACSConfiguration(self.tixi._handle.value, "")
            
        except tixiwrapper.TixiException, e:  
            raise e

    def getVectorX(self, prof_uid):
        xpath = self.tixi.uIDGetXPath(prof_uid)
        return self.tixi.getFloatVector(xpath + "/pointList/x", 31)

    def getVectorY(self, prof_uid):
        xpath = self.tixi.uIDGetXPath(prof_uid)
        return self.tixi.getFloatVector(xpath + "/pointList/y",31)
    
    def getVectorZ(self, prof_uid):
        xpath = self.tixi.uIDGetXPath(prof_uid)
        return self.tixi.getFloatVector(xpath + "/pointList/z",31)    
            
    def updatedictionary(self,path_dict, path_schema):
        dict_file = open(path_dict)
        schema_file = open(path_schema, 'r')
        flag = False
        res = ''
        with open(path_dict, 'a') as mydict :
            for line in schema_file :
                res = re.search("(?<=\<xsd:complexType name=\").*(?=Type\"\>)", line)
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
    def __init__(self, cpacs_file, cpacs_schema):
        super(EditorWindow, self).__init__()

        self.editor = QTextEdit()      
        self.temp = CPACS_Handler()  
        self.temp.loadFile(cpacs_file, cpacs_schema)
        text = self.temp.tixi.exportDocumentAsString()
        
        xpath = self.temp.tixi.uIDGetXPath('NACA0009')
        print xpath
        #directory = self.temp.tixi.exportDocumentAsString()
        #version = self.temp.tixi.getTextElement('/cpacs/vehicles/aircraft/model/name')
        #attributeValue = self.temp.tixi.getTextAttribute(config.path_element2, config.attrName2)
        
        vecX = self.temp.tixi.getFloatVector(xpath + "/pointList/x",100)
        vecY = self.temp.tixi.getFloatVector(xpath + "/pointList/y",100)
        vecZ = self.temp.tixi.getFloatVector(xpath + "/pointList/z",100)
        print vecX
        print vecY
        print vecZ
        self.temp.tixi.close()
        
        #print version
        #print attributeValue
        self.editor.setText(text)
        
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
    w = EditorWindow(Config.path_cpacs_A320_Fuse, Config.path_cpacs_21_schema)
    w.show()
    w.temp.updatedictionary(Config.path_code_completion_dict, Config.path_cpacs_21_schema)
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
