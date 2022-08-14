#!/usr/bin/python3
# -*- coding: utf-8 -*-


# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

"""
Head       :Camera Application V2020

Description:

Author     : Co Bao Hieu
Id         : M3718007
"""


################## Import Modules ##################
import sys
import os
import cv2
import numpy as np
import numpy.linalg
import PyQt5

################## Modules path ##################
sys.path.append(os.path.join(os.path.dirname(__file__), "./"))
iconDir = os.path.dirname(os.path.realpath(__file__))

from PyQt5 import QtCore as QtCore
from PyQt5 import QtDBus as QtDBus
from PyQt5 import QtGui as QtGui
from PyQt5 import QtWidgets as QtWidgets
from PyQt5 import QtXml as QtXml

################## Import sub modules ##################
from PyQt5.QtCore import (Qt, QSysInfo, QUrl, QMetaType, QSettings, QObject, QDir, QVariant, QIODevice, QThread, QMutex, QWaitCondition, QMutexLocker, QTime, QTimer, QFile, QAbstractItemModel, QModelIndex, QDataStream, QTextStream, pyqtSlot, QSize, QRect, QLocale, QMetaObject, QCoreApplication)
from PyQt5.QtGui import (QIcon, QFont, QImage, QPixmap, QDesktopServices, QColor, QPen, QPainter, QMouseEvent, QKeyEvent, QTextCursor, QTextBlock, QTransform, QPalette, QBrush, QTextFormat, QCloseEvent, QRegion)
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QFileDialog, QInputDialog, QGraphicsRectItem, QGraphicsScene, QMessageBox, QMainWindow, QToolTip, QPushButton, QLineEdit, QDialog, QHBoxLayout, QSlider, QAbstractButton, QCheckBox, QTableWidget, QButtonGroup, QDialogButtonBox, QSpacerItem, QGridLayout, QAction, QHeaderView, QVBoxLayout, QTextBrowser, QSizePolicy, QStyle, QPlainTextEdit, QScrollBar, QTreeView,QAbstractItemDelegate, QAbstractItemView, QHeaderView, QStyleOptionFocusRect, QStyleOption, QStyleOptionFrame, QStyleOptionTabWidgetFrame, QStyleOptionTabBarBase, QStyleOptionHeader, QStyleOptionButton, QStyleOptionProgressBar, QStyleOptionToolBar, QStyleOptionViewItem, QStyleOptionComplex, QStyleOptionSlider, QStyleOptionGraphicsItem, QStyleOptionDockWidget, QStyleOptionSpinBox, QAbstractScrollArea, QStyleOptionGroupBox, QStyleOptionSizeGrip, QStyleOptionComboBox, QStyleOptionTitleBar, QDesktopWidget, QTabWidget, QGroupBox, QMenuBar, QMenu, QComboBox)
from PyQt5.QtXml import (QDomDocument, QDomElement)
from PyQt5.uic import loadUi


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.setWindowModality(Qt.NonModal)
        mainWindow.setEnabled(True)
        mainWindow.resize(525, 475)
        mainWindow.setFocusPolicy(Qt.NoFocus)
        mainWindow.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))

        font = QFont()
        font.setFamily("Umpush")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)

        self.centralwidget = QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        # self.plainTextEdit.setEnabled(True)
        # self.plainTextEdit.setGeometry(QRect(0, 520, 645, 93))
        # self.plainTextEdit.setMaximumSize(QtCore.QSize(16777215, 108))
        # self.plainTextEdit.setSizeIncrement(QtCore.QSize(649, 108))
        # self.plainTextEdit.setFont(font)
        # self.plainTextEdit.setReadOnly(True)
        # self.plainTextEdit.setObjectName("plainTextEdit")

        self.tabConfig = QtWidgets.QTabWidget(self.centralwidget)
        self.tabConfig.setGeometry(QRect(0, 0, 527, 475))
        self.tabConfig.setFont(font)
        self.tabConfig.setObjectName("tabConfig")

        self.imageTab = QWidget()
        self.imageTab.setFont(font)
        self.imageTab.setObjectName("imageTab")

        self.image_grpbx = QGroupBox(self.imageTab)
        self.image_grpbx.setGeometry(QRect(5, -33, 511, 421))
        self.image_grpbx.setObjectName("image_grpbx")

        self.widget = QWidget(self.image_grpbx)
        self.widget.setGeometry(QRect(10, 30, 491, 387))
        # self.widget.setObjectName("widget")

        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.lbl_image_brightness = QLabel(self.image_grpbx)
        # self.lbl_image_brightness.setGeometry(QRect(14, 41, 75, 21))
        self.lbl_image_brightness.setFont(font)
        self.lbl_image_brightness.setObjectName("lbl_image_brightness")
        self.gridLayout.addWidget(self.lbl_image_brightness, 0, 0, 1, 1)

        self.lbl_image_contrast = QLabel(self.image_grpbx)
        # self.lbl_image_contrast.setGeometry(QRect(14, 72, 75, 21))
        self.lbl_image_contrast.setFont(font)
        self.lbl_image_contrast.setObjectName("lbl_image_contrast")
        self.gridLayout.addWidget(self.lbl_image_contrast, 1, 0, 1, 1)

        self.lbl_image_saturation = QLabel(self.image_grpbx)
        # self.lbl_image_saturation.setGeometry(QRect(14, 103, 75, 21))
        self.lbl_image_saturation.setFont(font)
        self.lbl_image_saturation.setObjectName("lbl_image_saturation")
        self.gridLayout.addWidget(self.lbl_image_saturation, 2, 0, 1, 1)

        # self.lbl_image_hue = QLabel(self.image_grpbx)
        # self.lbl_image_hue.setGeometry(QRect(14, 134, 75, 21))
        # self.lbl_image_hue.setFont(font)
        # self.lbl_image_hue.setObjectName("lbl_image_hue")

        self.lbl_image_gain = QLabel(self.image_grpbx)
        # self.lbl_image_gain.setGeometry(QRect(14, 165, 75, 21))
        # self.lbl_image_gain.setGeometry(QRect(14, 134, 75, 21))
        self.lbl_image_gain.setFont(font)
        self.lbl_image_gain.setObjectName("lbl_image_gain")
        self.gridLayout.addWidget(self.lbl_image_gain, 3, 0, 1, 1)

        self.lbl_image_exposure = QLabel(self.image_grpbx)
        # self.lbl_image_exposure.setGeometry(QRect(14, 196, 75, 21))
        # self.lbl_image_exposure.setGeometry(QRect(14, 165, 75, 21))
        self.lbl_image_exposure.setFont(font)
        self.lbl_image_exposure.setObjectName("lbl_image_exposure")
        self.gridLayout.addWidget(self.lbl_image_exposure, 4, 0, 1, 1)

        self.lbl_image_sharpness = QLabel(self.image_grpbx)
        # self.lbl_image_sharpness.setGeometry(QRect(14, 227, 75, 21))
        # self.lbl_image_sharpness.setGeometry(QRect(14, 196, 75, 21))
        self.lbl_image_sharpness.setFont(font)
        self.lbl_image_sharpness.setObjectName("lbl_image_sharpness")
        self.gridLayout.addWidget(self.lbl_image_sharpness, 5, 0, 1, 1)

        # self.lbl_image_temperature = QLabel(self.image_grpbx)
        # # self.lbl_image_temperature.setGeometry(QRect(14, 289, 75, 21))
        # # self.lbl_image_temperature.setGeometry(QRect(14, 227, 75, 21))
        # self.lbl_image_temperature.setFont(font)
        # self.lbl_image_temperature.setObjectName("lbl_image_temperature")
        # self.gridLayout.addWidget(self.lbl_image_temperature, 6, 0, 1, 1)

        self.lbl_image_focus = QLabel(self.image_grpbx)
        # self.lbl_image_focus.setGeometry(QRect(14, 258, 75, 21))
        # self.lbl_image_focus.setGeometry(QRect(14, 258, 75, 21))
        self.lbl_image_focus.setFont(font)
        self.lbl_image_focus.setObjectName("lbl_image_focus")
        self.gridLayout.addWidget(self.lbl_image_focus, 7, 0, 1, 1)

        self.lbl_image_zoom = QLabel(self.image_grpbx)
        # self.lbl_image_zoom.setGeometry(QRect(14, 320, 75, 21))
        # self.lbl_image_zoom.setGeometry(QRect(14, 289, 75, 21))
        self.lbl_image_zoom.setFont(font)
        self.lbl_image_zoom.setObjectName("lbl_image_zoom")
        self.gridLayout.addWidget(self.lbl_image_zoom, 8, 0, 1, 1)

        # self.lbl_image_pan = QLabel(self.image_grpbx)
        # # self.lbl_image_pan.setGeometry(QRect(14, 351, 75, 21))
        # # self.lbl_image_pan.setGeometry(QRect(14, 320, 75, 21))
        # self.lbl_image_pan.setFont(font)
        # self.lbl_image_pan.setObjectName("lbl_image_pan")
        # self.gridLayout.addWidget(self.lbl_image_pan, 9, 0, 1, 1)

        # self.lbl_image_tilt = QLabel(self.image_grpbx)
        # # self.lbl_image_tilt.setGeometry(QRect(14, 382, 75, 21))
        # # self.lbl_image_tilt.setGeometry(QRect(14, 351, 75, 21))
        # self.lbl_image_tilt.setFont(font)
        # self.lbl_image_tilt.setObjectName("lbl_image_tilt")
        # self.gridLayout.addWidget(self.lbl_image_tilt, 10, 0, 1, 1)

        self.horSlider_image_birghtness = QSlider(self.image_grpbx)
        # self.horSlider_image_birghtness.setGeometry(QRect(100, 45, 510, 13))
        self.horSlider_image_birghtness.setMaximum(255)
        self.horSlider_image_birghtness.setOrientation(Qt.Horizontal)
        self.horSlider_image_birghtness.setObjectName("horSlider_image_birghtness")
        self.gridLayout.addWidget(self.horSlider_image_birghtness, 0, 1, 1, 1)

        self.horSlider_image_constrast = QSlider(self.image_grpbx)
        # self.horSlider_image_constrast.setGeometry(QRect(100, 76, 510, 13))
        self.horSlider_image_constrast.setMaximum(255)
        self.horSlider_image_constrast.setOrientation(Qt.Horizontal)
        self.horSlider_image_constrast.setObjectName("horSlider_image_constrast")
        self.gridLayout.addWidget(self.horSlider_image_constrast, 1, 1, 1, 1)

        self.horSlider_image_staturation = QSlider(self.image_grpbx)
        # self.horSlider_image_staturation.setGeometry(QRect(100, 107, 510, 13))
        self.horSlider_image_staturation.setMaximum(255)
        self.horSlider_image_staturation.setOrientation(Qt.Horizontal)
        self.horSlider_image_staturation.setObjectName("horSlider_image_staturation")
        self.gridLayout.addWidget(self.horSlider_image_staturation, 2, 1, 1, 1)

        # self.horSlide_image_hue = QSlider(self.image_grpbx)
        # self.horSlide_image_hue.setGeometry(QRect(100, 138, 510, 13))
        # self.horSlide_image_hue.setMaximum(255)
        # self.horSlide_image_hue.setOrientation(Qt.Horizontal)
        # self.horSlide_image_hue.setObjectName("horSlide_image_hue")

        self.horSlider_image_gain = QSlider(self.image_grpbx)
        # self.horSlider_image_gain.setGeometry(QRect(100, 169, 510, 13))
        # self.horSlider_image_gain.setGeometry(QRect(100, 138, 510, 13))
        self.horSlider_image_gain.setMaximum(255)
        self.horSlider_image_gain.setOrientation(Qt.Horizontal)
        self.horSlider_image_gain.setObjectName("horSlider_image_gain")
        self.gridLayout.addWidget(self.horSlider_image_gain, 3, 1, 1, 1)

        self.horSlider_image_exposure = QSlider(self.image_grpbx)
        # self.horSlider_image_exposure.setGeometry(QRect(100, 200, 510, 13))
        # self.horSlider_image_exposure.setGeometry(QRect(100, 169, 510, 13))
        self.horSlider_image_exposure.setMaximum(255)
        self.horSlider_image_exposure.setOrientation(Qt.Horizontal)
        self.horSlider_image_exposure.setObjectName("horSlider_image_exposure")
        self.gridLayout.addWidget(self.horSlider_image_exposure, 4, 1, 1, 1)

        self.horSlider_image_sharpness = QSlider(self.image_grpbx)
        # self.horSlider_image_sharpness.setGeometry(QRect(100, 231, 510, 13))
        # self.horSlider_image_sharpness.setGeometry(QRect(100, 200, 510, 13))
        self.horSlider_image_sharpness.setMaximum(255)
        self.horSlider_image_sharpness.setOrientation(Qt.Horizontal)
        self.horSlider_image_sharpness.setObjectName("horSlider_image_sharpness")
        self.gridLayout.addWidget(self.horSlider_image_sharpness, 5, 1, 1, 1)

        # self.horSlider_image_temperature = QSlider(self.image_grpbx)
        # # self.horSlider_image_temperature.setGeometry(QRect(100, 293, 510, 13))
        # # self.horSlider_image_temperature.setGeometry(QRect(100, 231, 510, 13))
        # self.horSlider_image_temperature.setMaximum(255)
        # self.horSlider_image_temperature.setOrientation(Qt.Horizontal)
        # self.horSlider_image_temperature.setObjectName("horSlider_image_temperature")
        # self.gridLayout.addWidget(self.horSlider_image_temperature, 6, 1, 1, 1)

        self.horSlider_image_focus = QSlider(self.image_grpbx)
        # self.horSlider_image_focus.setGeometry(QRect(100, 262, 510, 13))
        # self.horSlider_image_focus.setGeometry(QRect(100, 262, 510, 13))
        self.horSlider_image_focus.setMaximum(255)
        self.horSlider_image_focus.setOrientation(Qt.Horizontal)
        self.horSlider_image_focus.setObjectName("horSlider_image_gamma")
        self.gridLayout.addWidget(self.horSlider_image_focus, 7, 1, 1, 1)

        self.horSlider_image_zoom = QSlider(self.image_grpbx)
        # self.horSlider_image_zoom.setGeometry(QRect(100, 324, 510, 13))
        # self.horSlider_image_zoom.setGeometry(QRect(100, 293, 510, 13))
        self.horSlider_image_zoom.setMaximum(255)
        self.horSlider_image_zoom.setOrientation(Qt.Horizontal)
        self.horSlider_image_zoom.setObjectName("horSlider_image_zoom")
        self.gridLayout.addWidget(self.horSlider_image_zoom, 8, 1, 1, 1)

        # self.horSlider_image_pan = QSlider(self.image_grpbx)
        # # self.horSlider_image_pan.setGeometry(QRect(100, 355, 510, 13))
        # # self.horSlider_image_pan.setGeometry(QRect(100, 324, 510, 13))
        # self.horSlider_image_pan.setMaximum(255)
        # self.horSlider_image_pan.setOrientation(Qt.Horizontal)
        # self.horSlider_image_pan.setObjectName("horSlider_image_pan")
        # self.gridLayout.addWidget(self.horSlider_image_pan, 9, 1, 1, 1)

        # self.horSlider_image_tilt = QSlider(self.image_grpbx)
        # # self.horSlider_image_tilt.setGeometry(QRect(100, 386, 510, 13))
        # # self.horSlider_image_tilt.setGeometry(QRect(100, 355, 510, 13))
        # self.horSlider_image_tilt.setMaximum(255)
        # self.horSlider_image_tilt.setOrientation(Qt.Horizontal)
        # self.horSlider_image_tilt.setObjectName("horSlider_image_tilt")
        # self.gridLayout.addWidget(self.horSlider_image_tilt, 10, 1, 1, 1)

        self.ckb_image_mirror = QCheckBox(self.image_grpbx)
        # self.ckb_image_mirror.setGeometry(QRect(15, 413, 77, 20))
        # self.ckb_image_mirror.setGeometry(QRect(15, 386, 77, 20))
        self.ckb_image_mirror.setFont(font)
        self.ckb_image_mirror.setObjectName("ckb_image_mirror")
        self.gridLayout.addWidget(self.ckb_image_mirror, 11, 0, 1, 1)

        self.ckb_image_rotateup = QCheckBox(self.image_grpbx)
        # self.ckb_image_rotateup.setGeometry(QRect(15, 444, 113, 20))
        # self.ckb_image_rotateup.setGeometry(QRect(15, 417, 113, 20))
        self.ckb_image_rotateup.setFont(font)
        self.ckb_image_rotateup.setObjectName("ckb_image_rotateup")
        self.gridLayout.addWidget(self.ckb_image_rotateup, 11, 1, 1, 1)

        self.tabConfig.addTab(self.imageTab, "")
        self.videoTab = QWidget()
        self.videoTab.setObjectName("videoTab")

        self.video_grpbx = QGroupBox(self.videoTab)
        self.video_grpbx.setGeometry(QRect(5, -33, 511, 421))
        self.video_grpbx.setObjectName("video_grpbx")

        self.widget1 = QWidget(self.video_grpbx)
        self.widget1.setGeometry(QRect(10, 30, 83, 187))
        # self.widget1.setObjectName("widget1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget1)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.ckb_video_mirror = QCheckBox(self.video_grpbx)
        # self.ckb_video_mirror.setGeometry(QRect(15, 45, 77, 20))
        self.ckb_video_mirror.setFont(font)
        self.ckb_video_mirror.setObjectName("ckb_video_mirror")
        self.gridLayout_2.addWidget(self.ckb_video_mirror, 0, 0, 1, 1)

        self.ckb_video_rotateup = QCheckBox(self.video_grpbx)
        # self.ckb_video_rotateup.setGeometry(QRect(15, 76, 113, 20))
        self.ckb_video_rotateup.setFont(font)
        self.ckb_video_rotateup.setObjectName("ckb_video_rotateup")
        self.gridLayout_2.addWidget(self.ckb_video_rotateup, 3, 0, 1, 1)

        self.ckb_video_blur = QCheckBox(self.video_grpbx)
        # self.ckb_video_blur.setGeometry(QRect(15, 107, 113, 20))
        self.ckb_video_blur.setFont(font)
        self.ckb_video_blur.setObjectName("ckb_video_blur")
        self.gridLayout_2.addWidget(self.ckb_video_blur, 2, 0, 1, 1)

        self.ckb_video_invert = QCheckBox(self.video_grpbx)
        # self.ckb_video_invert.setGeometry(QRect(15, 138, 113, 20))
        self.ckb_video_invert.setFont(font)
        self.ckb_video_invert.setObjectName("ckb_video_invert")
        self.gridLayout_2.addWidget(self.ckb_video_invert, 1, 0, 1, 1)

        self.ckb_video_mono = QCheckBox(self.video_grpbx)
        # self.ckb_video_mono.setGeometry(QRect(15, 169, 113, 20))
        self.ckb_video_mono.setFont(font)
        self.ckb_video_mono.setObjectName("ckb_video_mono")
        self.gridLayout_2.addWidget(self.ckb_video_mono, 4, 0, 1, 1)

        self.cbb_video_framerate = QComboBox(self.video_grpbx)
        # self.cbb_video_framerate.setGeometry(QRect(15, 200, 131, 22))
        self.cbb_video_framerate.setGeometry(QRect(10, 230, 141, 22))
        self.cbb_video_framerate.setFont(font)
        self.cbb_video_framerate.setCurrentText("")
        self.cbb_video_framerate.setObjectName("cbb_video_framerate")

        self.cbb_video_resolution = QComboBox(self.video_grpbx)
        # self.cbb_video_resolution.setGeometry(QRect(300, 200, 131, 22))
        self.cbb_video_resolution.setGeometry(QRect(225, 230, 141, 22))
        self.cbb_video_resolution.setFont(font)
        self.cbb_video_resolution.setObjectName("cbb_video_resolution")

        self.tabConfig.addTab(self.videoTab, "")
        self.logTab = QWidget()
        self.logTab.setObjectName("logTab")

        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.logTab)
        self.plainTextEdit.setGeometry(QRect(0, 0, 521, 390))
        self.plainTextEdit.setObjectName("plainTextEdit")

        # self.imgLabel = QLabel(self.logTab)
        # self.imgLabel.setGeometry(QRect(0, 0, 640, 480))
        # self.imgLabel.setSizeIncrement(QtCore.QSize(0, 0))
        # self.imgLabel.setFrameShape(QtWidgets.QFrame.Box)
        # self.imgLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.imgLabel.setLineWidth(1)
        # self.imgLabel.setText("")
        # self.imgLabel.setTextFormat(Qt.AutoText)
        # self.imgLabel.setObjectName("imgLabel")

        self.tabConfig.addTab(self.logTab, "")
        mainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(mainWindow)
        self.menuBar.setGeometry(QRect(0, 0, 525, 32))
        self.menuBar.setFont(font)
        self.menuBar.setObjectName("menuBar")

        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")

        self.menuAction = QMenu(self.menuBar)
        self.menuAction.setObjectName("menuAction")

        self.menuHelp = QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")

        mainWindow.setMenuBar(self.menuBar)

        self.actionHelp = QAction(mainWindow)
        self.actionHelp.setFont(font)
        self.actionHelp.setObjectName("actionHelp")

        self.actionAbout = QAction(mainWindow)
        self.actionAbout.setFont(font)
        self.actionAbout.setObjectName("actionAbout")

        # self.actionRun_Stop = QAction(mainWindow)
        # self.actionRun_Stop.setFont(font)
        # self.actionRun_Stop.setObjectName("actionRun_Stop")

        self.actionSave_profile = QAction(mainWindow)
        self.actionSave_profile.setFont(font)
        self.actionSave_profile.setObjectName("actionSave_profile")

        self.actionConfigure = QAction(mainWindow)
        self.actionConfigure.setFont(font)
        self.actionConfigure.setObjectName("actionConfigure")

        self.actionLoad_profile = QAction(mainWindow)
        self.actionLoad_profile.setFont(font)
        self.actionLoad_profile.setObjectName("actionLoad_profile")

        self.actionExit = QAction(mainWindow)
        self.actionExit.setFont(font)
        self.actionExit.setObjectName("actionExit")

        self.actionRestore_default_profile = QAction(mainWindow)
        self.actionRestore_default_profile.setFont(font)
        self.actionRestore_default_profile.setObjectName("actionRestore_default_profile")

        self.actionTake_Photo = QAction(mainWindow)
        self.actionTake_Photo.setFont(font)
        self.actionTake_Photo.setObjectName("actionTake_Photo")

        self.actionRecord_Video = QAction(mainWindow)
        self.actionRecord_Video.setFont(font)
        self.actionRecord_Video.setObjectName("actionRecord_Video")

        self.actionDetect_Color = QAction(mainWindow)
        self.actionDetect_Color.setFont(font)
        self.actionDetect_Color.setObjectName("actionDetect_Color")

        self.actionDetect_Face = QAction(mainWindow)
        self.actionDetect_Face.setFont(font)
        self.actionDetect_Face.setObjectName("actionDetect_Face")

        self.actionDetect_Mask = QAction(mainWindow)
        self.actionDetect_Mask.setFont(font)
        self.actionDetect_Mask.setObjectName("actionDetect_Mask")

        self.actionDetect_Vegetables = QAction(mainWindow)
        self.actionDetect_Vegetables.setFont(font)
        self.actionDetect_Vegetables.setObjectName("actionDetect_Vegetables")

        self.actionScan_Code = QAction(mainWindow)
        self.actionScan_Code.setFont(font)
        self.actionScan_Code.setObjectName("actionScan_Code")

        # self.menuFile.addSeparator()
        # self.menuFile.addSeparator()
        # self.menuFile.addSeparator()

        # Save Camera profiles
        self.menuFile.addAction(self.actionSave_profile)

        # Load Camera Parameters
        self.menuFile.addAction(self.actionLoad_profile)

        # Restore default Parameters
        self.menuFile.addAction(self.actionRestore_default_profile)

        # Exit
        self.menuFile.addAction(self.actionExit)

        ##### Action
        # Start/Stop
        # self.menuAction.addAction(self.actionRun_Stop)

        # Take photo
        self.menuAction.addAction(self.actionTake_Photo)

        # Record Video
        self.menuAction.addAction(self.actionRecord_Video)

        # Detect Color
        self.menuAction.addAction(self.actionDetect_Color)

        # Detect Face
        self.menuAction.addAction(self.actionDetect_Face)

        # Detect Object
        self.menuAction.addAction(self.actionDetect_Mask)

        # Detect Vegetables
        self.menuAction.addAction(self.actionDetect_Vegetables)

        # Scan code
        self.menuAction.addAction(self.actionScan_Code)

        # self.menuHelp.addSeparator()
        # self.menuHelp.addSeparator()

        ##### Help
        # Help dialog
        self.menuHelp.addAction(self.actionHelp)

        # About dialog
        self.menuHelp.addAction(self.actionAbout)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuAction.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(mainWindow)
        self.tabConfig.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Camera Control (2020)"))

        ######################### MENU #########################
        self.menuFile.setTitle(_translate("mainWindow", "File"))
        self.actionSave_profile.setText(_translate("mainWindow", "Save profile"))
        self.actionLoad_profile.setText(_translate("mainWindow", "Load profile"))
        self.actionRestore_default_profile.setText(_translate("mainWindow", "Restore default profile"))
        self.actionExit.setText(_translate("mainWindow", "Exit"))
        
        self.menuAction.setTitle(_translate("mainWindow", "Action"))
        # self.actionRun_Stop.setText(_translate("mainWindow", "Start/Stop"))
        self.actionTake_Photo.setText(_translate("mainWindow", "Take Photo"))
        self.actionRecord_Video.setText(_translate("mainWindow", "Record Video"))
        self.actionDetect_Color.setText(_translate("mainWindow", "Detect Color "))
        self.actionDetect_Face.setText(_translate("mainWindow", "Detect and Recognize Face"))
        self.actionDetect_Mask.setText(_translate("mainWindow", "Detect Mask/No Mask"))
        self.actionDetect_Vegetables.setText(_translate("mainWindow", "Detect Vegetables"))
        self.actionScan_Code.setText(_translate("mainWindow", "Scan QR/Barcode"))
        self.actionConfigure.setText(_translate("mainWindow", "Configure"))
        
        self.menuHelp.setTitle(_translate("mainWindow", "Help"))
        self.actionHelp.setText(_translate("mainWindow", "Help"))
        self.actionAbout.setText(_translate("mainWindow", "About"))

        ######################### TAB #########################
        self.tabConfig.setTabText(self.tabConfig.indexOf(self.imageTab), _translate("mainWindow", "Photo setting"))
        # self.image_grpbx.setTitle(_translate("mainWindow", " "))
        self.lbl_image_brightness.setText(_translate("mainWindow", "Brightness"))
        self.lbl_image_contrast.setText(_translate("mainWindow", "Contrast"))
        self.lbl_image_saturation.setText(_translate("mainWindow", "Saturation"))
        self.lbl_image_gain.setText(_translate("mainWindow", "Gain"))
        self.lbl_image_exposure.setText(_translate("mainWindow", "Exposure"))
        self.lbl_image_sharpness.setText(_translate("mainWindow", "Sharpness"))
        # self.lbl_image_temperature.setText(_translate("mainWindow", "Temperature"))
        self.lbl_image_focus.setText(_translate("mainWindow", "Focus"))
        self.lbl_image_zoom.setText(_translate("mainWindow", "Zoom"))
        # self.lbl_image_pan.setText(_translate("mainWindow", "Pan"))
        # self.lbl_image_tilt.setText(_translate("mainWindow", "Tilt"))
        self.ckb_image_mirror.setText(_translate("mainWindow", "Mirror"))
        self.ckb_image_rotateup.setText(_translate("mainWindow", "Rotate up"))
        
        self.tabConfig.setTabText(self.tabConfig.indexOf(self.videoTab), _translate("mainWindow", "Video setting"))
        # self.video_grpbx.setTitle(_translate("mainWindow", " "))
        self.ckb_video_mirror.setText(_translate("mainWindow", "Mirror"))
        self.ckb_video_invert.setText(_translate("mainWindow", "Invert"))
        self.ckb_video_blur.setText(_translate("mainWindow", "Blur"))
        self.ckb_video_rotateup.setText(_translate("mainWindow", "Rotate up"))
        self.ckb_video_mono.setText(_translate("mainWindow", "Mono"))

        self.tabConfig.setTabText(self.tabConfig.indexOf(self.logTab), _translate("mainWindow", "Logs"))

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())

################## Fin ##################
