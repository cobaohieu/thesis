# import PyQt5
# from PyQt5 import QtCore, QtGui

# class MyWindow(QtGui.QWidget):
#     def __init__(self):
#         super().__init__()

#         layout = QtGui.QVBoxLayout()
#         self.setLayout(layout)

#         lblhm = QtGui.QLabel("Hauptmessung", self)
#         layout.addWidget(lblhm)

#         self.__hm_b = self.__add_button("Messung öffnen", layout)
#         self.__hm_config_b = self.__add_button("Configruation öffnen", layout)

#         lblzm = QtGui.QLabel("Zusatzmessung", self)
#         layout.addWidget(lblzm)

#         self.__zm_b = self.__add_button("Messung öffnen", layout)
#         self.__zm_config_b = self.__add_button("Configuration öffnen", layout)

#     def button_pressed(self):
#         print('Button pressed')

#     def __add_button(self, text: str, layout: QtGui.QLayout):
#         btn = QtGui.QPushButton(text, self)
#         layout.addWidget(btn)
#         btn.clicked.connect(self.button_pressed)
#         return btn



# if __name__== '__main__':
#     import sys
#     app = QtGui.QApplication(sys.argv)
#     wnd = MyWindow()
#     wnd.show()
#     sys.exit(app.exec_())
########################################################################
# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtWidgets import QMessageBox

# class Ui_MainWindow(object):
# 	# ...
# 	def show_popup(self):
# 		msg = QMessageBox()
# 		msg.setWindowTitle("Tutorial on PyQt5")
# 		msg.setText("This is the main text!")
# 		msg.setIcon(QMessageBox.Question)
# 		msg.setStandardButtons(QMessageBox.Cancel|QMessageBox.Retry|QMessageBox.Ignore)
# 		msg.setDefaultButton(QMessageBox.Retry)
# 		msg.setInformativeText("informative text, ya!")

# 		msg.setDetailedText("details")

# 		msg.buttonClicked.connect(self.popup_button)

# 	def popup_button(self, i):
# 		print(i.text())
########################################################################
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(240, 50, 321, 121))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionSave)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.actionNew.triggered.connect(lambda: self.clicked("New was clicked"))
        self.actionSave.triggered.connect(lambda: self.clicked("Save was clicked"))
        self.actionCopy.triggered.connect(lambda: self.clicked("Copy was clicked"))
        self.actionPaste.triggered.connect(lambda: self.clicked("Paste was clicked"))
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionCopy.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionPaste.setShortcut(_translate("MainWindow", "Ctrl+V"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))

    def clicked(self, text):
        self.label.setText(text)
        self.label.adjustSize()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())