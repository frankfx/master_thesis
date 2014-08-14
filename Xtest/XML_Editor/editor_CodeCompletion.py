'''
Created on Aug 12, 2014

@author: fran_re
'''
import sys
import re
import os
from PySide.QtGui import QTextEdit, QCompleter, QStringListModel, QTextCursor, QApplication, QWidget
from PySide.QtCore import SIGNAL, Qt

    
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
            print "dictionary not in anticipated location"
       
        model = QStringListModel(words, self.m_completer)
        
        self.m_completer.setModel(model)
        self.m_completer.setCompletionMode(QCompleter.PopupCompletion)
        #self.connect(self.m_completer, SIGNAL("activated()"), self.insertCompletion)
       
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
    
    def insertCompletionInline(self, completion):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        cursor.movePosition(QTextCursor.Left)
        cursor.movePosition(QTextCursor.EndOfWord)
        cursor.insertText(completion)
        cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, 4)
        self.setTextCursor(cursor)
        cursor.endEditBlock()
        
    def getTagName(self, pos):
        cursor = self.textCursor()
        cursor.select(QTextCursor.LineUnderCursor)
        txt = cursor.selectedText()[:pos]
        try :
            txt = re.findall('<.*?>', txt)[-1]
            pattern = "(?<=[<]).*?(?=[\s>])"        # (?<=[<]) === look behind [<] ;;; .*? === any sign but not greedy
            return re.search(pattern, txt).group(0) # (?=[\s>]) === look ahead [space or >] 
        except IndexError:
            return ''

    def textUnderCursor(self):
        cursor = self.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        return cursor.selectedText()
        
 
    def keyPressEvent(self, event):
        
        if self.m_completer.popup().isVisible() :
            if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return or event.key() == Qt.Key_Tab or event.key() == Qt.Key_Escape :
                event.ignore()
                return

        super(EditorCodeCompletion, self).keyPressEvent(event)
        
        # ============================================================================================= 
        # begin tag inline insertion 
        if self.flag_open_angle_bracket :
            if event.key() == 62  :  # >
                self.insertCompletionInline('</' + self.getTagName(self.textCursor().position()) + '>')
                self.tag_name = ""
                self.flag_open_angle_bracket = False            
        elif event.key() == 60  :  # <
            self.tag_start = self.textCursor().position()
            self.flag_open_angle_bracket = True
        # end tag inline insertion 
        # ============================================================================================= 
        
        completionPrefix = self.textUnderCursor()

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

    import config
    app = QApplication([])
    te = EditorCodeCompletion(config.Config.path_code_completion_dict)
    te.show()
    app.exec_()
