'''
Created on Jul 30, 2014

@author: fran_re
'''

import sys

from tiglwrapper import Tigl, TiglException
from tixiwrapper import Tixi
from PySide import QtOpenGL, QtGui, QtCore
from Xtest.Open_GL import utility
from _curses import noraw

try:
    from OpenGL import GL, GLU, GLUT
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

class Renderer():

    glMode = {"GL_POINTS" : GL.GL_POINTS, "GL_LINES" : GL.GL_LINES, "GL_LINE_STRIP" : GL.GL_LINE_STRIP, "GL_LINE_LOOP" : GL.GL_LINE_LOOP , "GL_QUADS" : GL.GL_QUADS, "GL_QUAD_STRIP" : GL.GL_QUAD_STRIP}
    
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
        self.pList_component_segment = self.createComponent()

        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.xTrans = 0
        self.yTrans = 0  
        self.scale = 10.0 
        self.aspect= 0.5  
        self.viewwidth = 0.0
        self.viewheight = 0.0
        
    def init(self):
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_LIGHTING)
        GL.glEnable(GL.GL_LIGHT0)
        GL.glEnable(GL.GL_NORMALIZE)
        GL.glShadeModel(GL.GL_SMOOTH)
        GL.glClearColor (1.0, 1.0, 1.0, 0.0)

    def resize(self, w, h):
        side = min(w, h)
        self.viewwidth = side
        self.viewheight = side
        
        GL.glViewport((w - side) / 2, (h - side) / 2, self.viewwidth, self.viewheight)

        self.__setRendermodus()        
        
    def __setRendermodus(self):
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
       
        GL.glOrtho(-1.0 * self.aspect * self.scale, +1.0 * self.aspect * self.scale,
                    +1.0* self.aspect * self.scale, -1.0* self.aspect * self.scale, -10.0, 12.0)

    def display(self):
        self.__setRendermodus()
 
        # Clear screen and Z-buffer
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT) 
        
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()         
        
        self.initLight()        
        
        GL.glPushMatrix()
        GL.glTranslatef(self.xTrans,self.yTrans,-1.5)
        GL.glRotated(self.xRot, 1.0, 0.0, 0.0)
        GL.glRotated(self.yRot, 0.0, 1.0, 0.0)
        GL.glRotated(self.zRot, 0.0, 0.0, 1.0)
        GL.glShadeModel(GL.GL_FLAT)
        
        self.draw()
        # GLUT.glutInit()#
        # GLUT.glutSolidTeapot(1.0)
        
        GL.glPopMatrix()

        GL.glFlush() 




    def draw(self):
        # draw upper
        self.drawShape(self.pList_wing_up, [0.0, 0.44, 0.67, 0.5], Renderer.glMode["GL_QUAD_STRIP"], 1, True)
        # draw lower
        self.drawShape(self.pList_wing_lo, [0.0, 0.44, 0.67, 0.5], Renderer.glMode["GL_QUADS"], 1, False)

        # draw reflect upper
        #self.drawShape(self.pList_wing_up, [0.76, 0.79, 0.50, 0.5], Renderer.glMode["GL_QUADS"], -1)
        # draw reflect lower
        #self.drawShape(self.pList_wing_lo, [0.76, 0.79, 0.50, 0.5], Renderer.glMode["GL_QUADS"], -1)
        
        # draw fuselage
        #self.drawShape(self.pList_fuselage, [0.0, 0.44, 0.67], Renderer.glMode["GL_QUADS"])

        # draw ComponentSegment
        #self.drawShape(self.pList_component_segment, [1.0, 0.0, 0.0], Renderer.glMode["GL_POINTS"], 1, False)
#        self.drawShape(self.pList_component_segment, [1.0, 0.0, 0.0], Renderer.glMode["GL_LINES"], 1, True)
#        self.drawShape(self.pList_component_segment, [1.0, 0.0, 0.0], Renderer.glMode["GL_QUAD_STRIP"], 1, True)

        # draw Points
        GL.glPointSize(6)
        GL.glColor3f(1, 0, 1)
        #self.drawShape(self.pList_wing_up, [1.0, 0.0, 1.0], Renderer.glMode["GL_POINTS"])

      


    def calculateSurfaceNormal(self, polynom):
        normal = [0.0, 0.0, 0.0]
        for i in range (len(polynom)) :
            cur = polynom[i]
            nxt = polynom[(i+1) % len(polynom)]
            
            normal[0] = normal[0] + ( (cur[1] - nxt[1]) * (cur[2] + nxt[2])) 
            normal[1] = normal[1] + ( (cur[2] - nxt[2]) * (cur[0] + nxt[0])) 
            normal[2] = normal[2] + ( (cur[0] - nxt[0]) * (cur[1] + nxt[1])) 
            
        return normal
    
    # normal in p1
    def calculateVertexNormal(self, p1, p2, p3):
        vec1 = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]]
        vec2 = [p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2]]
        v = [0.0, 0.0, 0.0]
        v[0] = vec1[1] * vec2[2] - vec1[2] * vec2[1] 
        v[1] = vec1[2] * vec2[0] - vec1[0] * vec2[2]
        v[2] = vec1[0] * vec2[1] - vec1[1] * vec2[0]
        
        return v
    

    
    def initLight(self):
        # mat_ambient   = [0.4, 0.4, 0.4, 1.0] 
        mat_ambient    = [0.6, 0.6, 0.6, 1.0]
        mat_diffuse    = [0.4, 0.8, 0.4, 1.0] 
        mat_specular   = [1.0, 1.0, 1.0, 1.0]
        light_position = [0.0, 0.0, 0.0, 1.0]        

        # GL_LIGHT_MODEL_AMBIENT, GL_LIGHT_MODEL_LOCAL_VIEWER,' GL_LIGHT_MODEL_TWO_SIDE und GL_LIGHT_MODEL_COLOR_CONTROL
        GL.glLightModelfv(GL.GL_LIGHT_MODEL_AMBIENT, mat_ambient)
        # Diffuse (non-shiny) light component
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, mat_diffuse)
        # Specular (shiny) light component
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_SPECULAR, mat_specular)
        
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, light_position)
        
        # The color of the sphere
        mat_materialColor = [0.2, 0.2, 1.0, 1.0]
        # The specular (shiny) component of the material
        mat_materialSpecular = [1.0, 1.0, 1.0, 1.0]
        # The color emitted by the material
        mat_materialEmission = [0, 0, 0, 1.0]
        #The shininess parameter
        mat_shininess  = 50.0 

        GL.glMaterialfv(GL.GL_FRONT, GL.GL_AMBIENT_AND_DIFFUSE, mat_materialColor)
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_SPECULAR, mat_materialSpecular)
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_EMISSION, mat_materialEmission)
        GL.glMaterialf(GL.GL_FRONT, GL.GL_SHININESS, mat_shininess)
    
    
    '''
    @param reflect: normal mode set 1 , reflect mode set -1
    @param flag_strip: strip mode set True , not strip set False
    '''
    def drawShape(self, pList, color, glMode, reflect=1, flag_Strip=False):
        #GL.glColor3f(color[0], color[1], color[2])
        
        quad = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
        
        GL.glBegin(glMode)
        for shape in pList :
            for i in range (0, len(shape)-1, 1):
                seg1 = shape[i] 
                seg2 = shape[i+1]
                for j in range(0, len(seg1)-1, 1) :
                    quad[0] = [seg1[j+1][0], reflect * seg1[j+1][1], seg1[j+1][2]]
                    quad[1] = [seg1[j][0]  , reflect * seg1[j][1]  , seg1[j][2]]
                    if(flag_Strip):
                        quad[2] = [seg2[j+1][0], reflect * seg2[j+1][1], seg2[j+1][2]]
                        quad[3] = [seg2[j][0]  , reflect * seg2[j][1]  , seg2[j][2]]                        
                    else :
                        quad[2] = [seg2[j][0]  , reflect * seg2[j][1]  , seg2[j][2]]
                        quad[3] = [seg2[j+1][0], reflect * seg2[j+1][1], seg2[j+1][2]]  

                    vec = self.calculateSurfaceNormal(quad)
                    GL.glNormal3f(vec[0], vec[1], vec[2])
                    GL.glVertex3f(quad[0][0], quad[0][1], quad[0][2])
                    GL.glNormal3f(vec[0], vec[1], vec[2])                     
                    GL.glVertex3f(quad[1][0], quad[1][1], quad[1][2])                     
                    GL.glNormal3f(vec[0], vec[1], vec[2])
                    GL.glVertex3f(quad[2][0], quad[2][1], quad[2][2])                     
                    GL.glNormal3f(vec[0], vec[1], vec[2])
                    GL.glVertex3f(quad[3][0], quad[3][1], quad[3][2])                     
        GL.glEnd() 



    '''
    @param reflect: normal mode set 1 , reflect mode set -1
    @param flag_strip: strip mode set True , not strip set False
    '''
    def drawShape2(self, pList, color, glMode, reflect=1, flag_Strip=False):
        #GL.glColor3f(color[0], color[1], color[2])
        
        quad = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
        
        GL.glBegin(glMode)
        for shape in pList :
            for i in range (0, len(shape)-1, 1):
                seg1 = shape[i] 
                seg2 = shape[i+1]
                for j in range(0, len(seg1)-1, 1) :
                    quad[0] = [seg1[j+1][0], reflect * seg1[j+1][1], seg1[j+1][2]]
                    quad[1] = [seg1[j][0]  , reflect * seg1[j][1]  , seg1[j][2]]
                    if(flag_Strip):
                        quad[2] = [seg2[j+1][0], reflect * seg2[j+1][1], seg2[j+1][2]]
                        quad[3] = [seg2[j][0]  , reflect * seg2[j][1]  , seg2[j][2]]                        
                    else :
                        quad[2] = [seg2[j][0]  , reflect * seg2[j][1]  , seg2[j][2]]
                        quad[3] = [seg2[j+1][0], reflect * seg2[j+1][1], seg2[j+1][2]]  

                    vec = self.calculateSurfaceNormal(quad)
                    GL.glNormal3f(vec[0], vec[1], vec[2])
                    GL.glVertex3f(quad[0][0], quad[0][1], quad[0][2])
                    GL.glNormal3f(vec[0], vec[1], vec[2])                     
                    GL.glVertex3f(quad[1][0], quad[1][1], quad[1][2])                     
                    GL.glNormal3f(vec[0], vec[1], vec[2])
                    GL.glVertex3f(quad[2][0], quad[2][1], quad[2][2])                     
                    GL.glNormal3f(vec[0], vec[1], vec[2])
                    GL.glVertex3f(quad[3][0], quad[3][1], quad[3][2])                     
        GL.glEnd() 






    def createComponent(self, point_cnt_eta = 6, point_cnt_xsi = 20):
        eta_List = utility.createXcoordsLinear(1.0, point_cnt_eta)
        xsi_List = utility.createXcoordsLinear(1.0, point_cnt_xsi) 
             
        plistComp = []     
                    
        for wingIndex in range(1, self.tigl.getWingCount()+1) :
            plistSeg = []
            for compSegmentIndex in range(1, self.tigl.wingGetComponentSegmentCount(wingIndex)+1) : 
                componentSegmentUID = self.tigl.wingGetComponentSegmentUID(wingIndex, compSegmentIndex)
                for eta in eta_List :
                    p_tmp = []
                    for xsi in xsi_List :
                        x, y, z = self.tigl.wingComponentSegmentGetPoint(componentSegmentUID, eta, xsi)
                        p_tmp.append([x,y,z])
                    plistSeg.append(p_tmp)
            plistComp.append(plistSeg)

        return plistComp
        
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
        self.width = 800
        self.height = 800
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

        #Betrachtsfeld = -aspect bis aspect
        
        oglXunit = 2.0 * self.renderer.aspect * self.renderer.scale
        oglYunit = oglXunit
        
        # pixel real world to Pixel ogl world 
        oglXTrans = oglXunit * 1.0 / self.renderer.viewwidth
        oglYTrans = oglYunit * 1.0 / self.renderer.viewheight
        
        self.renderer.xTrans += (dx * oglXTrans) 
        self.renderer.yTrans += (dy * oglYTrans)

        self.updateGL()

    def keyPressEvent(self, event):
        redraw = False
        offset_rot   = 2.0
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