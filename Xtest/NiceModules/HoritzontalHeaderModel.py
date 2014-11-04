'''
Created on Nov 3, 2014

@author: fran_re
'''
import sys
  
from PySide import QtCore, QtGui
  
  
datas = [
    "a",
    "b",
    "c",
]
  
class Demo(QtGui.QWidget):
    def __init__(self):
  
        QtGui.QWidget.__init__(self)
  
        self.treeView = QtGui.QTreeView()
        self.model = QtGui.QStandardItemModel()
        for name in datas:
            item = QtGui.QStandardItem(name)
            self.model.appendRow(item)
        self.treeView.setModel(self.model)
  
        self.model.setHorizontalHeaderLabels([self.tr("Object")])
  
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.treeView)
        self.setLayout(layout)
  
  
        self.popup_menu = QtGui.QMenu(self)
  
        # menu item
        self.item_add_act = QtGui.QAction("Add", self)
        self.item_add_act.triggered.connect(self.add_cb)
        self.popup_menu.addAction(self.item_add_act)
  
    def add_cb(self):
        print "add callback"
  
    def contextMenuEvent(self, event):
        point = self.mapToGlobal(event.pos())
        widget = QtGui.QApplication.widgetAt(point)
        print "widget:", widget
  
        act = self.popup_menu.exec_(point)
  
        if act == self.item_add_act:
            print "item add clicked"
  
        return super(Demo, self).contextMenuEvent(event)
  
    def show_and_raise(self):
        self.show()
        self.raise_()
  
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
  
    demo = Demo()
    demo.show_and_raise()
  
    sys.exit(app.exec_())