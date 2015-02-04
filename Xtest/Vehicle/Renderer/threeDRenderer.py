import sys
from tiglwrapper   import TiglException
from PySide import QtOpenGL, QtGui, QtCore

from Xtest.Vehicle.vehicleData import VehicleData
from Xtest.Open_GL import utility
from Xtest.Vehicle.point import Point
from Xtest.Vehicle.selectionList import SelectionList

try:
    from OpenGL import GL, GLU, GLUT
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

class ThreeDRenderer(QtOpenGL.QGLWidget):

    def __init__(self, width, height, tixi, tigl, data):
        super(ThreeDRenderer, self).__init__()
        
        self.indexGenerated = QtGui.QAction(self)
        self.before_indexGenerated = QtGui.QAction(self)
        
        
        self.index = -1
        
        # point lists
        self.data = data
        
        # transformations
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.xTrans = 0
        self.yTrans = 0  
        self.aspect = max(self.data.configurationGetLength, self.data.wingspan) / 1.5
        self.scale  = self.aspect # self.data.configurationGetLength / 1.5 # helper for setZoom
        
        self.viewwidth = 0.0
        self.viewheight = 0.0

        # helper
        self.r_color = 0.7
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

        # selection
        self.ctrlIsPressed  = False
        self.selectedPoints = []
        self.selectedPointsCnt = 5*[0]
        self.selectionList = SelectionList()

        # widget option
        #self.setFocusPolicy(QtCore.Qt.ClickFocus)

    def getRenderIndex(self):
        return self.index
    
    def setRenderIndex(self, index):
        self.index = index

    def setRotation(self, angleX, angleY, angleZ):
        self.xRot = self.normalizeAngle(angleX)
        self.yRot = self.normalizeAngle(angleY)
        self.zRot = self.normalizeAngle(angleZ)

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.updateGL()
            
    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)        
        if angle != self.yRot:
            self.yRot = angle
            self.updateGL()   
    
    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)        
        if angle != self.zRot:
            self.zRot = angle
            self.updateGL()    
    
    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 2
        while angle > 360 * 2:
            angle -= 360 * 2
        return angle 
    
    def updateLists(self, data):
        self.data = data
      #  try:
      #      GL.glDeleteLists(self.index, 10)
      #  except:
      #      print "not worked"
        self.initializeGL()
        self.updateGL()

    def initializeGL(self):
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glEnable(GL.GL_LIGHTING)
        GL.glEnable(GL.GL_LIGHT0)
        GL.glEnable(GL.GL_LIGHT1)
        GL.glEnable(GL.GL_NORMALIZE)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)  
                   
        GL.glClearColor (1.0, 1.0, 1.0, 0.0)
        
        self.before_indexGenerated.trigger()
        self.createOglLists()
       # self.indexGenerated.trigger()  
        
    def resizeGL(self, w, h):       
        self.viewwidth  = w
        self.viewheight = h
        
        GL.glViewport(0, 0, self.viewwidth, self.viewheight)
        self.__setProjection()        
        
    def __setProjection(self):
        h  = self.viewheight
        if(h == 0):
            h = 1
        ratio = 1.0* self.viewwidth / h
        
        self.aspect_width = self.aspect*ratio
        
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(-self.aspect_width, self.aspect_width,
                   self.aspect, -self.aspect, -100.0, 100.0)

    def setTransparent(self, value):
        self.alpha_rgb = value

    def paintGL(self):
        self.__setProjection()
        # Clear screen and Z-buffer
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT) 
        
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()   

        #GL.glPolygonMode( GL.GL_FRONT_AND_BACK, GL.GL_LINE )
        # set to center and translate values
        GL.glTranslatef(self.xTrans, self.yTrans, -1.5)
        # GL.glTranslatef(self.data.configurationGetLength/2.0, 0, 0)
        GL.glRotated(self.xRot, 1.0, 0.0, 0.0)
        GL.glRotated(self.yRot, 0.0, 1.0, 0.0)
        GL.glRotated(self.zRot, 0.0, 0.0, 1.0)
        # GL.glTranslatef(-self.data.configurationGetLength/2.0, 0, 0)
        GL.glTranslatef(-self.data.configurationGetLength/2.0, 0, 0) 
          
        if self.flag_show_grid:
            self.drawGrid(self.data.configurationGetLength, -self.data.configurationGetLength)    

        self.drawAircraft() 
       
        GL.glFlush() 

    '''
    generic drawing function
    '''
    def drawAircraft(self):
        if self.flag_show_compnt :
            GL.glColor3fv([1.0, 0.0, 0.0])
            GL.glCallList(self.index+5)

        if self.flag_show_flap_TE_Device :
            GL.glCallList(self.index+6)
        
        if self.flag_show_flap_LE_Device :
            GL.glCallList(self.index+7)
        
        if self.flag_show_flap_spoiler :
            GL.glCallList(self.index+8)            
            
        if self.flag_show_spars :
            GL.glCallList(self.index+9)
        
        if self.flag_show_wing1_up :  
            self.draw(self.data.pList_wing_up, self.data.pList_wing_up_normals, [0.0, 0.5, 0.8,self.alpha_rgb], 1, self.selectionList.wingUpIsEmpty())
            
        if self.flag_show_wing1_lo :
            self.draw(self.data.pList_wing_lo, self.data.pList_wing_lo_normals, [0.0, 0.5, 0.8,self.alpha_rgb], 2, self.selectionList.wingLoIsEmpty())
        
        if self.flag_show_wing2_up :
            self.draw(self.data.pList_wing_up_reflect, self.data.pList_wing_up_reflect_normals, [0.75164, 0.60648, 0.22648,1.0], 3, self.selectionList.wingUpRIsEmpty())
            
        if self.flag_show_wing2_lo :
            self.draw(self.data.pList_wing_lo_reflect, self.data.pList_wing_lo_reflect_normals, [0.75164, 0.60648, 0.22648,1.0], 4, self.selectionList.wingLoRIsEmpty())
        
        if self.flag_show_fuselage :
            self.draw(self.data.pList_fuselage, self.data.pList_fuselage_normals, [0.0, 0.5, 0.8,self.alpha_rgb], 0, self.selectionList.fuseIsEmpty())        
    

    '''
    drawing function for the fuselage. 
    If fuselage segment was selected, a special function will be activated otherwise the ogl list will be drawn
    @param plist: fuselage point list
    @param color: vertex color
    @param idx: index of precompiled ogl list
    '''
    def draw(self, plist, normals, color, idx, normalMode=True):
        if normalMode :
            GL.glColor4fv(color)  
            GL.glCallList(self.index + idx)     
        else:
            GL.glCallList(self.select_index + idx)

    '''
    checks if fuslage segment was selected
    @param plist: fuselage point list
    @param point: selected point
    '''
    def updateOglShapeSelectionList(self, plist, plist_normals, selectionList, color, idx):
        GL.glNewList(self.select_index+idx, GL.GL_COMPILE)
        self.createOglShapeSelection(plist, plist_normals, selectionList, color)
        GL.glEndList()
        
    def createOglShapeSelection(self, plist, plist_normals, selectionList, color):
        GL.glBegin(GL.GL_QUADS)
        for shaIdx in range(len(plist)) :
            segCnt = len(plist[shaIdx])
            for segIdx in range(segCnt) :
                GL.glColor4fv(self.__getSegmentColor(shaIdx, segIdx, selectionList, color)) 
                stripeCnt = len(plist[shaIdx][segIdx])
                for stripeIdx in range(0, stripeCnt) :
                    self.__setVertices(plist, plist_normals, shaIdx, segIdx, stripeIdx, segCnt, stripeCnt)
        GL.glEnd()

    '''
    determines the color of the segment (selected segments will be drawn red)
    '''
    def __getSegmentColor(self, shaIdx, segIdx, selectionList, color):
        pos = -1 ; i = 0
        for p in selectionList :
            if segIdx == p.getSegmentIdx() and shaIdx == p.getShapeIdx() :
                if pos == -1 :  pos = i
                else : 
                    del selectionList[i]
                    del selectionList[pos]
                    return color
            i += 1
        if pos == -1 : return color
        else : return [1.0, 0.0, 0.0, self.alpha_rgb]


    '''
    checks if fuslage segment was selected
    @param plist: fuselage point list
    @param point: selected point
    '''
    def __getSelectedSegment(self, plist, point):
        for shaIdx in range(len(plist)) :
            segCnt = len(plist[shaIdx])
            for segIdx in range(segCnt) :
                stripeCnt = len(plist[shaIdx][segIdx])
                for stripeIdx in range(stripeCnt) :
                    stripe1 = plist[shaIdx][segIdx][stripeIdx]
                    (se , st) = (segIdx , stripeIdx+1) if stripeIdx +1 < stripeCnt else (segIdx+1 , 0)
                    if se >= segCnt : break
                    stripe2 = plist[shaIdx][se][st]
                    for i in range(0, len(plist[shaIdx][segIdx][stripeIdx])-1) :  
                        if(utility.isPinRectangle([stripe1[i], 
                                                   stripe2[i], 
                                                   stripe2[i+1], 
                                                   stripe1[i+1]], point)) :
                            return (shaIdx, segIdx) 
        return (None, None)

    '''
    drawing function for the wings
    @param plist: wing point list
    @param color: vertex color
    @param idx: index of precompiled ogl list
    @param reflect: 1 for not reflected, -1 for reflected
    '''
    def __getSelectedWingSegment(self, plist, point, reflect=1):
        for shaIdx in range(1 ,len(plist)+1):
            segIdx = self.isWingSegmentSelected(shaIdx, point, reflect) 
            if segIdx != -1 :
                return (shaIdx-1, segIdx-1)
        return (None, None)
    
    '''
    checks if wing segment was selected
    @param wingIdx: index of a wing
    @param point: selected point
    @param reflect: 1 for not reflected, -1 for reflected
    '''
    def isWingSegmentSelected(self, wingIdx, point, reflect=1):
        segIdx = -1
        try:
            segIdx, _, _, _ = self.data.tigl.wingGetSegmentEtaXsi(wingIdx, point[0], reflect*point[1], point[2])
        except TiglException as e :
            print ("selection failed : " , e.error)
        return segIdx

    '''
    drawing function if selection was activated
    @param plist: given point list
    @param color: vertex color
    @param shapeIndex: index of the shape which should be drawn
    @param segmentIndex: index of the segment which should be drawn
    '''
    def drawInSelectionMode(self, plist, normals, color, shapeIndex, segmentIndex):
        GL.glColor4fv(color)
        GL.glBegin(GL.GL_QUADS)
        for shapeIdx in range(len(plist)) :
            for segIdx in range(len(plist[shapeIdx])) :
                if(shapeIdx == shapeIndex and segIdx == segmentIndex):
                    self.__drawSegment(plist[shapeIdx][segIdx], normals[shapeIdx][segIdx], [1.0, 0.0, 0.0, self.alpha_rgb], color)
                else:
                    self.__drawSegment(plist[shapeIdx][segIdx], normals[shapeIdx][segIdx],color, color)
        GL.glEnd()
        
    '''
    special segment drawing function
    @param plist: given point list
    @param color_new: selection of color for the selected segment
    @param color_old: default shape color
    '''        
    def __drawSegment(self, plist, normals, color_new, color_old):
        GL.glColor4fv(color_new)
        for stripeIdx in range(len(plist)-1) :
            stripe1 = plist[stripeIdx]
            stripe2 = plist[stripeIdx+1]
            for i in range(len(stripe1)-1) :
                GL.glNormal3fv(normals[stripeIdx][i])
                GL.glVertex3fv(stripe1[i])
                
                GL.glNormal3fv(normals[stripeIdx+1][i])
                GL.glVertex3fv(stripe2[i])
                
                GL.glNormal3fv(normals[stripeIdx+1][i+1])
                GL.glVertex3fv(stripe2[i+1])
                
                GL.glNormal3fv(normals[stripeIdx][i+1])
                GL.glVertex3fv(stripe1[i+1])
        GL.glColor4fv(color_old)

    '''
    precompile all point lists
    '''               
    def createOglLists(self): 
        if self.index < 0:
            self.index = GL.glGenLists(10)
        
        GL.glNewList(self.index, GL.GL_COMPILE) # compile the first one
        self.createOglShape(self.data.pList_fuselage, self.data.pList_fuselage_normals)
        GL.glEndList()

        GL.glNewList(self.index+1, GL.GL_COMPILE)
        self.createOglShape(self.data.pList_wing_up, self.data.pList_wing_up_normals)
        GL.glEndList()

        GL.glNewList(self.index+2, GL.GL_COMPILE)
        self.createOglShape(self.data.pList_wing_lo, self.data.pList_wing_lo_normals)
        GL.glEndList()

        # draw reflect upper wing
        GL.glNewList(self.index+3, GL.GL_COMPILE)
        self.createOglShape(self.data.pList_wing_up_reflect, self.data.pList_wing_up_reflect_normals)
        GL.glEndList()

        GL.glNewList(self.index+4, GL.GL_COMPILE)
        self.createOglShape(self.data.pList_wing_lo_reflect, self.data.pList_wing_lo_reflect_normals)
        GL.glEndList()

        GL.glNewList(self.index+5, GL.GL_COMPILE)
        self.createOglComponentSegment(self.data.pList_component_segment)
        GL.glEndList()

        GL.glNewList(self.index+6, GL.GL_COMPILE)
        self.createOglFlaps(self.data.pList_flaps_TEDevice, self.data.pList_flaps_TE_normals, 0.04)
        GL.glEndList()

        GL.glNewList(self.index+7, GL.GL_COMPILE)
        self.createOglFlaps(self.data.pList_flaps_LEDevice, self.data.pList_flaps_LE_normals, 0.06)
        GL.glEndList()

        GL.glNewList(self.index+8, GL.GL_COMPILE)
        self.createOglFlaps(self.data.pList_flaps_Spoiler, self.data.pList_flaps_Spoiler_normals, 0.08)
        GL.glEndList()

        GL.glNewList(self.index+9, GL.GL_COMPILE)
        self.createOglSpars(self.data.pList_spares)
        GL.glEndList()

    '''
    draw grid
    @param start: right/up delimiter
    @param end: left/bottom delimiter
    '''        
    def drawGrid(self, start = 2, end = -2):
        start *= self.aspect
        end = -start
        # Draw a grid "floor".
        GL.glColor3f(1.0, 0.0, 1.0);
        GL.glBegin(GL.GL_LINES)
        i = end
        
        while i <= start :
            GL.glVertex3f(i, start, 0); GL.glVertex3f(i, end, 0)
            GL.glVertex3f(start, i, 0); GL.glVertex3f(end, i, 0)
            i += start / 8.0
        GL.glEnd()


    '''
    creates component segment ogl list
    @param plist: given point list
    @param color: vertex color
    '''
    def createOglComponentSegment(self, plist):
        GL.glBegin(GL.GL_LINES)
        for sha in plist :
            for seg in sha :
                for stripe in seg :
                    for p in stripe :
                        GL.glVertex3fv(p)
        GL.glEnd()
    
    
    '''
    creates shape ogl list
    @param plist: given point list
    @param plist_normals: per vertex normals
    @param color: vertex color
    '''
    def createOglShape(self, plist, plist_normals):
        GL.glBegin(GL.GL_QUADS)
        for shaIdx in range(0, len(plist)) :
            segCnt = len(plist[shaIdx])
            for segIdx in range(segCnt) :
                stripeCnt = len(plist[shaIdx][segIdx])
                for stripeIdx in range(0, len(plist[shaIdx][segIdx])) :
                    self.__setVertices(plist, plist_normals, shaIdx, segIdx, stripeIdx, segCnt, stripeCnt) 
        GL.glEnd()
    
    '''
    creates flaps ogl list
    @param plist: given point list
    @param offset: offset to prevent z-fighting
    '''
    '''
    creates flaps ogl list
    @param plist: given point list
    @param offset: offset to prevent z-fighting
    '''
    def createOglFlaps(self, pList, norm, offset):
        GL.glBegin(GL.GL_QUADS)
        for shaIdx in range(len(pList)) :
            for segIdx in range(len(pList[shaIdx])) :
                for flapIdx in range(len(pList[shaIdx][segIdx])) :
                    color = self.newColorVec()
                    GL.glColor3fv(color)
                    p = pList[shaIdx][segIdx][flapIdx]
                    n = norm[shaIdx][segIdx][flapIdx]
                    
                    GL.glNormal3fv(n[0])
                    GL.glVertex3f(p[0][0], p[0][1], p[0][2] + offset)
                    
                    GL.glNormal3fv(n[1])
                    GL.glVertex3f(p[1][0], p[1][1], p[1][2] + offset)
                    
                    GL.glNormal3fv(n[3])
                    GL.glVertex3f(p[3][0], p[3][1], p[3][2] + offset)
                    
                    GL.glNormal3fv(n[2])
                    GL.glVertex3f(p[2][0], p[2][1], p[2][2] + offset)
        GL.glEnd()
        
    '''
    creates spars ogl list
    @param plist: given point list
    '''        
    def createOglSpars(self, pList):
        for sha in pList :
            for seg in sha :
                for spares in seg :  
                    GL.glColor3fv(self.newColorVec())      
                    GL.glBegin(GL.GL_LINE_STRIP)       
                    for vert in spares :
                        GL.glVertex3fv(vert) 
                    GL.glEnd()


    def __setVertices(self, plist, plist_normals, shaIdx, segIdx, stripeIdx, segCnt, stripeCnt):
        (tmp_seg , tmp_stripe) = (segIdx , stripeIdx+1) if stripeIdx +1 < stripeCnt else (segIdx+1 , 0)
        if tmp_seg >= segCnt : return
        for i in range(0, len(plist[shaIdx][segIdx][stripeIdx])-1) :
            j = (i+1)
            p1 = plist[shaIdx][segIdx][stripeIdx][i]
            p2 = plist[shaIdx][tmp_seg][tmp_stripe][i]
            p3 = plist[shaIdx][tmp_seg][tmp_stripe][j] 
            p4 = plist[shaIdx][segIdx][stripeIdx][j]

            n1 = plist_normals[shaIdx][segIdx][stripeIdx][i]
            n2 = plist_normals[shaIdx][tmp_seg][tmp_stripe][i]
            n3 = plist_normals[shaIdx][tmp_seg][tmp_stripe][j] 
            n4 = plist_normals[shaIdx][segIdx][stripeIdx][j]                        
                        
            GL.glNormal3fv(n1)
            GL.glVertex3fv(p1)

            GL.glNormal3fv(n2)
            GL.glVertex3fv(p2)
                        
            GL.glNormal3fv(n3)
            GL.glVertex3fv(p3)
                        
            GL.glNormal3fv(n4)
            GL.glVertex3fv(p4)         
        
    # =========================================================================================================
    # =========================================================================================================    
    # code selection
    # =========================================================================================================  
    # =========================================================================================================                

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
        
        return point

    def keyPressEvent(self, event):
        if event.modifiers() == QtCore.Qt.ControlModifier:
            self.ctrlIsPressed = True
            self.updateGL()
    
    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_Control :
            self.ctrlIsPressed = False
            self.updateGL()
            
    def mousePressEvent(self, event):  
        self.lastPos_x = event.pos().x()
        self.lastPos_y = event.pos().y()
        
        if self.ctrlIsPressed:
            selectedPoint = self.__winPosTo3DPos(self.lastPos_x, self.lastPos_y)

            (shaIdx, segIdx) = self.__getSelectedSegment(self.data.pList_fuselage, selectedPoint)
            if shaIdx is not None :
                self.selectionList.addPointToFuse(Point(shaIdx, segIdx, selectedPoint))
                self.updateOglShapeSelectionList(self.data.pList_fuselage, self.data.pList_fuselage_normals, self.selectionList.fuselist, [0.0, 0.5, 0.8,self.alpha_rgb], 0)
                self.updateGL()
            else:    
                (shaIdx, segIdx) = self.__getSelectedWingSegment(self.data.pList_wing_up, selectedPoint)
                if shaIdx is not None :
                    self.selectionList.addPointToWingUp(Point(shaIdx, segIdx, selectedPoint))
                    self.updateOglShapeSelectionList(self.data.pList_wing_up, self.data.pList_wing_up_normals, self.selectionList.wing_up, [0.0, 0.5, 0.8,self.alpha_rgb], 1)
                    self.updateGL()
                else:
                    (shaIdx, segIdx) = self.__getSelectedWingSegment(self.data.pList_wing_lo, selectedPoint)
                    if shaIdx is not None :
                        self.selectionList.addPointToWingLo(Point(shaIdx, segIdx, selectedPoint))
                        self.updateOglShapeSelectionList(self.data.pList_wing_lo, self.data.pList_wing_lo_normals, self.selectionList.wing_lo, [0.0, 0.5, 0.8,self.alpha_rgb], 2)
                        self.updateGL()            
                    else:
                        (shaIdx, segIdx) = self.__getSelectedWingSegment(self.data.pList_wing_up_reflect, selectedPoint, -1)
                        if shaIdx is not None :
                            self.selectionList.addPointToWingUpRefl(Point(shaIdx, segIdx, selectedPoint))
                            self.updateOglShapeSelectionList(self.data.pList_wing_up_reflect, self.data.pList_wing_up_reflect_normals, self.selectionList.wing_up_r, [0.75164, 0.60648, 0.22648,self.alpha_rgb], 3)
                            self.updateGL()     
                        else :
                            (shaIdx, segIdx) = self.__getSelectedWingSegment(self.data.pList_wing_lo_reflect, selectedPoint, -1)
                            if shaIdx is not None :
                                self.selectionList.addPointToWingLoRefl(Point(shaIdx, segIdx, selectedPoint))
                                self.updateOglShapeSelectionList(self.data.pList_wing_lo_reflect, self.data.pList_wing_lo_reflect_normals, self.selectionList.wing_lo_r, [0.75164, 0.60648, 0.22648,self.alpha_rgb], 4)
                                self.updateGL() 
        elif not self.selectionList.isEmpty() :
            self.selectionList.removeAll()
            self.updateGL()
    
    def mouseMoveEvent(self, event):
        dx = (event.x() - self.lastPos_x ) 
        dy = (event.y() - self.lastPos_y ) 
        
        self.lastPos_x += dx
        self.lastPos_y += dy

        #Betrachtsfeld = -aspect bis aspect
        
        oglXunit = 2.0 * self.aspect_width
        oglYunit = 2.0 * self.aspect
        
        # pixel real world to Pixel ogl world 
        oglXTrans = oglXunit * 1.0 / self.viewwidth
        oglYTrans = oglYunit * 1.0 / self.viewheight
        
        self.xTrans += (dx * oglXTrans) 
        self.yTrans += (dy * oglYTrans)

        self.updateGL()

       
    def newColorVec(self):   
        color = [self.r_color, self.g_color, self.b_color]
        
        offset = 0.5
        self.b_color += offset
        
        if self.b_color >= 1.0 : 
            self.g_color += offset ; self.b_color = 0.0
        if self.g_color >= 1.0 :
            self.r_color += offset ; self.g_color = 0.0
        if self.r_color >= 1.0 :
            self.r_color = 0.0 ; self.g_color = 0.0 ; self.b_color = 0.0
            
        return color        
