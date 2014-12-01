'''
Created on Jul 30, 2014

@author: fran_re
'''

import sys

from tiglwrapper import Tigl, TiglException
from tixiwrapper import Tixi
from PySide import QtOpenGL, QtGui, QtCore
from Xtest.Open_GL import utility
import numpy as np

try:
    from OpenGL import GL
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

class Renderer(QtOpenGL.QGLWidget):

    glMode = {"GL_POINTS" : GL.GL_POINTS, "GL_LINES" : GL.GL_LINES, "GL_LINE_STRIP" : GL.GL_LINE_STRIP, "GL_LINE_LOOP" : GL.GL_LINE_LOOP , "GL_QUADS" : GL.GL_QUADS, "GL_QUAD_STRIP" : GL.GL_QUAD_STRIP}
    
    def __init__(self, width, height):
        super(Renderer, self).__init__()
        
        self.tixi = Tixi()
        self.tixi.open('simpletest.cpacs.xml')
        #self.tixi.open('D150_CPACS2.0_valid.xml')
        
        self.tigl = Tigl()
        try:
            self.tigl.open(self.tixi,"")
        except TiglException as err:    
            print 'Error opening tigl document: ', err.__str__()
           
        self.pList_fuselage                    = self.createFuselage() 
        self.pList_wing_up, self.pList_wing_lo = self.createWing()
        self.pList_component_segment           = self.createComponent()
        self.pList_flaps_TEDevice              = self.createFlaps(("trailingEdgeDevices", "trailingEdgeDevice"))
        self.pList_flaps_LEDevice              = self.createFlaps(("leadingEdgeDevices", "leadingEdgeDevice"))
        self.pList_flaps_Spoiler               = self.createFlaps(("spoilers", "spoiler"))
        self.plist_ribs                        = self.createRibs()
        self.pList_spares                      = self.createSpars()
        
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.xTrans = 0
        self.yTrans = 0  
        self.scale = 10.0 
        self.aspect= 0.5  
        self.viewwidth = 0.0
        self.viewheight = 0.0
        
        # helper
        self.r_color = 0.0
        self.g_color = 0.0
        self.b_color = 0.0
        self.alpha_rgb = 1.0
       
        # viewing flags
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
                     
    def initializeGL(self):
        #GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_LIGHTING)
        GL.glEnable(GL.GL_LIGHT0)
        #GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glEnable(GL.GL_NORMALIZE)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)        
        #GL.glBlendFunc(GL.GL_DST_ALPHA, GL.GL_ONE_MINUS_DST_ALPHA)        
        #GL.glBlendFunc(GL.GL_DST_COLOR, GL.GL_SRC_COLOR)        
        #GL.glBlendFunc(GL.GL_DST_COLOR, GL.GL_SRC_ALPHA)        
       # GL.glBlendFunc(GL.GL_ONE, GL.GL_ZERO)        
       # GL.glBlendFunc(GL.GL_ONE_MINUS_DST_COLOR, GL.GL_ONE_MINUS_SRC_COLOR)  
        
                
        GL.glShadeModel(GL.GL_SMOOTH)
        GL.glClearColor (1.0, 1.0, 1.0, 0.0)
        self.initLight()
       
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

    def paintGL(self):
        self.__setProjection()
        #GL.glMatrixMode(GL.GL_PROJECTION)
        #GL.glLoadIdentity()
        # Clear screen and Z-buffer
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT) 
        
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()   
        
        
        
        
        GL.glTranslatef(self.xTrans,self.yTrans,-1.5)
        GL.glRotated(self.xRot, 1.0, 0.0, 0.0)
        GL.glRotated(self.yRot, 0.0, 1.0, 0.0)
        GL.glRotated(self.zRot, 0.0, 0.0, 1.0)
        self.initLight()

        self.draw()        
        #self.initLight()
        #self.drawTestObject()
        #GL.glShadeModel(GL.GL_FLAT)
        #GLUT.glutInit()#
        #GLUT.glutSolidSphere(0.5,40,40)
        
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
        self.createOglShape(self.pList_fuselage, [0.0, 0.44, 0.67, self.alpha_rgb], Renderer.glMode["GL_QUAD_STRIP"], 1, True)
        GL.glEndList()

        GL.glNewList(self.index+1, GL.GL_COMPILE)
        self.createOglShape(self.pList_wing_up, [0.0, 0.44, 0.67, self.alpha_rgb], Renderer.glMode["GL_QUADS"], 1, False)
        GL.glEndList()            
        
        GL.glNewList(self.index+2, GL.GL_COMPILE)
        self.createOglShape(self.pList_wing_lo, [0.0, 0.44, 0.67, self.alpha_rgb], Renderer.glMode["GL_QUADS"], 1, False)
        GL.glEndList()  
        
        # draw reflect upper wing
        GL.glNewList(self.index+3, GL.GL_COMPILE) 
        self.createOglShape(self.pList_wing_up, [0.76, 0.79, 0.50, self.alpha_rgb], Renderer.glMode["GL_QUADS"], -1, False)
        GL.glEndList()  

        GL.glNewList(self.index+4, GL.GL_COMPILE) 
        self.createOglShape(self.pList_wing_lo, [0.76, 0.79, 0.50, self.alpha_rgb], Renderer.glMode["GL_QUADS"], -1, False)
        GL.glEndList()         

        GL.glNewList(self.index+5, GL.GL_COMPILE) 
        self.createOglShape(self.pList_component_segment, [1.0, 0.0, 0.0, 1.0], Renderer.glMode["GL_LINES"], 1, True)
        GL.glEndList()        

        GL.glNewList(self.index+6, GL.GL_COMPILE) 
        self.createOglFlaps(self.pList_flaps_TEDevice)
        GL.glEndList()        

        GL.glNewList(self.index+7, GL.GL_COMPILE) 
        self.createOglFlaps(self.pList_flaps_LEDevice)
        GL.glEndList()     

        GL.glNewList(self.index+8, GL.GL_COMPILE) 
        self.createOglFlaps(self.pList_flaps_Spoiler)
        GL.glEndList() 

        GL.glNewList(self.index+9, GL.GL_COMPILE) 
        self.createOglSpars(self.pList_spares)
        GL.glEndList() 


    def createOglShape(self, pList, color, glMode, reflect, flag_Strip):
        quad = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
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
                    GL.glVertex3f(quad[0][0], quad[0][1], quad[0][2])
                    GL.glVertex3f(quad[1][0], quad[1][1], quad[1][2])                     
                    GL.glVertex3f(quad[2][0], quad[2][1], quad[2][2])                     
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
        GL.glLightf(GL.GL_LIGHT0, GL.GL_CONSTANT_ATTENUATION, 1.0)
        GL.glLightf(GL.GL_LIGHT0, GL.GL_LINEAR_ATTENUATION, 0.001)
        GL.glLightf(GL.GL_LIGHT0, GL.GL_QUADRATIC_ATTENUATION, 0.004)
        
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
       # GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_DIFFUSE, mat_diffuse)
        GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_SPECULAR, mat_specular)
        # GL.glMaterialfv(GL.GL_FRONT, GL.GL_EMISSION, mat_materialEmission)
        GL.glMaterialf(GL.GL_FRONT_AND_BACK, GL.GL_SHININESS, mat_shininess * 128)
    
    # =========================================================================================================
    # =========================================================================================================    
    # create Point lists
    # =========================================================================================================  
    # =========================================================================================================

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
        return plistComp
        
    def createRibs(self):
        for wingIndex in range(1, self.tigl.getWingCount()+1) :
            for compSegmentIndex in range(1, self.tigl.wingGetComponentSegmentCount(wingIndex)+1) :        
                try :
                    ribList = self.__createRibs(wingIndex, compSegmentIndex)
                except:
                    print "no ribs for wing " + str(wingIndex) + " found." ; break
                                
        return[]           
    
    def __createRibs(self, wingIndex, compSegmentIndex):
        path  = '/cpacs/vehicles/aircraft/model/wings/wing['+str(wingIndex)+']/componentSegments/componentSegment['\
                                                                            +str(compSegmentIndex)+']/structure/'
        for idx_ribDef in range(1, self.tixi.getNumberOfChilds(path + 'ribsDefinitions/')+1) :    
            path_ribs_pos = path + 'ribsDefinitions/ribsDefinition[' + str(idx_ribDef) + ']/ribsPositioning/' 
            
            ribreference         = self.tixi.getTextElement(path_ribs_pos + "ribReference")
            etaStart             = self.tixi.getTextElement(path_ribs_pos + "etaStart")
            etaEnd               = self.tixi.getTextElement(path_ribs_pos + "etaEnd")
            ribStart             = self.tixi.getTextElement(path_ribs_pos + "ribStart")
            ribEnd               = self.tixi.getTextElement(path_ribs_pos + "ribEnd")
            numberOfRibs         = self.tixi.getTextElement(path_ribs_pos + "numberOfRibs")
            ribCrossingBehaviour = self.tixi.getTextElement(path_ribs_pos + "ribCrossingBehaviour")

                
            if ribStart == 'trailingEdge' :
                xsiStart = 0.0 ; xsiEnd = 0.0
            elif ribStart == 'leadingEdge' :
                xsiStart = 1.0 ; xsiEnd = 1.0
            elif ribStart in self.__getSparPositionUIDs(wingIndex, compSegmentIndex) :
                print "unimplemented now"
                pass

            if ribEnd == 'trailingEdge' :
                xsiStart = 0.0 ; xsiEnd = 0.0
            elif ribEnd == 'leadingEdge' :
                xsiStart = 1.0 ; xsiEnd = 1.0
            elif ribreference in self.__getSparPositionUIDs(wingIndex, compSegmentIndex) :
                path_spar_pos_uid = path + 'spars/sparSegments/sparSegment[' + ribreference +']/sparPositionUIDs/' 
                sparPositionUIDs = []
                for idx_spar_pos_uid in range(1, self.tixi.getNumberOfChilds(path_spar_pos_uid)+1) : 
                    sparPositionUIDs.append(self.tixi.getTextElement(path_spar_pos_uid + "sparPositionUID["+idx_spar_pos_uid+"]"))

                for idx_spar_pos in range(1, self.tixi.getNumberOfChilds(path + 'spars/sparPositions/')):
                    uid = self.tixi.xPathExpressionGetTextByIndex(path + 'spars/sparPositions/sparPosition/@uID', idx_spar_pos)
                    if uid in sparPositionUIDs :
                        eta = self.tixi.getTextElement(path + "spars/sparPositions/sparPosition[" + uid +"]/eta/")
                        xsi = self.tixi.getTextElement(path + "spars/sparPositions/sparPosition[" + uid +"]/xsi/")
                xsiStart = xsi ; xsiEnd = xsi              
                
            # (b - a) / (count of Points - 1)    
            spacing = (etaEnd - etaStart) / (numberOfRibs-1)
                
                    
        return [] 


    def __getSparPositionUIDs(self, wingIndex, compSegmentIndex):
        path_sparSegments = '/cpacs/vehicles/aircraft/model/wings/wing['\
                                +str(wingIndex)+']/componentSegments/componentSegment['\
                                +str(compSegmentIndex)+']/structure/spars/sparSegments/'
        
        path = path_sparSegments + 'sparSegment/@uID' 

        uidList = []
        for sparSegmentIdx in range(1, self.tixi.getNumberOfChilds(path_sparSegments)+1) :
            uidList.append(self.tixi.xPathExpressionGetTextByIndex(path, sparSegmentIdx))
        return uidList

    
    def createSpars(self):
        plistWing = []
        for wingIndex in range(1, self.tigl.getWingCount()+1) :
            plistSeg = []
            for compSegmentIndex in range(1, self.tigl.wingGetComponentSegmentCount(wingIndex)+1) :         
                try :
                    sparList = self.__createSpars(wingIndex, compSegmentIndex)
                except:
                    print "no spar for wing " + str(wingIndex) + " found." ; break
                
                componentSegmentUID = self.tigl.wingGetComponentSegmentUID(wingIndex, compSegmentIndex)
                plistSparSeg = []
                for sparSegment in sparList : 
                    plistSpar = []
                    for spar in sparSegment :
                        x1, y1, z1 = self.tigl.wingComponentSegmentGetPoint(componentSegmentUID, spar[0], spar[1])       
                        plistSpar.append([x1, y1, z1])
                    plistSparSeg.append(plistSpar)
                plistSeg.append(plistSparSeg)
            plistWing.append(plistSeg)      
            
        return plistWing   
                
    def __createSpars(self, wingIndex, compSegmentIndex):
        path_sparSegments = '/cpacs/vehicles/aircraft/model/wings/wing['\
                                +str(wingIndex)+']/componentSegments/componentSegment['\
                                +str(compSegmentIndex)+']/structure/spars/sparSegments/'

        sparSegmentList = []
        for sparSegmentIdx in range(1, self.tixi.getNumberOfChilds(path_sparSegments)+1) :
            path = path_sparSegments + 'sparSegment[' + str(sparSegmentIdx) + ']/sparPositionUIDs/' 
            sparPositionUIDsList = []
            for sparPositionUIDIdx in range(1, self.tixi.getNumberOfChilds(path)+1) :
                sparPositionUIDsList.append(self.tixi.getTextElement(path + 'sparPositionUID[' + str(sparPositionUIDIdx) + ']'))
            sparSegmentList.append(sparPositionUIDsList)
        
        sparList = []
        for sparSegment in sparSegmentList :
            plist = []
            for uid in sparSegment :
                path = self.tixi.uIDGetXPath(uid)
                eta = self.tixi.getDoubleElement(path + '/eta')
                xsi = self.tixi.getDoubleElement(path + '/xsi')
                plist.append([eta, xsi])
            sparList.append(plist)
            
        return sparList


    
    '''
    @param flapType: (parent, child)-String-Tuple of flap types, eg. ("trailingEdgeDevices","trailingEdgeDevice")
    '''
    def createFlaps(self, flapType, point_cnt_eta = 10, point_cnt_xsi = 10):    
        plistWing = []
        (flapParent, _) = flapType
        
        for wingIndex in range(1, self.tigl.getWingCount()+1) :
            plistSeg = []
            for compSegmentIndex in range(1, self.tigl.wingGetComponentSegmentCount(wingIndex)+1) : 
                try :
                    if flapParent == 'trailingEdgeDevices' : 
                        flapList = self.__createFlapsTE(wingIndex, compSegmentIndex)
                    elif flapParent == 'leadingEdgeDevices' :
                        flapList = self.__createFlapsLE(wingIndex, compSegmentIndex)
                    elif flapParent == 'spoilers' :
                        flapList = self.__createFlaps_Spoiler(wingIndex, compSegmentIndex)
                    else : print "unexpected behaviour in createFlaps" ; sys.exit()
                except:
                    print "no " + str(flapType) + " for wing " + str(wingIndex) + " found." ; break

                componentSegmentUID = self.tigl.wingGetComponentSegmentUID(wingIndex, compSegmentIndex)
                plistFlaps = []
                for flap in flapList : 
                    x1, y1, z1 = self.tigl.wingComponentSegmentGetPoint(componentSegmentUID, flap[0], flap[2])       
                    x2, y2, z2 = self.tigl.wingComponentSegmentGetPoint(componentSegmentUID, flap[1], flap[3]) 
                    x3, y3, z3 = self.tigl.wingComponentSegmentGetPoint(componentSegmentUID, flap[4], flap[6]) 
                    x4, y4, z4 = self.tigl.wingComponentSegmentGetPoint(componentSegmentUID, flap[5], flap[7]) 
                    plistFlaps.append([[x1, y1, z1], [x2, y2, z2], [x3, y3, z3], [x4, y4, z4]])
                plistSeg.append(plistFlaps)
            plistWing.append(plistSeg)      
        return plistWing             
    
    def __createFlapsTE(self, wingIndex, compSegmentIndex):
        path_TE_Devices = '/cpacs/vehicles/aircraft/model/wings/wing['\
                                +str(wingIndex)+']/componentSegments/componentSegment['\
                                +str(compSegmentIndex)+']/controlSurfaces/trailingEdgeDevices/'
                                
        plistTE = []
        for _TE_Devices_Idx in range(1, self.tixi.getNumberOfChilds(path_TE_Devices)+1) :
            path_in  = path_TE_Devices + 'trailingEdgeDevice[' + str(_TE_Devices_Idx) + ']/outerShape/innerBorder/'
            path_out = path_TE_Devices + 'trailingEdgeDevice[' + str(_TE_Devices_Idx) + ']/outerShape/outerBorder/'
                    
            etaLE_in = self.tixi.getDoubleElement(path_in + 'etaLE')
            etaTE_in = self.tixi.getDoubleElement(path_in + 'etaTE')
            xsiLE_in = self.tixi.getDoubleElement(path_in + 'xsiLE')
            xsiTE_in = 1.0               
                    
            etaLE_out = self.tixi.getDoubleElement(path_out + 'etaLE')
            etaTE_out = self.tixi.getDoubleElement(path_out + 'etaTE')
            xsiLE_out = self.tixi.getDoubleElement(path_out + 'xsiLE')
            xsiTE_out = 1.0
                    
            plistTE.append([etaLE_in, etaTE_in, xsiLE_in, xsiTE_in, etaLE_out, etaTE_out, xsiLE_out, xsiTE_out])
        return plistTE     


    def __createFlapsLE(self, wingIndex, compSegmentIndex):
        path_LE_Devices = '/cpacs/vehicles/aircraft/model/wings/wing['\
                                +str(wingIndex)+']/componentSegments/componentSegment['\
                                +str(compSegmentIndex)+']/controlSurfaces/leadingEdgeDevices/'
                                
        plistLE = []
        for _LE_Devices_Idx in range(1, self.tixi.getNumberOfChilds(path_LE_Devices)+1) :
            path_in  = path_LE_Devices + 'leadingEdgeDevice[' + str(_LE_Devices_Idx) + ']/outerShape/innerBorder'
            path_out = path_LE_Devices + 'leadingEdgeDevice[' + str(_LE_Devices_Idx) + ']/outerShape/outerBorder'
                    
            etaLE_in = self.tixi.getDoubleElement(path_in + '/etaLE')
            etaTE_in = self.tixi.getDoubleElement(path_in + '/etaTE')
            xsiLE_in = 0.0 
            xsiTE_in = self.tixi.getDoubleElement(path_in + '/xsiTE')
                    
            etaLE_out = self.tixi.getDoubleElement(path_out + '/etaLE')
            etaTE_out = self.tixi.getDoubleElement(path_out + '/etaTE')
            xsiLE_out = 0.0
            xsiTE_out = self.tixi.getDoubleElement(path_out + '/xsiTE')
                    
            plistLE.append([etaLE_in, etaTE_in, xsiLE_in, xsiTE_in, etaLE_out, etaTE_out, xsiLE_out, xsiTE_out])
        return plistLE     


    def __createFlaps_Spoiler(self, wingIndex, compSegmentIndex):
        path_Spoiler = '/cpacs/vehicles/aircraft/model/wings/wing['\
                                +str(wingIndex)+']/componentSegments/componentSegment['\
                                +str(compSegmentIndex)+']/controlSurfaces/spoilers/'
        
        plistSpoiler = []
        for spoiler_Idx in range(1, self.tixi.getNumberOfChilds(path_Spoiler)+1) :
            path_in  = path_Spoiler + 'spoiler[' + str(spoiler_Idx) + ']/outerShape/innerBorder'
            path_out = path_Spoiler + 'spoiler[' + str(spoiler_Idx) + ']/outerShape/outerBorder'
                    
            etaLE_in = self.tixi.getDoubleElement(path_in + '/etaLE')
            etaTE_in = self.tixi.getDoubleElement(path_in + '/etaTE')
            xsiLE_in = self.tixi.getDoubleElement(path_in + '/xsiLE')
            xsiTE_in = self.tixi.getDoubleElement(path_in + '/xsiTE')
                    
            etaLE_out = self.tixi.getDoubleElement(path_out + '/etaLE')
            etaTE_out = self.tixi.getDoubleElement(path_out + '/etaTE')
            xsiLE_out = self.tixi.getDoubleElement(path_out + '/xsiLE')
            xsiTE_out = self.tixi.getDoubleElement(path_out + '/xsiTE')
                    
            plistSpoiler.append([etaLE_in, etaTE_in, xsiLE_in, xsiTE_in, etaLE_out, etaTE_out, xsiLE_out, xsiTE_out])
        return plistSpoiler  


        
    def createFuselage(self, point_cnt_eta = 1, point_cnt_zeta = 40):
        eta_List = utility.createXcoordsLinear(1.0, point_cnt_eta)
        zeta_List = utility.createXcoordsLinear(1.0, point_cnt_zeta) 
        
        plistFuse = []
        
        for fuselageIndex in range(1, self.tigl.getFuselageCount()+1) :
            plistSeg = []
            for segmentIndex in range(1, self.tigl.fuselageGetSegmentCount(fuselageIndex)+1) :
                #plistprofile = []
                for eta in eta_List :
                    plist = []
                    for zeta in zeta_List :
                        x, y, z = self.tigl.fuselageGetPoint(fuselageIndex, segmentIndex, eta, zeta)
                        plist.append([x,y,z])
                    #plistprofile.append(plist)
                    plistSeg.append(plist)
                #plistSeg.append(plistprofile)    
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

                
                
class Widget(QtGui.QWidget):
    def __init__(self, parent = None):
        super(Widget, self).__init__(parent)
        self.width = 800
        self.height = 800
        self.resize(self.width ,self.height)
        
        self.renderer = Renderer(self.width ,self.height)
        
        label1 = QtGui.QLabel("Transparency")
        slide_transparency = QtGui.QSlider(QtCore.Qt.Horizontal)
        slide_transparency.setRange(0, 100)
        slide_transparency.setSingleStep(10)
        slide_transparency.setPageStep(100)
        slide_transparency.setTickInterval(10)
        slide_transparency.setTickPosition(QtGui.QSlider.TicksRight)      
      
        slide_transparency.valueChanged.connect(self.setTransparency)
      
        grid = QtGui.QGridLayout()
        grid.addWidget(label1, 1,1)
        grid.addWidget(slide_transparency, 1,2)
        grid.addWidget(self.renderer,2,1,1,2)
        self.setLayout(grid)
        
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setSizePolicy ( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        # set up context menu
        self.showOptions = [QtGui.QAction("Show fuselage", self), QtGui.QAction("Show wing1up", self),
                       QtGui.QAction("Show wing1lo", self), QtGui.QAction("Show wing2up", self),
                       QtGui.QAction("Show wing2lo", self), QtGui.QAction("Show components", self),
                       QtGui.QAction("Show TE_Device", self), QtGui.QAction("Show LE_Device", self),
                       QtGui.QAction("Show spoiler", self), QtGui.QAction("Show ribs", self),
                       QtGui.QAction("Show spars", self)]

        self.menu = QtGui.QMenu(self)
                
        for i in range (len(self.showOptions)) :
            self.showOptions[i].setCheckable(True)
            self.menu.addAction(self.showOptions[i])
         
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

        self.renderer.updateGL()

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

        # Request paintGL update
        if redraw :
            self.renderer.updateGL()
    
    def contextMenuEvent(self, event):
        self.menu.exec_(event.globalPos())
        self.renderer.updateGL()
    
    def setTransparency(self, value):
        self.renderer.alpha_rgb = 1.0 - value/100.0
        self.renderer.initializeGL()
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
        
    def setShowRibs(self):
        self.renderer.flag_show_ribs = not self.renderer.flag_show_ribs


if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = Widget()
    widget.show()
    app.exec_()    