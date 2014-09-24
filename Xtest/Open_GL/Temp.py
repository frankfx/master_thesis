        n = 4                   # for safty
                                # plist = getCompleteList
      
        
        axis0 = []              # result list
        idx_b = 0               # index botList first point
        idx_t = len(plist) - 1  # index topList first point
        
        # for all bottom points 
        for idx_b in range(0, idx_t) : 
            if not idx_b + n < idx_t : break

            # get x, y, z of bottom
            x_b = plist[idx_b][0]
            y_b = plist[idx_b][1]
            z_b = plist[idx_b][2]
            
            # set i to last possible value of top points (trailing edge)
            i = len(plist)-1 if idx_t + n > len(plist)-1 else idx_t + n
            
            # save idx_t
            tmp_idx_t = idx_t
            
            # dist help value, set to None
            dist = -1.0
            
            # look for top points
            for i in range(i, idx_b, -1) :
                if not i > idx_b + n : break
                
                x_t = plist[i][0]
                y_t = plist[i][1]
                z_t = plist[i][2]                
                
                # cur_dist = distance between current bot and top point
                cur_dist = ((x_t-x_b)*(x_t-x_b))+((y_t-y_b)*(y_t-y_b))
                
                # find closest distance
                if ((dist < 0.0) or ((cur_dist <= dist) and (cur_dist>1e-10))) :
                    idx_t = i 
                    dist = cur_dist
                if ((dist >= 0.0) and (cur_dist > dist)) :
                    break
                
            if (dist >= 0.0) :
                # stop if non valid closest point found
                if (idx_t - idx_b <= n+1) :
                    idx_t = tmp_idx_t 
                    break 
                
                x_t = plist[idx_t][0]
                y_t = plist[idx_t][1]
                z_t = plist[idx_t][2]
                
                axis0.append([0.5*(x_b + x_t), 0.5*(y_b + y_t), 0.5*(z_b + z_t)])