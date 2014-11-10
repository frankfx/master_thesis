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
    from OpenGL import GL, GLU, GLUT
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

class Renderer():

    glMode = {"GL_POINTS" : GL.GL_POINTS , "GL_QUADS" : GL.GL_QUADS, "GL_QUAD_STRIP" : GL.GL_QUAD_STRIP}
    
    def __init__(self, width, height):

        self.tixi = Tixi()
        self.tixi.open('simpletest.cpacs.xml')
        
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
        self.scale = 5.0 
        self.aspect= 0.5  
        self.viewwidth = 0.0
        self.viewheight = 0.0
        
        self.highShininess    = False # Whether the shininess parameter is high
        self.lowSpecularity   = False # Whether the specularity parameter is high
        self.emission         = False # Whether the emission parameter is turned on        
          

    def init(self):
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_LIGHTING)
        GL.glEnable(GL.GL_LIGHT0)
        GL.glEnable(GL.GL_NORMALIZE)
       # GL.glEnable(GL.GL_AUTO_NORMAL)
        #GL.glShadeModel(GL.GL_SMOOTH)
       # GL.glDisable(GL.GL_COLOR_MATERIAL)         
#    def init(self):
#        GL.glClearColor (1.0, 1.0, 1.0, 0.0)
#        GL.glShadeModel (GL.GL_SMOOTH)

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
        
        GL.glPushMatrix()
        GL.glTranslatef(self.xTrans,self.yTrans,-1.5)
        GL.glRotated(self.xRot, 1.0, 0.0, 0.0)
        GL.glRotated(self.yRot, 0.0, 1.0, 0.0)
        GL.glRotated(self.zRot, 0.0, 0.0, 1.0)
        
        #self.draw()
        self.drawCube()
        GLUT.glutInit()
        GLUT.glutSolidCone(1.0,1.0,150,80)
        #GLUT.glutSolidTeapot(1.4)        
        GL.glPopMatrix()

        #self.initMaterial()        
        self.initLight()


        GL.glFlush() 




    def draw(self):
        #GL.glLineWidth(2)
        GL.glPointSize(8)
       # GL.glColor3f(0.0, 1.0, 0.0)
        #GL.glEnable(GL.GL_BLEND)
        #GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_SRC_ALPHA)
        # draw upper
        #self.drawShape(self.pList_wing_up, [0.0, 0.44, 0.67, 0.5], Renderer.glMode["GL_QUADS"])
        # draw lower
        #self.drawShape(self.pList_wing_lo, [0.0, 0.44, 0.67, 0.5], Renderer.glMode["GL_QUADS"])

        # draw reflect upper
        #self.drawShape(self.pList_wing_up, [0.76, 0.79, 0.50, 0.5], Renderer.glMode["GL_QUADS"], -1)
        # draw reflect lower
        #self.drawShape(self.pList_wing_lo, [0.76, 0.79, 0.50, 0.5], Renderer.glMode["GL_QUADS"], -1)
        
        # draw fuselage
        
       # self.drawShape(self.pList_fuselage, [0.0, 0.44, 0.67], Renderer.glMode["GL_QUADS"])

        # draw ComponentSegment
       # GL.glLineWidth(9)
       # self.drawShape(self.pList_component_segment, [1.0, 0.0, 0.0])

        # draw Points
        # GL.glPointSize(6)
        # GL.glColor3f(1, 0, 1)
       #self.drawShape(self.pList_wing_up, [1.0, 0.0, 1.0], Renderer.glMode["GL_POINTS"])



    #------------------------------------------------------ def initLight(self):
#------------------------------------------------------------------------------ 
        #------------------------------ #Farben der Lichtquelle setzen (r,g,b,a)
        #--------------------------------------- ambient  = [0.1, 0.0, 0.0, 1.0]
        #--------------------------------------- diffuse  = [0.6, 0.4, 0.2, 1.0]
        #--------------------------------------- specular = [0.6, 0.6, 0.4, 1.0]
#------------------------------------------------------------------------------ 
        #--------------------------------------------- GL.glEnable(GL.GL_LIGHT0)
        #------------------- GL.glLightfv(GL.GL_LIGHT0, GL.GL_AMBIENT,  ambient)
        #------------------- GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE,  diffuse)
        #------------------ GL.glLightfv(GL.GL_LIGHT0, GL.GL_SPECULAR, specular)
#------------------------------------------------------------------------------ 
    #--------------------------------------------------- def initMaterial(self):
        #------------------------------------- # Materialfarben setzen (r,g,b,a)
        #---------------------------------- globalAmbient = [0.0, 0.0, 0.0, 1.0]
        #---------------------------------- ambient       = [1.0, 1.0, 1.0, 1.0]
        #---------------------------------- diffuse       = [1.0, 1.0, 1.0, 1.0]
        #---------------------------------- specular      = [1.0, 1.0, 1.0, 1.0]
#------------------------------------------------------------------------------ 
        #---------------------------------------- # Globale ambiente Beleuchtung
        #--------------------------------------------- # komplett herunternehmen
        #----------- GL.glLightModelfv(GL.GL_LIGHT_MODEL_AMBIENT, globalAmbient)
#------------------------------------------------------------------------------ 
        #-------------------------------------------- # Materialparameter setzen
        #----------- GL.glMaterialfv(GL.GL_FRONT_AND_BACK,GL.GL_AMBIENT,ambient)
        #----------- GL.glMaterialfv(GL.GL_FRONT_AND_BACK,GL.GL_DIFFUSE,diffuse)
        #--------- GL.glMaterialfv(GL.GL_FRONT_AND_BACK,GL.GL_SPECULAR,specular)
        #------------ GL.glMaterialf (GL.GL_FRONT_AND_BACK,GL.GL_SHININESS,16.0)
       

    def drawCube(self):
        GL.glBegin(GL.GL_QUADS)    # Begin drawing the color cube with 6 quads
        val = 0.5
        
        # Front
        GL.glNormal3f(0.0, 0.0, 1.0)
        GL.glVertex3f(-1.5, -1.0, 1.5)
        GL.glVertex3f(1.5, -1.0, 1.5)
        GL.glVertex3f(1.5, 1.0, 1.5)
        GL.glVertex3f(-1.5, 1.0, 1.5)
        
        # Right
        GL.glNormal3f(1.0, 0.0, 0.0)
        GL.glVertex3f(1.5, -1.0, -1.5)
        GL.glVertex3f(1.5, 1.0, -1.5)
        GL.glVertex3f(1.5, 1.0, 1.5)
        GL.glVertex3f(1.5, -1.0, 1.5)
        
        # Back
        GL.glNormal3f(0.0, 0.0, -1.0)
        GL.glVertex3f(-1.5, -1.0, -1.5)
        GL.glVertex3f(-1.5, 1.0, -1.5)
        GL.glVertex3f(1.5, 1.0, -1.5)
        GL.glVertex3f(1.5, -1.0, -1.5)
        
        # Left
        GL.glNormal3f(-1.0, 0.0, 0.0)
        GL.glVertex3f(-1.5, -1.0, -1.5)
        GL.glVertex3f(-1.5, -1.0, 1.5)
        GL.glVertex3f(-1.5, 1.0, 1.5)
        GL.glVertex3f(-1.5, 1.0, -1.5)      
        GL.glEnd()
    
    def initLight(self):

        ambientLight = [0.2, 0.2, 0.2, 1.0]
        GL.glLightModelfv(GL.GL_LIGHT_MODEL_AMBIENT, ambientLight)

        lightColor  = [0.6, 0.6, 0.6, 1.0]
        lightPos    = [1.5, 2, 1.5, 1.0]
        # Diffuse (non-shiny) light component
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, lightColor)
        # Specular (shiny) light component
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_SPECULAR, lightColor)
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, lightPos)

        specularity = 0.0
        emissivity  = 0.0
        shininess   = 0.0

        if self.lowSpecularity :
            specularity = 0.3
        else :
            specularity = 1.0

        if self.emission :
            emissivity = 0.05
        else :
            emissivity = 0

        if self.highShininess :
            shininess = 25
        else :
            shininess = 12

        # The color of the sphere
        materialColor = [0.2, 0.2, 1.0, 1.0]
        # The specular (shiny) component of the material
        materialSpecular = [specularity, specularity, specularity, 1.0]
        # The color emitted by the material
        materialEmission = [emissivity, emissivity, emissivity, 1.0]

        GL.glMaterialfv(GL.GL_FRONT, GL.GL_AMBIENT_AND_DIFFUSE, materialColor)
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_SPECULAR, materialSpecular)
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_EMISSION, materialEmission)
        GL.glMaterialf(GL.GL_FRONT, GL.GL_SHININESS, shininess) #The shininess parameter
    
    
    
    
    
    '''
    @param reflect: normal mode set 1 , reflect mode set -1
    @param flag_strip: strip mode set True , not strip set False
    '''
    def drawShape(self, pList, color, glMode, reflect=1, flag_Strip=False):
       # GL.glColor4f(color[0], color[1], color[2], color[3])
       # GL.glColor3f(color[0], color[1], color[2])
        
        GL.glBegin(glMode)
        for shape in pList :
            for i in range (0, len(shape)-1, 1):
                seg1 = shape[i] 
                seg2 = shape[i+1]
                for j in range(0, len(seg1)-1, 1) :
                    GL.glVertex3f(seg1[j+1][0], reflect * seg1[j+1][1], seg1[j+1][2])                     
                    GL.glVertex3f(seg1[j][0]  , reflect * seg1[j][1]  , seg1[j][2])
                    if(flag_Strip):
                        GL.glVertex3f(seg2[j+1][0], reflect * seg2[j+1][1], seg2[j+1][2])                     
                        GL.glVertex3f(seg2[j][0]  , reflect * seg2[j][1]  , seg2[j][2])
                    else :
                        GL.glVertex3f(seg2[j][0]  , reflect * seg2[j][1]  , seg2[j][2])
                        GL.glVertex3f(seg2[j+1][0], reflect * seg2[j+1][1], seg2[j+1][2])
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
                      #  _,_,eta_s, xsi_s = self.tigl.wingComponentSegmentPointGetSegmentEtaXsi(componentSegmentUID, eta, xsi)
                     #   print "eta = " , eta , " ; xsi = " , xsi , " ------>  " ,  "eta_s = " , eta_s , " ; xsi_s = " , xsi_s
                        
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
        elif event.key() == QtCore.Qt.Key_Escape :
            sys.exit()
        elif event.key() == QtCore.Qt.Key_S :
            self.renderer.highShininess = not self.renderer.highShininess
            redraw = True
        elif event.key() == QtCore.Qt.Key_P :
            self.renderer.lowSpecularity = not self.renderer.lowSpecularity
            redraw = True
        elif event.key() == QtCore.Qt.Key_E :
            self.renderer.emission = not self.renderer.emission
            redraw = True    
  
        # Request display update
        if redraw :
            self.updateGL()
    
if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = Widget()
    widget.show()
    app.exec_()    