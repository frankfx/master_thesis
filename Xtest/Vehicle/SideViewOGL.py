'''
Created on Jul 30, 2014

@author: fran_re
'''

import sys

from vehicleData   import VehicleData
from PySide        import QtOpenGL, QtGui, QtCore
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

class Renderer(QtOpenGL.QGLWidget):

    glMode = {"GL_POINTS" : GL.GL_POINTS, "GL_LINES" : GL.GL_LINES, "GL_LINE_STRIP" : GL.GL_LINE_STRIP,\
              "GL_LINE_LOOP" : GL.GL_LINE_LOOP , "GL_QUADS" : GL.GL_QUADS, "GL_QUAD_STRIP" : GL.GL_QUAD_STRIP}
    
    def __init__(self, width, height):
        super(Renderer, self).__init__()
        
        # point lists
        self.data = VehicleData()
        
        # transformations
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.xTrans = 0
        self.yTrans = 0  
        self.scale = 5.0 
        self.aspect= 0.5  
        self.viewwidth = 0.0
        self.viewheight = 0.0

        # helper
        self.r_color = 0.0
        self.g_color = 0.0
        self.b_color = 0.0
        self.alpha_rgb = 1.0
       
        # show flags
        self.flag_show_fuselage       = False
        self.flag_show_wing1_up       = False
        self.flag_show_wing1_lo       = False
        self.flag_show_wing2_up       = False
        self.flag_show_wing2_lo       = False
        self.flag_show_compnt         = False
        self.flag_show_flap_TE_Device = False
        self.flag_show_flap_LE_Device = False
        self.flag_show_flap_spoiler   = False
        self.flag_show_ribs           = False
        self.flag_show_spars          = False
        self.flag_show_grid           = False      
        self.flag_selection           = False

        
        # view flags
        self.flag_view_3d             = False
        self.flag_view_side           = False
        self.flag_view_front          = False
        self.flag_view_top            = False 
           
        # selection
        self.selectedPoint = None

        # widget option
        self.setFocusPolicy(QtCore.Qt.ClickFocus)

    
    

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.emit(QtCore.SIGNAL("xRotationChanged(int)"), angle)
            self.updateGL()
            
    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)        
        if angle != self.yRot:
            self.yRot = angle
            self.emit(QtCore.SIGNAL("yRotationChanged(int)"), angle)
            self.updateGL()   
    
    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)        
        if angle != self.zRot:
            self.zRot = angle
            self.emit(QtCore.SIGNAL("zRotationChanged(int)"), angle)
            self.updateGL()    
    
    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 2
        while angle > 360 * 2:
            angle -= 360 * 2
        return angle 
    
    def updateLists(self):
        self.createOglLists()
        self.updateGL()

    def initializeGL(self):
        GL.glEnable(GL.GL_DEPTH_TEST)
      #  GL.glEnable(GL.GL_LIGHTING)
     #   GL.glEnable(GL.GL_LIGHT0)
        #GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glEnable(GL.GL_NORMALIZE)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)             
        GL.glShadeModel(GL.GL_SMOOTH)
        GL.glClearColor (1.0, 1.0, 1.0, 0.0)
     #   self.initLight()
        
        self.createOglLists()
        
    def resizeGL(self, w, h):       
        side = min(w, h)
        self.viewwidth = side
        self.viewheight = side
        
        GL.glViewport((w - side) / 2, (h - side) / 2, self.viewwidth, self.viewheight)
        self.__setProjection()        
        
    def __setProjection(self):
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
       
        GL.glOrtho(-1.0 * self.aspect * self.scale, +1.0 * self.aspect * self.scale,
                   +1.0* self.aspect * self.scale, -1.0* self.aspect * self.scale, -100.0, 100.0)

    def setTransparent(self, value):
        self.alpha_rgb = value
       # if value < 1.0 :
       #     GL.glDisable(GL.GL_DEPTH_TEST)
       # else :
       #     GL.glEnable(GL.GL_DEPTH_TEST)

    def paintGL(self):
        self.__setProjection()
        # Clear screen and Z-buffer
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT) 
        
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()   

        GL.glTranslatef(self.xTrans,self.yTrans,-1.5)
        
        if not self.flag_selection :
            GL.glRotated(self.xRot, 1.0, 0.0, 0.0)
            GL.glRotated(self.yRot, 0.0, 1.0, 0.0)
            GL.glRotated(self.zRot, 0.0, 0.0, 1.0)
            #self.initLight()
         
       # GLUT.glutInit()
        #GLUT.glutSolidSphere(1,25,25)
        #self.initLight()
        self.draw()    
        if self.flag_show_grid:
            self.drawGrid()    
       
        
        #GL.glShadeModel(GL.GL_FLAT)
        GL.glFlush() 

    
    
    
    def draw(self):      
        if self.flag_show_fuselage :
            GL.glCallList(self.index)
        if self.flag_show_wing1_up :        
            GL.glCallList(self.index+1)
        if self.flag_show_wing1_lo :
            GL.glCallList(self.index+2)
        if self.flag_show_wing2_up :
            GL.glCallList(self.index+3)
        if self.flag_show_wing2_lo :
            GL.glCallList(self.index+4)
        if self.flag_show_compnt :
            GL.glCallList(self.index+5)
        if self.flag_show_flap_TE_Device :
            GL.glCallList(self.index+6)
        if self.flag_show_flap_LE_Device :
            GL.glCallList(self.index+7)
        if self.flag_show_flap_spoiler :
            GL.glCallList(self.index+8)
        if self.flag_show_spars :
            GL.glCallList(self.index+9)

    def createOglLists(self): 
        self.index = GL.glGenLists(10)

        GL.glNewList(self.index, GL.GL_COMPILE) # compile the first one
        self.createOglShape(self.data.pList_fuselage, [0.0, 0.44, 0.67, self.alpha_rgb], Renderer.glMode["GL_QUADS"], 1, False)
        GL.glEndList()


        GL.glNewList(self.index+1, GL.GL_COMPILE)
        self.createOglShape(self.data.pList_wing_up, [0.0, 0.44, 0.67, self.alpha_rgb], Renderer.glMode["GL_QUADS"], 1, False)
        GL.glEndList() 

        GL.glNewList(self.index+2, GL.GL_COMPILE)
        self.createOglShape(self.data.pList_wing_lo, [0.0, 0.44, 0.67, self.alpha_rgb], Renderer.glMode["GL_QUADS"], 1, False)
        GL.glEndList()
 
        # draw reflect upper wing
        GL.glNewList(self.index+3, GL.GL_COMPILE)
        self.createOglShape(self.data.pList_wing_up, [0.76, 0.79, 0.50, self.alpha_rgb], Renderer.glMode["GL_QUADS"], -1, False)
        GL.glEndList()

        GL.glNewList(self.index+4, GL.GL_COMPILE)
        self.createOglShape(self.data.pList_wing_lo, [0.76, 0.79, 0.50, self.alpha_rgb], Renderer.glMode["GL_QUADS"], -1, False)
        GL.glEndList()

        GL.glNewList(self.index+5, GL.GL_COMPILE)
        self.createOglShape(self.data.pList_component_segment, [1.0, 0.0, 0.0, 1.0], Renderer.glMode["GL_LINES"], 1, True)
        GL.glEndList()

        GL.glNewList(self.index+6, GL.GL_COMPILE)
        self.createOglFlaps(self.data.pList_flaps_TEDevice)
        GL.glEndList()
 
        GL.glNewList(self.index+7, GL.GL_COMPILE)
        self.createOglFlaps(self.data.pList_flaps_LEDevice)
        GL.glEndList()

        GL.glNewList(self.index+8, GL.GL_COMPILE)
        self.createOglFlaps(self.data.pList_flaps_Spoiler)
        GL.glEndList()

        GL.glNewList(self.index+9, GL.GL_COMPILE)
        self.createOglSpars(self.data.pList_spares)
        GL.glEndList()


    def drawGrid(self, start = 2, end = -2):

        # Draw a white grid "floor".
        GL.glColor3f(1.0, 0.0, 1.0);
        GL.glBegin(GL.GL_LINES)
        i = -2.0
        
        while i <= 2.0 :
            GL.glVertex3f(i, start, 0); GL.glVertex3f(i, end, 0)
            GL.glVertex3f(start, i, 0); GL.glVertex3f(end, i, 0)
            i += 0.25
        GL.glEnd()


    def createOglShape(self, pList, color, glMode, reflect, flag_Strip):
        quad = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]

        if self.flag_selection and self.selectedPoint is not None \
                               and self.isElementSelected(pList, reflect, flag_Strip, self.selectedPoint) :
                color = [1.0, 0.0, 0.0, self.alpha_rgb]

        GL.glColor4fv(color)
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
                    GL.glNormal3fv([1,0,0])
                    GL.glVertex3f(quad[0][0], quad[0][1], quad[0][2])
                    GL.glNormal3fv([1,1,0])
                    GL.glVertex3f(quad[1][0], quad[1][1], quad[1][2])
                    GL.glNormal3fv([0,1,0])
                    GL.glVertex3f(quad[2][0], quad[2][1], quad[2][2])
                    GL.glNormal3fv([0,0,1])
                    GL.glVertex3f(quad[3][0], quad[3][1], quad[3][2])
        GL.glEnd()

    def createOglFlaps(self, pList):
        GL.glBegin(GL.GL_QUADS)
        for shape in pList :
            for segments in shape :
                for flaps in segments :
                    color = self.newColorVec()
                    GL.glColor3fv(color)
                    GL.glVertex3fv(flaps[0])
                    GL.glVertex3fv(flaps[1])
                    GL.glVertex3fv(flaps[3])
                    GL.glVertex3fv(flaps[2])
        GL.glEnd()
        
    def createOglSpars(self, pList):
        for shape in pList :
            for segments in shape :
                for spares in segments :  
                    GL.glColor3fv(self.newColorVec())      
                    GL.glBegin(GL.GL_LINE_STRIP)       
                    for vert in spares :
                        GL.glVertex3fv(vert) 
                    GL.glEnd()


    def initLight(self):
        mat_ambient    = [0.4, 0.4, 0.4, 1.0]
        mat_diffuse    = [0.4, 0.8, 0.4, 1.0] 
        mat_specular   = [1.0, 1.0, 1.0, 1.0]
        
        light_position = [0.0, 0.0, 1.0, 2.0]        

        GL.glLightModelfv(GL.GL_LIGHT_MODEL_AMBIENT, mat_ambient)
        # Diffuse (non-shiny) light component
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, mat_diffuse)
        # Specular (shiny) light component
     #   GL.glLightfv(GL.GL_LIGHT0, GL.GL_SPECULAR, mat_specular)
        
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, light_position)
        
        # GL.glLightf(GL.GL_LIGHT0, GL.GL_CONSTANT_ATTENUATION, 1.0)
        # GL.glLightf(GL.GL_LIGHT0, GL.GL_LINEAR_ATTENUATION, 0.001)
        # GL.glLightf(GL.GL_LIGHT0, GL.GL_QUADRATIC_ATTENUATION, 0.004)
        
        # The color of the sphere
        mat_materialColor = [0.2, 0.2, 1.0, 1.0]
        # The specular (shiny) component of the material
        mat_specular   = [0.628281, 0.555802, 0.366065, 1.0]
        # The color emitted by the material
        mat_materialEmission = [0, 0, 0, 1.0]
        #The shininess parameter
        mat_shininess  = 0.5 

        mat_ambient    = [0.64725,  0.5995, 0.3745, 1.0]
        mat_diffuse    = [0.75164, 0.60648, 0.52648, 1.0] 
        
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_AMBIENT, mat_ambient)
        # GL.glMaterialfv(GL.GL_FRONT, GL.GL_DIFFUSE, mat_diffuse)
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_SPECULAR, mat_specular)
        # GL.glMaterialfv(GL.GL_FRONT, GL.GL_EMISSION, mat_materialEmission)
        GL.glMaterialf(GL.GL_FRONT, GL.GL_SHININESS, mat_shininess * 128)
        
        #GL.glEnable(GL.GL_LIGHT1)
                    
    # =========================================================================================================
    # =========================================================================================================    
    # code selection
    # =========================================================================================================  
    # =========================================================================================================                
    def isElementSelected(self, plist, reflect, flag_Strip, point):
        quad = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
        for shape in plist :
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
                    if(utility.isPinRectangle(quad, point)) :
                        return True
        return False

    def __winPosTo3DPos(self, x, y):
        point = [None, None, None]                              # result point
        modelview  = GL.glGetDoublev(GL.GL_MODELVIEW_MATRIX)    # get the modelview info
        projection = GL.glGetDoublev(GL.GL_PROJECTION_MATRIX)   # get the projection matrix info
        viewport   = GL.glGetIntegerv(GL.GL_VIEWPORT)           # get the viewport info
 
        # in OpenGL y soars (steigt) from bottom (0) to top
        y_new = viewport[3] - y     
 
        # read depth buffer at position (X/Y_new)
        z = GL.glReadPixels(x, y_new, 1, 1, GL.GL_DEPTH_COMPONENT, GL.GL_FLOAT)
        # z should not be 0!!!
        # error when projection matrix not identity (gluPerspective) 
        point[0], point[1], point[2] = GLU.gluUnProject(x, y_new, z, modelview, projection, viewport)                         
        
        #point[0] = round(point[0],2)
        #point[1] = round(point[1],2)
        #point[2] = round(point[2],2)
        
        return point


    def mousePressEvent(self, event):  
        self.lastPos_x = event.pos().x()
        self.lastPos_y = event.pos().y()
        
        if self.flag_selection:
            self.selectedPoint = self.__winPosTo3DPos(self.lastPos_x, self.lastPos_y)
            self.initializeGL()
            self.updateGL()
            
    def mouseMoveEvent(self, event):
        dx = (event.x() - self.lastPos_x ) 
        dy = (event.y() - self.lastPos_y ) 
        
        self.lastPos_x += dx
        self.lastPos_y += dy

        #Betrachtsfeld = -aspect bis aspect
        
        oglXunit = 2.0 * self.aspect * self.scale
        oglYunit = oglXunit
        
        # pixel real world to Pixel ogl world 
        oglXTrans = oglXunit * 1.0 / self.viewwidth
        oglYTrans = oglYunit * 1.0 / self.viewheight
        
        self.xTrans += (dx * oglXTrans) 
        self.yTrans += (dy * oglYTrans)

        self.updateGL()

       
    def newColorVec(self):   
        color = [self.r_color, self.g_color, self.b_color]
        
        offset = 0.2
        self.b_color += offset
        
        if self.b_color >= 1.0 : 
            self.g_color += offset ; self.b_color = 0.0
        if self.g_color >= 1.0 :
            self.r_color += offset ; self.g_color = 0.0
        if self.r_color >= 1.0 :
            self.r_color = 0.0 ; self.g_color = 0.0 ; self.b_color = 0.0
            
        return color        
                
                
class Widget(QtGui.QWidget):
    def __init__(self, parent = None):
        super(Widget, self).__init__(parent)
        
        # window preferences
        self.width = 800
        self.height = 800
        self.resize(self.width ,self.height)
        
        # objects
        self.renderer = Renderer(self.width ,self.height)
        
        # window elements
        self.xSlider = self.createSlider(QtCore.SIGNAL("xRotationChanged(int)"),
                                         self.renderer.setXRotation)
        self.ySlider = self.createSlider(QtCore.SIGNAL("yRotationChanged(int)"),
                                         self.renderer.setYRotation)
        self.zSlider = self.createSlider(QtCore.SIGNAL("zRotationChanged(int)"),
                                         self.renderer.setZRotation)           
  
        label1 = QtGui.QLabel("opacity")
        label2 = QtGui.QLabel("   xRot")
        label3 = QtGui.QLabel("yRot")
        label4 = QtGui.QLabel("zRot")
        label5 = QtGui.QLabel("zoom")

        transparency = QtGui.QSpinBox()
        transparency.setRange(0, 100)
        transparency.setSingleStep(5)
        transparency.setSuffix('%')
        transparency.setValue(0)        
        transparency.valueChanged.connect(self.setTransparency)
      
        zoom = QtGui.QSpinBox()
        zoom.setRange(1, 200)
        zoom.setSingleStep(5)
        zoom.setSuffix('%')
        zoom.setValue(50)        
        zoom.valueChanged.connect(self.setZoom)      
      
        grid = QtGui.QGridLayout()
        grid.addWidget(label1, 1,0)
        grid.addWidget(transparency, 1,1)
        grid.addWidget(label5, 1,2)
        grid.addWidget(zoom, 1,3)
        
        grid.addWidget(label2       ,2, 0)
        grid.addWidget(label3       ,2, 2)
        grid.addWidget(label4       ,2, 4)        
        grid.addWidget(self.xSlider ,2, 1)
        grid.addWidget(self.ySlider ,2, 3)
        grid.addWidget(self.zSlider ,2, 5)
        grid.addWidget(self.renderer,4,0,1,6)
        self.setLayout(grid)
        
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setSizePolicy ( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        # context menu
        self.menu = QtGui.QMenu(self)
        self.submenu_view = self.menu.addMenu("views")
        
        # context menu actions
        self.viewOptions = [QtGui.QAction("top view", self), QtGui.QAction("front view", self),
                            QtGui.QAction("side view", self), QtGui.QAction("3D view", self)]
        self.showOptions = [QtGui.QAction("Show fuselage", self), QtGui.QAction("Show wing1up", self),
                            QtGui.QAction("Show wing1lo", self), QtGui.QAction("Show wing2up", self),
                            QtGui.QAction("Show wing2lo", self), QtGui.QAction("Show components", self),
                            QtGui.QAction("Show TE_Device", self), QtGui.QAction("Show LE_Device", self),
                            QtGui.QAction("Show spoiler", self), QtGui.QAction("Show ribs", self),
                            QtGui.QAction("Show spars", self), QtGui.QAction("Show grid", self)]
        selectAction     =  QtGui.QAction("select", self)
        aircraftAction   =  QtGui.QAction("Show aircraft", self)

        # context menu add actions
        self.menu.addSeparator() 
        
        for i in range(len(self.viewOptions)) :
            self.submenu_view.addAction(self.viewOptions[i])        

        for i in range (len(self.showOptions)) :
            self.showOptions[i].setCheckable(True)
            self.menu.addAction(self.showOptions[i])

        self.menu.addSeparator()
        self.menu.addAction(aircraftAction)
        
        self.menu.addSeparator()
        selectAction.setCheckable(True)
        self.menu.addAction(selectAction)

        # connect actions with methods       
        self.showOptions[0].triggered.connect(self.setShowFuse) 
        self.showOptions[1].triggered.connect(self.setShowWing1up) 
        self.showOptions[2].triggered.connect(self.setShowWing1lo) 
        self.showOptions[3].triggered.connect(self.setShowWing2up) 
        self.showOptions[4].triggered.connect(self.setShowWing2lo) 
        self.showOptions[5].triggered.connect(self.setShowCompnt) 
        self.showOptions[6].triggered.connect(self.setShowFlapTE) 
        self.showOptions[7].triggered.connect(self.setShowFlapLE) 
        self.showOptions[8].triggered.connect(self.setShowFlapSpoiler) 
        self.showOptions[9].triggered.connect(self.setShowRibs) 
        self.showOptions[10].triggered.connect(self.setShowSpars)
        self.showOptions[11].triggered.connect(self.setShowGrid)     
        aircraftAction.triggered.connect(self.setShowAircraft)      
        selectAction.triggered.connect(self.setFlagSelection) 
        self.viewOptions[0].triggered.connect(self.setTopView) 
        self.viewOptions[1].triggered.connect(self.setFrontView) 
        self.viewOptions[2].triggered.connect(self.setSideView) 
        self.viewOptions[3].triggered.connect(self.set3DView) 
        
        # set check flags
        self.showOptions[0].setChecked(self.renderer.flag_show_fuselage) 
        self.showOptions[1].setChecked(self.renderer.flag_show_wing1_up) 
        self.showOptions[2].setChecked(self.renderer.flag_show_wing1_lo) 
        self.showOptions[3].setChecked(self.renderer.flag_show_wing2_up) 
        self.showOptions[4].setChecked(self.renderer.flag_show_wing2_lo) 
        self.showOptions[5].setChecked(self.renderer.flag_show_compnt) 
        self.showOptions[6].setChecked(self.renderer.flag_show_flap_TE_Device) 
        self.showOptions[7].setChecked(self.renderer.flag_show_flap_LE_Device) 
        self.showOptions[8].setChecked(self.renderer.flag_show_flap_spoiler) 
        self.showOptions[9].setChecked(self.renderer.flag_show_ribs) 
        self.showOptions[10].setChecked(self.renderer.flag_show_spars)
        self.showOptions[10].setChecked(self.renderer.flag_show_grid)
        selectAction.setChecked(self.renderer.flag_selection)
 
 
    def setTransparency(self, value):
        self.renderer.setTransparent(1.0 - value/100.0)
        self.renderer.updateLists()
        
    def setZoom(self, value):
        self.renderer.scale = value * 0.10
        self.renderer.updateGL()
    
    def setShowFuse(self):
        self.renderer.flag_show_fuselage = not self.renderer.flag_show_fuselage

    def setShowWing1up(self):
        self.renderer.flag_show_wing1_up = not self.renderer.flag_show_wing1_up

    def setShowWing1lo(self):
        self.renderer.flag_show_wing1_lo = not self.renderer.flag_show_wing1_lo
        
    def setShowWing2up(self):
        self.renderer.flag_show_wing2_up = not self.renderer.flag_show_wing2_up
        
    def setShowWing2lo(self):
        self.renderer.flag_show_wing2_lo = not self.renderer.flag_show_wing2_lo
        
    def setShowCompnt(self):
        self.renderer.flag_show_compnt = not self.renderer.flag_show_compnt
    
    def setShowFlapLE(self):
        self.renderer.flag_show_flap_LE_Device = not self.renderer.flag_show_flap_LE_Device
    
    def setShowFlapTE(self):
        self.renderer.flag_show_flap_TE_Device = not self.renderer.flag_show_flap_TE_Device
    
    def setShowFlapSpoiler(self):
        self.renderer.flag_show_flap_spoiler = not self.renderer.flag_show_flap_spoiler
        
    def setShowSpars(self):
        self.renderer.flag_show_spars = not self.renderer.flag_show_spars
    
    def setShowGrid(self):
        self.renderer.flag_show_grid = not self.renderer.flag_show_grid
    
    def setTopView(self):
        self.__setView(True, False, False, False)
        self.__setRotations(0, 0, 0)    
    
    def setFrontView(self):
        self.__setView(False, True, False, False)
        self.__setRotations(90, 0, 270)
    
    def setSideView(self):
        self.__setView(False, False, True, False)
        self.__setRotations(90, 0, 0)       
    
    def set3DView(self):
        self.__setView(False, False, False, True)
        self.__setRotations(45, 0, 315)

    def __setRotations(self, xRot, yRot, zRot):
        self.renderer.xRot = xRot
        self.renderer.yRot = yRot
        self.renderer.zRot = zRot        

    def __setView(self, bool_top, bool_front, bool_side, bool_3d):
        self.renderer.flag_view_top   = bool_top
        self.renderer.flag_view_front = bool_front
        self.renderer.flag_view_side  = bool_side
        self.renderer.flag_view_3d    = bool_3d
    
    
    def __checkAircraft(self, vbool):
        self.renderer.flag_show_fuselage = vbool
        self.renderer.flag_show_wing1_up = vbool
        self.renderer.flag_show_wing1_lo = vbool
        self.renderer.flag_show_wing2_up = vbool
        self.renderer.flag_show_wing2_lo = vbool
        for i in range(5) : 
            self.showOptions[i].setChecked(vbool)
        
    def setShowAircraft(self):
        for i in range(5) : 
            if not self.showOptions[i].isChecked() :
                print self.showOptions[i].isChecked()
                self.__checkAircraft(True) ; return
        self.__checkAircraft(False)
    
    def setShowRibs(self):
        self.renderer.flag_show_ribs = not self.renderer.flag_show_ribs

    def setFlagSelection(self):
        self.renderer.flag_selection = not self.renderer.flag_selection
        self.renderer.selectedPoint = None
        self.renderer.updateLists()
  
    def contextMenuEvent(self, event):
        self.menu.exec_(event.globalPos())

    def createSlider(self, changedSignal, setterSlot):
        slider = QtGui.QSlider(QtCore.Qt.Horizontal)

        slider.setRange(0, 360 * 2)
        slider.setSingleStep(2)
        slider.setPageStep(15 * 2)
        slider.setTickInterval(15 * 2)
        slider.setTickPosition(QtGui.QSlider.TicksRight)

        self.renderer.connect(slider, QtCore.SIGNAL("valueChanged(int)"), setterSlot)
        self.connect(self.renderer, changedSignal, slider, QtCore.SLOT("setValue(int)"))

        return slider

if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = Widget()
    widget.show()
    app.exec_()    