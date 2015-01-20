


file = open("test")

max = 0
for line in file:
    for c in line :
        try :
            x = float(c)
            max = x if x > max else max
        except Exception:
            pass    

file.close()


print max


