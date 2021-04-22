#!/usr/bin/python3.8
# -*- coding: utf-8 -*-

"""
Head       :Pixy Application V2020

Description:

Author     : Co Bao Hieu
Id         : M3718007
"""

################## Import Modules ##################
import sys
import os
import PyQt5
import time
import datetime
import numpy
import usb
import usb.core
import usb.util
import usb.backend.libusb1
import time
import ctypes
import cv2
import argparse
import imutils
# import pyzar


# import config_ui
# import detect
import main_ui
import config_ui
import about_ui
# import detect


# import PyQt5.Qt as Qt
import PyQt5.QtCore as QtCore
import PyQt5.QtDBus as QtDBus
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtXml as QtXml
# import PyQt5.QtMultimedia as QtMultimedia
# import PyQt5.QtNetwork as QtNetwork
# import PyQt5.QtXmlPatterns as QtXmlPatterns
# from PyQt5 import *
# from PyQt5.QtCore import Qt, QString, QSysInfo, QUrl, QMetaType, QSettings, QObject, QDir, QScopedPointer, QVariant, QIODevice, QThread, QMutex, QWaitCondition, QStringList, QList, QDebug, QMutexLocker, QTime

################## Import sub modules ##################
from time import gmtime, strftime
from PIL import Image
from imutils.video import VideoStream
# from pyzbar import pyzbar
# from pyzbar.pyzbar import decode



from PyQt5.QtCore import (Qt, QSysInfo, QUrl, QMetaType, QSettings, QObject, QDir, QVariant, QIODevice, QThread, QMutex, QWaitCondition, QMutexLocker, QTime, QTimer, QFile, QAbstractItemModel, QModelIndex, QDataStream, QTextStream)

from PyQt5.QtGui import (QIcon, QFont, QImage, QPixmap, QDesktopServices, QColor, QPen, QPainter, QMouseEvent, QKeyEvent, QTextCursor, QTextBlock, QTransform, QPalette, QBrush, QTextFormat)

# from PyQt5.QtMultimedia import QVideoFrame, QVideoEncoderSettings, QVideoSurfaceFormat, QMediaContent, QMediaPlayer
# from PyQt5.QtMultimediaWidgets import QVideoWidget

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QFileDialog, QInputDialog, QGraphicsRectItem, QGraphicsScene, QMessageBox, QMainWindow, QToolTip, QPushButton, QLineEdit, QDialog, QHBoxLayout, QSlider, QAbstractButton, QCheckBox, QTableWidget, QButtonGroup, QDialogButtonBox, QSpacerItem, QGridLayout, QAction, QHeaderView, QVBoxLayout, QTextBrowser, QSizePolicy, QStyle, QPlainTextEdit, QScrollBar, QTreeView,QAbstractItemDelegate, QAbstractItemView, QHeaderView, QStyleOptionFocusRect, QStyleOption, QStyleOptionFrame, QStyleOptionTabWidgetFrame, QStyleOptionTabBarBase, QStyleOptionHeader, QStyleOptionButton, QStyleOptionProgressBar, QStyleOptionToolBar, QStyleOptionViewItem, QStyleOptionComplex, QStyleOptionSlider, QStyleOptionGraphicsItem, QStyleOptionDockWidget, QStyleOptionSpinBox, QAbstractScrollArea, QStyleOptionGroupBox, QStyleOptionSizeGrip, QStyleOptionComboBox, QStyleOptionTitleBar, QDesktopWidget)

from PyQt5.QtXml import (QDomDocument, QDomElement)

from PyQt5.uic import loadUi

from main_ui import Ui_mainWindow as Ui_mainWindow
from config_ui import Ui_ConfigForm as Ui_ConfigColorForm
from about_ui import Ui_AboutForm as Ui_AboutForm
# from detect import

################## Modules path ##################
sys.path.append(os.path.join(os.path.dirname(__file__), "./get_blocks"))
# from get_blocks import Blocks

sys.path.append(os.path.join(os.path.dirname(__file__), "./pantilt"))
# from pan_tilt import Blocks, Gimbal

################## Class function ##################
class DecodeQRCode:
    def __init__(self, node, row, parent=None):
        self.decode = parent

    def decode(self):
        # construct the argument parser and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
            help="path to output CSV file containing barcodes")
        args = vars(ap.parse_args())
        # initialize the video stream and allow the camera sensor to warm up
        print("[INFO] starting video stream...")
        # vs = VideoStream(src=0).start()
        vs = VideoStream(usePiCamera=True).start()
        time.sleep(2.0)
        # open the output CSV file for writing and initialize the set of
        # barcodes found thus far
        csv = open(args["output"], "w")
        found = set()

        # loop over the frames from the video stream
        while True:
            # grab the frame from the threaded video stream and resize it to
            # have a maximum width of 400 pixels
            frame = vs.read()
            frame = imutils.resize(frame, width=400)
            # find the barcodes in the frame and decode each of the barcodes
            barcodes = pyzbar.decode(frame)
            for barcode in barcodes:
                # extract the bounding box location of the barcode and draw
                # the bounding box surrounding the barcode on the image
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                # the barcode data is a bytes object so if we want to draw it
                # on our output image we need to convert it to a string first
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type
                # draw the barcode data and barcode type on the image
                text = "{} ({})".format(barcodeData, barcodeType)
                cv2.putText(frame, text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                # if the barcode text is currently not in our CSV file, write
                # the timestamp + barcode to disk and update the set
                if barcodeData not in found:
                    csv.write("{},{}\n".format(datetime.datetime.now(),
                        barcodeData))
                    csv.flush()
                    found.add(barcodeData)
                    # show the output frame
                    cv2.imshow("Barcode Scanner", frame)
                    key = cv2.waitKey(1) & 0xFF

                # if the `q` key was pressed, break from the loop
                if key == ord("q"):
                    break
        # close the output CSV file do a bit of cleanup
        print("[INFO] cleaning up...")
        csv.close()
        cv2.destroyAllWindows()
        vs.stop()
################## Reading Xml file ##################
class DomItem(object):
    def __init__(self, node, row, parent=None):
        self.domNode = node
        # Record the item's location within its parent.
        self.rowNumber = row
        self.parentItem = parent
        self.childItems = {}

    def node(self):
        return self.domNode

    def parent(self):
        return self.parentItem

    def child(self, i):
        if i in self.childItems:
            return self.childItems[i]

        if 0 <= i < self.domNode.childNodes().count():
            childNode = self.domNode.childNodes().item(i)
            childItem = DomItem(childNode, i, self)
            self.childItems[i] = childItem
            if childNode.nodeName() == 'branches':
                # based on your example xml there should be only one child entry
                # for each "branches" node, but, just in case, let's cycle amongst
                # every possible child node
                subChildNodes = childNode.childNodes()
                childIndex = 0
                for c in range(subChildNodes.count()):
                    subChild = subChildNodes.at(c)
                    for tag in subChild.nodeValue().split(','):
                        branch = childNode.ownerDocument().createElement(tag)
                        childNode.appendChild(branch)
                        branchItem = DomItem(branch, childIndex, childItem)
                        childItem.childItems[childIndex] = branchItem
                        childIndex += 1
            return childItem
        return None

class DomModel(QAbstractItemModel):
    def __init__(self, document, parent=None):
        super(DomModel, self).__init__(parent)
        self.domDocument = document
        self.rootItem = DomItem(self.domDocument, 0)

    def columnCount(self, parent):
    # return 3
        return 2

    def data(self, index, role):
        if not index.isValid():
            return None
        if role != Qt.DisplayRole:
            return None
        item = index.internalPointer()
        node = item.node()
        if index.column() == 0:
            # print(node.nodeName())
            if node.nodeName() != '#text':
                return node.nodeName()
            else:
                return None
        if index.column() == 1:
            value = node.nodeValue()
            if value is None:
                 return ''
            else:
                return ' '.join(node.nodeValue().split('\n'))
        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return "Category"
            if section == 1:
                return "Name"
        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, child):
        if not child.isValid():
            return QModelIndex()
        childItem = child.internalPointer()
        parentItem = childItem.parent()
        if not parentItem or parentItem == self.rootItem:
            return QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

            return parentItem.node().childNodes().count()

################## About class ##################
class aboutForm(QDialog, about_ui.Ui_AboutForm):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent=parent)
        self.setupUi(self)

################## Config class ##################
class configForm(QDialog, config_ui.Ui_ConfigForm):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent=parent)
        self.setupUi(self)

################## Main class ##################
class mainForm(QMainWindow, main_ui.Ui_mainWindow):
    def __init__(self, parent=None):
        super(mainForm, self).__init__(parent)
        self.setupUi(self)
        self.center()

        self.detectUsb()
        ################## File ##################
        # Config dialog
        self.actionConfigure.setShortcut('Ctrl+,')
        self.actionConfigure.triggered.connect(self.configure_dialog)

        # Save Pixy parameters
        self.actionSave_Pixy_parameters.setShortcut('Ctrl+C')
        self.actionSave_Pixy_parameters.triggered.connect(self.save_pixy_parameters_function)

        # Load Pixy Parameters
        self.actionLoad_Pixy_parameters.setShortcut('Ctrl+X')
        self.actionLoad_Pixy_parameters.triggered.connect(self.load_pixy_parameters_function)

        # Restore default Parameters
        self.actionRestore_default_parameters.setShortcut('Ctrl+Z')
        self.actionRestore_default_parameters.triggered.connect(self.restore_default_parameters_function)

        # Save images
        self.actionSave_Image.setShortcut('Ctrl+S')
        self.actionSave_Image.triggered.connect(self.save_image_function)

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
        self.actionGet_frame.setShortcut('Ctrl+G')
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
        self.form = configForm()
        self.form.show()
        # self.QDialogButtonBox.Cancel.clicked.connect(self.closeWindow)
        print('Your code here for modify color text box|slider and button Apply|Cancel|OK')

    # Save parameters fucntion:
    #   Store all hex color of Red Green Blue values in a text file
    def save_pixy_parameters_function(self):
        self.saveFileDialog()
        print('Your code here process print parameters to a file *.rpm')

    # Load parameters function:
    #   Load a text file which contain all hex color of Red Green Blue values
    #   and show it on camera preview
    def load_pixy_parameters_function(self):
        # self.openFileNameDialog()
        self.getParameterFile()
        print('Your code here process load input parameters to camera and show in video view')

    # Restore default parameters function:
    #   Restore default a text file which contain all hex color of Red Green Blue values
    #   and show it on camera preview
    def restore_default_parameters_function(self):
        print('Your code here process restore default input parameters to camera and show in video view')

    def save_image_function(self):
        print('Your code here process restore default input parameters to camera and show in video view')

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

    def getSaveFileName(self):
        file_filter = 'All Files (*);;PixyMon Files (*.prm)'
        response = QFileDialog.getSaveFileNam(
            parent = self,
            caption = 'Select a data file',
            directory = 'config.prm',
            filter = file_filter,
            initialFilter = ';PixyMon Files (*.prm)'
        )
        print(response)
        return response[0]

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

    ################## Support functions ##################
    def center(self):
        form = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        form.moveCenter(cp)
        self.move(form.topLeft())
        # self.move(form.center())
        # self.move(form.bottomLeft())
        # self.move(form.bottomRight())

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
            data = "Pixy CMU5 camera device is not found..."
            self.plainTextEdit.setPlainText(data)
        else:
            data = "Pixy CMU5 camera device is found!"
            self.plainTextEdit.setPlainText(data)

################## Support Functions ##################
################## Debug function ##################
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
