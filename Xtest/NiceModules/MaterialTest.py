'''
Created on Nov 6, 2014

@author: fran_re
'''
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
        self.scale = 6.0 
        self.aspect= 0.5  
        self.viewwidth = 0.0
        self.viewheight = 0.0
        
        
        
        # =====================================
        self.angle = 0.0

        self.redDiffuseMaterial = [1.0, 0.0, 0.0]
        # set the material to white
        self.whiteSpecularMaterial = [1.0, 1.0, 1.0]
        # set the material to green
        self.greenEmissiveMaterial = [0.0, 1.0, 0.0]

        # set the light specular to white
        self.whiteSpecularLight = [1.0, 1.0, 1.0]
        # set the light ambient to black
        self.blackAmbientLight = [0.0, 0.0, 0.0]
        #set the diffuse light to white
        self.whiteDiffuseLight = [1.0, 1.0, 1.0]
        
        # set the diffuse light to white
        self.blankMaterial = [0.0, 0.0, 0.0] 
        # set the shininess of the material
        self.mShininess = [128]        
        
        
        self.diffuse = False
        self.emissive = False
        self.specular = False        
        
        # =====================================
        
        
        
    def init(self):
        # GL.glEnable(GL.GL_COLOR_MATERIAL)
          
        mat_specular   = [1.0, 1.0, 1.0, 1.0]
        mat_shininess  = [50.0]
        light_position = [0.75, 0.0, 1.0, 0.0]
   
        GL.glClearColor (1.0, 1.0, 1.0, 0.0)
        GL.glShadeModel (GL.GL_SMOOTH)

        GL.glMaterialfv(GL.GL_FRONT, GL.GL_SPECULAR, mat_specular)
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_SHININESS, mat_shininess)
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, light_position)

        #GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glEnable(GL.GL_LIGHTING)
        GL.glEnable(GL.GL_LIGHT0)
        GL.glEnable(GL.GL_DEPTH_TEST)        
        
        
       # GL.glClearColor(1.0, 1.0 , 1.0, 1.0)

    def light(self):
        # Now I am just assigning the colours to the current light       
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_SPECULAR, self.whiteSpecularLight)
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_AMBIENT, self.blackAmbientLight)
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, self.whiteDiffuseLight)

    def resize(self, w, h):
        GL.glViewport(0,0,w,h)
        GL.glMatrixMode (GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective (60, w / h, 1.0, 100.0)
        GL.glMatrixMode (GL.GL_MODELVIEW)
        
        
        #side = min(w, h)
        #self.viewwidth = side
        #self.viewheight = side
        
       # GL.glViewport((w - side) / 2, (h - side) / 2, self.viewwidth, self.viewheight)

       # self.__setProjection()

    def __setProjection(self):
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
       
        GL.glOrtho(-1.0 * self.aspect * self.scale, +1.0 * self.aspect * self.scale,
                    +1.0* self.aspect * self.scale, -1.0* self.aspect * self.scale, 0.0, 12.0)
        
        #http://devernay.free.fr/cours/opengl/materials.html
        mat = []
        mat[0] = 0.24725
        mat[1] = 0.1995 
        mat[2] = 0.0745 
        mat[3] = 1.0
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_AMBIENT, mat)
        mat[0] = 0.75164
        mat[1] = 0.60648
        mat[2] = 0.22648
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_DIFFUSE, mat)
        mat[0] = 0.628281 
        mat[1] = 0.555802 
        mat[2] = 0.366065
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_SPECULAR, mat)
        GL.glMaterialf(GL.GL_FRONT, GL.GL_SHININESS, 0.4 * 128.0)








    def display(self):
       # self.__setProjection()
        
      #  GL.glClearColor (0.0,0.0,0.0,1.0)
        # Clear screen and Z-buffer
        #GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT) 
        
       # GL.glLoadIdentity()
       # self.light()
       # GL.glTranslatef(0,0,-5)
    
       # GL.glRotatef(self.angle,1,1,1)
        
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GLUT.glutInit()
        GLUT.glutSolidSphere (1.0, 20, 16)
        GL.glFlush()        
        
        
       # GL.glTranslatef(self.xTrans,self.yTrans,-1.5)
       # GL.glRotated(self.xRot, 1.0, 0.0, 0.0)
       # GL.glRotated(self.yRot, 0.0, 1.0, 0.0)
       # GL.glRotated(self.zRot, 0.0, 0.0, 1.0) 

        # rotate around x to see the profile
        #GL.glRotatef(90,1,0,0)    
        GLUT.glutInit()
        GLUT.glutSolidTeapot(2)
        self.angle+=1
        #self.draw()
        GL.glFlush()    


    def draw(self):
        #GL.glLineWidth(2)
        GL.glPointSize(8)
        GL.glColor3f(0.0, 1.0, 0.0)
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
        self.drawShape(self.pList_fuselage, [0.0, 0.44, 0.67], Renderer.glMode["GL_QUADS"])

        # draw ComponentSegment
       # GL.glLineWidth(9)
       # self.drawShape(self.pList_component_segment, [1.0, 0.0, 0.0])

        # draw Points
        # GL.glPointSize(6)
        # GL.glColor3f(1, 0, 1)
       #self.drawShape(self.pList_wing_up, [1.0, 0.0, 1.0], Renderer.glMode["GL_POINTS"])

    '''
    @param reflect: normal mode set 1 , reflect mode set -1
    @param flag_strip: strip mode set True , not strip set False
    '''
    def drawShape(self, pList, color, glMode, reflect=1, flag_Strip=False):
       # GL.glColor4f(color[0], color[1], color[2], color[3])
        GL.glColor3f(color[0], color[1], color[2])
        
        GL.glTexGeni(GL.GL_S, GL.GL_TEXTURE_GEN_MODE, GL.GL_SPHERE_MAP)
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
        #-------------------------------------------------------- redraw = False
        #---------------------------------------------------- offset_rot   = 1.0
        #---------------------------------------------------- offset_scale = 0.1
        # Right arrow - increase rotation by 5 degree
        #------------------------------- if event.key() == QtCore.Qt.Key_Right :
            #---------------------------------- self.renderer.yRot += offset_rot
            #----------------------------------------------------- redraw = True
        #-------------------------- # Left arrow - decrease rotation by 5 degree
        #------------------------------ elif event.key() == QtCore.Qt.Key_Left :
            #---------------------------------- self.renderer.yRot -= offset_rot
            #----------------------------------------------------- redraw = True
        #-------------------------------- elif event.key() == QtCore.Qt.Key_Up :
            #---------------------------------- self.renderer.xRot += offset_rot
            #----------------------------------------------------- redraw = True
        #------------------------------ elif event.key() == QtCore.Qt.Key_Down :
            #---------------------------------- self.renderer.xRot -= offset_rot
            #----------------------------------------------------- redraw = True
        #------------------------------ elif event.key() == QtCore.Qt.Key_Plus :
            #------------------------------- self.renderer.scale += offset_scale
            #----------------------------------------------------- redraw = True
        #----------------------------- elif event.key() == QtCore.Qt.Key_Minus :
            #------------------------------- self.renderer.scale -= offset_scale
            #----------------------------------------------------- redraw = True
  
        if event.key() == QtCore.Qt.Key_S :
            if self.renderer.specular==False :
                # If specular is enabled then set the specular material to the white material,
                # and the shininess to our shininess value
                self.renderer.specular = True
                GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_SPECULAR, self.renderer.whiteSpecularMaterial)
                GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_SHININESS, self.renderer.mShininess)
            elif self.renderer.specular == True :
                # If specular is not enabled then set the specular material to the blank material,
                # and the shininess value to our blank material
                self.renderer.specular = False
                GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_SPECULAR, self.renderer.blankMaterial)
                GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_SHININESS, self.renderer.blankMaterial)

        if event.key() == QtCore.Qt.Key_D :
            if self.renderer.diffuse == False :
                #If diffuse is enabled then set the diffuse material to the red material
                self.renderer.diffuse = True
                GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_DIFFUSE, self.renderer.redDiffuseMaterial)
            elif self.renderer.diffuse==True :
                #If diffuse is not enabled then set the diffuse material to the blank material
                self.renderer.diffuse = False
                GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_DIFFUSE, self.renderer.blankMaterial)

        if event.key() == QtCore.Qt.Key_E :
            if self.renderer.emissive == False :
                # If emissive is enabled then set the emissive material to the green material
                self.renderer.emissive = True
                GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_EMISSION, self.renderer.greenEmissiveMaterial)
            elif self.renderer.emissive == True :
                # If emissive is not enabled then set the emissive material to the blank material
                self.renderer.emissive = False
                GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_EMISSION, self.renderer.blankMaterial)
  
  
        # Request display update
       # if redraw :
        self.updateGL()
    
if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = Widget()
    widget.show()
    app.exec_()    