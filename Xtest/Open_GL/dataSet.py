'''
Created on Sep 11, 2014

@author: rene
'''
import sys
import math
import utility
from PySide import QtOpenGL, QtGui, QtCore
from cpacsHandler import CPACS_Handler
from Xtest.Open_GL.configuration.config import Config
import logging
import datetime
from chaikin_spline import Chaikin_Spline

try:
    from OpenGL import GL, GLU, GLUT
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.info('\n#####################################################\nstart\n#####################################################')
logging.info(datetime.datetime.now().time())

class DataSet() :
    def __init__(self, uid, parent = None):

        # ==========================================================
        self.tixi = CPACS_Handler()
        self.tixi.loadFile(Config.path_cpacs_A320_Fuse, Config.path_cpacs_21_schema)
        # ==========================================================        
        
        self.pointList                          = self.__createPointList(uid)
        self.trailingEdge                       = self.__computeTrailingEdge(self.pointList)
        self.leadingEdge                        = self.__computeLeadingEdge(self.pointList)
        self.pointList_bot , self.pointList_top = self.__createPointList_bot_top(self.leadingEdge, self.pointList)
        self.pointList_chord                    = self.__createPointList_chord(self.leadingEdge, self.trailingEdge, len(self.pointList_top))        
        self.pointList_camber                   = self.__createPointList_camber(self.pointList_bot, self.pointList_top, self.pointList_chord)
        self.pointList_top_rot                  = self.pointList_top
        self.pointList_bot_rot                  = self.pointList_bot
       
    '''
    @param: uid from cpacs
    @return: lists for top and bottom profile in format [ [x0,y0,z0] , [x1,y1,z1] , ...  ]
    '''       
    def __createPointList(self, uid) :
        vecX = self.tixi.getVectorX(uid)
        vecY = self.tixi.getVectorZ(uid)
        vecZ = self.tixi.getVectorY(uid)
        
        res = []
        for i in range(0, len(vecX)) :
            res.append([vecX[i], vecY[i], vecZ[i]])
        return res        

    '''
    @param plist: point list
    @return: the trailing edge ; the center of the first and the last point of plist
    ''' 
    def __computeTrailingEdge(self, plist):
        return utility.getCenterPoint(plist[0], plist[len(plist)-1])

    '''
    @param plist: point list
    @return: the leading edge ; the farthest point of trailing edge
    '''         
    def __computeLeadingEdge(self, plist):    
        trailingEdge = self.getTrailingEdge()
        dist = -1
        idx  = -1
        
        for i in range(0, len(plist)) : 
            cur_dist = utility.getDistanceBtwPoints(plist[i], trailingEdge)
            if cur_dist > dist : 
                dist = cur_dist
                idx = i
            else : return plist[idx]
        return plist[idx]
    
    '''
    @param leadingEdge: the leading edge of the profile
    @param plist: the complete profile point list
    @return: bottom list and top list of the profile
    '''         
    def __createPointList_bot_top(self, leadingEdge, plist):
        idx = utility.searchPoint(leadingEdge, plist)
        return  plist[:idx+1] , plist[idx:]         
 
    '''
    @param p1: leading edge
    @param p2: trailing edge
    @param point_cnt: count of points to create
    @return: list with chord points    
    ''' 
    def __createPointList_chord(self, p1, p2, point_cnt) : 
        dist = utility.getDistanceBtwPoints(p1, p2)
        interval = dist/ point_cnt  
         
        res = [p1]
        for i in range(1, point_cnt+1):
            p = utility.computePointOnLine(p1[0] + i*interval, p1, p2)
            res.append(p)
        
        return res   

    '''
    @param plist_top: point list of top profile
    @param plist_bot: point list of bottom profile
    @return: list with camber points    
    ''' 
    def __createPointList_camber2(self, plist_bot, plist_top) : 
        plist_top.reverse()
        axis0 = self.__createApproximateCamber(plist_bot, plist_top)
        axis1 = self.__createApproximateCamber(plist_top, plist_bot)
        axis  = self.__createApproximateCamber(axis0, axis1)
        print "d" , axis0
        print "e" , axis1
        print "f" , axis
        
        return self.__createApproximateCamber(axis0, axis1) 

    def __createApproximateCamber(self, plist1, plist2):
        axis = []
        for p1 in plist1 : 
            p = utility.computePointWithMinDistance(p1, plist2)
            p = utility.getCenterPoint(p, p1) if  p != self.leadingEdge else p  
            axis.append(p)
        return axis    
    

    def __createPointList_camber(self, plist_bot, plist_top, plist_chord):
        res= []
        for p_chord in plist_chord :
            m, b = utility.createPerpendicular(self.leadingEdge, self.trailingEdge, p_chord)
            # fkt has gradient 0, then fkt x = b and compute y by neigbors
            if m == None :
                p_bot = [b,self.approxYByNeighbors(b, plist_bot), p_chord[2]]
                p_top = [b,self.approxYByNeighbors(b, plist_top), p_chord[2]]
            else :
                p_bot = self.__getPointWithMinDistanceToChordPerpendicular(m, b, plist_bot)
                p_top = self.__getPointWithMinDistanceToChordPerpendicular(m, b, plist_top)
            res.append(utility.getCenterPoint(p_bot, p_top))
        print res
        return res
        
    '''
    not save!!! danger!!!
    '''    
    def approxYByNeighbors(self, x, plist):
        for i in range(0, len(plist)):
            if plist[i][0] == x :
                return plist[i][1]
            elif plist[i-1][0] > x and plist[i][0] < x or plist[i-1][0] < x and plist[i][0] > x:
                return utility.getCenterPoint(plist[i-1], plist[i])[1]

            
            
    def __getPointWithMinDistanceToChordPerpendicular(self, m_per, b_per, plist):
        dist = -1.0
        point = None
        for p1 in plist :
            m1, b1 = utility.createLineFunction(self.leadingEdge, self.trailingEdge, p1) 
            isectP = utility.getIntersectionPoint(m_per, b_per, m1, b1)
            cur_dist   = utility.getDistanceBtwPoints(isectP, p1)
            if (dist < 0.0 or cur_dist < dist) :
                dist = cur_dist      
                point = p1
        return point  


    # ============================================================================================================
    # rotation functions
    # ============================================================================================================
    def __createRotPointList(self, plist, angle, curTransX = 1):
        res = []
        for p in plist :
            rotP = self.__getRotPoint(p[0]-curTransX, p[1], p[2], self.degToRad(angle))
            rotP = [rotP[0]+curTransX, rotP[1], rotP[2]]
            res.append(rotP)
        return res

    def __getRotPoint(self, x, y, z, theta):
        x_new = x * math.cos(theta) - y * math.sin(theta)
        y_new = x * math.sin(theta) + y * math.cos(theta)
        z_new = z
        return [x_new, y_new, z_new]

    # ================================================================================================================
    # getter and setter
    # ================================================================================================================
    def setPointList(self, plist):
        self.pointList = plist
   
    def setPointListTop(self, plist):
        self.pointList_top = plist

    def setPointListBot(self, plist):
        self.pointList_bot = plist
        
    def setPointListChord(self, plist):
        self.pointList_chord = plist
        
    def setPointListCamber(self, plist):
        self.pointList_camber = plist        
    
    def setPointListTop_rot(self, plist):
        self.pointList_top_rot = plist
        
    def setPointListBot_rot(self, plist):
        self.pointList_bot_rot = plist
   
    def getCompletePointList(self):
        return self.pointList
    
    def getPointList(self):
        return self.pointList

    def getPointListTop(self):
        return self.pointList_top
    
    def getPointListBot(self):
        return self.pointList_bot
    
    def getPointListChord(self):
        return self.pointList_chord
    
    def getPointListCamber(self):
        return self.pointList_camber

    def getPointListTop_rot(self):
        return self.pointList_top_rot
        
    def getPointListBot_rot(self):
        return self.pointList_bot_rot    
    
    def getLenChord(self):
        return utility.getDistanceBtwPoints(self.getTrailingEdge(), self.getLeadingEdge())   
    
    def getEndPoints(self):
        return self.leadingEdge, self.trailingEdge
    
    def getTrailingEdge(self):
        return self.trailingEdge
  
    def getLeadingEdge(self):
        return self.leadingEdge
  
    def getProfileThickness(self):
        return 100 * self.__computeProfileThickness(self.pointList_top, self.pointList_bot)        

    def getProfileArch(self):
        return 100.0 * self.__computeProfileArch(self.pointList_chord, self.pointList_camber)  
  
    def getSplineCurve(self):
        spline = Chaikin_Spline(self.getCompletePointList())
        spline.IncreaseLod()
        spline.IncreaseLod()
        return spline.getPointList()
      
    # ============================================================================================================
    # update functions
    # ============================================================================================================
    def updateLeadingEdge(self):
        self.leadingEdge = self.__computeLeadingEdge(self.pointList)
    
    def updateTrailingEdge(self):
        self.trailingEdge = self.__computeTrailingEdge(self.pointList)    
        
    def updatePointList_Bot_Top(self):
        self.pointList_bot, self.pointList_top  = self.__createPointList_bot_top(self.leadingEdge, self.pointList)            
    
    def updatePointListChord(self):
        self.pointList_chord = self.__createPointList_chord(self.leadingEdge, self.trailingEdge, len(self.pointList)/2)    
    
    def updatePointListCamber(self):
        self.pointList_camber = self.__createPointList_camber(self.pointList_bot, self.pointList_top)    
    
    def updateRotationLists(self, angle):
        length = self.getLenChord()       
        self.pointList = self.__createRotPointList(self.getPointList(), angle, length)
        #self.pointList_top = self.__createRotPointList(self.pointList_top_rot, angle, length)
        #self.pointList_bot = self.__createRotPointList(self.pointList_bot_rot, angle, length)
        self.updatePointLists()

    def updatePointListsForNaca(self):
        self.updateTrailingEdge()
        self.updateLeadingEdge()
        self.updatePointList_Bot_Top()
        self.updatePointListChord()
 
    # ================================================================================================================
    # geometrie helper
    # ================================================================================================================
    '''
    @param plist: format [ [x0,y0,z0] , [x1,y1,z1] , ...  ]
    @param dim: dimension e.g. 0==x, 1==y, 2==z 
    @return: minimum and maximum point compared by dim 
    '''
    def get_min_max_of_List(self, plist, dim=0):
        id_max = 0 
        id_min = 0
        for i in range (1, len(plist),1) :
            if plist[id_max][dim] < plist[i][dim] :
                id_max = i
            if plist[id_min][dim] > plist[i][dim] :
                id_min = i
        return plist[id_min], plist[id_max] 
    
           
    '''
    @param list1: first list
    @param list2: second list
    @return: distance between p1 of list1 and corresponding p2 of list2
    '''   
    def __computeProfileThickness(self, list1, list2):
        dist = -1.0
        for p in self.getPointListCamber() :
            dist1 = utility.computeMinDistance(p, list1)
            dist2 = utility.computeMinDistance(p, list2)
            cur_dist = dist1 + dist2
            if dist < 0.0 or cur_dist > dist :            
                dist = cur_dist
        return dist
 
    '''
    @param list1: first list
    @param list2: second list
    @return: distance between p1 of list1 and corresponding p2 of list2
    '''   
    def __computeProfileArch(self, list1, list2):
        dist = -1.0
        for p in list1 :
            cur_dist = utility.computeMinDistance(p, list2)
            if cur_dist > dist :            
                dist = cur_dist
        return dist
 

    
    # ============================================================================================================
    # normal helper
    # ============================================================================================================
    '''
    @param angle: angle in degrees
    @return: angle in radians 
    '''   
    def degToRad(self, angle):
        return angle/(180/math.pi)   
    
    '''
    @param angle: angle in radians
    @return: angle in degrees 
    '''   
    def radToDeg(self, angle):
        return angle*(180/math.pi)
    
    '''
    @param value: positive or negative number
    @return: positive number 
    '''     
    def abs(self, value):
        return -value if value < 0 else value 


    # ================================================================================================================
    # debug helper
    # ================================================================================================================    
    def __debug(self, value):
        logging.debug("#######################################################################")
        logging.debug(str(value))
        logging.debug("#######################################################################") 
       


        