import sys
from tiglwrapper   import TiglException
from PySide import QtOpenGL, QtGui, QtCore

from Xtest.Vehicle.vehicleData import VehicleData
from Xtest.Open_GL import utility
from Xtest.Vehicle.point import Point
from Xtest.Vehicle.selectionList import SelectionList


from PyQGLViewer import *

try:
    from OpenGL import GL, GLU, GLUT
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

