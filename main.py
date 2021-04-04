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
import usb.core
import usb.util
import usb.backend.libusb1
# import cv2
import numpy as numpy
from time import gmtime, strftime
import time

# import config
# import config_ui
# import detect
import main_ui
import main_w_textedit
import config_ui
import configcolor_ui
import about_ui
# import detect


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
from PyQt5.QtCore import (Qt, QSysInfo, QUrl, QMetaType, QSettings, QObject, QDir, QVariant, QIODevice, QThread, QMutex, QWaitCondition, QMutexLocker, QTime, QTimer, QFile)

from PyQt5.QtGui import (QIcon, QFont, QImage, QPixmap, QDesktopServices, QColor, QPen, QPainter, QMouseEvent, QKeyEvent, QTextCursor, QTextBlock)

# from PyQt5.QtMultimedia import QVideoFrame, QVideoEncoderSettings, QVideoSurfaceFormat, QMediaContent, QMediaPlayer
# from PyQt5.QtMultimediaWidgets import QVideoWidget

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QFileDialog, QInputDialog, QGraphicsRectItem, QGraphicsScene, QMessageBox, QMainWindow, QToolTip, QPushButton, QLineEdit, QDialog, QHBoxLayout, QSlider, QAbstractButton, QCheckBox, QTableWidget, QButtonGroup, QDialogButtonBox, QSpacerItem, QGridLayout, QAction, QHeaderView, QVBoxLayout, QTextBrowser, QSizePolicy, QStyle, QPlainTextEdit, QScrollBar)

from PyQt5.uic import loadUi

from main_ui import Ui_mainWindow as Ui_mainWindow
from config_ui import Ui_ConfigForm as Ui_ConfigForm
from configcolor_ui import Ui_ConfigForm as Ui_ConfigColorForm
from about_ui import Ui_AboutForm as Ui_AboutForm
# from detect import

sys.path.append(os.path.join(os.path.dirname(__file__), "./get_blocks"))
# from get_blocks import Blocks

sys.path.append(os.path.join(os.path.dirname(__file__), "./pantilt"))
# from pan_tilt import Blocks, Gimbal

class aboutForm(QDialog, about_ui.Ui_AboutForm):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent=parent)
        self.setupUi(self)

class configForm(QDialog, config_ui.Ui_ConfigForm):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent=parent)
        self.setupUi(self)

class configColorForm(QDialog, configcolor_ui.Ui_ConfigForm):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent=parent)
        self.setupUi(self)

class mainForm(QMainWindow, main_w_textedit.Ui_mainWindow):
    def __init__(self, parent=None):
        super(mainForm, self).__init__(parent)
        self.setupUi(self)

        self.detectUsb()
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
        # self.form = configForm()
        self.form = configColorForm()
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
        # self.openFileNameDialog()
        self.getParameterFile()
        print('Your code here process load input parameter to camera and show in video view')

    def getParameterFile(self):
        options = QFileDialog()
        options.setFileMode(QFileDialog.AnyFile)
        options.setFilter(QDir.Files)

        if options.exec_():
            fileName = options.selectedFiles()

            if fileName[0].endswith('.prm'):
                with open(fileName[0], 'r') as f:
                    data = f.read()
                    self.plainTextEdit.setPlainText(data)
                    f.close()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", r"//home//$USER//Documents//PixyMon//", "All Files (*);;PixyMon Files (*.prm)", options=options)
        if fileName[0]:
            print(fileName)
            with open(fileName[0], 'r') as f:
                    data = f.read()
                    self.plainTextEdit.setPlainText(data)
                    f.close()

    def openFilesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "Open Files", r"//home//$USER//Documents//PixyMon//", "All Files (*);;PixyMon Files (*.prm)", options=options)
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

    ################## Support ##################
    def detectUsb(self):
        VENDOR_ID = 0xb1ac
        PRODUCT_ID = 0xf000
        BDeviceClass = 255
        devClass = usb.core.find(bDeviceClass=BDeviceClass)
        printers = usb.core.find(find_all=True, bDeviceClass=BDeviceClass)

        # SUBSYSTEM=="usb", ATTR{idVendor}=="1fc9", ATTR{idProduct}=="000c", MODE="0666"

        # find our device
        dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
        if dev is None:
            # sys.exit("Could not find device")
            # sys.stdout.write("error: No Pixy devices have been detected.")
            # raise RuntimeError('Pixy CMU5 camera device is not found.')
            # print("Pixy CMU5 camera device is not found.")
            data = "Pixy CMU5 camera device is not found."
            self.plainTextEdit.setPlainText(data)
        else:
            print("Pixy CMU5 camera device is found!")

        # reattach = False

        # # was it found?
        # if dev.is_kernel_driver_active(0):
        #     reattach = True
        #     dev.detach_kernel_driver(0)
        #     dev.reset()

        # print("deviceClass = " + str(dev.bDeviceClass))
        # for cfg in dev:
        #     sys.stdout.write("configuration: " + str(cfg.bConfigurationValue) + '\n')
        #     for intf in cfg:
        #         sys.stdout.write('\tInterface: ' + \
        #                             str(intf.bInterfaceNumber) + \
        #                             ',' + \
        #                             str(intf.bAlternateSetting) + \
        #                             '\n')
        #         for ep in intf:
        #             sys.stdout.write('\t\tEndpoint: ' + \
        #                                 str(ep.bEndpointAddress) + \
        #                                 ',' + \
        #                                 str(ep.bmAttributes) + \
        #                                 '\n')

        # # set the active configuration. With no arguments, the first
        # # configuration will be the active one
        # dev.set_configuration()


        # for bRequest in range(255):
        #     try:
        #         ret = dev.ctrl_transfer(0xC0, bRequest, 0, 0, 1)
        #         print("bRequest ",bRequest)
        #         print(ret)
        #     except:
        #         # failed to get data for this request
        #         pass

        # # first endpoint
        # endpoint = dev[0][(0,0)][0]

        # # get an endpoint instance
        # cfg = dev.get_active_configuration()
        # interface_number = cfg[(0,0)].bInterfaceNumber
        # alternate_setting = usb.control.get_interface(dev,interface_number)
        # intf = usb.util.find_descriptor(cfg, bInterfaceNumber = interface_number, bAlternateSetting = alternate_setting)
        # alt = usb.util.find_descriptor(cfg, find_all=True, bInterfaceNumber=1)


        # ep = usb.util.find_descriptor(
        #     intf,
        #     # match the first OUT endpoint
        #     custom_match = \
        #     lambda e: \
        #         usb.util.endpoint_direction(e.bEndpointAddress) == \
        #         usb.util.ENDPOINT_OUT)

        # if (ep is None):
        #     print("Success connect Pixy CMU5")
        #     # content for do something

        # else:
        #     print("error: No Pixy devices have been detected.")

# printers = usb.core.find(find_all=1, custom_match=find_all(7))

def qt_message_handler(mode, context, message):
    if mode == QtCore.QtInfoMsg:
        mode = 'INFO'
    elif mode == QtCore.QtWarningMsg:
        mode = 'WARNING'
    elif mode == QtCore.QtCriticalMsg:
        mode = 'CRITICAL'
    elif mode == QtCore.QtFatalMsg:
        mode = 'FATAL'
    else:
        mode = 'DEBUG'
    print('qt_message_handler: line: %d, func: %s(), file: %s' % (context.line, context.function, context.file))
    print('  %s: %s\n' % (mode, message))
QtCore.qInstallMessageHandler(qt_message_handler)

################## Main ##################
def main():
    app = QApplication(sys.argv)
    QtCore.qDebug('Something informative')
    form = mainForm()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()

################## Fin ##################
