# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_w_textedit.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.setWindowModality(QtCore.Qt.NonModal)
        mainWindow.setEnabled(True)
        mainWindow.resize(677, 626)
        mainWindow.setFocusPolicy(QtCore.Qt.NoFocus)
        mainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 0, 659, 471))
        self.layoutWidget.setObjectName("layoutWidget")
        self.videoLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.videoLayout.setContentsMargins(0, 0, 0, 0)
        self.videoLayout.setObjectName("videoLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setEnabled(True)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 470, 661, 107))
        self.plainTextEdit.setMaximumSize(QtCore.QSize(16777215, 108))
        self.plainTextEdit.setSizeIncrement(QtCore.QSize(649, 108))
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        mainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(mainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 677, 19))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuAction = QtWidgets.QMenu(self.menuBar)
        self.menuAction.setObjectName("menuAction")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        mainWindow.setMenuBar(self.menuBar)
        ##### File
        self.actionConfigure = QtWidgets.QAction(mainWindow)
        self.actionConfigure.setObjectName("actionConfigure")
        self.actionSave_Pixy_parameters = QtWidgets.QAction(mainWindow)
        self.actionSave_Pixy_parameters.setObjectName("actionSave_Pixy_parameters")
        self.actionLoad_Pixy_parameters = QtWidgets.QAction(mainWindow)
        self.actionLoad_Pixy_parameters.setObjectName("actionLoad_Pixy_parameters")
        self.actionRestore_default_parameters = QtWidgets.QAction(mainWindow)
        self.actionRestore_default_parameters.setObjectName("actionRestore_default_parameters")
        self.actionSave_Image = QtWidgets.QAction(mainWindow)
        self.actionSave_Image.setObjectName("actionSave_Image")
        self.actionExit = QtWidgets.QAction(mainWindow)
        self.actionExit.setObjectName("actionExit")
        ##### Action
        self.actionRun_Stop = QtWidgets.QAction(mainWindow)
        self.actionRun_Stop.setObjectName("actionRun_Stop")
        self.actionDefault_Program = QtWidgets.QAction(mainWindow)
        self.actionDefault_Program.setObjectName("actionDefault_Program")
        self.actionGet_frame = QtWidgets.QAction(mainWindow)
        self.actionGet_frame.setObjectName("actionGet_frame")
        self.actionRGB_color_detect = QtWidgets.QAction(mainWindow)
        self.actionRGB_color_detect.setObjectName("actionRGB_color_detect")
        self.actionScan_QR_code = QtWidgets.QAction(mainWindow)
        self.actionScan_QR_code.setObjectName("actionScan_QR_code")
        ##### Help
        self.actionHelp = QtWidgets.QAction(mainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionAbout = QtWidgets.QAction(mainWindow)
        self.actionAbout.setObjectName("actionAbout")
        # self.menuFile.addSeparator()
        # self.menuFile.addSeparator()
        # self.menuFile.addSeparator()
        ##### File
        self.menuFile.addAction(self.actionConfigure)
        self.menuFile.addAction(self.actionSave_Pixy_parameters)
        self.menuFile.addAction(self.actionLoad_Pixy_parameters)
        self.menuFile.addAction(self.actionRestore_default_parameters)
        self.menuFile.addAction(self.actionSave_Image)
        self.menuFile.addAction(self.actionExit)
        ##### Action
        self.menuAction.addAction(self.actionRun_Stop)
        self.menuAction.addAction(self.actionDefault_Program)
        self.menuAction.addAction(self.actionGet_frame)
        self.menuAction.addAction(self.actionRGB_color_detect)
        self.menuAction.addAction(self.actionScan_QR_code)
        # self.menuHelp.addSeparator()
        # self.menuHelp.addSeparator()
        ##### Help
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionAbout)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuAction.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Pixy Camera Control (2020)"))
        ##### File
        self.menuFile.setTitle(_translate("mainWindow", "File"))
        self.actionConfigure.setText(_translate("mainWindow", "Configure"))
        self.actionSave_Pixy_parameters.setText(_translate("mainWindow", "Save Pixy parameters"))
        self.actionLoad_Pixy_parameters.setText(_translate("mainWindow", "Load Pixy parameters"))
        self.actionRestore_default_parameters.setText(_translate("mainWindow", "Restore default parameters"))
        self.actionSave_Image.setText(_translate("mainWindow", "Save Image"))
        self.actionExit.setText(_translate("mainWindow", "Exit"))
        ##### Action
        self.menuAction.setTitle(_translate("mainWindow", "Action"))
        self.actionRun_Stop.setText(_translate("mainWindow", "Start/Stop"))
        self.actionDefault_Program.setText(_translate("mainWindow", "Default program"))
        self.actionGet_frame.setText(_translate("mainWindow", "Get frame"))
        self.actionRGB_color_detect.setText(_translate("mainWindow", "RGB color detect"))
        self.actionScan_QR_code.setText(_translate("mainWindow", "Scan QR code"))
        ##### Help
        self.menuHelp.setTitle(_translate("mainWindow", "Help"))
        self.actionHelp.setText(_translate("mainWindow", "Help"))
        self.actionAbout.setText(_translate("mainWindow", "About"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
