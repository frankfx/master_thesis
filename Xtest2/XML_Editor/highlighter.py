'''
Created on Jul 24, 2014

@author: fran_re
'''

from PySide import QtCore, QtGui

class Highlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

        keywordFormat = QtGui.QTextCharFormat()
        keywordFormat.setForeground(QtCore.Qt.blue)
        keywordPatterns = ["<[^\s>]*[\s>]", ">"]
        self.highlightingRules = [(QtCore.QRegExp(pattern), keywordFormat)
                for pattern in keywordPatterns]        

        attributeFormat = QtGui.QTextCharFormat()
        attributeFormat.setForeground(QtCore.Qt.red)
        attributePatterns = ["\s([.\S]*)(?=\=\")"]
        self.highlightingRules += [(QtCore.QRegExp(pattern), attributeFormat)
                for pattern in attributePatterns]         

        self.multiLineCommentFormat = QtGui.QTextCharFormat()
        self.multiLineCommentFormat.setForeground(QtCore.Qt.gray)

        quotationFormat = QtGui.QTextCharFormat()
        quotationFormat.setForeground(QtCore.Qt.darkCyan)
        self.highlightingRules.append((QtCore.QRegExp("\"[^\"]*\""),
                quotationFormat))

        self.commentStartExpression = QtCore.QRegExp("<!--") 
        self.commentEndExpression = QtCore.QRegExp("-->")

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartExpression.indexIn(text)

        while startIndex >= 0:
            endIndex = self.commentEndExpression.indexIn(text, startIndex)

            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()

            self.setFormat(startIndex, commentLength,
                    self.multiLineCommentFormat)
            startIndex = self.commentStartExpression.indexIn(text,
                    startIndex + commentLength);
