'''
Created on Oct 8, 2014

@author: fran_re
'''

from tixiwrapper import Tixi, TixiException
from tiglwrapper import Tigl, TiglException
from Xtest.config import Config
from Xtest.Open_GL.airfoil.airfoilMainWidget import AirfoilMainWidget
from Xtest.Open_GL.fuselage.fuselageMainWidget import FuselageMainWidget
from Xtest.Open_GL.fuselage.fuselage import Fuselage
from Xtest.Open_GL.airfoil.airfoil import Airfoil
from PySide import QtGui

class MainWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        super(MainWidget, self).__init__(parent)

        self.tixi = Tixi()
        self.tigl = Tigl()

        self.loadFile(Config.path_cpacs_A320_Fuse, Config.path_cpacs_21_schema)

        buttonAirf = QtGui.QPushButton("airfoil")
        buttonFuse = QtGui.QPushButton("fuselage")

        grid = QtGui.QGridLayout()
        grid.addWidget(buttonAirf,0,0)
        grid.addWidget(buttonFuse, 0,1)

        self.setWindowTitle('Profile-Editor-Widget')    
        self.setLayout(grid)
        self.resize(560,520)

        # fuse or airfoil window
        self.window = None

        # actions
        buttonAirf.clicked.connect(self.getAirfoilMainWidget)
        buttonFuse.clicked.connect(self.getFuselageMainWidget)

      
    def loadFile(self, xmlFilename, cpacs_schema):
        try:
            self.tixi.openDocument(xmlFilename) 
            self.tixi.schemaValidateFromFile(cpacs_schema)
        except TixiException as e:  
            raise e

        try:
            self.tigl.open(self.tixi,"")
        except TiglException as err:    
            print ('Error opening tigl document: ', err.__str__() )  


    def getVectorX(self, prof_uid):
        xpath = self.tixi.uIDGetXPath(prof_uid)
        numX = self.tixi.getVectorSize(xpath + "/pointList/x")
        return self.tixi.getFloatVector(xpath + "/pointList/x",numX)

    def getVectorY(self, prof_uid):
        xpath = self.tixi.uIDGetXPath(prof_uid)
        numY = self.tixi.getVectorSize(xpath + "/pointList/y")
        return self.tixi.getFloatVector(xpath + "/pointList/y",numY)
    
    def getVectorZ(self, prof_uid):
        xpath = self.tixi.uIDGetXPath(prof_uid)
        numZ = self.tixi.getVectorSize(xpath + "/pointList/z")
        return self.tixi.getFloatVector(xpath + "/pointList/z",numZ)       
      
    '''
    @param: uid from cpacs
    @return: lists for top and bottom profile in format [ [x0,y0,z0] , [x1,y1,z1] , ...  ]
    '''       
    def __createPointList(self, uid) :
        vecX = self.getVectorX(uid)
        vecY = self.getVectorY(uid)
        vecZ = self.getVectorZ(uid)
        
        res = []
        for i in range(len(vecX)) :
            res.append([vecX[i], vecY[i], vecZ[i]])
        return res     

    def getAirfoilMainWidget(self, uid='NACA0000'):
        airfoil = Airfoil(uid, self.tigl, self.__createPointList(uid))
        self.window = AirfoilMainWidget(airfoil)

    def getFuselageMainWidget(self, uid='CircleProfile'):
        fuselage = Fuselage(uid, self.tigl, self.__createPointList(uid))
        self.window = FuselageMainWidget(fuselage)

if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = MainWidget()
    widget.show()
    app.exec_()    