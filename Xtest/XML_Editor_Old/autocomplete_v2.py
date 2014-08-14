import sys
import os
from PySide.QtGui import QTextEdit, QCompleter, QStringListModel, QTextCursor, QApplication, QWidget
from PySide.QtCore import SIGNAL, Qt

class MyTextEdit(QTextEdit):
    def __init__(self):
        super(MyTextEdit, self).__init__()  
        self.m_completer = QCompleter(self)
        self.m_completer.setWidget(self)
        
        words = []
        
        try:
            script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
            rel_path = "config/keywords"
            abs_file_path = os.path.join(script_dir, rel_path)
            f = open(abs_file_path,"r")
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
        extra = len(self.m_completer.completionPrefix())
         
        cursor.movePosition(QTextCursor.Left)
        cursor.movePosition(QTextCursor.EndOfWord)
        cursor.insertText(completion[extra:])
        self.setTextCursor(cursor)

    def textUnderCursor(self):
        cursor = self.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        return cursor.selectedText()
 
    def keyPressEvent(self, event):
        if self.m_completer.popup().isVisible() :
            if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return or event.key() == Qt.Key_Tab or event.key() == Qt.Key_Escape :
                event.ignore()
                return
        
        super(MyTextEdit, self).keyPressEvent(event)
        completionPrefix = self.textUnderCursor()
        
        isShortcut = (event.modifiers() == Qt.ControlModifier and
                      event.key() == Qt.Key_Space)
        
        if completionPrefix != self.m_completer.completionPrefix() :
            self.m_completer.setCompletionPrefix(completionPrefix)
            self.m_completer.popup().setCurrentIndex(self.m_completer.completionModel().index(0,0))
            
        #if not event.text() != "" and len(completionPrefix) > 2 :
        if len(completionPrefix) > 2 and isShortcut :
            cr = self.cursorRect()
            cr.setWidth(2 * (self.m_completer.popup().sizeHintForColumn(0)
                        + self.m_completer.popup().verticalScrollBar().sizeHint().width()) )
            
            self.m_completer.complete(cr) ## popup it up!
            
if __name__ == "__main__":

    app = QApplication([])
    te = MyTextEdit()
    te.show()
    app.exec_()