'''
Created on Jul 30, 2014

@author: fran_re
'''

import sys

from tiglwrapper import Tigl, TiglException
from tixiwrapper import Tixi, TixiException
from numpy import array
from PySide import QtOpenGL, QtGui, QtCore
from Xtest.Open_GL import utility

try:
    from OpenGL import GL, GLU
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

class Renderer():
    def __init__(self, width, height):

        self.tixi = Tixi()
        self.tixi.open('simpletest.cpacs.xml')
        
        self.tigl = Tigl()
        try:
            self.tigl.open(self.tixi,"")
        except TiglException as err:    
            print 'Error opening tigl document: ', err.__str__()
            
        self.up_List, self.lo_List = self.createWing()

        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0   
        self.scale = 1.0 
        self.aspect= 1.0  

        #print self.get_modelUIDs()
        #print self.get_allFuselageProfileUIDs()
        
## Jonas - tixiExtension
## ============================================================================================        
  
    def xPathGetAllElements(self, XPath):
            if not self.tixi.checkElement(XPath):
                return []
            try:
                numElem = self.tixi.xPathEvaluateNodeNumber(XPath)
            except TixiException:
                return []
            return [self.tixi.xPathExpressionGetTextByIndex(XPath, i) for i in range(1, numElem + 1)]  

## ===========================================================================================         
  
## Jonas - cpacsPy/Basic/Selector
## ============================================================================================    
    def get_modelUIDs(self):
        '''
        Returns all model UIDs inside the given aircraft model.
        '''
        modelsXPath = '/cpacs/vehicles/aircraft/model/@uID'
        return self.xPathGetAllElements(modelsXPath)   

    def get_allFuselageProfileUIDs(self):
        '''
        Returns all fuselage profile UIDs from the current CPACS file.
        '''
        fuseProfXPath = '/cpacs/vehicles/profiles/fuselageProfiles/fuselageProfile/@uID'
        return self.xPathGetAllElements(fuseProfXPath)

    def get_fuselageUIDs(self, aircraftModelXPath):
        '''
        Returns all fuselage UIDs inside the given aircraft model.
        '''
        fuselagesXPath = aircraftModelXPath + '/fuselages/fuselage/@uID'
        return self.xPathGetAllElements(fuselagesXPath)
    

## ===========================================================================================   
        
    def init(self):
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glClearColor(0.0, 0.0 , 0.0, 1.0)
    
    def resize(self, w, h):
        side = min(w, h)
        GL.glViewport(0,0,w,h)
        #GL.glViewport((w - side) / 2, (h - side) / 2, side, side)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
       
#        '''gluunproject vs gluperspective'''
        
        GL.glOrtho(-0.5 * self.aspect, +0.5 * self.aspect, +0.5* self.aspect, -0.5* self.aspect, 0.0, 12.0)




        
    def display(self):
        # Clear screen and Z-buffer
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT) 
        
        # Reset transformations
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
       
        GL.glTranslated(0.0, 0.0, -1.5)              
        GL.glRotated(self.xRot, 1.0, 0.0, 0.0)
        GL.glRotated(self.yRot, 0.0, 1.0, 0.0)
        GL.glRotated(self.zRot, 0.0, 0.0, 1.0) 
        GL.glScalef(self.scale,self.scale,self.scale)
        

        # rotate around x to see the profile
        GL.glRotatef(90,1,0,0)    
        self.draw()
        GL.glFlush()    


    def draw(self):
        #GL.glLineWidth(2)
        GL.glPointSize(8)
        GL.glColor3f(0.0, 1.0, 0.0)
        #GL.glBegin(GL.GL_TRIANGLE_STRIP)
        
        
        GL.glColor3f(0.0, 1.0, 0.0)
        GL.glBegin(GL.GL_QUADS)
        for i in range(0, len(self.up_List), 2) :
            
        for l in self.up_List :
            for p in l :
                GL.glVertex3f(p[0], p[1], p[2]) 
#        GL.glColor3f(1.0, 0.0, 0.0)      
#        for l in self.lo_List :
#            for p in l :
 #               GL.glVertex3f(p[0], p[1], p[2]) 
        GL.glEnd()     


    def createWing(self):
        up_List = []
        lo_List = [] 
        eta_List = utility.createXcoordsLinear(1.0, 3)
        xsi_List = utility.createXcoordsCosineSpacing(1.0, 20)         
  
        for wingIndex in range(1, self.tigl.getWingCount()+1) :
            for segmentIndex in range(1, self.tigl.wingGetSegmentCount(wingIndex)+1) :
                for eta in eta_List :
                    up_tmp = []
                    lo_tmp = []
                    for xsi in xsi_List : 
                        ux, uy, uz = self.tigl.wingGetUpperPoint(wingIndex, segmentIndex, eta, xsi)
                        lx, ly, lz = self.tigl.wingGetLowerPoint(wingIndex, segmentIndex, eta, xsi)       
                        up_tmp.append([ux, uy, uz])
                        lo_tmp.append([lx, ly, lz])
                    up_List.append(up_tmp)
                    lo_List.append(lo_tmp)
                    
        return up_List, lo_List
    






    def drawTriangle(self):
        GL.glLineWidth(2)
        GL.glColor3f(0.0, 0.0, 1.0)
        GL.glBegin(GL.GL_LINE_STRIP) 
        plist = self.plist[0]
        for p in plist :
            GL.glVertex3f(p[0], p[1], p[2])              
        GL.glEnd()

        


        

class Widget(QtOpenGL.QGLWidget):
    def __init__(self, parent = None):
        super(Widget, self).__init__(parent)
        self.width = 320
        self.height = 302
        self.resize(self.width ,self.height)
        self.setWindowTitle("Rene Test")
      
      
        grid = QtGui.QGridLayout()
        
        self.setLayout(grid)
        
        
        #self.setFixedSize(QtCore.QSize(400,400))
        self.setSizePolicy ( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.renderer = Renderer(self.width ,self.height)    
    
    def initializeGL(self):
        self.renderer.init()
    
    def resizeGL(self, w, h):
        self.renderer.resize(w, h)
 
    def paintGL(self):
        self.renderer.display()

    def mousePressEvent(self, event):
        self.lastPos = QtCore.QPoint(event.pos())

    def mouseMoveEvent(self, event):
        
        if event.buttons() & QtCore.Qt.LeftButton:
            ()
            #self.renderer.set_coordinates(event.x(), event.y(), 1)
        elif event.buttons() & QtCore.Qt.RightButton :
            ()

        self.lastPos = QtCore.QPoint(event.pos())
        self.updateGL()

    def keyPressEvent(self, event):
        redraw = False
        offset_rot   = 5
        offset_scale = 0.1
        # Right arrow - increase rotation by 5 degree
        if event.key() == QtCore.Qt.Key_Right :
            self.renderer.yRot += offset_rot
            redraw = True
        # Left arrow - decrease rotation by 5 degree
        elif event.key() == QtCore.Qt.Key_Left :
            self.renderer.yRot -= offset_rot
            redraw = True
        elif event.key() == QtCore.Qt.Key_Up :
            self.renderer.xRot += offset_rot
            redraw = True
        elif event.key() == QtCore.Qt.Key_Down :
            self.renderer.xRot -= offset_rot 
            redraw = True
        elif event.key() == QtCore.Qt.Key_Plus :
            self.renderer.scale += offset_scale
            redraw = True
        elif event.key() == QtCore.Qt.Key_Minus :
            self.renderer.scale -= offset_scale 
            redraw = True
  
        # Request display update
        if redraw :
            self.updateGL()
    
if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = Widget()
    widget.show()
    app.exec_()    