'''
Created on Aug 11, 2014

@author: fran_re
'''

from PySide import QtGui, QtOpenGL
from PySide.QtCore import QFile, QEvent,Qt
from PySide.QtGui import QStackedWidget, QMessageBox, QAction, QLabel, QColor, QTextFormat, QTextDocument, QTextCursor


class NumberBar(QtGui.QWidget):
    def __init__(self, *args):
        QtGui.QWidget.__init__(self, *args)
        self.edit = None
        # This is used to update the width of the control.
        # It is the highest line that is currently visibile.
        self.highest_line = 0
 
    def setTextEdit(self, stats):
        self.states = stats
        self.edit = stats.get("editor")
        self.flag_view_algo = False
 
    def update(self):
        '''
        Updates the number bar to display the current set of numbers.
        Also, adjusts the width of the number bar if necessary.
        '''
        # The + 4 is used to compensate for the current line being bold.
        width = self.fontMetrics().width(str(self.highest_line)) + 4
        if self.width() != width:
            self.setFixedWidth(width)
        QtGui.QWidget.update(self)

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
        if(self.states.get("searchbox").isFocused()) :
            self.flag_view_algo = True
        else :
            self.flag_view_algo = False
        
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
        
        if self.flag_view_algo == True :
            self.states.get("searchbox").setFocus()      
        
