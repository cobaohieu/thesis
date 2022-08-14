#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Head       :Camera Application V2020

Description:

Author     : Co Bao Hieu
Id         : M3718007
"""

################## Import Modules ##################
import sys
import os
import datetime
import time

# os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['OPENCV_VIDEOIO_PRIORITY_MSMF'] = '0'

import cv2
import imutils
import numpy as np
import numpy.linalg
import PyQt5
import pyshine as ps

################## Modules path ##################
sys.path.append(os.path.join(os.path.dirname(__file__), "./"))
iconDir = os.path.dirname(os.path.realpath(__file__))

import PyQt5.QtCore as QtCore
import PyQt5.QtDBus as QtDBus
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtXml as QtXml

import main_ui
# import start_camera
import detect_mask_nomask
import detect_vegetable
import face_recognition_detector_with_hog
import take_photo
import filter
import detect_colors
# import detect_face_with_mask
# import detect_object
# import get_fps
import takephoto_v2
import record_video
import multiple_threading_fps
import multiple_threading_opencv_v2
import simple_camera
import detect_qr_code
import process_xml
import usb_detect

################## Import sub modules ##################
from time import gmtime, strftime
from datetime import datetime
from math import radians, degrees, cos, sin, tan
from PIL import Image
from imutils.video import VideoStream
from screeninfo import get_monitors
from threading import Thread

from collections import OrderedDict
from collections import deque
from multiprocessing.pool import ThreadPool

from PyQt5.QtCore import (pyqtSignal, Qt, QSysInfo, QUrl, QMetaType, QSettings, QObject, QDir, QVariant, QIODevice, QThread, QMutex, QWaitCondition, QMutexLocker, QTime, QTimer, QFile, QAbstractItemModel, QModelIndex, QDataStream, QTextStream, pyqtSlot, QSize, QRect, QLocale, QMetaObject, QCoreApplication)
from PyQt5.QtGui import (QIcon, QFont, QImage, QPixmap, QDesktopServices, QColor, QPen, QPainter, QMouseEvent, QKeyEvent, QTextCursor, QTextBlock, QTransform, QPalette, QBrush, QTextFormat, QCloseEvent)
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QFileDialog, QInputDialog, QGraphicsRectItem, QGraphicsScene, QMessageBox, QMainWindow, QToolTip, QPushButton, QLineEdit, QDialog, QHBoxLayout, QSlider, QAbstractButton, QCheckBox, QTableWidget, QButtonGroup, QDialogButtonBox, QSpacerItem, QGridLayout, QAction, QHeaderView, QVBoxLayout, QTextBrowser, QSizePolicy, QStyle, QPlainTextEdit, QScrollBar, QTreeView,QAbstractItemDelegate, QAbstractItemView, QHeaderView, QStyleOptionFocusRect, QStyleOption, QStyleOptionFrame, QStyleOptionTabWidgetFrame, QStyleOptionTabBarBase, QStyleOptionHeader, QStyleOptionButton, QStyleOptionProgressBar, QStyleOptionToolBar, QStyleOptionViewItem, QStyleOptionComplex, QStyleOptionSlider, QStyleOptionGraphicsItem, QStyleOptionDockWidget, QStyleOptionSpinBox, QAbstractScrollArea, QStyleOptionGroupBox, QStyleOptionSizeGrip, QStyleOptionComboBox, QStyleOptionTitleBar, QDesktopWidget, QTabWidget, QGroupBox, QMenuBar, QMenu, QComboBox)
from PyQt5.QtXml import (QDomDocument, QDomElement)
from PyQt5.uic import loadUi

# from usb_detect import detectUsb
# from process_xml import saveFinalParameters
# from record_video import record
# from take_photo import capture

global stream
global camera_number 

# stream = None
camera_number = -1
device = ['device', '/dev/video0']
device_source = 0
height = 720
width = 1280
stream = cv2.VideoCapture(0, cv2.CAP_V4L2)# cv2.VideoCapture(0)
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

################## FPS Calculator ##################
class FpsCalculator(object):
    def __init__(self, buffer_len = 1):
        self._start_tick = cv2.getTickCount()
        self._freq = 1000.0 / cv2.getTickFrequency()
        self._difftimes = deque(maxlen = buffer_len)

    def get(self):
        current_tick = cv2.getTickCount()
        different_time = (current_tick - self._start_tick) * self._freq
        self._start_tick = current_tick

        self._difftimes.append(different_time)

        fps = 1000.0 / (sum(self._difftimes) / len(self._difftimes))
        fps_rounded = round(fps, 3)

        return fps_rounded

################## Camera clas ##################

################## Main class ##################
class mainForm(QMainWindow, main_ui.Ui_mainWindow):
    def __init__(self, parent=None):
        super(mainForm, self).__init__(parent)
        self.setupUi(self)
        self.center()
        self.logic = 0
        self.value = 1
        self.timer = QTimer()
        self.stopped = False
        self.image = None
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        # self.timer.timeout.connect(self.nextFrameSlot)
        self.timeInfo = "Now is: " +  strftime("%d-%m-%Y %H:%M:%S", gmtime())
        # self.plainTextEdit.setPlainText(str(timeInfo))
        print('[INFO    ]: ', str(self.timeInfo))

        self.filename = '/home/administrator/Pictures/C922/IMG_'+str(time.strftime("%Y-%b-%d at %H.%M.%S %p"))+'.png'
        # Will hold the temporary image for display
        self.temp = None
        self.brightness_value_now = 0 # Updated brightness value
        self.blur_value_now = 0 # Updated blur value
        self.fps = 0
        self.started = False

        self.detect_usb()
        # self.setRange(-100, 100)
        # self.setSingleStep(10)
        # self.setPageStep(10)

        ################## Image Tab ##################
        # Horizontal Slider
        self.horSlider_image_birghtness.valueChanged.connect(self.control_brightness)
        # self.horSlider_image_birghtness.valueChanged['int'].connect(self.brightness_value)
        self.horSlider_image_birghtness.setRange(0, 255)
        self.horSlider_image_birghtness.setPageStep(1)
        self.horSlider_image_birghtness.setValue(128)

        self.horSlider_image_constrast.valueChanged.connect(self.control_contrast)
        self.horSlider_image_constrast.setRange(0, 255)
        self.horSlider_image_constrast.setPageStep(1)
        self.horSlider_image_constrast.setValue(128)

        self.horSlider_image_staturation.valueChanged.connect(self.control_staturation)
        self.horSlider_image_staturation.setRange(0, 255)
        self.horSlider_image_staturation.setPageStep(1)
        self.horSlider_image_staturation.setValue(128)

        # self.horSlide_image_hue.valueChanged.connect(self.control_hue)

        self.horSlider_image_gain.valueChanged.connect(self.control_gain)
        self.horSlider_image_gain.setRange(0, 255)
        self.horSlider_image_gain.setPageStep(1)
        self.horSlider_image_gain.setValue(25)

        self.horSlider_image_exposure.valueChanged.connect(self.control_exposure)
        self.horSlider_image_exposure.setRange(3, 2047)
        self.horSlider_image_exposure.setPageStep(1)
        self.horSlider_image_exposure.setValue(500)

        self.horSlider_image_sharpness.valueChanged.connect(self.control_sharpness)
        # self.horSlider_image_sharpness.valueChanged['int'].connect(self.blur_value)
        self.horSlider_image_sharpness.setRange(0, 255)
        self.horSlider_image_sharpness.setPageStep(1)
        self.horSlider_image_sharpness.setValue(128)

        # self.horSlider_image_temperature.valueChanged.connect(self.control_temperature)
        # self.horSlider_image_temperature.setRange(2000, 6500)
        # self.horSlider_image_temperature.setPageStep(1)
        # self.horSlider_image_temperature.setValue(3500)

        self.horSlider_image_focus.valueChanged.connect(self.control_gamma)
        self.horSlider_image_focus.setRange(0, 250)
        self.horSlider_image_focus.setPageStep(1)
        self.horSlider_image_focus.setValue(0)

        self.horSlider_image_zoom.valueChanged.connect(self.control_zoom)
        self.horSlider_image_zoom.setRange(100, 500)
        self.horSlider_image_zoom.setPageStep(1)
        self.horSlider_image_zoom.setValue(0)

        # self.horSlider_image_pan.valueChanged.connect(self.control_pan)
        # self.horSlider_image_pan.setRange(-3600, 3600)
        # self.horSlider_image_pan.setPageStep(10)
        # self.horSlider_image_pan.setValue(0)

        # self.horSlider_image_tilt.valueChanged.connect(self.control_tilt)
        # self.horSlider_image_tilt.setRange(-3600, 3600)
        # self.horSlider_image_tilt.setPageStep(10)
        # self.horSlider_image_tilt.setValue(0)

        # Checkbox
        self.ckb_image_mirror.stateChanged.connect(self.state_mirror_changed)
        self.ckb_image_rotateup.stateChanged.connect(self.state_rotate_up_changed)


        ################## Video Tab ##################
        # Checkbox
        # self.ckb_video_mirror.stateChanged.connect(self.state_mirror_changed)
        # self.ckb_video_rotateup.stateChanged.connect(self.state_rotate_up_changed)
        # self.ckb_video_blur.stateChanged.connect(self.state_blur_changed)
        self.ckb_video_invert.stateChanged.connect(self.state_invert_changed)
        self.ckb_video_mono.stateChanged.connect(self.state_mono_changed)

        # Combo box
        # self.cbb_video_framerate.addItems('5FPS 10FPS 15FPS 20FPS 24FPS 30FPS 50FPS 60FPS 120FPS 240FPS 360FPS 480FPS'.split())
        fps_list = ["5 FPS" ,"7.5 FPS", "10 FPS", "15 FPS", "20 FPS", "24 FPS", "30 FPS", "50 FPS", "60 FPS"] #, "120FPS", "240FPS", "360FPS", "480FPS"]
        self.cbb_video_framerate.addItems(fps_list)
        self.cbb_video_framerate.setCurrentIndex(3)
        # self.cbb_video_framerate.activated.connect(self.change_fps())

        # self.cbb_video_resolution.addItems('1920x1080 1600x896 1280x720 1024x576 960x720 864x480 800x600 800x448 640x360 352x288 320x240 320x180 176x144 160x120 160x90'.split())
        resolution_list = ["1920x1080", "1600x896", "1280x720", "1024x576", "960x720", "960x540", "864x480", "800x600", "800x448", "640x480", "640x360", "432x240", "352x288", "320x240", "320x180", "176x144", "160x120", "160x90"]
        self.cbb_video_resolution.addItems(resolution_list)
        self.cbb_video_resolution.setCurrentIndex(9)
        # self.cbb_video_resolution.activated.connect(self.change_res())

        ################## File ##################
        # Save Camera profiles
        self.actionSave_profile.setShortcut('Ctrl+S')
        self.actionSave_profile.triggered.connect(self.save_profile_function)

        # Load Camera Parameters
        self.actionLoad_profile.setShortcut('Ctrl+L')
        self.actionLoad_profile.triggered.connect(self.load_profile_function)

        # Restore default Parameters
        self.actionRestore_default_profile.setShortcut('Ctrl+D')
        self.actionRestore_default_profile.triggered.connect(self.restore_default_profile_function)

        # Exit
        self.actionExit.setShortcut('Ctrl+W')
        self.actionExit.triggered.connect(self.exit)

        ################## Action ##################
        # Start/Stop
        # self.btn_start_stop.setShortcut('Space')
        # self.btn_start_stop.clicked.connect(self.loadImage)
        # self._actionRun_Stop_counter = 0

        # Take Photo
        self.btn_take_photo.setShortcut('Ctrl+T')
        self.btn_take_photo.clicked.connect(self.take_photo)
        # self.btn_take_photo.clicked.connect(self.savePhoto)

        # Record videos
        self.btn_record_video.setShortcut('Ctrl+R')
        self.btn_record_video.clicked.connect(self.record_video)

        # Detect Color
        self.actionColor.setShortcut('Ctrl+C')
        self.actionColor.triggered.connect(self.detect_color_function)

        # Detect Mask
        self.actionMask_No_Mask.setShortcut('Ctrl+O')
        self.actionMask_No_Mask.triggered.connect(self.detect_mask_no_mask_function)

        # Detect Vegetables
        self.actionVegetables.setShortcut('Ctrl+V')
        self.actionVegetables.triggered.connect(self.detect_vegetables_function)

        # Detect code
        self.actionQR_Code.setShortcut('Ctrl+Q')
        self.actionQR_Code.triggered.connect(self._detect_qr_code_function)

        # Detect Face
        self.actionFrontalFace.setShortcut('Ctrl+F')
        self.actionFrontalFace.triggered.connect(self.recognize_face_function)

        # Increase FPS
        self.actionFPS.setShortcut('Ctrl+G')
        self.actionFPS.triggered.connect(self.increase_fps)

        ################## Help ##################        
        # Help dialog
        self.actionWiki.setShortcut('F1')
        self.actionWiki.triggered.connect(self.help_wiki_dialog)
        
        # About dialog
        self.actionAbout.setShortcut('F12')
        self.actionAbout.triggered.connect(self.help_about_dialog)


################## Process Function ##################	
    # def loadImage(self):
    #     """ This function will load the camera device, obtain the image
    #         and set it to label using the setPhoto function
    #     """
    #     if self.started:
    #         self.started = False
    #         self.btn_start_stop.setText('Start camera')	
    #     else:
    #         self.starte = True
    #         self.btn_start_stop.setText('Stop camera')
        
    #     cam = True # True for webcam
    #     if cam:
    #         stream = cv2.VideoCapture(0) #, cv2.CAP_V4L2)
    #     # else:
    #     # 	stream = cv2.VideoCapture('video.mp4')
		
    #     cnt = 0
    #     frames_to_count = 20
    #     st = 0
    #     fps = 0
        
    #     while(stream.isOpened()):
            
    #         frame, self.image = stream.read()
    #         self.image  = imutils.resize(self.image, height = 480)
            
    #         gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY) 
    #         faces = faceCascade.detectMultiScale(
    #         gray,
    #         scaleFactor = 1.15,  
    #         minNeighbors = 7, 
    #         minSize = (80, 80), 
    #         flags = cv2.CASCADE_SCALE_IMAGE)
            
    #         for (x, y, w, h) in faces:
    #             cv2.rectangle(self.image, (x, y), (x + w, y + h), (10, 228, 220), 5)
                
    #         if cnt == frames_to_count:
    #             try: # To avoid divide by 0 we put it in try except
    #                 print(frames_to_count/(time.time()-st),'FPS')
    #                 self.fps = round(frames_to_count/(time.time()-st)) 
					
    #                 st = time.time()
    #                 cnt = 0
    #             except:
    #                 pass
			
    #         cnt += 1
            
    #         self.update()
    #         key = cv2.waitKey(1) & 0xFF
    #         if self.started == False:
    #             break
    #             print('Loop break')

    #@pyqtSlot()
    # def setPhoto(self, image):
    #     """ This function will take image input and resize it 
    #         only for display purpose and convert it to QImage
    #         to set at the label.
    #     """
    #     self.temp = image
    #     image = imutils.resize(image, width=640)
    #     frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #     image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
    #     self.label.setPixmap(QtGui.QPixmap.fromImage(image))

    #@pyqtSlot()
    # def brightness_value(self, value):
    #     """ This function will take value from the slider
    #         for the brightness from 0 to 99
    #     """
    #     self.brightness_value_now = value
    #     print('Brightness: ', value)
    #     self.update()

    #@pyqtSlot()
    # def blur_value(self, value):
    #     """ This function will take value from the slider 
    #         for the blur from 0 to 99 """
    #     self.blur_value_now = value
    #     print('Blur: ', value)
    #     self.update()
    
    #@pyqtSlot()
    # def control_brightness(self, frame, value):
    #     """ This function will take an image (frame) and the brightness
    #         value. It will perform the brightness change using OpenCv
    #         and after split, will merge the frame and return it.
    #     """
    #     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #     h,s,v = cv2.split(hsv)
    #     lim = 255 - value
    #     v[v>lim] = 255
    #     v[v<=lim] += value
    #     final_hsv = cv2.merge(h, s, v)
    #     frame = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    #     return frame
        
    #@pyqtSlot()
    # def control_blur(self, frame, value):
    #     """ This function will take the frame image and blur values as inputs.
    #         After perform blur operation using opencv function, it returns 
    #         the image frame.
    #     """
    #     kernel_size = (value+1, value+1) # +1 is to avoid 0
    #     frame = cv2.blur(frame, kernel_size)
    #     return frame

    #@pyqtSlot()
    def choose_resolution(self):
        print('')

    def choose_fps(self):
        print('')

    #@pyqtSlot()
    def control_brightness(self):
        print('')

    #@pyqtSlot()
    def control_contrast(self):
        print('')

    #@pyqtSlot()
    def control_staturation(self):
        print('')

    #@pyqtSlot()
    def control_hue(self):
        print('')

    #@pyqtSlot()
    def control_gain(self):
        print('')

    #@pyqtSlot()
    def control_exposure(self):
        print('')

    #@pyqtSlot()
    def control_sharpness(self):
        print('')

    #@pyqtSlot()
    def control_gamma(self):
        print('')

    #@pyqtSlot()
    def control_temperature(self):
        print('')

    #@pyqtSlot()
    def control_zoom(self):
        print('')

    #@pyqtSlot()
    def control_pan(self):
        print('')

    #@pyqtSlot()
    def control_tilt(self):
        print('')

    #@pyqtSlot()
    def control_blur(self):
        print('')

    def turn_on_mirror(self):
        print('')

    def turn_on_rotate_up(self):
        print('')

    def turn_on_mono(self):
        print('')

    def turn_on_invert(self):
        print('')


    #@pyqtSlot()
    # def update(self):
    #     """ This function will update the photo according to the 
    #         current values of blur and brightness and set it to photo label.
    #     """
    #     frame = self.control_brightness(self.image, self.brightness_value_now)
    #     frame = self.control_blur(frame, self.blur_value_now)

	# 	# Here we add display text to the image
    #     text  =  'FPS: '+str(self.fps)
    #     frame = ps.putBText(frame,text,text_offset_x=20,text_offset_y=30,vspace=20,hspace=10, font_scale=1.0,background_RGB=(10,20,222),text_RGB=(255,255,255))
    #     text = str(time.strftime("%H:%M %p"))
    #     frame = ps.putBText(frame,text,text_offset_x=self.image.shape[1]-180,text_offset_y=30,vspace=20,hspace=10, font_scale=1.0,background_RGB=(228,20,222),text_RGB=(255,255,255))
    #     text  =  f"Brightness: {self.brightness_value_now}"
    #     frame = ps.putBText(frame,text,text_offset_x=80,text_offset_y=425,vspace=20,hspace=10, font_scale=1.0,background_RGB=(20,210,4),text_RGB=(255,255,255))
    #     text  =  f'Blur: {self.blur_value_now}: '
    #     frame = ps.putBText(frame,text,text_offset_x=self.image.shape[1]-200,text_offset_y=425,vspace=20,hspace=10, font_scale=1.0,background_RGB=(210,20,4),text_RGB=(255,255,255))

    #     self.setPhoto(frame)

    # #@pyqtSlot()
    # def savePhoto(self):
    #     """ This function will save the image"""
	# 	# self.filename = 'Snapshot '+ str(time.strftime("%Y-%b-%d at %H.%M.%S %p"))+ '.png'
    #     self.filename = '/home/administrator/Pictures/C922/IMG_'+str(time.strftime("%Y-%b-%d at %H.%M.%S %p"))+'.png'
    #     cv2.imwrite(self.filename, self.temp)
    #     print('Image saved as:', self.filename)


    #@pyqtSlot()
    # def state_blur_changed(self):
        # if self.ckb_video_blur.isChecked():
        #     print("CHECKED!")
        #     self.ckb_video_invert.setChecked(False)
        #     # self.ckb_video_mirror.setChecked(False)
        #     self.ckb_video_mono.setChecked(False)
        #     # self.ckb_video_rotateup.setChecked(False)
        #     self.ckb_image_mirror.setChecked(False)
        #     self.ckb_image_rotateup.setChecked(False)
        #     # self.clear_camera(stream)
        #     self.clear_camera(stream)
        #     filter.blur(stream)
        # else:
        #     print("UNCHECKED!")

    #@pyqtSlot()
    def state_invert_changed(self):
        if self.ckb_video_invert.isChecked():
            print("CHECKED!")
            # self.ckb_video_blur.setChecked(False)
            # self.ckb_video_mirror.setChecked(False)
            self.ckb_video_mono.setChecked(False)
            # self.ckb_video_rotateup.setChecked(False)
            self.ckb_image_mirror.setChecked(False)
            self.ckb_image_rotateup.setChecked(False)
            # self.clear_camera(stream)
            self.clear_camera(stream)
            filter.invert(stream)
        else:
            print("UNCHECKED!")

    #@pyqtSlot()
    def state_mirror_changed(self):
        if self.ckb_image_mirror.isChecked():
            print("CHECKED!")
            # self.ckb_video_blur.setChecked(False)
            self.ckb_video_invert.setChecked(False)
            # self.ckb_video_mirror.setChecked(False)
            self.ckb_video_mono.setChecked(False)
            # self.ckb_video_rotateup.setChecked(False)
            self.ckb_image_rotateup.setChecked(False)
            # self.clear_camera(stream)
            self.clear_camera(stream)
            # filter.rotate_y_axis()

        # elif self.ckb_video_mirror.isChecked():
        #     print("CHECKED!")
        #     self.ckb_video_blur.setChecked(False)
        #     self.ckb_video_invert.setChecked(False)
        #     self.ckb_video_mono.setChecked(False)
        #     # self.ckb_video_rotateup.setChecked(False)
        #     self.ckb_image_mirror.setChecked(False)
        #     self.ckb_image_rotateup.setChecked(False)
        #     # self.clear_camera(stream)
        #     self.clear_camera(stream)
        #     filter.rotate_y_axis(stream)
        else:
            print("UNCHECKED!")

    #@pyqtSlot()
    def state_mono_changed(self):
        if self.ckb_video_mono.isChecked():
            print("CHECKED!")
            # self.ckb_video_blur.setChecked(False)
            self.ckb_video_invert.setChecked(False)
            # self.ckb_video_mirror.setChecked(False)
            # self.ckb_video_rotateup.setChecked(False)
            self.ckb_image_mirror.setChecked(False)
            self.ckb_image_rotateup.setChecked(False)
            # self.clear_camera(stream)
            self.clear_camera(stream)
            filter.mono(stream)
        else:
            print("UNCHECKED!")

    #@pyqtSlot()
    def state_rotate_up_changed(self):
        if self.ckb_image_rotateup.isChecked():
            print("CHECKED!")
            # self.ckb_video_blur.setChecked(False)
            self.ckb_video_invert.setChecked(False)
            # self.ckb_video_mirror.setChecked(False)
            self.ckb_video_mono.setChecked(False)
            # self.ckb_video_rotateup.setChecked(False)
            self.ckb_image_mirror.setChecked(False)
            # self.clear_camera(stream)
            self.clear_camera(stream)

        # elif self.ckb_video_rotateup.isChecked():
        #     print("CHECKED!")
        #     self.ckb_video_blur.setChecked(False)
        #     self.ckb_video_invert.setChecked(False)
        #     self.ckb_video_mirror.setChecked(False)
        #     self.ckb_video_mono.setChecked(False)
        #     self.ckb_image_mirror.setChecked(False)
        #     self.ckb_image_rotateup.setChecked(False)
        #     # self.clear_camera(stream)
        #     self.clear_camera(stream)
        #     filter.rotate_x_axis(stream)

        else:
            print("UNCHECKED!")

    #@pyqtSlot()
    def change_fps(self):
        print("code change fps here")

    #@pyqtSlot()
    def change_res(self):
        print('code change res here')

    # Save profiles function:
    #   Store all hex color of Red Green Blue values in a text file
    #@pyqtSlot()
    def save_profile_function(self):
        self.saveFinalParameters()

    # Load profiles function:
    #   Load a text file which contain all hex color of Red Green Blue values
    #   and show it on camera preview
    #@pyqtSlot()
    def load_profile_function(self):
        self.loadParameters()

    # Restore default profiles function:
    #   Restore default a text file which contain all hex color of Red Green Blue values
    #   and show it on camera preview
    #@pyqtSlot()
    def restore_default_profile_function(self):
        self.saveDefaultParameters()

    #@pyqtSlot()
    def take_photo(self):
        # take_photo.capture(stream)
        takephoto_v2.main()
        self.clear_camera(stream)

    #@pyqtSlot()
    def record_video(self):
        record_video.record(stream)
        self.clear_camera(stream)

    # Exit dialog:
    #   A form which show Yes or No when you want to exit the app
    #   If Yes  -> Exit
    #   If No   -> return
    #@pyqtSlot()
    def exit(self):
        ret = QMessageBox.question(self, "Exit", "Do you want to exit the app?")
        if ret == QMessageBox.Yes:
            self.logic = 0
            self.stopped = True
            QApplication.quit()
            exit()
        else:
            return

    #@pyqtSlot()
    def closeEvent(self, event:QtGui.QCloseEvent):
        ret = QMessageBox.question(self, "Exit", "Do you want to exit the app?")
        if ret == QMessageBox.Yes:
            self.logic = 0
            self.stopped = True
            QApplication.quit()
            exit()
            super().closeEvent(event)
        else:
            event.ignore()

    # def closeEvent(self, event:QtGui.QCloseEvent):
    #     return
    #     super().closeEvent(event)

    #@pyqtSlot()
    def clear_camera(self, stream):
        stream.release()
        # cv2.destroyAllWindows()

    ################## Action ##################
    # Run/Stop function:
    #   Allow turn on camera or pause camera like Play/Pause in music
    #   You could you once space to start cmaera and twice space to pause camera
    # #@pyqtSlot()
    def run_stop_function(self):
        # start_camera.display_camera()
        # self.start_webcam()
        print("Function sometimes error but I don't know why")
        # self.plainTextEdit.setPlainText("Function sometimes error but I don't know why")

    def stop_preview(self):
        self.timer.stop()
        self.stream.release()

    #@pyqtSlot()
    def start_camera(self):
        """Initialize camera.
        """
        self.stream = cv2.VideoCapture(0, cv2.CAP_V4L2)
        self.stream.set(cv2.CAP_PROP_SETTINGS, 0)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)

        self.timer = QTimer(self)
        # self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(5)

    def pause_camera(self):
        self.timer.stop()
        self.stream.release()

    def release_camera(self):
        stream.release()

    def set_file_photo_name(self, ext='png'):
        path = '/home/jetson/Pictures/C922/VID_'
        time = str(strftime("%Y-%b-%d at %H.%M.%S %p"))
        ext = ext
        filename = path+time+'.'+ext
        return filename
    
    def process_frame_blur(self, frame):
        # some intensive computation...
        frame = cv2.GaussianBlur(frame, (11, 11), 0)
        return frame

    def blur(frame):
        # some intensive computation...
        frame = cv2.GaussianBlur(frame, (11, 11), 0)
        return frame

    def mono(self, frame):
        frame =  cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return frame

    def hue(self, frame):
        frame =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
        return frame

    def invert(self, frame):
        frame =  cv2.bitwise_not(frame)
        return frame
            
    def rotate_x_axis(self, frame):
        frame = cv2.flip(frame, 0)
        return frame

    ### def mirror is the same def rotate_y_axis
    def rotate_y_axis(self, frame):
        frame = cv2.flip(frame, 1)
        return frame

    def rotate_both_axis(self, frame):
        frame = cv2.flip(frame, -1)
        return frame

    def set_file_video_name(self, ext='avi'):
        path = '/home/jetson/Videos/C922/VID_'
        time = str(strftime("%Y-%b-%d at %H.%M.%S %p"))
        ext = ext
        pathfile = path+time+'.'+ext
        return pathfile

    def get_frame(self, count, FpsCalc):
        while stream.isOpened():
            count = count + 1
            display_fps = round(FpsCalc.get(), 3)
            # print("FPS: ", display_fps)

            success, frame = stream.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue
        return (frame, display_fps, count)
        
    # def take_photo(self, stream, pathfile=filename, width=int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))):
    def take_photo(self):
        self.start_camera()
        # stream = cv2.VideoCapture(0, cv2.CAP_V4L2)
        # font which we will be using to display FPS
        font = cv2.FONT_HERSHEY_SIMPLEX
        FpsCalc = FpsCalculator(buffer_len = 50)
        # codec = 0x47504A4D 
        # stream.set(cv2.CAP_PROP_FPS, 30.0)
        # stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m','j','p','g'))
        # stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M','J','P','G'))
        # stream.set(cv2.CAP_PROP_FOURCC, codec)
        # stream.set(3, 1280)
        # stream.set(4, 720)
        pathfile = self.set_file_photo_name()
        # width = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))
        # height = int(stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
        count = 0

        # Get date and time
        date_and_time = datetime.now() 
        today = str(date_and_time.strftime("%Y-%m-%d %H:%M:%S"))
        frame = self.get_frame(count, FpsCalc)
        self.put_text(frame[0], font, today, frame[1])


        cv2.imwrite(pathfile.format(frame[2]), frame[0])
        cv2.imshow("Capture image mode", frame[0])

        self.release_camera()
        # stream.release()

    # def break_frame(self):

    #     key = cv2.waitKey(1)

    #     if key == 27 or key == ord('q') or key == ord('Q'):
    #         break
    #     return key

    def put_text(self, frame, today, font, display_fps):
            # puting the FPS count on the frame and display date and time
            cv2.rectangle(frame, (0, 2), (81, 21), (0, 0, 0), -1)        
            cv2.rectangle(frame, (0, 35), (149, 18), (0, 0, 0), -1)

            cv2.putText(frame, "FPS: " + str(display_fps), ((0), 15), font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, str(today), ((0), 30), font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

    # Standard Video Dimensions Sizes
    STD_DIMENSIONS = {
        "96p" : (128, 96),        # 4:3
        "120p" : (160, 122),      # 4:3
        "144p" : (176, 144),      # 11:9 | 256×144 16:9
        "240p" : (320, 240),      # 4:3  | 426×240 16:9
        "360p" : (640, 360),      # 4:3  | 640×360 16:9
        "480p" : (720, 480),
        "540p" : (960, 549),
        "720p" : (1280, 720),
        "1080p": (1920, 1080),
        "1440p": (2560, 1440),
        "2k"   : (2048, 1080),    # (3840, 2160),
        "4k"   : (3840, 2160),
        "8k"   : (7680, 4320),
        "16k"  : (15360, 8640),
        "64k"  : (61440, 34560)}

    # grab resolution dimensions and set video capture to it.
    # def get_dims(stream, res=res):
    #     width, height = STD_DIMENSIONS["720p"]
    #     if res in STD_DIMENSIONS:
    #         width,height = STD_DIMENSIONS[res]
    #     change_res(stream, width, height)
    #     return width, height

    # Video Encoding, might require additional installs
    # Types of Codes: http://www.fourcc.org/codecs.php
    VIDEO_TYPE = {
        # 'avi': cv2.VideoWriter_fourcc(*'XVID'),
        'avi': cv2.VideoWriter_fourcc(*'DIVX'),
        # 'avi': cv2.VideoWriter_fourcc(*'WMV1'),
        # 'avi': cv2.VideoWriter_fourcc(*'WMV2'),
        'avi': cv2.VideoWriter_fourcc('M','J','P','G'),
        # 'mp4': cv2.VideoWriter_fourcc(*'MJPG'),
        # 'mp4': cv2.VideoWriter_fourcc('M','J','P','G'),
        # 'mp4': cv2.VideoWriter_fourcc(*'X264'),
        # 'mp4': cv2.VideoWriter_fourcc(*'XVID'),
        'mkv': cv2.VideoWriter_fourcc(*'X264')}

    def get_video_type(filename):
        filename, ext = os.path.splitext(filename)
        if ext in VIDEO_TYPE:
            return  VIDEO_TYPE[ext]
        return VIDEO_TYPE['avi']

    def record(self, stream):
        if not stream.isOpened() or (stream.isOpened() == False):
            print("Unable to open camera")
            exit()

        stream.set(cv2.CAP_PROP_FOURCC ,cv2.VideoWriter_fourcc(*'MJPG'))
        stream.set(cv2.CAP_PROP_FPS, frames_per_second)

        # stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        # stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        # width = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))

        FpsCalc = FpsCalculator(buffer_len = 50)
        count = 0
        frames_per_second=self.get_fps()
        resolution=self.get_res()
        filename = set_file_video_name()
        out = cv2.VideoWriter(filename, get_video_type(filename), frames_per_second, get_dims(stream, resolution))
        # while True:
        while stream.isOpened():
            count = count + 1
            fps = round(FpsCalc.get(), 3)
            print(fps)
            # Read and display each frame
            (ret, frame) = stream.read()
            
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
                # sys.exit()

            frame = cv2.flip(frame, 1)
            # puting the FPS count on the frame and display date and time
            put_text_on_video(frame, fps, time)
            cv2.imshow("Record video mode", frame)

            key = cv2.waitKey(1) & 0xFF
            # Specify the countdown
            j = 30
            # set the key for the countdown to begin
            if key == ord('q'):
                while j>=10:
                    (ret, frame) = stream.read()
                    frame = cv2.flip(frame, 1)

                    # Display the countdown after 10 frames so that it is easily visible otherwise,
                    # it will be fast. You can set it to anything or remove this condition and put 
                    # countdown on each frame
                    if j%10 == 0:
                        # specify the font and draw the countdown using puttext
                        font = cv2.FONT_HERSHEY_SIMPLEX

                        # get coords based on boundary
                        textX = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH) / 2.5)
                        textY = int(stream.get(cv2.CAP_PROP_FRAME_HEIGHT) / 1.35)
                        cv2.putText(frame, str(j//10), (textX, textY), font, 15, (255,255,255), 10, cv2.LINE_AA)

                    # puting the FPS count on the frame and display date and time
                    put_text_on_video(frame, fps, time)

                    cv2.imshow("Record video mode", frame)
                    cv2.waitKey(125)
                    j = j-1
                else:
                    (ret, frame) = stream.read()
                    frame = cv2.flip(frame, 1)
                    # Display the clicked frame for 1 sec.
                    # You can increase time in waitKey alsoE_AA)

                    # puting the FPS count on the frame and display date and time
                    put_text_on_video(frame, fps, time)
                    out.write(frame)
                    cv2.imshow("Record video mode", frame)
                    cv2.waitKey(1)

            # Pause the camera
            if key == 32:
                cv2.waitKey()
            # Stop the camera
            elif key == 27:
                break

        stream.release()
        out.release()

    def get_res(self):
        # print("Get resolution from resolution combobox")
        resolution = self.cbb_video_resolution.currentText()
        return resolution

    def get_fps(self):
        # print("Get resolution from resolution combobox")
        fps = cbb_video_framerate.currentText()
        return fps

    # default program function:
    #   Don't know what to descire the function

    # rgb color detect function:
    #   So difficult function
    #   A function could detect color of object
    #   and detect what is the name of object
    #   After that, store it a text file and detect another object
    #   The function must be training and testing
    #@pyqtSlot()
    def detect_color_function(self):
        detect_colors.detect_color(stream)
        self.clear_camera(stream)

    #@pyqtSlot()
    def detect_mask_no_mask_function(self):
        detect_mask_nomask.main(device)
        self.clear_camera(stream)

    #@pyqtSlot()
    def detect_vegetables_function(self):
        detect_vegetable.main(device)
        self.clear_camera(stream)

    # get fram function:
    #   We could get frame of camera to default or higher than
    #   A form will display for you choose value that you want like
    #   Frame: 0 |=================||=================| 255fps
    #                             50fps
    

    # scan qr code function:
    #   Enable function scan qr code and decode the picture or image
    #   and show it on screen
    #   We could import a image from local or scan via camera
    #@pyqtSlot()
    def _detect_qr_code_function(self):
        detect_qr_code.detect_qr_code(stream)
        self.clear_camera(stream)

    #@pyqtSlot()
    def recognize_face_function(self):
        # self.stream = cv2.VideoCapture(0, cv2.CAP_V4L2)
        face_recognition_detector_with_hog.main(cv2.VideoCapture(0, cv2.CAP_V4L2))
        # multiple_threading_fps.main()
        # simple_camera.main()
        self.clear_camera(stream)

    #@pyqtSlot()
    def increase_fps(self):
        multiple_threading_fps.main()
        self.clear_camera(stream)


    ################## Help ##################
    #@pyqtSlot()
    def help_wiki_dialog(self):
        QMessageBox.information(self, "Wiki", "Please visit wiki page at.\nhttps://cobaohieu.github.io/")

    #@pyqtSlot()
    def help_about_dialog(self):
        QMessageBox.information(self, "About", "Camera Control\nVersion: 1.0.0\nDate: 03/2021\nCopyright by Co Bao Hieu | M3718007")

    ################## Support functions ##################
    def center(self):
        form = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        form.moveCenter(cp)
        self.move(form.topLeft())

    def detect_usb(self):
        VENDOR_ID = 0x046d
        PRODUCT_ID = 0x085c
        B_DEVICE_CLASS = 255
        # self.plainTextEdit.setPlainText(str(usb_detect.detectUsb(VENDOR_ID, PRODUCT_ID, B_DEVICE_CLASS)))
        print('[INFO    ]: ', str(usb_detect.detectUsb(VENDOR_ID, PRODUCT_ID, B_DEVICE_CLASS)))

    # def clear_image(self):
    #     self.imgLabel.clear()
    #     self.imgLabel.setText("")

    #@pyqtSlot()
    def loadFileNameDialog(self):
        options = QFileDialog()
        options.setWindowTitle('Open')
        options.setDirectory(QDir.currentPath())
        options.setNameFilter('All Files (*.);;Camera profile(*.xml)')
        options.setFileMode(QFileDialog.AnyFile)
        options.setFilter(QDir.Files)

        if options.exec_():
            fileName = options.selectedFiles()

            if fileName[0].endswith('*.*'):
                with open(fileName[0], 'r') as f:
                    data = f.read()
                    # self.plainTextEdit.setPlainText(data)
                    print('[INFO    ]: ', data)
                    f.close()

    #@pyqtSlot()
    def loadParameters(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileNames(self, "Open", "config.xml", "All Files (*.*);;Camera profile(*.xml)", options = options)

        if fileName:
            # with open(fileName[0], "r") as f:
            #     data = f.read()
            #     self.plainTextEdit.setPlainText(str(data))
            #     f.close()
            process_xml.loadPhotoParameters(fileName)
            process_xml.loadVideoParameters(fileName)
        # print(files)

    #@pyqtSlot()
    def saveDefaultParameters(self):
        path = os.path.dirname(os.path.realpath(__file__))        
        fileName = os.path.sep + 'config.xml'
        process_xml.saveDefaultParameters(fileName)

    #@pyqtSlot()
    def saveFinalParameters(self):
        options = QFileDialog.Options()
        # data_paths = [i for i in (os.path.join(in_dir, f) for f in os.listdir(in_dir)) if os.path.isfile(i)]
        fileName, _ = QFileDialog.getSaveFileName(self, "Save as", "config.xml", "All Files (*.*);;Camera profile(*.xml)", options = options)
        # self.plainTextEdit.setPlainText(str(fileName))
        print('[INFO    ]: ', str(fileName))
        if fileName:
            # with open(fileName[0], "w") as f:
            #     data = "Config some thing that you want!"
            #     f.write(data)
            #     f.close()
            # return fileName[0]
            process_xml.saveFinalParameters(fileName)

    # def getSaveFileName(self):
    #     file_filter = 'Camera profile(*.xml)'
    #     response = QFileDialog.getSaveFileNam(
    #         parent = self,
    #         caption = 'Select a data file',
    #         directory = 'config.xml',
    #         filter = file_filter,
    #         initialFilter = 'All Files;;;Camera profile(*.xml)'
    #     )
    #     print(response)
    #     return response[0]
    # def dataReady(self):
    #     cursor = self.plainTextEdit.textCursor()
    #     cursor.movePosition(cursor.End)
    #     cursor.insertText(str(self.process.readAll()))
    #     self.plainTextEdit.ensureCursorVisible()

    def callProgram(self):
        # run the process
        # start takes the exec and a list of arguments
        self.process.start('python',['tenfile.py'])

################## Support Functions Outside ##################

################## Debug function ##################
def qt_message_handler(mode, context, message):
    now = datetime.now()
    curr_time = now.strftime("%H:%M:%S")
    if mode == QtCore.QtInfoMsg:
        mode = 'INFO    '
    elif mode == QtCore.QtWarningMsg:
        mode = 'WARNING '
    elif mode == QtCore.QtCriticalMsg:
        mode = 'CRITICAL'
    elif mode == QtCore.QtFatalMsg:
        mode = 'FATAL    '
    else:
        mode = 'DEBUG   '
    print('[%s]: %s: line: %d, function: %s(), file: %s' % (mode, curr_time, context.line, context.function, context.file))
    print('[%s]: %s\n' % (mode, message))
QtCore.qInstallMessageHandler(qt_message_handler)

################## Main Program ##################
def main():
    app = QApplication(sys.argv)
    QtCore.qDebug('Use this function to debug code')
    form = mainForm()
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()

##################################### Fin #####################################
