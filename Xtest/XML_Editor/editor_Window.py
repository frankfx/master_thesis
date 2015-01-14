import sys
import re

from tixiwrapper import Tixi, TixiException
from Xtest.XML_Editor.newFileDialog import NewFileDialog
from xPathDialog import XPathDialog


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
        
        self.popUpWidget = None
        
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
    def loadFile(self, xmlFilename=None, cpacs_scheme=Config.path_cpacs_21_schema):
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

        self.button1.clicked.connect(self.fire_search_backward)
        self.button2.clicked.connect(self.fire_search_foreward)
         
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
        clearAction.triggered.connect(self.editor.clear)

        numbarAction = QAction('Line Number', self)
        numbarAction.triggered.connect(self.fireSwitchLayout)                 

        xpathAction = QAction('Current XPath', self)
        xpathAction.triggered.connect(self.getCursorXPath)  

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
        editormenu.addAction(xpathAction)
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
    def fire_search_backward(self):
        self.editor.find(self.searchbox.text(), QTextDocument.FindBackward)  
        self.searchbox.setFocus()
        
    ''' find next button '''    
    def fire_search_foreward(self):
        
        searchList = filter(lambda a : a!='',  self.searchbox.text().split('/'))
        if len(searchList) == 1 :
            if self.editor.find(searchList[0]) : 
                pass
            elif not self.editor.find(searchList[0], QTextDocument.FindBackward):
                QMessageBox.about(self, "error", "String %s not found" % (searchList[0]))
            else :
                self.editor.moveCursor(QTextCursor.Start)
                self.editor.find(searchList[0])
        else :
            self.searchXPath(self.searchbox.text(), searchList)
                
        self.searchbox.setFocus()     
      
    def searchXPath(self, path, searchList):
        try:
            self.tixi.xPathEvaluateNodeNumber(path)
            self.editor.moveCursor(QTextCursor.Start)
            for s in searchList :
                if not self.editor.find(s) :
                    QMessageBox.about(self, "error", "XPath %s not found" % path)
                    return 
        except TixiException :
            QMessageBox.about(self, "error", "XPath %s not found" % path)
        
        
    def getCursorXPath(self):
        '''
        returns the current cursor xpath position
        '''        
        self.editor.find('uID', QTextDocument.FindBackward)
        self.editor.find('"')

        tc = self.editor.textCursor()        
        tc.select(QTextCursor.WordUnderCursor)
        uID = tc.selectedText()

        self.popUpWidget = XPathDialog(self.tixi.uIDGetXPath(uID)) 

        self.setEnabled(False)
        self.popUpWidget.copyAct.triggered.connect(self.__copyXPath)
        self.popUpWidget.closed.triggered.connect(self.__resetPopUpWidget)
        
        self.popUpWidget.show()
      
      
    def __copyXPath(self):
        print "hallo welt"    

    def updateLineNumber(self): 
        '''
        sets the line and column number
        '''
        self.lineNumber = self.editor.textCursor().blockNumber() + 1
        self.colNumber = self.editor.textCursor().columnNumber() + 1
        self.m_statusRight.setText("row: " + str(self.lineNumber) + ", col:"  + str(self.colNumber))           

       
    def highlightCurrentLine(self) :
        '''
        highlight line under cursor
        ''' 
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
        print ('dummy function - update the model')


    def fireRevert(self):
        '''
        reloads cpacs file if not updated yet
        '''
        if(self.cur_file_path and self.cur_schema_path) :
            self.loadFile(self.cur_file_path, self.cur_schema_path)
        else :
            QMessageBox.about(self, "error", "CPACS-File or Validation-Schema not available")
            

    def fireSwitchLayout(self): 
        '''
        function to show or hide line numbers
        '''
        if(self.flag_layout) :
            self.number_bar.show()
        else :  
            self.number_bar.hide()
        self.flag_layout = not self.flag_layout 
    
    def fireNewAction(self):
        '''
        opens new file input form   
        '''          
        self.setEnabled(False)
        self.popUpWidget = NewFileDialog()
        self.popUpWidget.buttonBox.accepted.connect(self.__createNewCpacsFile)
        self.popUpWidget.buttonBox.rejected.connect(self.__resetPopUpWidget)
        self.popUpWidget.show()
        
       
    def __createNewCpacsFile(self):
        '''
        closes all documents and creates new empty cpacs temporary file   
        '''        
        idict = self.popUpWidget.submitInput()
        self.tixi.closeAllDocuments()
        self.tixi.create('cpacs')
        self.tixi.addCpacsHeader(idict['name'], idict['creator'], idict['version'], idict['description'], idict['cpacsVersion'])
        self.tixi.saveDocument('../cpacs_files/temp.xml')
        self.loadFile('../cpacs_files/temp.xml')
        self.__resetPopUpWidget()
        
    def __resetPopUpWidget(self):
        print "reset yea"
        self.popUpWidget.close()
        self.popUpWidget = None    
        self.setEnabled(True)
    
    
    def fireComment(self):  
        '''
        inserts open respective closing tag before and after a selected text. 
        '''
        tc = self.editor.textCursor()

        tc.beginEditBlock()
        tc.setPosition(self.editor.textCursor().selectionStart())
        tc.insertText("<!--")
        
        tc.setPosition(self.editor.textCursor().selectionEnd())
        tc.insertText("-->")  
        tc.endEditBlock()      


    def fireUnComment(self):
        '''
        removes open respective closing tag before and after a selected text. 
        '''        
        tc = self.editor.textCursor()
        selectTxt = tc.selectedText()
        
        if selectTxt.find('<!--') != -1 : 
            if selectTxt.rfind('-->') != -1 :
                selectTxt = selectTxt.replace('<!--', '', 1)
                selectTxt = self.__rreplace(selectTxt, '-->' , '', 1)
                tc.insertText(selectTxt)
            else:
                QMessageBox.about(self, "error", "no open tag (%s) in selection" % ('-->')) 
        else:
            QMessageBox.about(self, "error", "no close tag (%s) in selection" % ('<!--')) 
        

    def fireSearchView(self):
        '''
        show and hide searchbox and buttons
        '''        
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

    def keyPressEvent(self,event):
        '''
        handle for searching strings by pressing enter key
        '''        
        if self.searchbox.isFocused() and event.key() == Qt.Key_Return :            
            self.fire_search_foreward()   
   
    # ======================================================================================================================
    # utilities
    # ======================================================================================================================
    
    def __rreplace(self, s, old, new, occurrence):
        '''
        reverse string replace function
        @param s: source string
        @param old: char to be replaced
        @param new: new char 
        @param occurrence: only the given count occurrences are replaced.
        ''' 
        li = s.rsplit(old, occurrence)
        return new.join(li)   
           
def main():
    app = QApplication(sys.argv)
    w = EditorWindow()
    conf = Config()
    w.loadFile(conf.path_cpacs_A320_Wing, conf.path_cpacs_21_schema)
    # w.loadFile(conf.path_cpacs_D150, conf.path_cpacs_21_schema)
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()

