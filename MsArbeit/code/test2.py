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