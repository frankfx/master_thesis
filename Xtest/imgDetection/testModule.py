'''
Created on Sep 2, 2014

@author: rene
'''

class Test():

    def __get_min_max_of_List(self, plist):
        m_max = -1000 # random value
        m_min = 1000  # random value
        id_max = -1
        id_min = -1
        for i in range (0, len(plist),1) :
            if m_max < plist[i][0] :
                m_max = plist[i][0]
                id_max = i
            if m_min > plist[i][0] :
                m_min = plist[i][0]
                id_min = i
        
        return plist[id_min], plist[id_max]

    def computePoint(self, p1, plist):
        index_r = -1
        index_l = -1 
        mini, maxi = self.__get_min_max_of_List(plist)
        
        right_of_x = maxi[0]
        left_of_x = mini[0]
        
        for i in range(0 , len(plist)) :
            if plist[i][0] < p1[0] and plist[i][0] > left_of_x :
                left_of_x = plist[i][0]
                index_l = i
            if plist[i][0] > p1[0] and plist[i][0] < right_of_x :
                right_of_x = plist[i][0]    
                index_r = i
    
    
        # m = (y2-y1) / (x2-x1)
        # b = y2 - m-x2
        m = ( plist[index_r][1] - plist[index_l][1] ) / 1.0 * ( plist[index_r][0] - plist[index_l][0] )  
        b = plist[index_r][1] - m * plist[index_r][0]
                
        y = m * p1[0] + b
        
        return [p1[0], p1[1] - (p1[1] - y) / 2.0, p1[2]]
    

a= Test()
p1 = [2,4,0]
plist = [ [1,2,0], [3,2,0] ]
print a.computePoint(p1, plist)