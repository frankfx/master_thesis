'''
Created on Oct 1, 2014

@author: fran_re
'''
import sys
import math
from PySide import QtOpenGL, QtGui, QtCore


try:
    from OpenGL import GL, GLU, GLUT
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

class TestItem(QtGui.QGraphicsItem):

    def __init__(self, parent=None, scene=None):
        super(TestItem, self).__init__(parent, scene)
        self.setFlags(self.ItemIsMovable | self.ItemIsSelectable)

    def boundingRect(self):
        return QtCore.QRectF(0,0,50,50)

    def paint(self, painter, options, widget=None):
        painter.drawRect(self.boundingRect())

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu()
        testAction = QtGui.QAction('Test', None)
        testAction.triggered.connect(self.print_out)
        menu.addAction(testAction)
        menu.exec_(event.screenPos())
#        menu.exec_(event.globalPos())

    def print_out(self):
        print 'Triggered'

if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    window = QtGui.QWidget()
    scene = QtGui.QGraphicsScene()

    item = TestItem(scene=scene)
    view = QtGui.QGraphicsView(scene)

    layout = QtGui.QVBoxLayout()
    layout.addWidget(view)
    window.setLayout(layout)
    window.show()
    sys.exit(app.exec_())