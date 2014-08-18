import sys
from Xtest.XML_Editor import highlighter
from lxml import etree
from PySide.QtGui import QStackedWidget, QActionGroup, QMessageBox, QAction, QLabel, QColor, QTextFormat, QTextDocument, QTextCursor, QFocusEvent, QMainWindow, QGridLayout, QHBoxLayout, QWidget, QPushButton, QSizePolicy, QLineEdit, QFont, QTextEdit, qApp, QApplication
from PySide.QtCore import QFile, QEvent, Qt, SIGNAL
from Xtest.XML_Editor.editor_CodeCompletion import EditorCodeCompletion
from searchField import SearchField
from numberBar import NumberBar
from cpacsHandler import CPACS_Handler
from config import Config
import tixiwrapper
import re

class EditorWindow(QMainWindow):
    
    """initialize editor"""
    def __init__(self ,model):
        super(EditorWindow, self).__init__()   
       
        self.cpacsHandler = CPACS_Handler()
        self.cur_file_path = ""
        self.cur_schema_path = ""
        
        self.setupEditor()
        self.setupButtonMenu()
        self.setupSearchBox()
        self.setupStatusbar()
        self.setupMenubar()
        self.setupNumbar()
        
        self.flag_layout = False
       
        self.hbox = QHBoxLayout()
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(0,0,0,0)
        self.hbox.addWidget(self.number_bar)
        self.hbox.addWidget(self.editor)         
        
        self.layout = QGridLayout()
        self.layout.addWidget(self.searchbox, 0, 0, 1, 4)
        self.layout.addWidget(self.button1,   0, 4, 1, 1)
        self.layout.addWidget(self.button2,   0, 5, 1, 1)
        self.layout.addLayout(self.hbox,      2, 0, 1, 6)       
       
        self.window = QWidget()
        self.window.setLayout(self.layout) 

        self.setWindowTitle('Simple XML editor')
        self.setCentralWidget(self.window)
        self.resize(800, 800)
        self.show()       
        
        
    def setupButtonMenu(self):
        self.button1    = QPushButton("previous" )
        self.button2    = QPushButton("next" )
        
        self.button1.hide()
        self.button2.hide()

        self.button1.clicked.connect(self.handleButton1)
        self.button2.clicked.connect(self.handleButton2)
                   
    def setupEditor(self):
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        
        self.editor = EditorCodeCompletion(Config().path_code_completion_dict)       
        self.editor.setFont(font)
        self.editor.setTabStopWidth(20)
        self.editor.setAcceptRichText(False)
        self.editor.setLineWrapMode(QTextEdit.NoWrap)
        self.editor.textChanged.connect(self.validate)
        
        #self.connect(self.editor, SIGNAL("cursorPositionChanged()"),self.updateLineNumber)
        self.highlighter = highlighter.Highlighter(self.editor.document())
    
    def setupNumbar(self):
        self.number_bar = NumberBar()
        self.number_bar.setTextEdit(self.getStates())
        self.editor.cursorPositionChanged.connect(self.fireUpdateNumbar)        
        self.connect(self.editor.verticalScrollBar(), SIGNAL("valueChanged(int)"), self.fireUpdateNumbar)  

    def setupStatusbar(self):
        self.lineNumber = -1
        self.colNumber = -1
        self.m_statusRight = QLabel("row: " + str(self.lineNumber) + ", col:"  + str(self.colNumber), self)
        self.statusBar().addPermanentWidget(self.m_statusRight, 0) 

    def setupSearchBox(self):
        self.searchbox = SearchField() 
        self.searchbox.hide()     
        
    def setupMenubar(self):
        commentAction = QAction('Comment', self)
        commentAction.setShortcut('Ctrl+K')
        commentAction.setStatusTip('Comment Block')
        commentAction.triggered.connect(self.fireComment)
        
        uncommentAction = QAction('Uncomment', self)
        uncommentAction.setShortcut('Ctrl+Shift+K')
        uncommentAction.setStatusTip('Comment Block')
        uncommentAction.triggered.connect(self.fireUnComment)        
                        
        newAction = QAction('New', self)
        newAction.setShortcut('Ctrl+N') 
        newAction.setStatusTip('creats empty cpacs-file')
        newAction.triggered.connect(self.fireNewAction)                       
                        
        updateAction = QAction('Update', self)
        updateAction.setShortcut('Ctrl+U')
        updateAction.setStatusTip('Update CPACS')
        updateAction.triggered.connect(self.fireUpdate)

        revertAction = QAction('Revert', self)
        revertAction.setShortcut('Ctrl+R')
        revertAction.triggered.connect(self.fireRevert)        

        clearAction = QAction('Clear', self)
        clearAction.setStatusTip('Clear Editor')
        clearAction.triggered.connect(self.fireClear)

        numbarAction = QAction('LineNumber', self)
        numbarAction.triggered.connect(self.fireSwitchLayout)                 

        link_to_node_YesAction = QAction('yes', self)
        link_to_node_YesAction.triggered.connect(self.dummyFuction)  

        link_to_node_NoAction = QAction('no', self)
        link_to_node_NoAction.triggered.connect(self.dummyFuction)  

        menubar = self.menuBar()
        filemenu = menubar.addMenu("File")
        filemenu.addAction(newAction)
        filemenu.addAction(updateAction) 
        filemenu.addAction(revertAction)         
        sourcemenu = menubar.addMenu("Source")  
        sourcemenu.addAction(commentAction)  
        sourcemenu.addAction(uncommentAction)
        editormenu = menubar.addMenu("Editor")
        editormenu.addAction(clearAction) 
        editormenu.addSeparator()
        editormenu.addAction(numbarAction)
        editormenu_child1 = editormenu.addMenu('Link to node')
        editormenu_child1.addAction(link_to_node_YesAction)
        editormenu_child1.addAction(link_to_node_NoAction)

    def fireUpdateNumbar(self):
        self.updateLineNumber()
        self.number_bar.update()

    def dummyFuction(self):
        print "not implemented yet"
  
    def getStates(self):
        self.stats = { "searchbox":self.searchbox, "editor":self.editor}
        return self.stats    
        
    def updateModel(self, mmodel):
        print "test"  

    ''' find previous button '''    
    def handleButton1(self):
        self.editor.find(self.searchbox.text(), QTextDocument.FindBackward)  
        self.searchbox.setFocus()
        
    ''' find next button '''    
    def handleButton2(self):
        list_p = self.searchbox.text().split('/')
        if len(list_p) == 1 :
            if self.editor.find(self.searchbox.text()) : 
                ()
            elif not self.editor.find(self.searchbox.text(), QTextDocument.FindBackward):
                QMessageBox.about(self, "error", "String %s not found" % (self.searchbox.text()))
            else :
                self.editor.moveCursor(QTextCursor.Start)
                self.editor.find(self.searchbox.text())
        else :
            self.searchXPath(self.searchbox.text())
                
        self.searchbox.setFocus()     
      
    def searchXPath(self, path):
        list_p = self.searchbox.text().split('/')
        list_p = list_p[1:] if list_p[0] == '' else list_p
        for x in list_p :
            print x
            if '[' in x :
                num = int(re.findall('\d+', x)[0])
                x = x.split('[').group(0)
                while num > 0 : 
                    if not self.editor.find(x) : QMessageBox.about(self, "error", "XPath %s not found" % path)
                    num -= 1
            elif not self.editor.find(x) : 
                QMessageBox.about(self, "error", "XPath %s not found" % path) 
                return
          
        
    def updateLineNumber(self): 
        self.lineNumber = self.editor.textCursor().blockNumber() + 1
        self.colNumber = self.editor.textCursor().columnNumber() + 1
        self.m_statusRight.setText("row: " + str(self.lineNumber) + ", col:"  + str(self.colNumber))           
        
    def highlightCurrentLine(self) :
        extraSelections = []
        selection = QTextEdit.ExtraSelection()
        lineColor = QColor(255, 250, 205)
        selection.format.setBackground(lineColor)
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        selection.cursor = self.editor.textCursor()
        selection.cursor.clearSelection()
        extraSelections.append(selection)
        self.editor.setExtraSelections(extraSelections)
        self.editor.setFocus()  
 
 
    def fireUpdate(self):
        print ('dummy funciton - update the model')

    '''reloads cpacs file if not updated yet'''
    def fireRevert(self):
        if(self.cur_file_path != "" and self.cur_schema_path) :
            self.openFile(self.cur_file_path, self.cur_schema_path)
        else :
            QMessageBox.about(self, "error", "CPACS-File or Validation-Schema not available")
            
    def fireSearchSTRING(self):
        self.searchOpt = self.searchOptions.STRING
        
    def fireSearchXPATH(self):
        self.searchOpt = self.searchOptions.XPATH
    
    def fireNewAction(self):
        self.editor.clear()
        self.editor.setText(Config.cpacs_default)
    
    def fireClear(self):
        self.editor.clear()
 
    def fireSwitchLayout(self): 
        if(self.flag_layout) :
            self.number_bar.show()
        else :  
            self.number_bar.hide()
        
        self.flag_layout = not self.flag_layout 
 
    def fireComment(self):  
        tc = self.editor.textCursor()

        tc.beginEditBlock()
        tc.setPosition(self.editor.textCursor().selectionStart())
        tc.movePosition(QTextCursor.StartOfLine)
        tc.insertBlock()
        tc.movePosition(QTextCursor.PreviousBlock)
        tc.insertText("<!--")
        
        tc.setPosition(self.editor.textCursor().selectionEnd())
        tc.movePosition(QTextCursor.EndOfLine)
        tc.insertBlock()
        tc.insertText("-->")  
        tc.endEditBlock()      
        

    def fireUnComment(self):
        tc = self.editor.textCursor()
        c_shift = 0
        
        tc.beginEditBlock()
        s_row = tc.selectionStart()
        e_row = tc.selectionEnd()
        
        tc.setPosition(s_row)
        tc.select(QTextCursor.LineUnderCursor)
        txt = sel_txt = tc.selectedText()
        
        if txt == '' : return
        
        txt = txt.replace('<!--', '', 1)
        if txt == '' : 
            tc.select(QTextCursor.BlockUnderCursor)
            tc.removeSelectedText()
            c_shift = 5 # 4 (see else) +1 because of the deleted row
        elif txt != sel_txt : 
            tc.insertText(txt)
            c_shift = 4 # 4 because of the deleted </--
            
        tc.setPosition(e_row)
        tc.movePosition(QTextCursor.PreviousCharacter,QTextCursor.MoveAnchor, c_shift)
        tc.select(QTextCursor.LineUnderCursor)
        txt = sel_txt = tc.selectedText()
        
        if txt == '' : return
             
        txt = txt.replace('-->', '', 1)
        if txt == '' : 
            tc.select(QTextCursor.BlockUnderCursor)
            tc.removeSelectedText()
        elif txt != sel_txt :
            tc.insertText(txt)
        tc.endEditBlock()

    def validate(self):
        try:
            etree.fromstring(str(self.editor.toPlainText()))
            self.statusBar().showMessage("Valid XML")
        except etree.XMLSyntaxError, e:
            if e.error_log.last_error is not None:
                msg = e.error_log.last_error.message
                line=e.error_log.last_error.line
                col=e.error_log.last_error.column
                self.statusBar().showMessage("Invalid XML: Line %s, Col %s: %s"%(line,col,msg))
        except:
            self.statusBar().showMessage("Invalid XML: Unknown error") 
        

    def keyPressEvent(self,event):
            
        if event.key() == Qt.Key_F and event.modifiers() == Qt.ControlModifier :
            self.ctrlSearchView()
            self.searchbox.setText("/cpacs/vehicles/aircraft/model/name")

        elif self.searchbox.isFocused() and event.key() == Qt.Key_Return :            
            self.handleButton2()

    def ctrlSearchView(self):
        if self.searchbox.isFocused() :
            self.searchbox.hide()
            self.button1.hide()
            self.button2.hide()
        else :
            self.searchbox.show()
            self.button1.show()
            self.button2.show()
            self.searchbox.setFocus()

    def openFile(self, path=None, schema = None):
        if path and schema :
            try :
                text = self.cpacsHandler.loadFile(path, schema)
                self.editor.setPlainText(text)
                self.cur_file_path = path
                self.cur_schema_path = schema
            except tixiwrapper.TixiException, e :
                print e.error
                self.statusBar().showMessage('CPACS ERROR: ' + e.error)
     
     
              
def main():
    app = QApplication(sys.argv)
    w = EditorWindow(None)
    conf = Config()
    w.openFile(conf.path_cpacs_A380_Fuse, conf.path_cpacs_21_schema)
  #  w.openFile(conf.path_cpacs_D150, conf.path_cpacs_21_schema)
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()

