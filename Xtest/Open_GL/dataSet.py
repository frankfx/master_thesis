'''
Created on Sep 11, 2014

@author: rene
'''
import sys
import math
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
        
        self.pointList_bot, self.pointList_top  = self.__createPointList(uid)
        self._leftEndP , self._rightEndP        = self.__computeEndPoints(self.pointList_top, self.pointList_bot)
        self.pointList_chord                    = self.__createPointList_chord(self._leftEndP, self._rightEndP, len(self.pointList_top))
        self.pointList_camber                   = self.__createPointList_camber(self.pointList_top, self.pointList_bot)
        self.pointList_top_rot                  = self.pointList_top
        self.pointList_bot_rot                  = self.pointList_bot
       
        
    '''
    @param: uid from cpacs
    @param: sort_desc boolean flag for splitting option
    @return: lists for top and bottom profile in format [ [x0,y0,z0] , [x1,y1,z1] , ...  ]
    [3,2,1,0,1,2,3] --> [3,2,1] , [0,1,2,3] --> topList, botList
    [0,1,2,3,2,1,0] --> [0,1,2] , [3,2,1,0]
    '''
    def __createPointList(self, uid, sort_desc = True):
        vecX = self.tixi.getVectorX(uid)
        vecY = self.tixi.getVectorZ(uid)
        vecZ = self.tixi.getVectorY(uid)
        
        l_fst = []
        l_snd = []
        for i in range(0, len(vecX)-1, 1) :
            if sort_desc:
                if(vecX[i] > vecX[i+1]) :
                    l_fst.append([ vecX[i], vecY[i], vecZ[i] ])
                else : 
                    l_fst.append([ vecX[i], vecY[i], vecZ[i] ])
                    break
            else :
                if vecX[i] < vecX[i+1] :
                    l_fst.append([ vecX[i], vecY[i], vecZ[i] ])
                else:
                    l_fst.append([ vecX[i], vecY[i], vecZ[i] ])
                    break                    

        for j in range(i, len(vecX), 1) :
            l_snd.append([ vecX[j], vecY[j], vecZ[j] ])
        #l_snd.reverse()
        return l_fst , l_snd
   
    '''
    @param p1: profile start point (nose)
    @param p2: profile end point
    @param point_cnt: count of points to create
    @return: list with chord points    
    '''
    def __createPointList_chord(self, p1, p2, point_cnt) : 
        dist = p2[0] - p1[0]
        interval = dist/ point_cnt  
        
        res = [p1]
        for i in range(1, point_cnt+1):
            p = self.__computePointOnLine(p1[0] + i*interval, p1, p2)
            res.append(p)
        return res   

    # ============================================================================================================
    # camber functions
    # ============================================================================================================
   
    '''
    @param topList: top list
    @param botList: bottom list
    @return: list of camber points 
    '''
    def __createPointList_camber(self, topList, botList):
        return self.__computeCamber(topList, botList)
   
    '''
    @return: camber list
    ''' 
    def __computeCamber(self, topList, botList):
        res = []
        for p in self.pointList_chord :
            fct_perpendicular   = self.__createLinePerpendicular(self.pointList_chord, p)
            #print "fct_perpendicular" , fct_perpendicular
            if fct_perpendicular is None:
               # print "not intersect case"
                return self.__computeCamber2(topList, botList)
            else:
                #print "intersect case"
                intersect_top       = self.__computeIntersectionPoint(topList, fct_perpendicular)
                intersect_bot       = self.__computeIntersectionPoint(botList, fct_perpendicular)
            
                res.append( self.getPointBtwPoints(intersect_top, intersect_bot)) 
        return res

    def __computeCamber2(self, topList, botList):
        res = []    
        for i in range(0, len(topList)):     
            p = self.__computePoint(topList[i], botList)    
            res.append(p)    
        return res   
    
    '''
    @param plist: list with line coordinates
    @param srcPoint: point on plist where perpendicular intersects
    @return: perpendicular as lambda function  or  None if m is 0
    '''
    def __createLinePerpendicular(self, plist, srcPoint):
        m_perpendicular = self.__computeLinePerpendicularGradient(plist)
        b = srcPoint[1] - m_perpendicular * srcPoint[0]
        
        return None if m_perpendicular == 0 else lambda x : m_perpendicular * x + b     

    '''
    @param plist: list of line
    @return: gradient of line perpendicular
    '''
    def __computeLinePerpendicularGradient(self, plist):
        if len(plist) < 2 :
            return None
        p1 = plist[0] 
        p2 = plist[1]
        # m = (y2-y1) / (x2-x1) ;;; b = y2 - m-x2 
        m = ( p2[1] - p1[1] ) / ( p2[0] - p1[0] )
        
        m_perpendicular = 0 if m == 0 else -1/m
        return m_perpendicular      

    '''
    @param plist: top or bottom list
    @param fct_perpendicular: the perpendicular of chord line as a lambda function 
    @return: approximated intersection point between plist line and chord perpendicular
    '''
    def _d_computeIntersectionPoint(self, plist, fct_perpendicular):
        res = None
        for p in plist :
            if res is None :
                res = p
            else:
                y = fct_perpendicular (p[0])
                #print y, p, " ==== " , self.abs(y - p[1])
                if self.abs(y - p[1]) < self.abs(y-res[1]) :
                    res = p
       # print "intersect Point" , res
        return res      
   
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

    # ============================================================================================================
    # endpoints functions
    # ============================================================================================================
    '''
    @return: left and right end point
    '''
    def computeEndPoints(self):
        return self.__computeEndPoints(self.pointList_top, self.pointList_bot)         
        
    '''
    @param toplist: profile top
    @param botlist: profile bottom
    @return: left and right end point
    '''
    def __computeEndPoints(self, toplist, botlist):
        dim = 0
        _ , max_top = self.get_min_max_of_List(toplist, dim)
        _ , max_bot = self.get_min_max_of_List(botlist, dim)

        maxP = max_top if max_top >= max_bot else max_bot
        maxP = [maxP[0], max_bot[1] + (max_top[1] - max_bot[1])/2, maxP[2]]

        minP = [maxP]
        max_dist = 0
        tmp_dist = 0

        for p in toplist + botlist :
            tmp_dist = self.__getDistanceBtwPoints(p, maxP)
            if tmp_dist > max_dist :
                max_dist = tmp_dist
                minP     = p
        return minP , maxP 
   
    # ================================================================================================================
    # getter and setter
    # ================================================================================================================
   
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
        return  self.pointList_bot + self.pointList_top[1:]
    
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
        start, end = self.getEndPoints()
        return self.__getDistanceBtwPoints(start, end)   
    
    def getEndPoints(self):
        return self._leftEndP , self._rightEndP

    def getEndPoint(self, plist):
        dim = 0
        _ , maxi = self.get_min_max_of_List(plist, dim)
        return maxi
  
    def getProfileThickness(self):
        return 100 * self.get_max_distance_btw_pointLists(self.pointList_top, self.pointList_bot)        

    def getProfileArch(self):
        ()
        #return 100.0 * self.get_max_distance_btw_pointLists(self.pointList_chord, self.pointList_camber)  
  
    def updateRotationLists(self, angle):
        length = self.getLenChord()       
        self.pointList_top = self.__createRotPointList(self.pointList_top_rot, angle, length)
        self.pointList_bot = self.__createRotPointList(self.pointList_bot_rot, angle, length)
        self.updatePointLists()

    def updatePointLists(self):
        self._leftEndP , self._rightEndP = self.__computeEndPoints(self.pointList_top, self.pointList_bot)
        self.pointList_chord = self.__createPointList_chord(self._leftEndP, self._rightEndP, len(self.pointList_top))  
      #  self.pointList_camber = self.__createPointList_camber(self.pointList_top, self.pointList_bot)     

    def getSplineCurve(self):
        spline = Chaikin_Spline(self.getCompletePointList())
        spline.IncreaseLod()
        spline.IncreaseLod()
        return spline.getPointList()
        
 
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
    computes points between the two given points
    '''    
    def getPointBtwPoints(self, p1, p2):
        distX = p1[0] - p2[0]
        distY = p1[1] - p2[1]
        halfX = distX / 2
        halfY = distY / 2
        return [p1[0] - halfX, p1[1] - halfY, p1[2]]
       
    '''
    @param p1: first point
    @param p2: second point
    @return: distance between p1 and p2
    '''    
    def __getDistanceBtwPoints(self, p1, p2):
        a = (p1[0] - p2[0]) * (p1[0] - p2[0])
        b = (p1[1] - p2[1]) * (p1[1] - p2[1])
        return math.sqrt( a + b )  
 
    '''
    @param x: x-value of result point
    @param p1: point one of line p1 to p2
    @param p2: point two of line p1 to p2
    @return: Point on Line of Points p1 to p2
    '''
    def __computePointOnLine(self, x, p1, p2):
        fst = p1 if p1[0] <= p2[0] else p2
        snd = p2 if p1[0] <= p2[0] else p1
        if (x < fst[0] or x > snd[0]):
            self.__debug("None in dataSet.__computePointOnLine\nPoint " + str(x) + ' not in Range [' + str(p1) + ', ' + str(p2) + ']')
            return None

        # m = (y2-y1) / (x2-x1) ;;; b = y2 - m-x2 
        m = ( snd[1] - fst[1] ) / ( snd[0] - fst[0] )
        b = snd[1] - m * snd[0]

        y = m * x + b
        return [x, y, p1[2]]      
    
    '''
    @param list1: first list
    @param list2: second list
    @return: distance between p1 of list1 and corresponding p2 of list2
    '''   
    def get_max_distance_btw_pointLists(self, list1, list2):
        dist = -1   
        for p in list1 :
            p1 = self.__computePoint(p, list2)
            if p1 is None:
                return None
            cur_dist = self.__getDistanceBtwPoints(p, p1)
            dist = cur_dist if cur_dist > dist else dist            
        return dist  
    
       

     

    
    
    
            
        
    '''
    @return: gradient of chord
    '''    










    
    def computePoint(self, p1, plist):
        diff = None
        for p in plist :
            p_left , p_right = self.__getNeighbors(p, plist)
            gradient         = self.__computeGradient(p_left, p_right)
            perpendicular    = self.__computePerpendicularInPoint(gradient, p)
            p                = self.__computeIntersectionPoint(plist, perpendicular)

    def __computePerpendicularInPoint(self, m, srcPoint):
        m_perpendicular = 0 if m == 0 else -1/m
        b = srcPoint[1] - m_perpendicular * srcPoint[0]
        
        return None if m_perpendicular == 0 else lambda x : m_perpendicular * x + b

    def __computeIntersectionPoint(self, plist, fct_perpendicular):
        res = None
        for p in plist :
            if res is None :
                res = p
            else:
                y = fct_perpendicular (p[0])
                if self.abs(y - p[1]) < self.abs(y-res[1]) :
                    res = p
        return res 


    def __computeGradient(self, p1, p2):
        return ( p2[1] - p1[1] ) / ( p2[0] - p1[0] )


    def __getNeighbors(self, p, plist):
        idx = self.__getIndexOfPointInList(p, plist)

        if idx == -1 :
            raise ValueError('p not in List')
        elif idx != 0 and idx != len(plist) - 1  :
            return plist[idx-1] , plist[idx+1]
        elif idx != 0 :
            return plist[idx-1] , None
        else:
            return None , plist[idx+1]


    def __getIndexOfPointInList(self, p, plist):
        for i in range(0, len(plist)) :
            if plist[i] == p :
                return i
            
        return -1



    
    
    

    
    
     
        
    '''
    ?????????????????????????????????????????????????????
    Bug - nachragen wie line bestimmt wird
    ????????????????????????????????????????????????????
    @param p1: point of topList
    @param plist: botList
    @return: Point in the center of topList and botList at position x  
    '''
    def __computePoint(self, p1, plist):

        idx_r  , idx_l   = -1   , -1
        flag_l , flag_r = False , False

        for i in range(0 , len(plist)) :
            if plist[i][0] <= p1[0]:
                if not flag_l :
                    idx_l = i
                    flag_l = True
                elif plist[i][0] > plist[idx_l][0]:
                    idx_l = i

            if plist[i][0] >= p1[0] :
                if not flag_r:
                    idx_r = i
                    flag_r = True
                elif plist[i][0] < plist[idx_r][0] :
                    idx_r = i

        if idx_r == -1 or idx_l == -1 :
            self.__debug("None in dataSet.__computePoint\nPoint " + str(p1) + ' not in List\n'  + str(plist))

            mini, maxi = self.get_min_max_of_List(plist, 0)
            p_r = maxi if idx_r == -1 else plist[idx_r]
            p_l = mini if idx_l == -1 else plist[idx_l]

            p_new = self.__computePointOnLine(p1[0], p_l, p_r)
            return [p1[0], p1[1] - (p1[1] - p_new[1]) / 2.0, p1[2]]

        elif idx_r == idx_l :
            y = p1[1] - (p1[1] - plist[idx_l][1]) / 2
            return [p1[0], y, p1[2]]

        p_new = self.__computePointOnLine(p1[0], plist[idx_l], plist[idx_r])
        return [p1[0], p1[1] - (p1[1] - p_new[1]) / 2.0, p1[2]]






    
    # ============================================================================================================
    # helper
    # ============================================================================================================
    '''
    @param val: search value
    @param plist: point list
    @param dim: dimension
    @return: index of searched value 
    '''     
    def contain(self, val, plist, dim=0):
        i = 0
        for l in plist :
            if l[dim] == val : 
                return i
            i += 1
        return -1     
     
    def bezierCurve(self, x, c, i, N) :
        return x/c     
       
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
    
    def abs(self, value):
        return -value if value < 0 else value 

    # ================================================================================================================
    # debug helper
    # ================================================================================================================    
    
    def __debug(self, value):
        logging.debug("#######################################################################")
        logging.debug(str(value))
        logging.debug("#######################################################################")
       
    def __printDetails(self):
        print "top: " , self.pointList_top
       # print "bot: " , self.pointList_bot[::-1]
       # print "cham:" , self.pointList_camber
        #print "chord:", self.pointList_chord
        #print "arch"  , self.get_profile_arch()
        #print "len"   , self.get_len_chord()
        #print "thick" , self.get_profile_thickness() 
       
        