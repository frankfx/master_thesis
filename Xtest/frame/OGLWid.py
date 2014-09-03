'''
Created on Aug 24, 2014

@author: rene
'''
#! /usr/bin/env python


from PySide import QtGui, QtCore
from PySide.QtOpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import sys
from Xtest.frame import NewTest



class Viewer3DWidget(QGLWidget):

    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.setMouseTracking(True)
        # self.setMinimumSize(500, 500)
        self.isPressed = False
        self.oldx = self.oldy = 0

    def paintGL(self):
        glMatrixMode( GL_PROJECTION )
        glLoadIdentity()
        glMatrixMode( GL_MODELVIEW );
        glLoadIdentity();

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glDepthFunc( GL_LEQUAL );
        glEnable( GL_DEPTH_TEST );
        glEnable( GL_CULL_FACE );
        glFrontFace( GL_CCW );
        glDisable( GL_LIGHTING );
        glShadeModel( GL_FLAT );

        glColor(1.0, 1.0, 1.0)
        glBegin(GL_LINE_STRIP)
        glVertex(-1,-1,-1)
        glVertex( 1,-1,-1)
        glVertex( 1, 1,-1)
        glVertex(-1, 1,-1)
        glVertex(-1,-1, 1)
        glVertex( 1,-1, 1)
        glVertex( 1, 1, 1)
        glVertex(-1, 1, 1)
        glEnd()
        glColor(1.0, 0.0, 0.0)
        glBegin(GL_LINES)
        glVertex( 0, 0, 0)
        glVertex( 1, 0, 0)
        glEnd()
        glColor(0.0, 1.0, 0.0)
        glBegin(GL_LINES)
        glVertex( 0, 0, 0)
        glVertex( 0, 1, 0)
        glEnd()
        glColor(0.0, 0.0, 1.0)
        glBegin(GL_LINES)
        glVertex( 0, 0, 0)
        glVertex( 0, 0, 1)
        glEnd()

        glFlush()

    def resizeGL(self, widthInPixels, heightInPixels):
        glViewport(0, 0, widthInPixels, heightInPixels)

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)

        # glMatrixMode(GL_PROJECTION)
        # glLoadIdentity()

    def mouseMoveEvent(self, mouseEvent):
        if int(mouseEvent.buttons()) != QtCore.Qt.NoButton :
            # user is dragging
            delta_x = mouseEvent.x() - self.oldx
            self.update()
        self.oldx = mouseEvent.x()
        self.oldy = mouseEvent.y()

    def mouseDoubleClickEvent(self, mouseEvent):
        print "double click"

    def mousePressEvent(self, e):
        print "mouse press"
        self.isPressed = True

    def mouseReleaseEvent(self, e):
        print "mouse release"
        self.isPressed = False

class PythonQtOpenGLDemo(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('Python Qt OpenGL Demo')
        self.statusBar().showMessage("Hello there")

        exit = QtGui.QAction("Exit", self)
        exit.setShortcut("Ctrl+Q")
        exit.setStatusTip('Exit application')
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exit)

        self.setToolTip('This is a window, or <b>something</b>')

        viewer3D = NewTest.MyWidget()
        createButtons = True
        if createButtons:
            parentWidget = QtGui.QWidget()

            button1 = QtGui.QPushButton("Button 1")
            button1.setStatusTip('Button 1 does something')
            self.connect(button1, QtCore.SIGNAL('clicked()'), self.button1Action)
            button2 = QtGui.QPushButton("Button 2")
            button2.setToolTip('Button 2 does something else')
            self.connect(button2, QtCore.SIGNAL('clicked()'), self.button2Action)
            vbox = QtGui.QVBoxLayout()
            vbox.addWidget(button1)
            vbox.addWidget(button2)
            vbox.addStretch(1)
            viewer3D.setSizePolicy( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding )
            hbox = QtGui.QHBoxLayout()
            hbox.addLayout(vbox)
            hbox.addWidget(viewer3D)

            parentWidget.setLayout(hbox)
            self.setCentralWidget(parentWidget)
        else:
            self.setCentralWidget(viewer3D)

        self.resize(500,500)

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, "Confirmation",
            "Are you sure to quit?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    def button1Action( self ):
        print "button 1"
    def button2Action( self ):
        print "button 2"

if __name__ == '__main__':
    # app = QtGui.QApplication(['Python Qt OpenGL Demo'])
    app = QtGui.QApplication(sys.argv)
    window = PythonQtOpenGLDemo()
    window.show()
    sys.exit(app.exec_())

