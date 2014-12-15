


for i in range(0,20) :
    p = i
    p1 = i+1 if i%4 != 3 else i-3 
    p2 = i-1 if i%4 != 0 else i+3
    
    print p2 , p, p1