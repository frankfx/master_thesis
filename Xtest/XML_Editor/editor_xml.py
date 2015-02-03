import sys
import re

from tixiwrapper import Tixi, TixiException
from Xtest.XML_Editor.popUps.popUp_newFile import NewFileDialog
from Xtest.XML_Editor.popUps.popUp_showXPath import XPathDialog
from PySide.QtGui import QLineEdit

from lxml import etree
from PySide.QtGui import QMessageBox, QSpinBox, QAction, QLabel, QColor, QTextFormat, QTextDocument, QTextCursor, QMainWindow, QGridLayout, QHBoxLayout, QWidget, QPushButton, QFont, QTextEdit, QApplication
from PySide.QtCore import Qt, SIGNAL
from Xtest.XML_Editor.editor_comp import EditorCodeCompletion
from numberBar import NumberBar
from Xtest.config import Config

from highlighter import Highlighter
from Xtest.XML_Editor.popUps.tools.toolX import ToolX
from PySide import QtCore

class EditorWindow(QMainWindow):
    """initialize editor"""
    def __init__(self, tixi, xmlFilename, cpacs_scheme=Config.path_cpacs_21_schema):
        super(EditorWindow, self).__init__()   
        
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

        self.tixi = tixi
        self.loadFile(xmlFilename, cpacs_scheme) 

    '''
    loads cpacs file and validates it against the cpacs_schema
    @param xmlFilename: input file
    @param cpacs_scheme: validation scheme
    '''
    def loadFile(self, xmlFilename=None, cpacs_scheme=Config.path_cpacs_21_schema):
        if xmlFilename and cpacs_scheme :
            try:
                self.tixi.open(xmlFilename)
                #self.tixi.openDocument(xmlFilename) 
                #self.tixi.schemaValidateFromFile(cpacs_scheme)
                self.editor.setPlainText(self.tixi.exportDocumentAsString())
                self.cur_file_path = xmlFilename
                self.cur_schema_path = cpacs_scheme  
            except TixiException as e:  
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
        except etree.XMLSyntaxError as e:
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
        pass
        #self.tixi.close()
        #self.tixi.cleanup() 

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
        #self.editor.verticalScrollBar.valueChanged.connect(self.fireUpdateNumbar)

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
                        
        self.updateAction = QAction('Update', self)
        self.updateAction.setShortcut('Ctrl+U')
        self.updateAction.setStatusTip('Update CPACS')
        self.updateAction.triggered.connect(self.fireUpdate)

        revertAction = QAction('Revert', self)
        revertAction.setShortcut('Ctrl+R')
        revertAction.triggered.connect(self.fireRevert)        

        clearAction = QAction('Clear', self)
        clearAction.setStatusTip('Clear Editor')
        clearAction.triggered.connect(self.editor.clear)

        numbarAction = QAction('Line Number', self)
        numbarAction.triggered.connect(self.fireSwitchLayout)                 

        self.xpathAction = QAction('Current XPath', self)
        self.xpathAction.triggered.connect(self.getCursorXPath)  

        link_to_node_YesAction = QAction('yes', self)
        link_to_node_YesAction.triggered.connect(self.dummyFuction)  

        link_to_node_NoAction = QAction('no', self)
        link_to_node_NoAction.triggered.connect(self.dummyFuction)  

        toolXAction = QAction('Tool X',self)
        toolXAction.triggered.connect(self.fireToolX)

        menubar = self.menuBar()
        filemenu = menubar.addMenu("File")
        filemenu.addAction(newAction)
        filemenu.addAction(self.updateAction) 
        filemenu.addAction(revertAction)         
        sourcemenu = menubar.addMenu("Source")  
        sourcemenu.addAction(commentAction)  
        sourcemenu.addAction(uncommentAction)
        sourcemenu.addAction(searchAction)
        editormenu = menubar.addMenu("Editor")
        editormenu.addAction(clearAction) 
        editormenu.addSeparator()
        editormenu.addAction(numbarAction)
        editormenu.addAction(self.xpathAction)
        editormenu_child1 = editormenu.addMenu('Link to node')
        editormenu_child1.addAction(link_to_node_YesAction)
        editormenu_child1.addAction(link_to_node_NoAction)
        toolmenu = menubar.addMenu("Tools")
        toolmenu.addAction(toolXAction)

        self.editor.setContextMenuPolicy(Qt.CustomContextMenu)
        self.editor.customContextMenuRequested.connect(self.showMenu)
        #self.editor.connect(self.editor, SIGNAL( "customContextMenuRequested(QPoint)" ), self.showMenu )

    def showMenu( self, pos ):
        """ Show a context menu for the active layer in the legend """
        menu = self.editor.createStandardContextMenu()
        menu.addAction(self.xpathAction)
        menu.exec_(QtCore.QPoint( self.mapToGlobal( pos ).x() + 5, self.mapToGlobal( pos ).y() )) 
            

    def fireUpdateNumbar(self):
        self.updateLineNumber()
        self.number_bar.update()

    def dummyFuction(self):
        print ("not implemented yet")
  
    def getStates(self):
        self.stats = { "searchbox":self.searchbox, "editor":self.editor}
        return self.stats    
        
    ''' find previous button '''    
    def fire_search_backward(self):
        self.editor.find(self.searchbox.text(), QTextDocument.FindBackward)  
        self.searchbox.setFocus()
        
    ''' find next button '''    
    def fire_search_foreward(self):
        
        #print self.tixi.getNumberOfChilds('/cpacs/vehicles/aircraft/model[@uID="Aircraft1"]/wings/wing[@uID="Aircraft1_Wing1"]/transformation[@uID="Aircraft1_Wing1_Transf"]/scaling[@uID="Aircraft1_Wing1_Transf_Sca"]/z')
        
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
      
    # test  
    # /cpacs/vehicles/aircraft/model/wings/wing/sections/section
    def searchXPath(self, path, searchList):
        try:
            if self.tixi.xPathEvaluateNodeNumber(path) > 1 :
                QMessageBox.about(self, "error", "XPath %s not unique" % path)
                return
                
            self.editor.moveCursor(QTextCursor.Start)
            
            found = True

            # search index snd loop
            j = 0
        
            # search backwards for uid 
            for i in range(len(searchList)-1, -1, -1) :
                if '[' in searchList[i] :    
                    # get value in brackets : [x] --> x
                    uid = re.search(r'\[(.*)\]', searchList[i]).group(1)
                    uid = self.__transToSearchUid(searchList[:i+1], uid)
                    
                    found = self.editor.find(uid)
                    j = i+1
                    break
                
            # search forward for all nodes after last uid
            while found and j < len(searchList) :
                found = self.editor.find('<'+searchList[j])
                j += 1
            if not found :
                QMessageBox.about(self, "error", "XPath %s not found" % path)
        except TixiException :
            QMessageBox.about(self, "error", "XPath %s not found" % path)


    def __transToSearchUid(self, path_list, uid):
        try: 
            int(uid)
            path = ""
            for p in path_list : path = path + '/' + p 
            return self.tixi.getTextAttribute(path , 'uID')
        except ValueError: 
            return uid.replace('@', '')

    def getCursorXPath(self):
        start_pos = self.editor.textCursor().position()

        tag , tag_pos , isCursorInTag = self.getTagNameAtCursor()
        
        _,xpath_idx, xpath_uid = self.__findXPath_rec('/cpacs', '/cpacs' , tag, tag_pos)  
        
        if not isCursorInTag:
            xpath_idx = self.__strRemoveReverseToChar(xpath_idx, '/')
            xpath_uid = self.__strRemoveReverseToChar(xpath_uid, '/')
 
        self.__setCursorToPostion(start_pos)
        self.__startXPathPopUp(xpath_idx, xpath_uid)
        
        
    def getTagNameAtCursor(self):
        '''
        @return: name of tag , position of tag , cursor is btw open and closing tag 
        '''
        self.editor.find('<', QTextDocument.FindBackward)
        isClosingTag , fst_tag   = self.__getTagName()

        pos = self.editor.textCursor().position()
        
        if isClosingTag :
            # find open tag of this closing tag
            self.editor.find('<'+fst_tag, QTextDocument.FindBackward)
            pos = self.editor.textCursor().position()
            
            return fst_tag , pos , False
        else:
            return fst_tag , pos , True


    def __getTagName(self):
        tc = self.editor.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        
        tx = tc.selectedText()  
        isClosingTag = False
        
        if "</" in tx :
            # select next word
            tc.select(QTextCursor.WordUnderCursor)
            tx = tc.selectedText()
            isClosingTag = True
        
        return isClosingTag , "" if "<" in tx else tx
        

    def __findXPath_rec(self, xpath_idx, xpath_uid, search, pos):
        nodes = self.__getChildNodesIdxTuple(xpath_idx)
        
        for (node, idx) in nodes:
            if node != '#text' :
                new_xpath_idx, new_xpath_uid = self.__createNewXPath(xpath_idx, xpath_uid, node, idx)
                if search == node and self.isNodeAtSearchedTagPosition(new_xpath_uid, pos) :
                    print ("gefunden" , new_xpath_idx)
                    return True, new_xpath_idx , new_xpath_uid
                else:
                    flag , res_idx, res_uid = self.__findXPath_rec(new_xpath_idx, new_xpath_uid, search, pos)
                    if flag : return True, res_idx, res_uid
        return False , xpath_idx , xpath_uid


    def __getChildNodesIdxTuple(self, xpath):
        n = self.tixi.getNumberOfChilds(xpath) + 1
        node_list = map(lambda i : self.tixi.getChildNodeName(xpath, i), range(1,n))
        
        res = []
        for j in range(len(node_list)) :
            cnt = 1
            for k in range(j):
                if node_list[k] == node_list[j] : 
                    cnt = cnt + 1
            res.append((node_list[j],cnt))
        
        return res
    

    def __createNewXPath(self, xpath_idx, xpath_uid, node, idx):
        path_idx = xpath_idx + '/' + node
        path_uid = xpath_uid + '/' + node

        try :
            uID = self.tixi.getTextAttribute(path_idx + '[' + str(idx) + ']', 'uID')
            path_idx = path_idx + '[' + str(idx) + ']'
            path_uid = path_uid+'[@uID="' + uID + '"]'
            
        except TixiException:
            pass # e.error == 'ATTRIBUTE_NOT_FOUND
            
        return path_idx , path_uid


    
    def isNodeAtSearchedTagPosition(self, xpath, pos):
        '''
        @param xpath: xpath with uids (doesn't work with indices)
        @param param: 
        '''
        self.editor.moveCursor(QTextCursor.Start)
        
        # split string at / and remove all empty strings
        l = filter(lambda x : x != '' , xpath.split('/'))
        
        # search index snd loop
        j = 0
        
        # search backwards for uid 
        for i in range(len(l)-1, -1, -1) :
            if '[' in l[i] :    
                # get value in brackets : [x] --> x
                uid = re.search(r'\[@(.*)\]', l[i]).group(1)
                self.editor.find(uid)
                
                j = i+1
                break
        
        # search forward for all nodes after last uid
        while j < len(l) :
            self.editor.find('<'+l[j])
            j += 1

        return pos <= self.editor.textCursor().position()


    def __setCursorToPostion(self, pos):
        tc = self.editor.textCursor()
        tc.setPosition(pos)
        self.editor.setTextCursor(tc)

    def __startXPathPopUp(self, xpath_idx, xpath_uid):
        self.popUpWidget = XPathDialog(xpath_idx, xpath_uid) 

        self.setEnabled(False)
        self.popUpWidget.closeAct.triggered.connect(self.__resetPopUpWidget)
        
        self.popUpWidget.show()  


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
        text_file = open(Config.path_cpacs_tmp_file, "w")
        text_file.write(self.editor.toPlainText())
        text_file.close()
        
        
        #self.tixi.saveDocument(Config.path_cpacs_tmp_file)
      # '../cpacs_files/temp.xml'
        

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
            self.number_bar.flag_show_numbers = True
            self.update()
        else :  
            self.number_bar.flag_show_numbers = False
            self.update()
        self.flag_layout = not self.flag_layout 
    
    def fireNewAction(self):
        '''
        opens new file input form   
        '''          
        self.setEnabled(False)
        self.popUpWidget = NewFileDialog()
        self.popUpWidget.buttonBox.accepted.connect(self.__createNewCpacsFile)
        self.popUpWidget.buttonBox.rejected.connect(self.__resetPopUpWidget)
        self.popUpWidget.closeAct.triggered.connect(self.__resetPopUpWidget)
        self.popUpWidget.show()
   
    def fireToolX(self):
        self.popUpWidget = ToolX("X-Tool", self.tixi)
        self.setEnabled(False)
        self.popUpWidget.buttonBox.accepted.connect(self.__resetPopUpWidget)
        self.popUpWidget.buttonBox.rejected.connect(self.__resetPopUpWidget)
        # closeAct for pressing X to close window
        self.popUpWidget.closeAct.triggered.connect(self.__resetPopUpWidget)
        self.popUpWidget.show()        
       
    def __createNewCpacsFile(self):
        '''
        closes all documents and creates new empty cpacs temporary file   
        '''        
        idict = self.popUpWidget.fire_submitInput()
        self.tixi.closeAllDocuments()
        self.tixi.create('cpacs')
        self.tixi.addCpacsHeader(idict['name'], idict['creator'], idict['version'], idict['description'], idict['cpacsVersion'])
        self.tixi.saveDocument(Config.path_cpacs_tmp_file)
        self.loadFile(Config.path_cpacs_tmp_file)
        self.__resetPopUpWidget()
        
    def __resetPopUpWidget(self):
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
    def __strRemoveReverseToChar(self, s, c):
        return self.__rm_rec(s, c)
    
    def __rm_rec(self, s, c):
        if s == "" :
            return ""
        elif s[-1] == c :
            return s[:-1]
        else :
            return self.__rm_rec(s[:-1], c)     
    
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
   
class SearchField(QLineEdit):    
    '''This is a docstring'''
    def __init__(self):
        super(SearchField, self).__init__()
        self.__focus = False
        
    def focusInEvent(self, focusevent):
        self.__focus = True
        super(SearchField, self).focusInEvent(focusevent)

    def focusOutEvent(self, focusevent):
        self.__focus = False
        super(SearchField, self).focusInEvent(focusevent)

    def isFocused(self):
        '''returns true if focus is on text field'''
        return self.__focus   
   
           
def main():
    app = QApplication(sys.argv)
    tixi = Tixi()
    #tixi.open(Config.path_cpacs_simple, )
    w = EditorWindow(tixi, Config.path_cpacs_D150_2, Config.path_cpacs_21_schema)

   # w.loadFile(conf.path_cpacs_A320_Wing, conf.path_cpacs_21_schema)
    # w.loadFile(conf.path_cpacs_D150, conf.path_cpacs_21_schema)
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()

