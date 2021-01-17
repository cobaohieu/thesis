# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


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
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 659, 541))
        self.layoutWidget.setObjectName("layoutWidget")
        self.videoLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.videoLayout.setContentsMargins(0, 0, 0, 0)
        self.videoLayout.setObjectName("videoLayout")
        mainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(mainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 677, 25))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuAction = QtWidgets.QMenu(self.menuBar)
        self.menuAction.setObjectName("menuAction")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        mainWindow.setMenuBar(self.menuBar)
        self.actionHelp = QtWidgets.QAction(mainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionAbout = QtWidgets.QAction(mainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionRun_Stop = QtWidgets.QAction(mainWindow)
        self.actionRun_Stop.setObjectName("actionRun_Stop")
        self.actionDefault_Program = QtWidgets.QAction(mainWindow)
        self.actionDefault_Program.setObjectName("actionDefault_Program")
        self.actionScan_QR_code = QtWidgets.QAction(mainWindow)
        self.actionScan_QR_code.setObjectName("actionScan_QR_code")
        self.actionRGB_color_detect = QtWidgets.QAction(mainWindow)
        self.actionRGB_color_detect.setObjectName("actionRGB_color_detect")
        self.actionSave_Pixy_parameters = QtWidgets.QAction(mainWindow)
        self.actionSave_Pixy_parameters.setObjectName("actionSave_Pixy_parameters")
        self.actionConfigure = QtWidgets.QAction(mainWindow)
        self.actionConfigure.setObjectName("actionConfigure")
        self.actionLoad_Pixy_parameters = QtWidgets.QAction(mainWindow)
        self.actionLoad_Pixy_parameters.setObjectName("actionLoad_Pixy_parameters")
        self.actionExit = QtWidgets.QAction(mainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionGet_frame = QtWidgets.QAction(mainWindow)
        self.actionGet_frame.setObjectName("actionGet_frame")
        self.menuFile.addSeparator()
        self.menuFile.addSeparator()
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionConfigure)
        self.menuFile.addAction(self.actionSave_Pixy_parameters)
        self.menuFile.addAction(self.actionLoad_Pixy_parameters)
        self.menuFile.addAction(self.actionExit)
        self.menuAction.addAction(self.actionRun_Stop)
        self.menuAction.addAction(self.actionDefault_Program)
        self.menuAction.addAction(self.actionGet_frame)
        self.menuAction.addAction(self.actionRGB_color_detect)
        self.menuAction.addAction(self.actionScan_QR_code)
        self.menuHelp.addSeparator()
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionAbout)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuAction.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Pixy Camera Control V2020"))
        self.menuFile.setTitle(_translate("mainWindow", "File"))
        self.menuAction.setTitle(_translate("mainWindow", "Action"))
        self.menuHelp.setTitle(_translate("mainWindow", "Help"))
        self.actionHelp.setText(_translate("mainWindow", "Help (F1)"))
        self.actionAbout.setText(_translate("mainWindow", "About (F12)"))
        self.actionRun_Stop.setText(_translate("mainWindow", "Start/Stop (Space)"))
        self.actionDefault_Program.setText(_translate("mainWindow", "Default program (ctrl+D)"))
        self.actionScan_QR_code.setText(_translate("mainWindow", "Scan QR code (Ctrl+Q)"))
        self.actionRGB_color_detect.setText(_translate("mainWindow", "RGB color detect (Ctrl+R)"))
        self.actionSave_Pixy_parameters.setText(_translate("mainWindow", "Save Pixy parameters (Ctrl+P)"))
        self.actionConfigure.setText(_translate("mainWindow", "Configure (Ctrl+,)"))
        self.actionLoad_Pixy_parameters.setText(_translate("mainWindow", "Load Pixy parameters (Ctrl + L)"))
        self.actionExit.setText(_translate("mainWindow", "Exit (Ctrl+W)"))
        self.actionGet_frame.setText(_translate("mainWindow", "Get frame (Ctrl+G)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
