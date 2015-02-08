'''
Created on Sep 17, 2014

@author: fran_re
'''
import math

class Test():
    
    def __init__(self):
        self.pointList_top = [[1.0, 0.00095, 0.0], [0.95, 0.00605, 0.0], [0.9, 0.01086, 0.0], [0.8, 0.01967, 0.0], [0.7, 0.02748, 0.0], [0.6, 0.03423, 0.0], [0.5, 0.03971, 0.0], [0.4, 0.04352, 0.0], [0.3, 0.04501, 0.0], [0.25, 0.04456, 0.0], [0.2, 0.04303, 0.0], [0.15, 0.04009, 0.0], [0.1, 0.03512, 0.0], [0.075, 0.0315, 0.0], [0.05, 0.02666, 0.0], [0.025, 0.01961, 0.0], [0.0125, 0.0142, 0.0], [0.005, 0.0089, 0.0], [0.0, 0.0, 0.0]]
        self.pointList_bot = [[1.0, -0.00095, 0.0], [0.95, -0.00605, 0.0], [0.9, -0.01086, 0.0], [0.8, -0.01967, 0.0], [0.7, -0.02748, 0.0], [0.6, -0.03423, 0.0], [0.5, -0.03971, 0.0], [0.4, -0.04352, 0.0], [0.3, -0.04501, 0.0], [0.25, -0.04456, 0.0], [0.2, -0.04303, 0.0], [0.15, -0.04009, 0.0], [0.1, -0.03512, 0.0], [0.075, -0.0315, 0.0], [0.05, -0.02666, 0.0], [0.025, -0.01961, 0.0], [0.0125, -0.0142, 0.0], [0.005, -0.0089, 0.0], [0.0, 0.0, 0.0]]
        self._LeadingEdge , self._TrailingEdge        = self.__getEndPoints(self.pointList_top, self.pointList_bot)        
        self.pointList_chord                    = self.createPointList_chord(self._LeadingEdge, self._TrailingEdge, len(self.pointList_top)) 
        self.__linePerpendicularGradient_m      = self.__computeLinePerpendicularGradient(self.pointList_chord)
        self.pointList_camber                   = self.__computeCamber()
        print self.pointList_camber
    
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
    @param plist: list with line coordinates
    @param srcPoint: point on plist where perpendicular intersects
    @return: perpendicular as lambda function  or  None if m is 0
    '''
    def __createLinePerpendicular(self, plist, srcPoint):
        m_perpendicular = self.__computeLinePerpendicularGradient(plist)
        b = srcPoint[1] - m_perpendicular * srcPoint[0]
        
        return None if m_perpendicular == 0 else lambda x : m_perpendicular * x + b   
       
    '''
    @return: camber list
    ''' 
    def __computeCamber(self):
        res = []
        for p in self.pointList_chord :
            fct_perpendicular   = self.__createLinePerpendicular(self.pointList_chord, p)
            if fct_perpendicular is not None:
                intersect_top       = self.__computeIntersectionPoint(self.pointList_top, fct_perpendicular)
                intersect_bot       = self.__computeIntersectionPoint(self.pointList_bot, fct_perpendicular)
            
                res.append( self.getPointBtwPoints(intersect_top, intersect_bot)) 
            
        
        return res

    def __computeCamber2(self):
        for i in range(0, len(self.pointList_top)) :
            

    '''
    @param plist: top or bottom list
    @param fct_perpendicular: the perpendicular of chord line as a lambda function 
    @return: approximated intersection point between plist line and chord perpendicular
    '''
    def __computeIntersectionPoint(self, plist, fct_perpendicular):
        res = None
        for p in plist :
            if res is None :
                res = p
            else:
                y = fct_perpendicular (p[0])
                print y, p, " ==== " , self.absolut(y - p[1])
                if self.absolut(y - p[1]) < self.absolut(y-res[1]) :
                    res = p
        print "intersect Point" , res
        return res     


    def absolut(self, value):
        return -value if value < 0 else value

    '''
    @param p1: profile start point (nose)
    @param p2: profile end point
    @param point_cnt: count of points to create
    @return: list with chord points    
    '''
    def createPointList_chord(self, p1, p2, point_cnt) : 
        dist = p2[0] - p1[0]
        interval = dist/ point_cnt  
        
        res = [p1]
        for i in range(1, point_cnt+1):
            p = self.__computePointOnLine(p1[0] + i*interval, p1, p2)
            res.append(p)
        return res

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
            return None

        # m = (y2-y1) / (x2-x1) ;;; b = y2 - m-x2 
        m = ( snd[1] - fst[1] ) / ( snd[0] - fst[0] )
        b = snd[1] - m * snd[0]

        y = m * x + b
        return [x, y, p1[2]]  



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
            tmp_dist = self.__getDistanceBtwPoints(p, maxP)
            if tmp_dist > max_dist :
                max_dist = tmp_dist
                minP     = p
        return minP , maxP  
    
    '''
    @param p1: first point
    @param p2: second point
    @return: distance between p1 and p2
    '''    
    def __getDistanceBtwPoints(self, p1, p2):
        a = (p1[0] - p2[0]) * (p1[0] - p2[0])
        b = (p1[1] - p2[1]) * (p1[1] - p2[1])
        return math.sqrt( a + b )    
   
    def getPointBtwPoints(self, p1, p2):
        distX = p1[0] - p2[0]
        distY = p1[1] - p2[1]
        halfX = distX / 2
        halfY = distY / 2
        return [p1[0] - halfX, p1[1] - halfY, p1[2]]   
    
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
    
a = Test()