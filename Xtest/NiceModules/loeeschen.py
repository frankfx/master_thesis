def __strRemoveReverseToChar(s, c):
    return __rm_rec(s, c)
    
def __rm_rec(s, c):
    if s == "" :
        return ""
    elif s[-1] == c :
        return s[:-1]
    else :
        return __rm_rec(s[:-1], c)
        


def __breakStringAtPos(string, pos, end=40):
    if string == "" :
        return ""
    elif pos == end and string[0] == '/':
        return string[0] + "/n" + __breakStringAtPos(string[1:], 0)
    elif pos < end :
        return string[0] + __breakStringAtPos(string[1:], pos+1)
    else :
        return string[0] + __breakStringAtPos(string[1:], pos)


l = "Rene liebt/ Marita ganz/ ganz/ sehr. Und/ das ist fein"

print __breakStringAtPos(l, 0, 5)