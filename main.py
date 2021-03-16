#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Head       :Pixy Application V2020

Description:

Author     : Co Bao Hieu
Id         : M3718007
"""

import sys
import PyQt5
import time
import datetime
import numpy as np
import usb

# import config
# import config_ui
# import detect
import main_ui
# import about_ui

# import PyQt5.Qt as Qt
import PyQt5.QtCore as QtCore
import PyQt5.QtDBus as QtDBus
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
# import PyQt5.QtNetwork as QtNetwork
# import PyQt5.QtXmlPatterns as QtXmlPatterns
# from PyQt5 import *

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QInputDialog, QGraphicsRectItem, QGraphicsScene, QMessageBox, QMainWindow, QToolTip, QPushButton, QLineEdit, QDialog, QHBoxLayout, QSlider
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QIcon, QFont, QImage, QPixmap
from PyQt5.uic import loadUi

# from main_ui import Ui_mainWindow
# from about_ui import Ui_AboutForm

sys.path.append(os.path.join(os.path.dirname(__file__), "./get_blocks"))
from get_blocks import Blocks

sys.path.append(os.path.join(os.path.dirname(__file__), "./pantilt"))
from pan_tilt import Blocks, Gimbal


class mainApp(QMainWindow, main_ui.Ui_mainWindow):
    def __init__(self, parent=None):
        super(mainApp, self).__init__(parent)
        self.setupUi(self)

        ################## File ##################
        # Config dialog
        self.actionConfigure.setShortcut('Ctrl+,')
        self.actionConfigure.triggered.connect(self.configure_dialog)

        # Save Pixy parameter
        self.actionSave_Pixy_parameters.setShortcut('Ctrl+S')
        self.actionSave_Pixy_parameters.triggered.connect(self.save_pixy_parameters_function)

        # Load Pixy Parameter
        self.actionLoad_Pixy_parameters.setShortcut('Ctrl+L')
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
        print('Your code here')

    # Save parameter fucntion:
    #   Store all hex color of Red Green Blue values in a text file
    def save_pixy_parameters_function(self):
        print('Your code here')

    # Load parameter fucntion:
    #   Load a text file which contain all hex color of Red Green Blue values
    #   and show it on camera preview
    def load_pixy_parameters_function(self):
        print('Your code here')

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
        print('Your code here')

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
    form = mainApp()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()

################## Fin ##################
