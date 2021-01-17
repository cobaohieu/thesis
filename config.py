# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'config.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ConfigForm(object):
    def setupUi(self, ConfigForm):
        ConfigForm.setObjectName("ConfigForm")
        ConfigForm.resize(591, 305)
        self.centralwidget = QtWidgets.QWidget(ConfigForm)
        self.centralwidget.setObjectName("centralwidget")
        self.ConfigButton = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.ConfigButton.setGeometry(QtCore.QRect(10, 270, 571, 28))
        self.ConfigButton.setOrientation(QtCore.Qt.Horizontal)
        self.ConfigButton.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.ConfigButton.setObjectName("ConfigButton")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 571, 261))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.layoutWidget)
        self.tabWidget.setObjectName("tabWidget")
        self.pixyTab = QtWidgets.QWidget()
        self.pixyTab.setObjectName("pixyTab")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.pixyTab)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.pixyLayout = QtWidgets.QGridLayout()
        self.pixyLayout.setObjectName("pixyLayout")
        self.gridLayout_5.addLayout(self.pixyLayout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.pixyTab, "")
        self.pixymonTab = QtWidgets.QWidget()
        self.pixymonTab.setObjectName("pixymonTab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.pixymonTab)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.pixymonLayout = QtWidgets.QGridLayout()
        self.pixymonLayout.setObjectName("pixymonLayout")
        self.gridLayout_4.addLayout(self.pixymonLayout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.pixymonTab, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        ConfigForm.setCentralWidget(self.centralwidget)

        self.retranslateUi(ConfigForm)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(ConfigForm)

    def retranslateUi(self, ConfigForm):
        _translate = QtCore.QCoreApplication.translate
        ConfigForm.setWindowTitle(_translate("ConfigForm", "Configure"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.pixyTab), _translate("ConfigForm", "Pixy Parameters (saved on Pixy)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.pixymonTab), _translate("ConfigForm", "PixyMon Parameters (saved on computer)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConfigForm = QtWidgets.QMainWindow()
    ui = Ui_ConfigForm()
    ui.setupUi(ConfigForm)
    ConfigForm.show()
    sys.exit(app.exec_())
