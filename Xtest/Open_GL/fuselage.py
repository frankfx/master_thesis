'''
Created on Oct 8, 2014

@author: fran_re
'''
import sys
from PySide import QtGui
from profile import Profile


try:
    from OpenGL import GL, GLU
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

#class Fuselage(Profile):
#    def __init__(self, name, tigl, plist, parent = None):
#        super(Fuselage, self).__init__(name, tigl, plist, parent)

class Fuselage(Profile):
    def __init__(self, name, tigl, plist, parent = None):
        super(Fuselage, self).__init__(name, tigl, plist, parent)
