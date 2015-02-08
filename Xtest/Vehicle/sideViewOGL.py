'''
Created on Jul 30, 2014

@author: fran_re
'''

import sys
from tiglwrapper   import TiglException
from PySide import QtOpenGL, QtGui, QtCore

from Xtest.Vehicle.vehicleData import VehicleData
from Xtest import utility
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

class Renderer(QtOpenGL.QGLWidget):

    def __init__(self, width, height, tixi, tigl, data):
        super(Renderer, self).__init__()
        
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

        # view flags
        self.flag_view_3d             = False
        self.flag_view_side           = False
        self.flag_view_front          = False
        self.flag_view_top            = False 
           
        # selection
        self.ctrlIsPressed  = False
        self.selectedPoints = []
        self.selectedPointsCnt = 5*[0]
        self.selectionList = SelectionList()

        # widget option
        self.setFocusPolicy(QtCore.Qt.ClickFocus)

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
        self.createOglLists()
        #self.updateGL()

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
        
        self.createOglLists()
        
    def resizeGL(self, w, h):       
        side = min(w, h)
        self.viewwidth = w#side
        self.viewheight =h# side
        
        #GL.glViewport((w - side) / 2, (h - side) / 2, self.viewwidth, self.viewheight)
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
          
        self.drawAircraft()    
        if self.flag_show_grid:
            self.drawGrid(self.data.configurationGetLength, -self.data.configurationGetLength)    
       
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
        self.index = GL.glGenLists(10)
        self.select_index = GL.glGenLists(5)
        
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


#===============================================================================
#     def initLight(self):
#         light_ambient = [0.24725  , 0.1995, 0.0745, 1.0]
#         light_diffuse = [0.0, 1.0, 1.0, 1.0 ]
#         light_specular = [0.628281 ,    0.555802 ,    0.366065, 1.0]
#         light_position = [0.0, 0.0, 0.0, 1.0]
# 
#         GL.glLightfv(GL.GL_LIGHT0, GL.GL_AMBIENT, light_ambient)
#         GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, light_diffuse)
#         GL.glLightfv(GL.GL_LIGHT0, GL.GL_SPECULAR, light_specular)
#         GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, light_position)
#===============================================================================
 

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
                

class MainWidget(QtGui.QMainWindow):
    def __init__(self, tixi, tigl, parent = None):
        super(MainWidget, self).__init__(parent)    
        
        # data points
        self.data = VehicleData(tixi, tigl)
        
        self.plotWidgets = [Widget("Front", tixi, tigl, self.data), Widget("Top", tixi, tigl, self.data),
                            Widget("Side", tixi, tigl, self.data), Widget("3D", tixi, tigl, self.data)]

        self.dockList = []
        
        for widget in self.plotWidgets :
            self.addSimpleWidget(widget.getTitle(), widget)

    def addSimpleWidget(self, name, widget):
        dock = QtGui.QDockWidget(name)
        dock.setWidget(widget)
        #dock.setMinimumWidth(100)
        dock.setMinimumHeight(150)
        
        dock.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        dock.setFeatures(QtGui.QDockWidget.DockWidgetClosable |
                         QtGui.QDockWidget.DockWidgetMovable |
                         QtGui.QDockWidget.DockWidgetFloatable)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
        
    def updateView(self):
        self.data.updateTixiTiglData()
        for plotWidget in self.plotWidgets :
            plotWidget.renderer.updateLists(self.data)

                
class Widget(QtGui.QWidget):
    def __init__(self,name, tixi, tigl, data, parent = None):
        super(Widget, self).__init__(parent)
        
        # window preferences
        self.width = 300
        self.height = 300
        self.resize(self.width ,self.height)
        
        self.title = name
        
        # objects
        self.renderer = Renderer(self.width ,self.height, tixi, tigl, data)
        
        # window elements
        self.xSlider = self.createSlider(self.renderer.setXRotation)
        self.ySlider = self.createSlider(self.renderer.setYRotation)
        self.zSlider = self.createSlider(self.renderer.setZRotation)           
  
        label1 = QtGui.QLabel("opacity")
        label2 = QtGui.QLabel("xRot")
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
        zoom.setRange(1, 100)
        zoom.setSingleStep(1)
        zoom.setSuffix('%')
        zoom.setValue(50)        
        zoom.valueChanged.connect(self.setZoom)      

        grid = QtGui.QGridLayout()
        grid.addWidget(transparency, 1,0)
        grid.addWidget(label1,       1,1)
        grid.addWidget(zoom,         1,2)
        grid.addWidget(label5,       1,3)

        grid.addWidget(self.xSlider ,1, 4)
        grid.addWidget(self.ySlider ,1, 6)
        grid.addWidget(self.zSlider ,1, 8)        
        grid.addWidget(label2       ,1, 5)
        grid.addWidget(label3       ,1, 7)
        grid.addWidget(label4       ,1, 9)        


        grid.addWidget(self.renderer,4,0,1,10)

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
 
    def getTitle(self):
        return self.title
 
    def setTransparency(self, value):
        self.renderer.setTransparent(1.0 - value/100.0)
        self.renderer.updateGL()
        
    def setZoom(self, value):
        # slider range 1 to 100, therefor 50 is the center
        self.renderer.aspect = self.renderer.scale * ( (50.0-value) * 9.0/500.0 +1.0 )
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
        self.renderer.setXRotation(xRot)
        self.renderer.setYRotation(yRot)
        self.renderer.setZRotation(zRot)

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
                print ("setShowAircraft" , self.showOptions[i].isChecked())
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

    def createSlider(self, setterSlot):
        slider = QtGui.QSpinBox()
        slider.setRange(0, 360)
        slider.setSingleStep(5)
        slider.valueChanged.connect(setterSlot)
        return slider

if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = MainWidget()
    widget.show()
    app.exec_()