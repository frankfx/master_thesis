'''
Created on Sep 2, 2014

@author: rene
'''
from PySide.QtGui import QPushButton
from Xtest.Open_GL import TestSimpleOpenGL, ImageViewer, Profile
'''
Created on Jul 30, 2014

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


class Tab1(QtGui.QWidget):
    def __init__(self, parent = None):
        super(Tab1, self).__init__(parent)
        
        grid = QtGui.QGridLayout()
        self.ogl_widget = Profile.MyWidget()
        
        labZoomIn = QtGui.QLabel("+")
        labZoomOut = QtGui.QLabel("-")
        checkBox = QtGui.QCheckBox("show points")
        checkBox1 = QtGui.QCheckBox("fit to page")
        
        checkBox.toggled.connect(self.fireShowPoints)
        checkBox1.toggled.connect(self.fireFitToPage)
        
        self.sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.sld.setMinimum(1)
        self.sld.setValue(51)
        self.sld.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld.valueChanged[int].connect(self.ogl_widget.zoom)       

        header = ['Funktion', ' Wert']
        self.data_list = [
        ('Name',          self.ogl_widget.get_name()),
        ('Profiltiefe',   self.ogl_widget.get_chord()),
        ('Anstellwinkel', self.ogl_widget.get_work_angle()),
        ('Profildicke',   self.ogl_widget.get_profile_thickness()),
        ('Profilwoelbung',self.ogl_widget.get_profile_arch())
        ]        
        
        table_model = MyTableModel(self, self.data_list, header)
        table_view = QtGui.QTableView()
        table_view.setModel(table_model)
        
        grid.addWidget(labZoomOut, 1,1,1,1)
        grid.addWidget(self.sld, 1,2,1,4)
        grid.addWidget(labZoomIn, 1,6,1,1)
        grid.addWidget(checkBox, 1,8,1,1)
        grid.addWidget(checkBox1, 1,9,1,1)
        
        grid.addWidget(self.ogl_widget, 2, 1, 2, 10)
        grid.addWidget(table_view, 4, 1, 2, 10)        
        self.setLayout(grid)
        
    def fireShowPoints(self):
        self.ogl_widget.setFlagDrawPoints(not self.ogl_widget.getFlagDrawPoints())
    
    def fireFitToPage(self, value):
        if value:
            self.sld.setValue(51) 
            self.sld.setEnabled(False)
        else:
            self.sld.setEnabled(True)
        self.ogl_widget.fitToPage(value)
            

class MyTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, mylist, header, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist
        self.header = header
    def rowCount(self, parent):
        return len(self.mylist)
    def columnCount(self, parent):
        return len(self.mylist[0])
    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != QtCore.Qt.DisplayRole:
            return None
        return self.mylist[index.row()][index.column()]
    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]
        return None
    def sort(self, col, order):
        """sort table by given column number col"""
        ()
        #self.emit(SIGNAL("layoutAboutToBeChanged()"))
        #self.mylist = sorted(self.mylist,
        #    key=operator.itemgetter(col))
        #if order == Qt.DescendingOrder:
        #    self.mylist.reverse()
        #self.emit(SIGNAL("layoutChanged()"))


class Tab2(QtGui.QWidget):
    def __init__(self, parent = None):
        super(Tab2, self).__init__(parent)
        grid = QtGui.QGridLayout()
        label1 = QtGui.QLabel("maximale Profilwoelbung (%)")
        label2 = QtGui.QLabel("Woelbungsruecklage\n(in Zehnteln der Profilsehne)")
        label3 = QtGui.QLabel("maximale Profildicke (%)")
        text1 = QtGui.QLineEdit()
        text2 = QtGui.QLineEdit()
        text3 = QtGui.QLineEdit()
        but1 = QtGui.QPushButton("ok")
        but2 = QtGui.QPushButton("cancel")
        ogl_widget = TestSimpleOpenGL.MyWidget()
        grid.addWidget(label1, 1, 1)
        grid.addWidget(label2, 2, 1)
        grid.addWidget(label3, 3, 1)
        grid.addWidget(text1, 1, 2)
        grid.addWidget(text2, 2, 2)
        grid.addWidget(text3, 3, 2)
        grid.addWidget(but1, 4, 1)
        grid.addWidget(but2, 4, 2)
        grid.addWidget(ogl_widget, 5, 1, 2, 2)
        self.setLayout(grid)



class Tab3(QtGui.QWidget): 
    def __init__(self, parent = None):
        super(Tab3, self).__init__(parent)
        
        grid = QtGui.QGridLayout()
        img_widget = ImageViewer.ImageViewer()
        self.ogl_widget = TestSimpleOpenGL.MyWidget()
        #self.ogl_widget.setFixedSize(200,200)
        
        but1 = QtGui.QPushButton("ok")
        but2 = QtGui.QPushButton("cancel")
        grid.addWidget(but1, 1,1,1,1)
        grid.addWidget(but2, 1,2,1,1)
        grid.addWidget(img_widget,2,1,1,1)
        grid.addWidget(self.ogl_widget,2,2,1,1)
        
    
        self.setLayout(grid)
        

class TabWidget(QtGui.QTabWidget):
    def __init__(self, parent = None):
        super(TabWidget, self).__init__(parent)
        self.setWindowTitle("Tab")
        tab1 = Tab1()
        tab2 = Tab2()
        tab3 = Tab3()
        self.addTab(tab1, "tab1")
        self.addTab(tab2, "tab2")
        self.addTab(tab3, "tab3")


class MyWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        super(MyWidget, self).__init__(parent)
        
        grid = QtGui.QGridLayout()
        but = TabWidget()
        grid.addWidget(but,1,1)
        self.setLayout(grid)   
        
        self.setWindowTitle('Calculator')    
        self.resize(420,520)
        #self.setFixedSize(QtCore.QSize(400,400))
        self.show()
        

if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = MyWidget()
    widget.show()
    app.exec_()    