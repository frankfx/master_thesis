'''
Created on Sep 3, 2014

@author: rene
'''

import sys
import math
import utility
from PySide import QtGui
from profile import Profile

try:
    from OpenGL import GL
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

class Airfoil(Profile):
    def __init__(self, plist, parent = None):
        super(Airfoil, self).__init__(plist,parent)
        
        if plist == None : return

        self.trailingEdge                       = self.__computeTrailingEdge(self.pointList)
        self.leadingEdge                        = self.__computeLeadingEdge(self.pointList )
        self.pointList_bot , self.pointList_top = self.__createPointList_bot_top(self.leadingEdge, self.pointList)
        self.pointList_chord                    = self.__createPointList_chord(self.leadingEdge, self.trailingEdge,len(self.pointList_bot))        
        self.pointList_camber, self.thickness   = self.__createPointList_camber(self.pointList_bot, self.pointList_top, self.pointList_chord)
        self.pointList_top_rot                  = self.pointList_top
        self.pointList_bot_rot                  = self.pointList_bot

        self.flag_close_TrailingEdge = False
        self.flag_draw_camber        = False
        self.flag_draw_chord         = False

    # ================================================================================================================
    # drawing functions
    # ================================================================================================================
    def drawChord(self):
        start, end = self.getEndPoints()
        
        GL.glBegin(GL.GL_LINES)
        GL.glVertex3f(start[0], start[1], start[2]) # leftend (nose)
        GL.glVertex3f(end[0], end[1], end[2]) # right end
        GL.glEnd()

    def drawCamber(self):
        plist = self.getPointListCamber()
        GL.glBegin(GL.GL_LINE_STRIP)
        for i in range(0, len(plist)) :
            GL.glVertex3f(plist[i][0], plist[i][1], plist[i][2])# left end == nose
        GL.glEnd()

    # ================================================================================================================
    # computations
    # ================================================================================================================
    '''
    @param list1: first list
    @param list2: second list
    @return: max distance between p1 of list1 and corresponding p2 of list2
    '''   
    def __computeAirfoilThickness(self, list1, list2):
        dist = -1.0
        for p in self.getPointListCamber() :
            dist1 = utility.computeMinDistance(p, list1)
            dist2 = utility.computeMinDistance(p, list2)
            cur_dist = dist1 + dist2
            if dist < 0.0 or cur_dist > dist : 
                print "p" , p , dist1, dist2          
                dist = cur_dist
        return dist
 
    '''
    @param list1: first list
    @param list2: second list
    @return: distance between p1 of list1 and corresponding p2 of list2
    '''   
    def __computeAirfoilArch(self, list1, list2):
        dist = -1.0
        for p in list1 :
            cur_dist = utility.computeMinDistance(p, list2)
            if cur_dist > dist :
                dist = cur_dist
        return dist

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
        thickness = -1.0
        for p_chord in plist_chord :
            m, b = utility.createPerpendicular(self.leadingEdge, self.trailingEdge, p_chord)
            # fkt is perpendicular to y-axis, then for all y: fkt(y) = b and compute y by neigbors
            if m == (None, "y") :
                p_bot = [b,self.approxNeighbors(b, plist_bot), p_chord[2]]
                p_top = [b,self.approxNeighbors(b, plist_top), p_chord[2]]
            # fkt has gradient 0, then for all x: fkt(x) = b and compute x by neigbors
            elif m == (None, "x") :
                p_bot = [self.approxNeighbors(b, plist_bot, 1), b, p_chord[2]]
                p_top = [self.approxNeighbors(b, plist_top, 1), b, p_chord[2]]
            else :
                p_bot = self.__getPointWithMinDistanceToChordPerpendicular(m, b, plist_bot)
                p_top = self.__getPointWithMinDistanceToChordPerpendicular(m, b, plist_top)
            ## =================================================================================
            ## extra calculation --> thicknes
            cur_dist = utility.getDistanceBtwPoints(p_top, p_bot)
            if thickness < 0.0 or cur_dist > thickness :
                thickness = cur_dist
            ## =================================================================================
            
            res.append(utility.getCenterPoint(p_bot, p_top))
        return res , thickness
        
    def approxNeighbors(self, val, plist, dim=0):
        for i in range(0, len(plist)):
            if utility.equalFloats2(plist[i][dim], val) :
                return plist[i][1]
            elif self.__hasNeighborsAtIdx(i, val, plist, dim) :
                return utility.getCenterPoint(plist[i-1], plist[i])[0 if dim == 1 else 1]
        raise Exception("unexpected behavior in approxNeighbors")
      
    def __hasNeighborsAtIdx (self, i, val, plist, dim):      
        if i == 0 or i == len(plist) : return False
        elif plist[i-1][dim] > val and plist[i][dim] < val or \
             plist[i-1][dim] < val and plist[i][dim] > val :
            return True
            
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

    # ============================================================================================================
    # update functions
    # ============================================================================================================
    def updateThickness(self):
        self.thickness = self.__computeAirfoilThickness(self.pointList_top, self.pointList_bot)
    
    def updateLeadingEdge(self):
        self.leadingEdge = self.__computeLeadingEdge(self.pointList)
    
    def updateTrailingEdge(self):
        self.trailingEdge = self.__computeTrailingEdge(self.pointList)    
        
    def updatePointList_Bot_Top(self):
        #print "warning, depends on updated pointList and leading Edge"
        self.pointList_bot, self.pointList_top  = self.__createPointList_bot_top(self.leadingEdge, self.pointList)            
    
    def updatePointListChord(self):
        #print "warning, depends on updated pointList, trailing Edge and leading Edge"
        self.pointList_chord = self.__createPointList_chord(self.leadingEdge, self.trailingEdge, len(self.pointList)/2)    
    
    def updatePointListCamber(self):
        #print "warning, depends on updated pointList_bot, pointList_top and pointList_chord"
        self.pointList_camber , self.thickness = self.__createPointList_camber(self.pointList_bot, self.pointList_top, self.pointList_chord)    
    
    def updateRotationLists(self, angle):
        #print "warning, depends on updated pointList_chord and pointList"
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
        
    def updateAll(self):
        self.updatePointListsForNaca()
        self.pointList_camber , self.thickness  = self.__createPointList_camber(self.pointList_bot, self.pointList_top, self.pointList_chord)
        self.pointList_top_rot                  = self.pointList_top
        self.pointList_bot_rot                  = self.pointList_bot

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
        
    def setFlagDrawCamber(self, value):
        self.flag_draw_camber = value
        self.updateGL()      
        
    def setFlagDrawChord(self, value):
        self.flag_draw_chord = value
        self.updateGL()  

    def setFlagCloseTrailingEdge(self, value):
        self.flag_close_TrailingEdge = value
        self.updateGL()

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

    def getLenChord(self):
        return utility.getDistanceBtwPoints(self.getTrailingEdge(), self.getLeadingEdge())   
    
    def getEndPoints(self):
        return self.leadingEdge, self.trailingEdge
    
    def getTrailingEdge(self):
        return self.trailingEdge
  
    def getLeadingEdge(self):
        return self.leadingEdge

    '''
    thickness is defined as max circle diameter on camber line
    '''
    def getAirfoilThickness(self):
        # thickness will computed by camber construction. For Naca we use a seperate inbuild camber 
        # construction without thickness computing --> therefor call updateThickness
        return 100.0 * self.thickness   

    '''
    maximum deviation from camber line to chord line
    '''      
    def getAirfoilArch(self):
        return 100.0 * self.__computeAirfoilArch(self.pointList_chord, self.pointList_camber)  

    '''
    working angle of airfoil
    '''
    @utility.overrides(Profile)
    def getWorkAngle (self):
        # computes the the real rotation of the coordinates
        ## sin(x) = a/c
        start, _ = self.getEndPoints()
        x = start[1] / self.getLenChord()
        
        # get the virtual openGL rotate and sum both
        res = -self.getRotAngle() + math.sin(x)

        return 0 if res == -0 else res
  
    def getFlagCloseTrailingEdge(self):
        return self.flag_close_TrailingEdge
    
    def getFlagDrawCamber(self):
        return self.flag_draw_camber
    
    def getFlagDrawChord(self):
        return self.flag_draw_chord        