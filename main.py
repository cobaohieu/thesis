#!/usr/bin/python3.8
# -*- coding: utf-8 -*-

"""
Head       :Pixy Application V2020

Description:

Author     : Co Bao Hieu
Id         : M3718007
"""

import sys
import os
import PyQt5
import time
import datetime
import numpy as np
import usb

# import config
# import config_ui
# import detect
import main_ui
import config_ui
import about_ui

# import PyQt5.Qt as Qt
import PyQt5.QtCore as QtCore
import PyQt5.QtDBus as QtDBus
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
# import PyQt5.QtMultimedia as QtMultimedia
# import PyQt5.QtNetwork as QtNetwork
# import PyQt5.QtXmlPatterns as QtXmlPatterns
# from PyQt5 import *
# from PyQt5.QtCore import Qt, QString, QSysInfo, QUrl, QMetaType, QSettings, QObject, QDir, QScopedPointer, QVariant, QIODevice, QThread, QMutex, QWaitCondition, QStringList, QList, QDebug, QMutexLocker, QTime
from PyQt5.QtCore import Qt, QSysInfo, QUrl, QMetaType, QSettings, QObject, QDir, QVariant, QIODevice, QThread, QMutex, QWaitCondition, QMutexLocker, QTime
from PyQt5.QtGui import QIcon, QFont, QImage, QPixmap, QDesktopServices, QColor, QPen, QPainter
# from PyQt5.QtMultimedia import QVideoFrame, QVideoEncoderSettings, QVideoSurfaceFormat, QMediaContent, QMediaPlayer
# from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QInputDialog, QGraphicsRectItem, QGraphicsScene, QMessageBox, QMainWindow, QToolTip, QPushButton, QLineEdit, QDialog, QHBoxLayout, QSlider, QAbstractButton, QCheckBox, QTableWidget, QButtonGroup, QDialogButtonBox, QSpacerItem, QGridLayout, QAction, QHeaderView, QVBoxLayout, QTextBrowser, QSizePolicy, QStyle
from PyQt5.uic import loadUi



from main_ui import Ui_mainWindow as Ui_mainWindow
from config_ui import Ui_ConfigForm as Ui_ConfigForm
from about_ui import Ui_AboutForm as Ui_AboutForm

sys.path.append(os.path.join(os.path.dirname(__file__), "./get_blocks"))
# from get_blocks import Blocks

sys.path.append(os.path.join(os.path.dirname(__file__), "./pantilt"))
# from pan_tilt import Blocks, Gimbal


class configForm(QDialog, config_ui.Ui_ConfigForm):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent=parent)
        self.setupUi(self)

class aboutForm(QDialog, about_ui.Ui_AboutForm):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent=parent)
        self.setupUi(self)

class mainForm(QMainWindow, main_ui.Ui_mainWindow):
    def __init__(self, parent=None):
        super(mainForm, self).__init__(parent)
        self.setupUi(self)

        ################## File ##################
        # Config dialog
        self.actionConfigure.setShortcut('Ctrl+,')
        self.actionConfigure.triggered.connect(self.configure_dialog)

        # Save Pixy parameter
        self.actionSave_Pixy_parameters.setShortcut('Ctrl+S')
        self.actionSave_Pixy_parameters.triggered.connect(self.save_pixy_parameters_function)

        # Load Pixy Parameter
        self.actionLoad_Pixy_parameters.setShortcut('Ctrl+O')
        self.actionLoad_Pixy_parameters.triggered.connect(self.load_pixy_parameters_function)

        # Exit
        self.actionExit.setShortcut('Ctrl+W')
        self.actionExit.triggered.connect(self.exit_dialog)

        ################## Action ##################
        # Start/Stop
        self.actionRun_Stop.setShortcut('Space')
        self.actionRun_Stop.triggered.connect(self.run_stop_function)

        # Default program
        self.actionDefault_Program.setShortcut('Ctrl+D')
        self.actionDefault_Program.triggered.connect(self.default_program_function)

        # Get frame
        self.actionGet_frame.setShortcut('Ctrl+F')
        self.actionGet_frame.triggered.connect(self.get_frame_function)

        # RGB color detect
        self.actionRGB_color_detect.setShortcut('Ctrl+R')
        self.actionRGB_color_detect.triggered.connect(self.rgb_color_detect_function)

        # Scan QR code
        self.actionScan_QR_code.setShortcut('Ctrl+Q')
        self.actionScan_QR_code.triggered.connect(self.scan_qr_code_function)

        ################## Help ##################
        # Help dialog
        self.actionHelp.setShortcut('F1')
        self.actionHelp.triggered.connect(self.help_dialog)

        # About dialog
        self.actionAbout.setShortcut('F12')
        self.actionAbout.triggered.connect(self.about_dialog)

################## Process Function ##################

    ################## File ##################
    # Configuatrion Form:
    #   A form control Red Green Blue color which could modify
    #   via three scrolling horizontal menu with value from 0 - 255 like
    #       Red  : 0 |==================||================| 255
    #       Green: 0 |=========||=========================| 255
    #       Blue : 0 |===========================||=======| 255
    #       RestoreDefaults             Apply               Cancel
    #   Like Hue color encoding
    #   Or we could import from files: config (for coding) and config_ui (for GUI)
    def configure_dialog(self):
        # QMessageBox.NoIcon(self, "Configuration", "Call function code")
        #
        # QMessageBox.RestoreDefaults
        # QMessageBox.ResetRole
        # #
        # QMessageBox.Apply
        # QMessageBox.ApplyRole
        # #
        # QMessageBox.Cancel
        # QMessageBox.RejectRole
        self.form = configForm()
        self.form.show()
        print('Your code here for modify color text box|slider and button Apply|Cancel|OK')

    # Save parameter fucntion:
    #   Store all hex color of Red Green Blue values in a text file
    def save_pixy_parameters_function(self):
        self.saveFileDialog()
        print('Your code here process print parameters to a file *.rpm')

    # Load parameter fucntion:
    #   Load a text file which contain all hex color of Red Green Blue values
    #   and show it on camera preview
    def load_pixy_parameters_function(self):
        self.openFileNameDialog()
        print('Your code here process load input parameter to camera and show in video view')

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;PixyMon Files (*.prm)", options=options)
        if fileName:
            print(fileName)

    def openFilesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "Open Files", "", "All Files (*);;PixyMon Files (*.prm)", options=options)
        if files:
            print(files)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Save", "", "All Files (*);;PixyMon Files (*.prm)", options=options)
        if fileName:
            print(fileName)

    # Exit dialog:
    #   A form which show Yes or No when you want to exit the app
    #   If Yes  -> Exit
    #   If No   -> return
    def exit_dialog(self):
        ret = QMessageBox.question(self, "Exit", "Do you want to exit the app?")
        if ret == QMessageBox.Yes:
            QApplication.quit()
            exit()
        else:
            return

    ################## Action ##################
    # Run/Stop function:
    #   Allow turn on camera or pause camera like Play/Pause in music
    #   You could you once space to start cmaera and twice space to pause camera
    def run_stop_function(self):
        print('Your code here to show camera view on video view')

    # default program function:
    #   Don't know what to descire the function
    def default_program_function(self):
        print('Your code here')

    # get fram function:
    #   We could get frame of camera to default or higher than
    #   A form will display for you choose value that you want like
    #   Frame: 0 |=================||=================| 255fps
    #                             50fps
    def get_frame_function(self):
        print('Your code here')

    # rgb color detect function:
    #   So difficult function
    #   A function could detect color of object
    #   and detect what is the name of object
    #   After that, store it a text file and detect another object
    #   The function must be training and testing
    def rgb_color_detect_function(self):
        print('Your code here')

    # scan qr code function:
    #   Enable function scan qr code and decode the picture or image
    #   and show it on screen
    #   We could import a image from local or scan via camera
    def scan_qr_code_function(self):
        print('Your code here')

    ################## Help ##################
    def help_dialog(self):
        QMessageBox.information(self, "Help", "If you want know more about Pixy CMU5 Camera,\nplease visit this link below.\nhttps://docs.pixycam.com/wiki/doku.php?id=wiki:v1:pixymon_index/")

    def about_dialog(self):
        QMessageBox.information(self, "About", "Pixy Camera Control (2020)\nVersion: 1.0.0.0\nDate: 03/2021\nDesigned by Co Bao Hieu | M3718007")


################## Main ##################
def main():
    app = QApplication(sys.argv)
    form = mainForm()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()

################## Fin ##################
