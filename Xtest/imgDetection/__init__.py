l1 = [(0,0),(0.0334,-0.0767),(0.1087,-0.1437),(0.2253,-0.2011),(0.3824,-0.2489),(0.5790,-0.2870),\
      (0.8139,-0.3158),(1.0860,-0.3355),(1.3940,-0.3466),(1.7365,-0.3497),(2.1123,-0.3457),(2.5199,-0.3356),\
      (2.9580,-0.3209),(3.4252,-0.3029),(3.9198,-0.2835),(4.4427,-0.2625),(4.9936,-0.2377),(5.5666,-0.2102),\
      (6.1594,-0.1810),(6.7696,-0.1513),(7.3950,-0.1217),(8.0332,-0.0930),(8.6815,-0.0653),(9.3376,-0.0386),\
      (9.9988,-0.0125)]

l2 = [(0,0),(0.0095,0.0831),(0.0624,0.1691),(0.1590,0.2574),(0.2990,0.3467),(0.4824,0.4357),(0.7085,0.5225),\
      (0.9765,0.6050),(1.2855,0.6812),(1.6341,0.7488),(2.0206,0.8055),(2.4433,0.8492),(2.8998,0.8778),(3.3879,0.8897),\
      (3.9049,0.8833),(4.4459,0.8592),(5.0064,0.8210),(5.5876,0.7687),(6.1870,0.7023),(6.8016,0.6219),(7.4286,0.5277),\
      (8.0650,0.4197),(8.7080,0.2980),(9.3544,0.1623),(10.0012,0.0125)]

res = []
for i in range(0,len(l1)) :
    (x1, y1) = l1[i]
    (x2, y2) = l2[i]
    
    x3 = round(x1 + ((x2-x1)/2.0), 3) 
    y3 = round(y1 + ((y2-y1)/2.0), 3)
    
    res.append((x3, y3))

#print ''.join(map(str, res))
print "\draw[dashed,line width=1pt,fill=black!5] plot coordinates {" , ''.join(map(str, res)) , "};"
    