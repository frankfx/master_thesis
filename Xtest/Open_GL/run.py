'''
Created on Oct 8, 2014

@author: fran_re
'''

from cpacsHandler import CPACS_Handler
from Xtest.Open_GL.configuration.config import Config
from Xtest.Open_GL.airfoilMainWidget import AirfoilMainWidget
from Xtest.Open_GL.fuselageMainWidget import FuselageMainWidget
from fuselage import Fuselage
from airfoil import Airfoil
from PySide import QtGui

class profileMainWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        super(profileMainWidget, self).__init__(parent)
        
        # ==========================================================
        self.handler = CPACS_Handler()
        self.handler.loadFile(Config.path_cpacs_A320_Fuse, Config.path_cpacs_21_schema)
        # ==========================================================  

        butAirfoil = QtGui.QPushButton("airfoil")
        butFuselage = QtGui.QPushButton("fuselage")

        self.window = None

        butAirfoil.clicked.connect(self.getAirfoilMainWidget)
        butFuselage.clicked.connect(self.getFuselageMainWidget)

        grid = QtGui.QGridLayout()
        
        grid.addWidget(butAirfoil,0,0)
        grid.addWidget(butFuselage, 0,1)

        self.setLayout(grid)
        
        self.setWindowTitle('Profile-Widget')    
        self.resize(560,520)
        #self.setFixedSize(QtCore.QSize(400,400))
        self.show()        
        
    '''
    @param: uid from cpacs
    @return: lists for top and bottom profile in format [ [x0,y0,z0] , [x1,y1,z1] , ...  ]
    '''       
    def __createPointList(self, uid) :
        vecX = self.handler.getVectorX(uid)
        vecY = self.handler.getVectorY(uid)
        vecZ = self.handler.getVectorZ(uid)
        
        res = []
        for i in range(0, len(vecX)) :
            res.append([vecX[i], vecY[i], vecZ[i]])
        print res
        return res     

    def getAirfoilMainWidget(self, uid='NACA0009'):
        airfoil = Airfoil(uid, self.handler.getTigl(), self.__createPointList(uid))
        self.window = AirfoilMainWidget(airfoil)

    def getFuselageMainWidget(self, uid='CircleProfile'):
        fuselage = Fuselage(uid, self.handler.getTigl(), self.__createPointList(uid))
        self.window = FuselageMainWidget(fuselage)

if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = profileMainWidget()
    widget.show()
    app.exec_()    