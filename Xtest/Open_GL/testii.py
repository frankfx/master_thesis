# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
#from PySide import QtOpenGL, QtGui, QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_TabWidget(QtGui.QTabWidget):
    def setupUi(self, QTabWidget):
        QTabWidget.setObjectName(_fromUtf8("TabWidget"))
        QTabWidget.resize(653, 593)
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayoutWidget = QtGui.QWidget(self.tab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(80, 20, 501, 441))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget_2 = QtGui.QWidget(self.verticalLayoutWidget)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.tableWidget = QtGui.QTableWidget(self.widget_2)
        self.tableWidget.setGeometry(QtCore.QRect(-10, 160, 499, 291))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.widget_3 = QtGui.QWidget(self.widget_2)
        self.widget_3.setGeometry(QtCore.QRect(40, 30, 421, 111))
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.spinBox = QtGui.QSpinBox(self.widget_3)
        self.spinBox.setGeometry(QtCore.QRect(40, 40, 56, 22))
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.lineEdit_5 = QtGui.QLineEdit(self.widget_3)
        self.lineEdit_5.setGeometry(QtCore.QRect(0, 10, 113, 22))
        self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))
        self.verticalLayout.addWidget(self.widget_2)
        QTabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab1 = QtGui.QWidget()
        self.tab1.setObjectName(_fromUtf8("tab1"))
        self.gridLayoutWidget = QtGui.QWidget(self.tab1)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 20, 591, 511))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lineEdit_3 = QtGui.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.gridLayout.addWidget(self.lineEdit_3, 2, 1, 1, 1)
        self.widget = QtGui.QWidget(self.gridLayoutWidget)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.textEdit = QtGui.QTextEdit(self.widget)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 431, 201))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 2)
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.lineEdit_4 = QtGui.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.gridLayout.addWidget(self.lineEdit_4, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.lineEdit_2 = QtGui.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.gridLayout.addWidget(self.lineEdit_2, 3, 1, 1, 1)
        self.lineEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 4, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 5, 1, 1, 1)
        self.pushButton_3 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout.addWidget(self.pushButton_3, 5, 0, 1, 1)
        QTabWidget.addTab(self.tab1, _fromUtf8(""))

        self.retranslateUi(QTabWidget)
        QTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(QTabWidget)

    def retranslateUi(self, TabWidget):
        TabWidget.setWindowTitle(_translate("TabWidget", "TabWidget", None))
        TabWidget.setTabText(TabWidget.indexOf(self.tab), _translate("TabWidget", "Tab 1", None))
        self.label.setText(_translate("TabWidget", "maximale Profilwölbung (%)", None))
        self.label_3.setText(_translate("TabWidget", "Wölbungsrücklage (in Zehnteln der Profilsehne)", None))
        self.label_2.setText(_translate("TabWidget", "maximale Profildicke (%)", None))
        self.pushButton_2.setText(_translate("TabWidget", "PushButton", None))
        self.pushButton_3.setText(_translate("TabWidget", "PushButton", None))
        TabWidget.setTabText(TabWidget.indexOf(self.tab1), _translate("TabWidget", "Tab 2", None))





class MyWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        super(MyWidget, self).__init__(parent)
        self.resize(320,320)
        self.setWindowTitle("Rene Test")
        #self.setFixedSize(QtCore.QSize(400,400))
        lay = QtGui.QGridLayout()
        t = Ui_TabWidget()
        lay.addWidget(t)
        self.setLayout(lay)

if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = MyWidget()
    widget.show()
    app.exec_()   
