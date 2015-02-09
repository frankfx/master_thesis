'''
Created on Oct 8, 2014

@author: fran_re
'''

import sys

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
        grid.addWidget(buttonAirf, 0,0)
        grid.addWidget(buttonFuse, 0,1)

        self.setWindowTitle('Profile-Editor-Widget')    
        self.setLayout(grid)
        self.resize(560,520)

        # fuse or airfoil window
        self.window = None

        # actions
        buttonAirf.clicked.connect(self.fire_AirfoilMainWidget)
        buttonFuse.clicked.connect(self.fire_FuselageMainWidget)
      
    def loadFile(self, filePath, cpacsSchema):
        """loads a cpacs file with tixi and tigl.  
        
        Args:
            filePath (String): path to cpacs file
            cpacsSchema (String): path to cpacs schema file
        """         
        try:
            print filePath
            self.tixi.openDocument(filePath) 
            self.tixi.schemaValidateFromFile(cpacsSchema)
            try:
                self.tigl.open(self.tixi,"")
            except TiglException as e:    
                QtGui.QMessageBox.information(self, "Error", "TIGL: " + str(e.error))
        except TixiException as e:  
            msgBox = QtGui.QMessageBox()
            msgBox.setText('open file or exit application')
            btnOpen = QtGui.QPushButton('open')
            msgBox.addButton(btnOpen, QtGui.QMessageBox.YesRole)
            btnExit = QtGui.QPushButton('exit')
            msgBox.addButton(btnExit, QtGui.QMessageBox.NoRole)
            
            if msgBox.exec_() == 0 :
                (filePath,_) = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
                self.loadFile(filePath, cpacsSchema)
            else:
                sys.exit()
            

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
      
    def createPointList(self, uID) :
        """creates a point list with profile points of given uID  
        
        Args:
            uID (String): uID from cpacs profile
        
        Returns:
            lists of top and bottom profile points in format [ [x0,y0,z0] , [x1,y1,z1] , ...  ]
        """          
        vecX = self.getVectorX(uID)
        vecY = self.getVectorY(uID)
        vecZ = self.getVectorZ(uID)
        
        res = []
        for i in range(len(vecX)) :
            res.append([vecX[i], vecY[i], vecZ[i]])
        return res     

    def fire_AirfoilMainWidget(self, uid='NACA0000'):
        self.window = AirfoilMainWidget( Airfoil(uid, self.tigl, self.createPointList(uid)) )

    def fire_FuselageMainWidget(self, uid='CircleProfile'):
        self.window = FuselageMainWidget( Fuselage(uid, self.tigl, self.createPointList(uid)) )

if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = MainWidget()
    widget.show()
    app.exec_()    