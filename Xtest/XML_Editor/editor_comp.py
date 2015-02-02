'''
Created on Aug 12, 2014

@author: fran_re
'''
import re
from PySide.QtGui import QTextEdit, QCompleter, QStringListModel, QTextCursor, QApplication, QTextDocument
from PySide.QtCore import Qt
from Xtest import config  
	
class EditorCodeCompletion(QTextEdit):
    def __init__(self, path_dict):
        super(EditorCodeCompletion, self).__init__()  
        self.m_completer = QCompleter(self)
        self.m_completer.setWidget(self)
        words = []
        
        self.flag_open_angle_bracket = False
        self.tag_name = ""
        
        try:
            f = open(path_dict,"r")
            for word in f:
                words.append(word.strip())
            f.close()
        except IOError:
            print ("dictionary not in anticipated location")
       
        model = QStringListModel(words, self.m_completer)
        
        self.m_completer.setModel(model)
        self.m_completer.setCompletionMode(QCompleter.PopupCompletion)
        self.m_completer.activated.connect(self.insertCompletion)

    def insertCompletion (self, completion):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        cursor.movePosition(QTextCursor.Left)
        cursor.movePosition(QTextCursor.EndOfWord)
        extra = len(self.m_completer.completionPrefix())
        cursor.insertText(completion[extra:])
        self.setTextCursor(cursor)
        cursor.endEditBlock()

    def __insertTag(self):
        '''
        inserts the corresponding closing tag to an opening xml tag
        '''
        self.find('<', QTextDocument.FindBackward)
        tc = self.textCursor()        
        tc.select(QTextCursor.WordUnderCursor)
        txt = '' if self.__stringHasBracket(tc.selectedText().replace(' ', '')) else tc.selectedText()
        txt = '</' + txt + '>'
        
        self.find('>')    
        tc = self.textCursor()
        tc.clearSelection()
        
        tc.insertText(txt) 
        tc.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, len(txt))
        self.setTextCursor(tc)
    
    def __stringHasBracket(self, s):
        return '<' in s or '>' in s

    def __insertClosingTag(self, key):
        '''
        inserts a closing tag after the closing bracket of open tag
        @param key: keyboard input value as int
        '''
        if self.flag_open_angle_bracket :
            if key == 62  :  # >
                self.__insertTag()
                self.flag_open_angle_bracket = False            
        elif key == 62  :  # >
            return
        elif key == 60  :  # <
            self.flag_open_angle_bracket = True
 
    def keyPressEvent(self, event):
        '''
        checks keyboard input to set closing tag or start code completion 
        '''        
        if self.m_completer.popup().isVisible() :
            if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return or event.key() == Qt.Key_Tab or event.key() == Qt.Key_Escape :
                event.ignore()
                return

        super(EditorCodeCompletion, self).keyPressEvent(event)
        
        # ============================================================================================= 
        # begin tag inline insertion 
        self.__insertClosingTag(event.key())
        # end tag inline insertion 
        # ============================================================================================= 
        
        cursor = self.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)        
        completionPrefix = cursor.selectedText()

        isShortcut = (event.modifiers() == Qt.ControlModifier and
                      event.key() == Qt.Key_Space)

        if completionPrefix != self.m_completer.completionPrefix() :
            self.m_completer.setCompletionPrefix(completionPrefix)
            self.m_completer.popup().setCurrentIndex(self.m_completer.completionModel().index(0, 0))

        # if not event.text() != "" and len(completionPrefix) > 2 :
        if len(completionPrefix) > 2 and isShortcut :
            cr = self.cursorRect()
            cr.setWidth(2 * (self.m_completer.popup().sizeHintForColumn(0)
                         + self.m_completer.popup().verticalScrollBar().sizeHint().width()))

            self.m_completer.complete(cr)  # # popup it up!
           
     
if __name__ == "__main__":
    app = QApplication([])
    te = EditorCodeCompletion(config.Config.path_code_completion_dict)
    te.show()
    app.exec_()
