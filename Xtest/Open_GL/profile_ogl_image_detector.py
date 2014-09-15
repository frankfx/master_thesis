'''
Created on Sep 2, 2014

@author: rene
'''
import sys
import math
from PySide import QtOpenGL, QtGui, QtCore
from Xtest.Open_GL.profile_ogl import Profile

try:
    from OpenGL import GL, GLU, GLUT
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

class MyProfileWidget(Profile):
    def __init__(self, parent = None):
        super(MyProfileWidget, self).__init__(parent)
        
        self.imageLabel = QtGui.QLabel()
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        self.setSizePolicy ( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        #self.imageLabel.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)
        grid = QtGui.QGridLayout()

        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        #self.setCentralWidget(self.scrollArea)
        grid.addWidget(self.scrollArea)
        self.setLayout(grid)
        self.printer = QtGui.QPrinter()



        self.createActions()
        self.createMenus()

        self.setWindowTitle("Image Viewer")
        self.resize(100, 100)
      
    def open(self) :
        (fileName, _) = QtGui.QFileDialog.getOpenFileName(self,
                                     "Open File", QtCore.QDir.currentPath())
        
        image = None
        if (fileName) :
            print fileName
            image = QtGui.QImage(fileName)
            print image
            if (image is None) :
                QtGui.QMessageBox.information(self, "Image Viewer",
                                         "Cannot load " + str(fileName))
                return
    
            self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))
            self.scaleFactor = 1.0
    
            self.printAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if (not self.fitToWindowAct.isChecked()) :
                self.imageLabel.adjustSize()
     
 
    def printS(self):
        QtCore.Qt.Q_ASSERT(self.imageLabel.pixmap())

        dialog = QtGui.QPrintDialog(self.printer, self)
        if (dialog.exec_()) : 
            painter = QtGui.QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), QtCore.Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())


    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow :
            self.normalSize()
        self.updateActions()

    def about(self):
        QtGui.QMessageBox.about(self, tr("About Image Viewer"),
             tr("<p>The <b>Image Viewer</b> example shows how to combine QLabel "
                "and QScrollArea to display an image. QLabel is typically used "
                "for displaying a text, but it can also display an image. "
                "QScrollArea provides a scrolling view around another widget. "
                "If the child widget exceeds the size of the frame, QScrollArea "
                "automatically provides scroll bars. </p><p>The example "
                "demonstrates how QLabel's ability to scale its contents "
                "(QLabel::scaledContents), and QScrollArea's ability to "
                "automatically resize its contents "
                "(QScrollArea::widgetResizable), can be used to implement "
                "zooming and scaling features. </p><p>In addition the example "
                "shows how to use QPainter to print an image.</p>"))


    def echo(self):
        print()

    def createActions(self):
        self.openAct = QtGui.QAction('Open...', self)
        self.openAct.triggered.connect(self.open)
    
        self.printAct = QtGui.QAction("Print...", self)
        self.printAct.setEnabled(False)
        self.printAct.triggered.connect(self.echo)
        
        
        self.exitAct = QtGui.QAction("E&xit", self);
        self.exitAct.triggered.connect(self.close)
    
        self.zoomInAct = QtGui.QAction("Zoom In (25%)", self)
        self.zoomInAct.setEnabled(False)
        self.zoomInAct.triggered.connect(self.zoomIn)


        self.zoomOutAct = QtGui.QAction("Zoom Out (25%)", self)
        self.zoomOutAct.setEnabled(False)
        self.zoomOutAct.triggered.connect(self.zoomOut)

    
        self.normalSizeAct = QtGui.QAction("Normal Size", self)
        self.normalSizeAct.setEnabled(False)
        self.normalSizeAct.triggered.connect(self.normalSize)
    
        self.fitToWindowAct = QtGui.QAction("&Fit to Window", self)
        self.fitToWindowAct.setEnabled(False)
        self.fitToWindowAct.setCheckable(True)
        self.fitToWindowAct.triggered.connect(self.fitToWindow)

        
    def createMenus(self):
        fileMenu = QtGui.QMenu("File", self)
        fileMenu.addAction(self.openAct)
        fileMenu.addAction(self.printAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAct)

        viewMenu = QtGui.QMenu("View", self)
        viewMenu.addAction(self.zoomInAct)
        viewMenu.addAction(self.zoomOutAct)
        viewMenu.addAction(self.normalSizeAct)
        viewMenu.addSeparator()
        viewMenu.addAction(self.fitToWindowAct)

        menubar = QtGui.QMenuBar(self)
        menubar.addMenu(fileMenu)
        menubar.addMenu(viewMenu)


    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())
 

    def scaleImage(self, factor):
        #QtCore.Qt.Q_ASSERT(self.imageLabel.pixmap())
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0);
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333);

    def adjustScrollBar(self, scrollBar, factor) :
        scrollBar.setValue(factor * scrollBar.value() + ((factor - 1) * scrollBar.pageStep()/2))

 
        
if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = MyProfileWidget()
    widget.show()
    app.exec_()   