'''
Created on Jul 30, 2014

@author: fran_re
'''

import sys

from tiglwrapper import Tigl, TiglException
from tixiwrapper import Tixi
from PySide import QtOpenGL, QtGui, QtCore
from Xtest.Open_GL import utility

try:
    from OpenGL import GL
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
       #self.tixi.open('D150_CPACS2.0_valid.xml')
        
        self.tigl = Tigl()
        try:
            self.tigl.open(self.tixi,"")
        except TiglException as err:    
            print 'Error opening tigl document: ', err.__str__()
           
        self.pList_fuselage = self.createFuselage() 
        self.pList_wing_up, self.pList_wing_lo = self.createWing()

        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.xTrans = 0
        self.yTrans = 0  
        self.scale = 0.2 
        self.aspect= 1.0  

    def init(self):
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glClearColor(0.0, 0.0 , 0.0, 1.0)
    
    def resize(self, w, h):
        #GL.glViewport(0,0,w,h)
        side = min(w, h)
        GL.glViewport((w - side) / 2, (h - side) / 2, side, side)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
       
        GL.glOrtho(-0.5 * self.aspect, +0.5 * self.aspect, +0.5* self.aspect, -0.5* self.aspect, 0.0, 12.0)

    def display(self):
        # Clear screen and Z-buffer
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT) 
        
        # Reset transformations
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
       
        GL.glTranslatef(self.xTrans,self.yTrans,-1.5)
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
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_SRC_ALPHA)
        # draw upper
        #self.drawShape(self.pList_wing_up, [0.0, 1.0, 0.0])
        # draw lower
        #self.drawShape(self.pList_wing_lo, [0.0, 1.0, 0.0])

        # draw reflect upper
        #self.drawShape(self.pList_wing_up, [1.0, 1.0, 0.0], -1)
        # draw reflect lower
        #self.drawShape(self.pList_wing_lo, [1.0, 1.0, 0.0], -1)
        self.createComponent()
        # draw fuselage
        self.drawShape(self.pList_fuselage, [0.0, 0.0, 1.0])


    def drawShape(self, pList, color, reflect= 1):
        GL.glColor3f(color[0], color[1], color[2])
        
        GL.glBegin(GL.GL_QUAD_STRIP)
        for shape in pList :
            for i in range (0, len(shape)-1, 1):
                seg1 = shape[i] 
                seg2 = shape[i+1]
                for j in range(0, len(seg1)-1, 1) :
                    GL.glVertex3f(seg1[j+1][0], reflect * seg1[j+1][1], seg1[j+1][2])                     
                    GL.glVertex3f(seg1[j][0]  , reflect * seg1[j][1]  , seg1[j][2])
                    GL.glVertex3f(seg2[j+1][0], reflect * seg2[j+1][1], seg2[j+1][2])                     
                    GL.glVertex3f(seg2[j][0]  , reflect * seg2[j][1]  , seg2[j][2])
        GL.glEnd() 

        GL.glPointSize(6)
        GL.glColor3f(1, 0, 1)

    def drawPoints(self, pList, reflect= 1):
        GL.glBegin(GL.GL_POINTS)
        for shape in pList :
            for i in range (0, len(shape)-1, 1):
                seg1 = shape[i] 
                seg2 = shape[i+1]
                for j in range(0, len(seg1)-1, 1) :
                    GL.glVertex3f(seg1[j][0]  , reflect * seg1[j][1]  , seg1[j][2])
                    GL.glVertex3f(seg1[j+1][0], reflect * seg1[j+1][1], seg1[j+1][2]) 
                    GL.glVertex3f(seg2[j][0]  , reflect * seg2[j][1]  , seg2[j][2])
                    GL.glVertex3f(seg2[j+1][0], reflect * seg2[j+1][1], seg2[j+1][2]) 
        GL.glEnd()         


    def createComponent(self, point_cnt_eta = 6, point_cnt_xsi = 20):
        eta_List = utility.createXcoordsLinear(1.0, point_cnt_eta)
        xsi_List = utility.createXcoordsLinear(1.0, point_cnt_xsi) 
                    
        for wingIndex in range(1, self.tigl.getWingCount()+1) :
            for compSegmentIndex in range(1, self.tigl.wingGetComponentSegmentCount(wingIndex)+1) : 
                componentSegmentUID = self.tigl.wingGetComponentSegmentUID(wingIndex, compSegmentIndex)
                for eta in eta_List :
                    for xsi in xsi_List :
                        _,_,eta_s, xsi_s = self.tigl.wingComponentSegmentPointGetSegmentEtaXsi(componentSegmentUID, eta, xsi)
                        self.tigl.wing

    def createFuselage(self, point_cnt_eta = 6, point_cnt_zeta = 20):
        eta_List = utility.createXcoordsLinear(1.0, point_cnt_eta)
        zeta_List = utility.createXcoordsLinear(1.0, point_cnt_zeta) 
        
        plistFuse = []
        
        for fuselageIndex in range(1, self.tigl.getFuselageCount()+1) :
            plistSeg = []
            for segmentIndex in range(1, self.tigl.fuselageGetSegmentCount(fuselageIndex)+1) :
                for eta in eta_List :
                    p_tmp = []
                    for zeta in zeta_List :
                        x, y, z = self.tigl.fuselageGetPoint(fuselageIndex, segmentIndex, eta, zeta)
                        p_tmp.append([x,y,z])
                    plistSeg.append(p_tmp)    
            plistFuse.append(plistSeg)        
        
        return plistFuse 

    def createWing(self, point_cnt_eta = 4, point_cnt_xsi = 20):
        eta_List = utility.createXcoordsLinear(1.0, point_cnt_eta)
        xsi_List = utility.createXcoordsCosineSpacing(1.0, point_cnt_xsi) 
        
        plistWing_up = []
        plistWing_lo = []
        
        for wingIndex in range(1, self.tigl.getWingCount()+1) :
            plistSeg_up = []
            plistSeg_lo = []
            for segmentIndex in range(1, self.tigl.wingGetSegmentCount(wingIndex)+1) :
                for eta in eta_List :
                    p_tmp_up = []
                    p_tmp_lo = []
                    for xsi in xsi_List :   
                        xu, yu, zu = self.tigl.wingGetUpperPoint(wingIndex, segmentIndex, eta, xsi)
                        xl, yl, zl = self.tigl.wingGetLowerPoint(wingIndex, segmentIndex, eta, xsi)
                        p_tmp_up.append([xu,yu,zu])
                        p_tmp_lo.append([xl,yl,zl])
                    plistSeg_up.append(p_tmp_up)
                    plistSeg_lo.append(p_tmp_lo)
            plistWing_up.append(plistSeg_up)
            plistWing_lo.append(plistSeg_lo)
            
        return plistWing_up , plistWing_lo


class Widget(QtOpenGL.QGLWidget):
    def __init__(self, parent = None):
        super(Widget, self).__init__(parent)
        self.width = 500
        self.height = 500
        self.resize(self.width ,self.height)
      
        grid = QtGui.QGridLayout()
        self.setLayout(grid)
        
        self.setSizePolicy ( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.renderer = Renderer(self.width ,self.height)    
    
    def initializeGL(self):
        self.renderer.init()
    
    def resizeGL(self, w, h):
        self.renderer.resize(w, h)
 
    def paintGL(self):
        self.renderer.display()

    def mousePressEvent(self, event):  
        self.lastPos_x = event.pos().x()
        self.lastPos_y = event.pos().y()
                
    def mouseMoveEvent(self, event):
        dx = (event.x() - self.lastPos_x ) 
        dy = (event.y() - self.lastPos_y ) 
        
        self.lastPos_x += dx
        self.lastPos_y += dy

        #Betrachtsfeld = -1 bis 1
        
        #print self.width 
        #print self.height 
        
        self.renderer.xTrans += (2*dx / (self.width*1.0)) 
        self.renderer.yTrans += (2*dy / (self.height*1.0))

        self.updateGL()

    def keyPressEvent(self, event):
        redraw = False
        offset_rot   = 5
        offset_scale = 0.005
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