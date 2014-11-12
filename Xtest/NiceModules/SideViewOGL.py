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

    glMode = {"GL_POINTS" : GL.GL_POINTS, "GL_LINES" : GL.GL_LINES, "GL_LINE_STRIP" : GL.GL_LINE_STRIP, "GL_LINE_LOOP" : GL.GL_LINE_LOOP , "GL_QUADS" : GL.GL_QUADS, "GL_QUAD_STRIP" : GL.GL_QUAD_STRIP}
    
    def __init__(self, width, height):

        self.tixi = Tixi()
        self.tixi.open('simpletest.cpacs.xml')
        self.tixi.open('D150_CPACS2.0_valid.xml')
        
        self.tigl = Tigl()
        try:
            self.tigl.open(self.tixi,"")
        except TiglException as err:    
            print 'Error opening tigl document: ', err.__str__()
           
        self.pList_fuselage = self.createFuselage() 
        self.pList_wing_up, self.pList_wing_lo = self.createWing()
        self.pList_component_segment = self.createComponent()
        self.pList_flaps = self.createFlaps()
        
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
       # GL.glEnable(GL.GL_LIGHTING)
        
       # GL.glEnable(GL.GL_LIGHT0)
        GL.glEnable(GL.GL_NORMALIZE)
        GL.glShadeModel(GL.GL_SMOOTH)
        GL.glClearColor (1.0, 1.0, 1.0, 0.0)
        self.initLight()

    def resize(self, w, h):
        side = min(w, h)
        self.viewwidth = side
        self.viewheight = side
        
        GL.glViewport((w - side) / 2, (h - side) / 2, self.viewwidth, self.viewheight)

        self.__setProjection()        
        
    def __setProjection(self):
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
       
        GL.glOrtho(-1.0 * self.aspect * self.scale, +1.0 * self.aspect * self.scale,
                    +1.0* self.aspect * self.scale, -1.0* self.aspect * self.scale, -10.0, 30.0)

    def display(self):
        self.__setProjection()
        #GL.glMatrixMode(GL.GL_PROJECTION)
        #GL.glLoadIdentity()
        # Clear screen and Z-buffer
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT) 
        
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()         
        #self.initLight()
        GL.glTranslatef(self.xTrans,self.yTrans,-1.5)
       # GL.glPushMatrix()
        GL.glRotated(self.xRot, 1.0, 0.0, 0.0)
        GL.glRotated(self.yRot, 0.0, 1.0, 0.0)
        GL.glRotated(self.zRot, 0.0, 0.0, 1.0)
        
        self.draw()
        #GL.glPopMatrix()
        
        #self.initLight()
        #self.drawTestObject()
        #GL.glShadeModel(GL.GL_FLAT)
        #GLUT.glutInit()#
        #GLUT.glutSolidSphere(0.5,40,40)
        
        GL.glFlush() 


    def draw(self):
        # draw upper
        self.drawShape(self.pList_wing_up, [0.0, 0.44, 0.67, 0.5], Renderer.glMode["GL_QUADS"], 1, False)
        # draw lower
        #self.drawShape(self.pList_wing_lo, [0.0, 0.44, 0.67, 0.5], Renderer.glMode["GL_QUADS"], 1, False)

        # draw reflect upper
        #self.drawShape(self.pList_wing_up, [0.76, 0.79, 0.50, 0.5], Renderer.glMode["GL_QUADS"], -1, False)
        # draw reflect lower
        #self.drawShape(self.pList_wing_lo, [0.76, 0.79, 0.50, 0.5], Renderer.glMode["GL_QUADS"], -1, False)
        
        # draw fuselage
        #self.drawShape(self.pList_fuselage, [0.0, 0.44, 0.67], Renderer.glMode["GL_QUADS"], 1, False)

        # draw ComponentSegment
        #self.drawShape(self.pList_component_segment, [1.0, 0.0, 0.0], Renderer.glMode["GL_POINTS"], 1, False)
        #self.drawShape(self.pList_component_segment, [1.0, 0.0, 0.0], Renderer.glMode["GL_LINES"], 1, True)
#        self.drawShape(self.pList_component_segment, [1.0, 0.0, 0.0], Renderer.glMode["GL_QUAD_STRIP"], 1, True)

        # draw Flaps
        self.drawFlaps(self.pList_flaps)
        #self.drawShape(self.pList_flaps, [1.0,0.0,0.2], Renderer.glMode["GL_POINTS"], 1, False)

        # draw Points
        GL.glPointSize(6)
        GL.glColor3f(1, 0, 1)
        #self.drawShape(self.pList_wing_up, [1.0, 0.0, 1.0], Renderer.glMode["GL_POINTS"])


    '''
    @param reflect: normal mode set 1 , reflect mode set -1
    @param flag_strip: strip mode set True , not strip set False
    '''
    def drawShape(self, pList, color, glMode, reflect=1, flag_Strip=False):
        GL.glColor3f(color[0], color[1], color[2])
        
        quad = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
        
        GL.glBegin(glMode)
        for shape in pList :
            normals = self.calculateNormal(shape)
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
                    
                    #GL.glNormal3f(normals[i][j+1][0], normals[i][j+1][1], normals[i][j+1][2])
                    GL.glVertex3f(quad[0][0], quad[0][1], quad[0][2])

                    GL.glNormal3f(normals[i][j][0], reflect * normals[i][j][1], normals[i][j][2])
                    GL.glVertex3f(quad[1][0], quad[1][1], quad[1][2])                     
                   
                    #GL.glNormal3f(normals[i+1][j+1][0], normals[i+1][j+1][1], normals[i+1][j+1][2])
                    GL.glVertex3f(quad[2][0], quad[2][1], quad[2][2])                     
                    
                    # GL.glNormal3f(normals[i][j][0], reflect * normals[i][j][1], normals[i][j][2])
                    #GL.glNormal3f(0.0, -1.0, 0.0)
                    GL.glVertex3f(quad[3][0], quad[3][1], quad[3][2])     
                #break 
            #break               
        GL.glEnd() 


    def calculateNormal(self, plist):
        n = len(plist)
        m = len(plist[0])
        plist_n = []
        for i in range(n) :
            normal_tmp = []
            for j in range(m):
                n1 = [0.0, 0.0, 0.0] if j<=0   or i<=0   else self.calculateVertexNormal(plist[i][j], plist[i][j-1], plist[i-1][j])
                n2 = [0.0, 0.0, 0.0] if j+1>=m or i<=0   else self.calculateVertexNormal(plist[i][j], plist[i-1][j], plist[i][j+1])
                n3 = [0.0, 0.0, 0.0] if j+1>=m or i+1>=n else self.calculateVertexNormal(plist[i][j], plist[i][j+1], plist[i+1][j])
                n4 = [0.0, 0.0, 0.0] if j<=0   or i+1>=n else self.calculateVertexNormal(plist[i][j], plist[i+1][j], plist[i][j-1])
                
                n1 = self.normalised(n1)
                n2 = self.normalised(n2)
                n3 = self.normalised(n3)
                n4 = self.normalised(n4)
                
                normal = [n1[0] + n2[0] + n3[0] + n4[0] , n1[1] + n2[1] + n3[1] + n4[1] , n1[2] + n2[2] + n3[2] + n4[2]]
                normal_tmp.append(normal)
            plist_n.append(normal_tmp)
        return plist_n


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
    
    
    def lenVector(self, v):
        import math
        return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
    
    def normalised(self, v):
        l = self.lenVector(v)
        if l == 0.0 :
            return [0.0, 0.0, 0.0]
        else :
            return [v[0] / l, v[1] / l, v[2] / l]

    
    def initLight(self):
        # mat_ambient   = [0.4, 0.4, 0.4, 1.0] 
        mat_ambient    = [0.6, 0.6, 0.6, 1.0]
        mat_diffuse    = [0.4, 0.8, 0.4, 1.0] 
        mat_specular   = [1.0, 1.0, 1.0, 1.0]
        light_position = [0.0, 0.0, 0.0, 1.0]        

        # GL_LIGHT_MODEL_AMBIENT, GL_LIGHT_MODEL_LOCAL_VIEWER,' GL_LIGHT_MODEL_TWO_SIDE und GL_LIGHT_MODEL_COLOR_CONTROL
        GL.glLightModelfv(GL.GL_LIGHT_MODEL_AMBIENT, mat_ambient)
        # Diffuse (non-shiny) light component
        # GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, mat_diffuse)
        # Specular (shiny) light component
        #GL.glLightfv(GL.GL_LIGHT0, GL.GL_SPECULAR, mat_specular)
        
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, light_position)
        
        # The color of the sphere
        mat_materialColor = [0.2, 0.2, 1.0, 1.0]
        # The specular (shiny) component of the material
        mat_materialSpecular = [1.0, 1.0, 1.0, 1.0]
        # The color emitted by the material
        mat_materialEmission = [0, 0, 0, 1.0]
        #The shininess parameter
        mat_shininess  = 0.4 

        mat_ambient    = [0.24725,  0.1995, 0.0745, 1.0]
        mat_diffuse    = [0.75164, 0.60648, 0.22648, 1.0] 
        mat_specular   = [0.628281, 0.555802, 0.366065, 1.0]

        GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_AMBIENT, mat_ambient)
        GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_DIFFUSE, mat_diffuse)
        GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_SPECULAR, mat_specular)
        # GL.glMaterialfv(GL.GL_FRONT, GL.GL_EMISSION, mat_materialEmission)
        GL.glMaterialf(GL.GL_FRONT_AND_BACK, GL.GL_SHININESS, mat_shininess * 128)
    
    

    def drawFlaps(self, pList):
        GL.glColor3f(1.0,0.0,0.0)
        GL.glBegin(GL.GL_QUADS)
        
   #[[17.68372701659183, 1.8765691482297777, -1.3069431052896983], [17.662468281759608, 5.527072040668436, -0.9866284398469685]], [[17.662468281759608, 5.527072040668436, -0.9866284398469685], [20.15654040781586, 12.86990035947941, -0.4309175416085875]], [[20.224287216747996, 13.070573928438826, -0.41571594839042747], [21.414546358878717, 16.22662187664191, -0.18099399010930795]]]], [[[[34.02616147364511, 0.9959919678379325, 0.7842753561486957], [36.076928226508294, 5.9137023090377285, 1.2145192615078817]]]], [[[[33.59940406560077, -0.0020029219731199674, 1.8052095077496109], [36.26958618318385, -0.00200292197312204, 7.219940415966675]]
        
        a = 0.2
        b = 0.2
        c = 0.2
        
        for shape in pList :
            for segments in shape :
                for flaps in segments :
                    list1 = flaps[0]
                    list2 = flaps[1]
                    list3 = flaps[2]
                    list4 = flaps[3]
                    GL.glColor(a,b,c)
                    print list1
                    print list2
                    print list3
                    print list4
                    GL.glVertex3fv(list1)
                    GL.glVertex3fv(list2)
                    GL.glVertex3fv(list4)
                    GL.glVertex3fv(list3)
                    
                    if a >= 1.0:
                        b += 0.2
                    else :
                        a += 0.2
        GL.glEnd()
        
        
   


    def createComponent(self, point_cnt_eta = 10, point_cnt_xsi = 10):
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
            print "ComponentList:"
            print plistComp
        return plistComp
        
        
    def createFlaps(self, point_cnt_eta = 10, point_cnt_xsi = 10):    
        plistWing = []
        for wingIndex in range(1, self.tigl.getWingCount()+1) :
            plistSeg = []
            for compSegmentIndex in range(1, self.tigl.wingGetComponentSegmentCount(wingIndex)+1) : 
                componentSegmentUID = self.tigl.wingGetComponentSegmentUID(wingIndex, compSegmentIndex)
                flapList = self.__createFlaps(wingIndex, compSegmentIndex)
                plistFlaps = []
                for flap in flapList : 
                    x1, y1, z1 = self.tigl.wingComponentSegmentGetPoint(componentSegmentUID, flap[0], flap[2])       
                    x2, y2, z2 = self.tigl.wingComponentSegmentGetPoint(componentSegmentUID, flap[1],     1.0) 
                    x3, y3, z3 = self.tigl.wingComponentSegmentGetPoint(componentSegmentUID, flap[3], flap[5]) 
                    x4, y4, z4 = self.tigl.wingComponentSegmentGetPoint(componentSegmentUID, flap[4],     1.0) 
                    plistFlap = [[x1, y1, z1], [x2, y2, z2], [x3, y3, z3], [x4, y4, z4]]
                    plistFlaps.append(plistFlap)
                plistSeg.append(plistFlaps)
            plistWing.append(plistSeg)      
            
        print "FlapList:"
        print   plistWing  
        return plistWing           
        
    def __createFlaps(self, wingIndex, compSegmentIndex):
        path_TE_Devices = '/cpacs/vehicles/aircraft/model/wings/wing['+str(wingIndex)+']/componentSegments/componentSegment['+str(compSegmentIndex)+']/controlSurfaces/trailingEdgeDevices'
        te_devices = []
        for _TE_Devices_Idx in range(1, self.tixi.getNumberOfChilds(path_TE_Devices)+1) :
            path_in  = path_TE_Devices + '/trailingEdgeDevice[' + str(_TE_Devices_Idx) + ']/outerShape/innerBorder'
            path_out = path_TE_Devices + '/trailingEdgeDevice[' + str(_TE_Devices_Idx) + ']/outerShape/outerBorder'
                    
            etaLE_in = self.tixi.getDoubleElement(path_in + '/etaLE')
            etaTE_in = self.tixi.getDoubleElement(path_in + '/etaTE')
            xsiLE_in = self.tixi.getDoubleElement(path_in + '/xsiLE')
                    
            etaLE_out = self.tixi.getDoubleElement(path_out + '/etaLE')
            etaTE_out = self.tixi.getDoubleElement(path_out + '/etaTE')
            xsiLE_out = self.tixi.getDoubleElement(path_out + '/xsiLE')
                    
            te_devices.append([etaLE_in, etaTE_in, xsiLE_in, etaLE_out, etaTE_out, xsiLE_out])
        return te_devices
    
    
    def __createFlaps2(self):
        plistWing = []
        for wingIndex in range(1, self.tigl.getWingCount()+1) :
            plistCompSeg = []
            for compSegmentIndex in range(1, self.tigl.wingGetComponentSegmentCount(wingIndex)+1) : 
                path_TE_Devices = '/cpacs/vehicles/aircraft/model/wings/wing['+str(wingIndex)+']/componentSegments/componentSegment['+str(compSegmentIndex)+']/controlSurfaces/trailingEdgeDevices'
                for _TE_Devices_Idx in range(1, self.tixi.getNumberOfChilds(path_TE_Devices)+1) :
                    path_in  = path_TE_Devices + '/trailingEdgeDevice[' + str(_TE_Devices_Idx) + ']/outerShape/innerBorder'
                    path_out = path_TE_Devices + '/trailingEdgeDevice[' + str(_TE_Devices_Idx) + ']/outerShape/outerBorder'
                    
                    etaLE_in = self.tixi.getDoubleElement(path_in + '/etaLE')
                    etaTE_in = self.tixi.getDoubleElement(path_in + '/etaTE')
                    xsiLE_in = self.tixi.getDoubleElement(path_in + '/xsiLE')
                    
                    etaLE_out = self.tixi.getDoubleElement(path_out + '/etaLE')
                    etaTE_out = self.tixi.getDoubleElement(path_out + '/etaTE')
                    xsiLE_out = self.tixi.getDoubleElement(path_out + '/xsiLE')
                    
                    plistCompSeg.append([etaLE_in, etaTE_in, xsiLE_in, etaLE_out, etaTE_out, xsiLE_out])
            plistWing.append(plistCompSeg)           
        
        
    def createFuselage(self, point_cnt_eta = 2, point_cnt_zeta = 10):
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


    def createWing(self, point_cnt_eta = 3, point_cnt_xsi = 20):
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
        offset_scale = 0.2
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