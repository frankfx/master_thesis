import sys
import math
from PySide import QtCore, QtGui, QtOpenGL
from PySide.QtCore import QFile, QEvent,Qt

class LineTextWidget(QtGui.QMainWindow):
 
    class NumberBar(QtGui.QWidget):
 
        def __init__(self, *args):
            QtGui.QWidget.__init__(self, *args)
            self.edit = None
            # This is used to update the width of the control.
            # It is the highest line that is currently visibile.
            self.highest_line = 0
 
        def setTextEdit(self, edit):
            self.edit = edit
 
        def update(self, *args):
            '''
            Updates the number bar to display the current set of numbers.
            Also, adjusts the width of the number bar if necessary.
            '''
            # The + 4 is used to compensate for the current line being bold.
            width = self.fontMetrics().width(str(self.highest_line)) + 4
            if self.width() != width:
                self.setFixedWidth(width)
            QtGui.QWidget.update(self, *args)
 
        def highlightCurrentLine(self) :
            extraSelections = []
            selection = QtGui.QTextEdit.ExtraSelection()
            lineColor = QtGui.QColor(255,250,205)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
            selection.cursor = self.edit.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
            self.edit.setExtraSelections(extraSelections)
            self.edit.setFocus()             
 
        def paintEvent(self, event):
            contents_y = self.edit.verticalScrollBar().value()
            page_bottom = contents_y + self.edit.viewport().height()
            font_metrics = self.fontMetrics()
            current_block = self.edit.document().findBlock(self.edit.textCursor().position())
 
            self.highlightCurrentLine()
            painter = QtGui.QPainter(self)
 
            line_count = 0
            # Iterate over all text blocks in the document.
            block = self.edit.document().begin()
            while block.isValid():
                line_count += 1
 
                # The top left position of the block in the document
                position = self.edit.document().documentLayout().blockBoundingRect(block).topLeft()
 
                # Check if the position of the block is out side of the visible
                # area.
                if position.y() > page_bottom:
                    break
 
                # We want the line number for the selected line to be bold.
                bold = False
                if block == current_block:
                    bold = True
                    font = painter.font()
                    font.setBold(True)
                    painter.setFont(font)
 
                # Draw the line number right justified at the y position of the
                # line. 3 is a magic padding number. drawText(x, y, text).
                painter.drawText(self.width() - font_metrics.width(str(line_count)) - 1, round(position.y()) - contents_y + font_metrics.ascent(), str(line_count))
 
                # Remove the bold style if it was set previously.
                if bold:
                    font = painter.font()
                    font.setBold(False)
                    painter.setFont(font)
 
                block = block.next()
 
            self.highest_line = line_count
            painter.end()
 
            QtGui.QWidget.paintEvent(self, event)
 
 
    def __init__(self, *args):
        super(LineTextWidget, self).__init__()
 
        self.edit = QtGui.QTextEdit()
        self.edit.setAcceptRichText(False)
 
        self.number_bar = self.NumberBar()
        self.number_bar.setTextEdit(self.edit)
        self.edit.cursorPositionChanged.connect(self.number_bar.update)
 
        hbox = QtGui.QHBoxLayout()
        hbox.setSpacing(0)
        hbox.setContentsMargins(0,0,0,0)
        hbox.addWidget(self.number_bar)
        hbox.addWidget(self.edit)
        
        win = QtGui.QWidget()
        win.setLayout(hbox)
        
        self.setCentralWidget(win)
 
        self.edit.installEventFilter(self)
        self.edit.viewport().installEventFilter(self)

    def eventFilter(self, object, event):
          # Update the line numbers for all events on the text edit and the viewport.
        # This is easier than connecting all necessary singals.

        if object in (self.edit, self.edit.viewport()):
            self.number_bar.update()
            return False
        return  QtGui.QMainWindow.eventFilter(object, event)

    def getTextEdit(self):
        return self.edit
    
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = LineTextWidget()
    window.show()
    sys.exit(app.exec_())
    