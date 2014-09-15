'''
Created on Sep 11, 2014

@author: rene
'''
import sys
import math
from PySide import QtOpenGL, QtGui, QtCore
from cpacsHandler import CPACS_Handler
from config import Config
import logging
import datetime

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
        
        self.pointList_top, self.pointList_bot  = self.__createPointList(uid)
        self._leftEndP , self._rightEndP        = self.__getEndPoints(self.pointList_top, self.pointList_bot)
        self.pointList_chord                    = self.__createPointList_chord(self._leftEndP, self._rightEndP, len(self.pointList_top))
        self.pointList_camber                   = self.__createPointList_camber(self.pointList_top, self.pointList_bot)
        
        
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
        l_snd.reverse()
        print l_fst
        print l_snd 
        return l_fst , l_snd
   
   
    '''
    @return: left and right end point
    '''
    def getEndPoints(self):
        return self.__getEndPoints(self.pointList_top, self.pointList_bot)         
        
    '''
    @param toplist: profile top
    @param botlist: profile bottom
    @return: left and right end point
    '''
    def __getEndPoints(self, toplist, botlist):
        
        dim = 0
        _ , max_top = self.get_min_max_of_List(toplist, dim)
        _ , max_bot = self.get_min_max_of_List(botlist, dim)

        maxP = max_top if max_top >= max_bot else max_bot
        maxP = [maxP[0], max_bot[1] + (max_top[1] - max_bot[1])/2, maxP[2]]

        minP = maxP
        max_dist = 0
        tmp_dist = 0

        for p in toplist + botlist :
            tmp_dist = self.get_distance_btw_points(p, maxP)
            if tmp_dist > max_dist :
                max_dist = tmp_dist
                minP     = p
        return minP , maxP  
    
    '''
    @param p1: first point
    @param p2: second point
    @return: distance between p1 and p2
    '''    
    def get_distance_btw_points(self, p1, p2):
        a = (p1[0] - p2[0]) * (p1[0] - p2[0])
        b = (p1[1] - p2[1]) * (p1[1] - p2[1])
        return math.sqrt( a + b )

    '''
    @param list1: first list
    @param list2: second list
    @return: distance between p1 of list1 and corresponding p2 of list2
    '''   
    def get_max_distance_btw_pointLists(self, list1, list2):
        
        dist = -1   
        for p in list1 :
            p1 = self.__computePoint(p, list2)
            cur_dist = self.get_distance_btw_points(p, p1)
            dist = cur_dist if cur_dist > dist else dist            
        return dist  

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

    '''
    @param topList: top list
    @param botList: bottom list
    @return: list of camber points 
    '''
    def __createPointList_camber(self, topList, botList):
        res = []
        for i in range(0, len(topList)):
            p = self.__computePoint(topList[i], botList)
            res.append(p)
        return res
        
    def setPointListTop(self, plist):
        self.pointList_top = plist

    def setPointListBot(self, plist):
        self.pointList_bot = plist
        
    def getPointList_top(self):
        return self.pointList_top
    
    def getPointList_bot(self):
        return self.pointList_bot

    def setPointListCamber(self, plist):
        self.pointList_camber = plist

    def updatePointlistCamber(self):
        self.pointList_camber = self.__createPointList_camber(self.pointList_top, self.pointList_bot)        

    '''
    @param x: x-value of result point
    @param p1: point one of line p1 to p2
    @param p1: point two of line p1 to p2
    @return: Point on Line of Points p1 to p2
    '''
    def __computePointOnLine(self, x, p1, p2):
        fst = p1 if p1[0] <= p2[0] else p2
        snd = p2 if p1[0] <= p2[0] else p1
        if (x < fst[0] or x > snd[0]):
            logging.debug('None in MODULE: dataSet, FUNCTION: __computePointOnLine') 
            logging.debug(str(x) + ', ' + str(p1) + ', ' + str(p2))
            logging.debug('x < fst[0] or x > snd[0]')
            return None

        # m = (y2-y1) / (x2-x1) ;;; b = y2 - m-x2 
        m = ( snd[1] - fst[1] ) / ( snd[0] - fst[0] )
        b = snd[1] - m * snd[0]

        y = m * x + b
        return [x, y, p1[2]]        
        
        
    '''
    ?????????????????????????????????????????????????????
    Bug - nachragen wie line bestimmt wird
    ????????????????????????????????????????????????????
    @param p1: point of topList
    @param plist: botList
    @return: Point in the center of topList and botList at position x  
    '''
    def __computePoint(self, p1, plist):
                
        idx_r = -1
        idx_l = -1
        flag_l = False
        flag_r = False

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
            logging.debug('None in MODULE: dataSet, FUNCTION: __computePoint') 
            logging.debug(str(idx_r) + ', ' + str(idx_l))
            logging.debug('idx_r == -1 or idx_l == -1')
            return None
        elif idx_r == idx_l :
            y = p1[1] - (p1[1] - plist[idx_l][1]) / 2
            return [p1[0], y, p1[2]]

        p_new = self.__computePointOnLine(p1[0], plist[idx_l], plist[idx_r])
        return [p1[0], p1[1] - (p1[1] - p_new[1]) / 2.0, p1[2]]


    def cosineSpacing(self, x, c, i, N) :
        return x/c

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


    def contain(self, x, plist):
        i = 0
        for l in plist :
            if l[0] == x : 
                return i
            i += 1
        return None        
               
       
    def __echo(self, value):
        print "#######################################################################"
        print str(value)
        print "#######################################################################"
       
    def __printDetails(self):
        print "top: " , self.pointList_top
        print "bot: " , self.pointList_bot[::-1]
        print "cham:" , self.pointList_camber
        #print "chord:", self.pointList_chord
        #print "arch"  , self.get_profile_arch()
        #print "len"   , self.get_len_chord()
        #print "thick" , self.get_profile_thickness() 
       
        