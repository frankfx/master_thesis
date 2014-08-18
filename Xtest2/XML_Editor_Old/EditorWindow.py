import sys
import Highlighter
from lxml import etree
from PySide.QtGui import QAction, QLabel, QColor, QTextFormat, QTextDocument, QTextCursor, QFocusEvent, QMainWindow, QGridLayout, QHBoxLayout, QWidget, QPushButton, QSizePolicy, QLineEdit, QFont, QTextEdit, qApp, QApplication
from PySide.QtCore import QFile, QEvent, Qt, SIGNAL
from lineEdit import LineEdit
from numberBar import NumberBar

class EditorWindow(QMainWindow):
    
    """initialize editor"""
    def __init__(self ,model):
        super(EditorWindow, self).__init__()   
    
        self.setupEditor()
        self.setupButtonMenu()
        self.setupSearchBox()
        self.setupStatusbar()
        self.setupMenubar()
                
        layout = QGridLayout()
        # addWidget ( QWidget * widget, fromRow, fromColumn, rowSpan, columnSpan)
        layout.addWidget(self.searchbox, 0, 0, 1, 4)
        layout.addWidget(self.button1,   0, 4, 1, 1)
        layout.addWidget(self.button2,   0, 5, 1, 1)
        layout.addWidget(self.editor,    2, 0, 1, 6)

        window      = QWidget()
        window.setLayout(layout)
        
        self.setWindowTitle('Simple XML editor')
        self.setCentralWidget(window)
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

        self.editor = QTextEdit()
        self.number_bar = NumberBar()
        self.number_bar.setTextEdit(self.editor)         
        self.editor.setFont(font)
        self.editor.setTabStopWidth(20)
        self.editor.setAcceptRichText(False)
        self.editor.setLineWrapMode(QTextEdit.NoWrap)
        self.editor.textChanged.connect(self.validate)
        self.editor.cursorPositionChanged.connect(self.updateLineNumber)
        #self.connect(self.editor, SIGNAL("cursorPositionChanged()"),self.updateLineNumber)
        self.editor.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.highlighter = Highlighter.Highlighter(self.editor.document())
        
    def setupStatusbar(self):
        self.lineNumber = -1
        self.colNumber = -1
        self.m_statusRight = QLabel("row: " + str(self.lineNumber) + ", col:"  + str(self.colNumber), self)
        self.statusBar().addPermanentWidget(self.m_statusRight, 0) 

    def setupSearchBox(self):
        self.searchbox = LineEdit() 
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
                        
        updateAction = QAction('Update', self)
        updateAction.setShortcut('Ctrl+U')
        updateAction.setStatusTip('Update CPACS')
        updateAction.triggered.connect(self.fireUpdate)

        clearAction = QAction('Clear', self)
        clearAction.setStatusTip('Clear Editor')
        clearAction.triggered.connect(self.fireClear)

        revertAction = QAction('Revert', self)
        revertAction.setShortcut('Ctrl+R')
        revertAction.triggered.connect(self.fireRevert)        
                   
        
        menubar = self.menuBar()
        filemenu = menubar.addMenu("File")
        filemenu.addAction(updateAction) 
        filemenu.addAction(clearAction) 
        filemenu.addAction(revertAction)         
        sourcemenu = menubar.addMenu("Source")  
        sourcemenu.addAction(commentAction)  
        sourcemenu.addAction(uncommentAction)

        
    def updateModel(self, mmodel):
        print "test"  

    ''' find previous button '''    
    def handleButton1(self):
        self.editor.find(self.searchbox.text(), QTextDocument.FindBackward)  
        self.searchbox.setFocus()
        
    ''' find next button '''    
    def handleButton2(self):
        # search from cursor position to the end.
        if self.button1.isEnabled() == False :
            self.editor.moveCursor(QTextCursor.Start)
        if self.editor.find(self.searchbox.text()) :
            self.button1.setEnabled(True)    
        self.searchbox.setFocus()     
        
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

    def fireRevert(self):
        print ('dummy funciton - reload the cpacs file if not updated yet')  
        
    def fireClear(self):
        self.editor.clear()
 
    def fireComment(self):
        doc = self.editor.document()
        s_row = doc.findBlock(
                 self.editor.textCursor().selectionStart()).blockNumber()
        e_row = doc.findBlock(
                 self.editor.textCursor().selectionEnd()).blockNumber()
        
        tc = self.editor.textCursor()
        
        tc.movePosition(QTextCursor.Start)
        tc.movePosition(QTextCursor.NextBlock, QTextCursor.KeepAnchor, s_row)
        tc.clearSelection()
        tc.insertText("<!--")
        
        tc.movePosition(QTextCursor.Start)
        tc.movePosition(QTextCursor.NextBlock, QTextCursor.KeepAnchor, e_row)
        tc.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
        tc.clearSelection()
        tc.insertText("-->")
        
    def fireUnComment(self):
        doc = self.editor.document()
        tc = self.editor.textCursor()
                
        s_row = doc.findBlock(
                 self.editor.textCursor().selectionStart()).blockNumber()
        e_row = doc.findBlock(
                 self.editor.textCursor().selectionEnd()).blockNumber()
        
        text1 = doc.findBlockByLineNumber( s_row ).text().replace('<!--', '', 1)
        
        if s_row == e_row :
            text1 = text1.replace('-->', '', 1)
        else :
            text2 = doc.findBlockByLineNumber( e_row ).text().replace('-->', '', 1)
 
            tc.movePosition(QTextCursor.Start)
            tc.movePosition(QTextCursor.NextBlock, QTextCursor.KeepAnchor, e_row)
            tc.select(QTextCursor.BlockUnderCursor)
            tc.insertBlock()
            tc.insertText(text2) 
           
        tc.movePosition(QTextCursor.Start)
        tc.movePosition(QTextCursor.NextBlock, QTextCursor.KeepAnchor, s_row)
        tc.select(QTextCursor.BlockUnderCursor)
        if s_row != 0 :
            tc.insertBlock()
        tc.insertText(text1)


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

    def openFile(self, path=None):
        #---------------------------------------------------------- if not path:
            #------- path = QtGui.QFileDialog.getOpenFileName(self, "Open File",
                    #---------------------------- '', "XML Files (*.xml *.XML)")
        if path:
            inFile = QFile(path)
            if inFile.open(QFile.ReadOnly | QFile.Text):
                text = inFile.readAll()
                try:
                    # Python v3.
                    text = str(text, encoding='ascii')
                except TypeError:
                    # Python v2.
                    text = str(text)
                self.editor.setPlainText(text)             
              
def main():
    app = QApplication(sys.argv)
    w = EditorWindow(None)
    w.openFile("A320_FuseOffset.xml")
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
