import sys
import re

from tixiwrapper import Tixi, TixiException

from lxml import etree
from PySide.QtGui import QMessageBox, QSpinBox, QAction, QLabel, QColor, QTextFormat, QTextDocument, QTextCursor, QMainWindow, QGridLayout, QHBoxLayout, QWidget, QPushButton, QFont, QTextEdit, QApplication
from PySide.QtCore import Qt, SIGNAL
from editor_CodeCompletion import EditorCodeCompletion
from Xtest.XML_Editor.search_field import SearchField
from numberBar import NumberBar
from Xtest.XML_Editor.config import Config

from highlighter import Highlighter

class EditorWindow(QMainWindow):
    """initialize editor"""
    def __init__(self):
        super(EditorWindow, self).__init__()   
       
        self.tixi = Tixi()
       
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
        
        self.layout.addWidget(self.searchbox,       0, 0, 1, 4)
        self.layout.addWidget(self.button1,         0, 4, 1, 1)
        self.layout.addWidget(self.button2,         0, 5, 1, 1)
        self.layout.addLayout(self.hbox,            2, 0, 1, 8)       
        self.layout.addWidget(self.fontsizeSpinBox, 0, 6, 1, 1)
        self.layout.addWidget(self.label1,          0, 7, 1, 1)
       
        self.window = QWidget()
        self.window.setLayout(self.layout) 

        self.setWindowTitle('Simple XML editor')
        self.setCentralWidget(self.window)
        self.resize(800, 800)
        self.show()       

    '''
    loads cpacs file and validates it against the cpacs_schema
    @param xmlFilename: input file
    @param cpacs_scheme: validation scheme
    '''
    def loadFile(self, xmlFilename=None, cpacs_scheme=None):
        if xmlFilename and cpacs_scheme :
            try:
                self.tixi.openDocument(xmlFilename) 
                self.tixi.schemaValidateFromFile(cpacs_scheme)
                
                self.editor.setPlainText(self.tixi.exportDocumentAsString())
                self.cur_file_path = xmlFilename
                self.cur_schema_path = cpacs_scheme                
            except TixiException, e:  
                print e.error
                self.statusBar().showMessage('CPACS ERROR: ' + e.error)

    '''
    update the dictionary by the cpacs scheme
    @param path_dict: path to directory
    @param path_scheme: path to cpacs_scheme
    '''
    def updatedictionary(self, path_dict=Config.path_code_completion_dict, path_scheme=Config.path_cpacs_21_schema):
        found       = False
        olddict      = open(path_dict)
        scheme_file = open(path_scheme, 'r')
        
        with open(path_dict, "a") as newdict :
            for line in scheme_file :
                word = re.search("(?<=\<xsd:complexType name=\").*(?=\"\>)", line)
                if word != None :
                    for tmp in olddict : 
                        if tmp == word.group(0) +"\n" :
                            found = True
                            break
                    if(not found) :
                        newdict.write(word.group(0)+"\n")
                        olddict.seek(0)
                    found = False
            
        olddict.close()
        newdict.close()
        scheme_file.close()            

    '''
    validate xml file and write result to statusBar
    '''
    def validate(self):
        try:
            etree.fromstring(str(self.editor.toPlainText()))
            self.statusBar().showMessage("Valid XML")
        except etree.XMLSyntaxError, e:
            if e.error_log.last_error is not None:
                msg  = e.error_log.last_error.message
                line = e.error_log.last_error.line
                col  = e.error_log.last_error.column
                self.statusBar().showMessage("Invalid XML: Line %s, Col %s: %s"%(line,col,msg))
        except:
            self.statusBar().showMessage("Invalid XML: Unknown error") 

    '''
    close and cleanup tixi
    '''
    def __del__(self):
        self.tixi.close()
        self.tixi.cleanup() 

    '''
    set and connect the search buttons
    '''
    def setupButtonMenu(self):
        self.button1         = QPushButton("previous" )
        self.button2         = QPushButton("next" )
        self.label1          = QLabel("font")
        self.fontsizeSpinBox = QSpinBox()
        
        self.button1.hide()
        self.button2.hide()
        self.label1.hide()
        self.fontsizeSpinBox.hide()

        self.button1.clicked.connect(self.handleButton1)
        self.button2.clicked.connect(self.handleButton2)
         
        self.fontsizeSpinBox.setRange(4, 30)
        self.fontsizeSpinBox.setSingleStep(1)
        self.fontsizeSpinBox.setSuffix('pt')
        self.fontsizeSpinBox.setValue(10)        
        self.fontsizeSpinBox.valueChanged.connect(self.setfontsize)         
    
    def setfontsize(self, value):
        self.font.setPointSize(value)
        self.editor.setFont(self.font)
                
    def setupEditor(self):
        self.font = QFont()
        self.font.setFamily('Courier')
        self.font.setFixedPitch(True)
        self.font.setPointSize(10)
        
        self.editor = EditorCodeCompletion(Config().path_code_completion_dict)       
        self.editor.setFont(self.font)
        self.editor.setTabStopWidth(20)
        self.editor.setAcceptRichText(False)
        self.editor.setLineWrapMode(QTextEdit.NoWrap)
        self.editor.textChanged.connect(self.validate)
        
        self.highlighter = Highlighter(self.editor.document())
    
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
                        
        searchAction = QAction('search', self)
        searchAction.setShortcut('Ctrl+F')
        searchAction.setStatusTip('search')
        searchAction.triggered.connect(self.fireSearchView)     
        
                        
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
        sourcemenu.addAction(searchAction)
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
          
    '''
    set the line and column number
    '''
    def updateLineNumber(self): 
        self.lineNumber = self.editor.textCursor().blockNumber() + 1
        self.colNumber = self.editor.textCursor().columnNumber() + 1
        self.m_statusRight.setText("row: " + str(self.lineNumber) + ", col:"  + str(self.colNumber))           

    '''
    highlight something
    '''        
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
 
    #TODO: implemnt
    def fireUpdate(self):
        print ('dummy funciton - update the model')

    '''
    reloads cpacs file if not updated yet
    '''
    def fireRevert(self):
        if(self.cur_file_path and self.cur_schema_path) :
            self.loadFile(self.cur_file_path, self.cur_schema_path)
        else :
            QMessageBox.about(self, "error", "CPACS-File or Validation-Schema not available")
            
    '''
    resets the editor
    '''
    def fireClear(self):
        self.editor.clear()
 
    '''
    function to show or hide line numbers
    '''
    def fireSwitchLayout(self): 
        if(self.flag_layout) :
            self.number_bar.show()
        else :  
            self.number_bar.hide()
        self.flag_layout = not self.flag_layout 
 
 
 
 
    def fireSearchSTRING(self):
        self.searchOpt = self.searchOptions.STRING
        
    def fireSearchXPATH(self):
        self.searchOpt = self.searchOptions.XPATH
    
    def fireNewAction(self):
        self.editor.clear()
        self.editor.setText(Config.cpacs_default)
 
 
 
 
 
 
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

    '''
    handle for searching strings by pressing enter key
    '''
    def keyPressEvent(self,event):
        if self.searchbox.isFocused() and event.key() == Qt.Key_Return :            
            self.handleButton2()

    '''
    show and hide searchbox and buttons
    '''
    def fireSearchView(self):
        if self.searchbox.isFocused() :
            self.searchbox.hide()
            self.button1.hide()
            self.button2.hide()
            self.label1.hide()
            self.fontsizeSpinBox.hide()
        else :
            self.searchbox.show()
            self.button1.show()
            self.button2.show()
            self.label1.show()
            self.fontsizeSpinBox.show()
            self.searchbox.setFocus()
              
def main():
    app = QApplication(sys.argv)
    w = EditorWindow()
    conf = Config()
    w.loadFile(conf.path_cpacs_A320_Wing, conf.path_cpacs_21_schema)
    # w.loadFile(conf.path_cpacs_D150, conf.path_cpacs_21_schema)
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()

