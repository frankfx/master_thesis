'''
Created on Aug 19, 2014

@author: fran_re
'''
import pydoc
import inspect

def test():
    """This is an example of algorithm documentation entries.

    Note using capitalized keyword "ALGO" to see
    algorithm pydoc entries more quickly in the
    code.

    Also note the use of "pass" in the example: If
    a comment is not followed by at least one line
    of actual code it does not end up in
    inspect.getsource() and inspect.getsourcelines."""

    #ALGO: If file exists:
    if True:
        #ALGO: Delete file
        pass

    #ALGO: Create the file
    pass

    #ALGO: Open file
    pass

    #ALGO: Write data to file
    pass

    #ALGO: Close file
    pass

def getdoc(object):
    algoComments = []
    sourceLines = inspect.getsourcelines(object)[0]
    for line in sourceLines:
        lineLower = line.lower()

        while True:
            s = "# algo "
            if lineLower.find(s) != -1:
                break
            s = "# algo: "
            if lineLower.find(s) != -1:
                break
            s = "#algo "
            if lineLower.find(s) != -1:
                break
            s = "#algo: "
            if lineLower.find(s) != -1:
                break

            s = None
            break

        if s is not None:
            start       = lineLower.find(s)
            end         = start + len(s)
            indent      = line[:start - 1]
            algoComment = line[end:]
            algoComments.append(indent + algoComment)

    s = inspect_getdoc(object)

    if len(algoComments) > 0:
        s += "\n\nAlgorithm:\n"
        for c in algoComments:
            s += c

    return s

# "Install" the extension by replacing inspect.getdoc().
# Keep the reference to the previous inspect.getdoc()
# to call it ourselves.
inspect_getdoc = inspect.getdoc
inspect.getdoc = getdoc

if __name__ == "__main__":
    pydoc.help(test)