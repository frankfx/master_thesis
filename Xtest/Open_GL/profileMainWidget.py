'''
Created on Oct 8, 2014

@author: fran_re
'''

from cpacsHandler import CPACS_Handler
from Xtest.Open_GL.configuration.config import Config
from Xtest.Open_GL.airfoilMainWidget import AirfoilMainWidget
from Xtest.Open_GL.fuselageMainWidget import FuselageMainWidget
from PySide import QtGui

class profileMainWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        super(profileMainWidget, self).__init__(parent)
        
        # ==========================================================
        self.tixi = CPACS_Handler()
        self.tixi.loadFile(Config.path_cpacs_A320_Fuse, Config.path_cpacs_21_schema)
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
        vecX = self.tixi.getVectorX(uid)
        vecY = self.tixi.getVectorY(uid)
        vecZ = self.tixi.getVectorZ(uid)
        
        res = []
        for i in range(0, len(vecX)) :
            res.append([vecX[i], vecZ[i], vecY[i]])
        return res     

    def getAirfoilMainWidget(self, uid='NACA0009'):
        self.window = AirfoilMainWidget(self.__createPointList(uid))

    def getFuselageMainWidget(self, uid='CircleProfile'):
        self.window = FuselageMainWidget(self.__createPointList(uid))

    

if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = profileMainWidget()
    widget.show()
    app.exec_()    