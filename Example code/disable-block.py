from PyQt5 import QtWidgets, QtGui

app = QtWidgets.QApplication([])

self.b = QtWidgets.QPlainTextEdit()
self.b.show()

t = QtGui.QTextCursor(self.b.document())
t.insertText('plain text')
t.insertBlock()
t.insertText('tags, tags, tags')
t.block().setVisible(False)

print(self.b.document().toPlainText())

app.exec_()