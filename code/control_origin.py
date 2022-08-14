from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QSlider, QLabel, QPushButton, QHBoxLayout, QFormLayout, QGridLayout
from PyQt5.QtGui import QImage, QPixmap
import face_recognition
import cv2
import pickle
import os
import datetime
import time
import math
import numpy as np
import numpy.linalg
import sys

from numpy import argmin
from time import gmtime, strftime
from datetime import datetime
from math import radians, degrees, cos, sin, tan
from collections import OrderedDict, deque

global stream
date_and_time = datetime.now()
#
# width = 320
# height = 240
#
# width = 480
# height = 360
#
# width = 640
# height = 360
#
width = 640
height = 480
#
# width = 720
# height = 360
# #
# width = 720
# height = 480

# width = 960
# height = 540
# HD
# width = 1280
# height = 720
# Full HD
# width = 1920
# height = 1080

username = os.getlogin()

class MainApp(QTabWidget):

    def __init__(self):
        QTabWidget.__init__(self)
        self.acquisition_tab = QWidget()
        # self.tab2 = QWidget()
        # self.tab3 = QWidget()
        # self.tab3 = QWidget()
        # self.video_size = QSize(640, 480)
        self.video_size = QSize(960, 540)
        # self.video_size = QSize(1280, 720)
        # self.video_size = QSize(1920, 1200)
        self.addTab(self.acquisition_tab,"Acquisition")
        # self.addTab(self.tab2,"Tab 2")
        # self.addTab(self.tab3,"Tab 3")
        self.acquisition_tab_UI()
        self.setWindowTitle("Camera Control (2020)")

    def acquisition_tab_UI(self):
        """Initialize widgets.
        """
        self.image_label = QLabel()
        self.temp = None # Updated brightness value
        self.image_label.setFixedSize(self.video_size)

        start_preview_button = QPushButton("Start preview")
        start_preview_button.clicked.connect(self.setup_camera)

        stop_preview_button = QPushButton("Stop preview")
        stop_preview_button.clicked.connect(self.stop_preview)

        quit_button = QPushButton("Quit")
        quit_button.clicked.connect(self.close)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.saveVideo)

        brightness_label = QLabel("Brightness", self)
        brightness_slider = QSlider(Qt.Horizontal, self)
        brightness_slider.setFocusPolicy(Qt.NoFocus)
        brightness_slider.setValue(128)
        brightness_slider.valueChanged[int].connect(self.changedBrightnessValue)
        brightness_slider.setMaximum(255)
        # self.brightness_value = QLabel()
        # self.brightness_value.setNum(brightness_slider.value())

        contrast_label = QLabel("Contrast")
        contrast_slider = QSlider(Qt.Horizontal, self)
        contrast_slider.setFocusPolicy(Qt.NoFocus)
        contrast_slider.setValue(128)
        contrast_slider.valueChanged[int].connect(self.changedContrastValue)
        contrast_slider.setMaximum(255)

        saturation_label = QLabel("Saturation")
        saturation_slider = QSlider(Qt.Horizontal, self)
        saturation_slider.setFocusPolicy(Qt.NoFocus)
        saturation_slider.setValue(128)
        saturation_slider.valueChanged[int].connect(self.changedSaturationValue)
        saturation_slider.setMaximum(255)

        gain_label = QLabel("Gain")
        gain_slider = QSlider(Qt.Horizontal, self)
        gain_slider.setFocusPolicy(Qt.NoFocus)
        gain_slider.setValue(0)
        gain_slider.valueChanged[int].connect(self.changedGainValue)
        gain_slider.setMaximum(255)
        gain_slider.setRange(0,255)
        # gain_slider.setPageStep(10)
        # gain_slider.setTickInterval(10)
        gain_slider.setSingleStep(1)
        gain_slider.setTickPosition(QSlider.TicksBelow)
        

        exposure_label = QLabel("Exposure")
        exposure_slider = QSlider(Qt.Horizontal, self)
        exposure_slider.setFocusPolicy(Qt.NoFocus)
        exposure_slider.setValue(-5)
        exposure_slider.valueChanged[int].connect(self.changedExposureValue)
        # exposure_slider.setMinimum(3)
        exposure_slider.setMaximum(2047)

        sharpness_label = QLabel("Sharpness")
        sharpness_slider = QSlider(Qt.Horizontal, self)
        sharpness_slider.setFocusPolicy(Qt.NoFocus)
        sharpness_slider.setValue(128)
        sharpness_slider.valueChanged[int].connect(self.changedSharpnessValue)
        sharpness_slider.setMaximum(255)

        focus_label = QLabel("Focus")
        focus_slider = QSlider(Qt.Horizontal, self)
        focus_slider.setFocusPolicy(Qt.NoFocus)
        focus_slider.setValue(0)
        focus_slider.valueChanged[int].connect(self.changedFocusValue)
        focus_slider.setMaximum(250)

        zoom_label = QLabel("Zoom")
        zoom_slider = QSlider(Qt.Horizontal, self)
        zoom_slider.setFocusPolicy(Qt.NoFocus)
        zoom_slider.setValue(100)
        zoom_slider.valueChanged[int].connect(self.changedZoomValue)
        zoom_slider.setMaximum(500)

        l2 = QFormLayout()
        l2.addWidget(QLabel())
        l2.addWidget(QLabel())
        l2.addWidget(QLabel())
        l2.addWidget(QLabel())
        l2.addWidget(QLabel())
        l2.addWidget(QLabel())
        l2.addWidget(QLabel())
        l2.addWidget(QLabel())
        l2.addRow(brightness_label, brightness_slider) #, self.brightness_value)
        l2.addRow(contrast_label, contrast_slider)
        l2.addRow(saturation_label, saturation_slider)
        l2.addRow(gain_label, gain_slider)
        l2.addRow(exposure_label, exposure_slider)
        l2.addRow(sharpness_label, sharpness_slider)
        l2.addRow(focus_label, focus_slider)
        l2.addRow(zoom_label, zoom_slider)

        l3 = QHBoxLayout()
        l3.addWidget(start_preview_button)
        l3.addWidget(stop_preview_button)
        l3.addWidget(save_button)
        l3.addWidget(quit_button)

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.image_label, 0, 0)
        grid.addLayout(l3,1,0)

        layout = QHBoxLayout()
        layout.addLayout(grid)
        layout.addLayout(l2)
        self.acquisition_tab.setLayout(layout)

    def changedBrightnessValue(self,value):
        brightness = (value - 0) * 255 / (250 - 0)
        self.capture.set(10,brightness)
        print("Brightness now is:", brightness)

    def changedContrastValue(self,value):
        contrast = (value - 0) * 255 / (250 - 0)
        self.capture.set(11,contrast)
        print("Contrast now is:", contrast)

    def changedSaturationValue(self,value):
        saturation = (value - 0) * 255 / (250 - 0)
        self.capture.set(12,saturation)
        print("Saturation now is:", saturation)

    def changedGainValue(self,value):
        gain = (value - 0) * 255 / (250 - 0)
        self.capture.set(14,gain)
        print("Gain now is:", gain)

    def changedExposureValue(self,value):
        exposure = (value - 0) * 2047 / (2047 - 0)
        self.capture.set(15,exposure)
        print("Exposure now is:", exposure)

    def changedSharpnessValue(self,value):
        sharpness = (value - 0) * 255 / (255 - 0)
        self.capture.set(20,sharpness)
        print("Sharpness now is:", sharpness)

    def changedFocusValue(self,value):
        focus = (value - 0) * 250 / (250 - 0)
        self.capture.set(28,focus)
        print("Focus now is:", focus)

    def changedPanValue(self,value):
        pan = (value - 0) * 36000 / (36000 - 0)
        self.capture.set(33,pan)
        print("Pan now is:", pan)

    def changedTiltValue(self,value):
        tilt = (value - 0) * 36000 / (36000 - 0)
        self.capture.set(34,tilt)
        print("Tilt now is:", tilt)

    def changedZoomValue(self,value):
        zoom = (value - 0) * 500 / (500 - 0)
        self.capture.set(27,zoom)
        print("Zoom now is:", zoom)

    def setup_camera(self):
        """Initialize camera.
        """
        self.capture = (cv2.VideoCapture(0, cv2.CAP_V4L2))
        # self.capture = (cv2.VideoCapture(2, cv2.CAP_V4L2))
        self.capture.set(cv2.CAP_PROP_SETTINGS, 0)
        self.capture.set(3,width)
        self.capture.set(4,height)
        # self.capture.set(3, self.video_size.width())
        # self.capture.set(4, self.video_size.height())
        self.filename = '/home/'+username+'/Pictures/C922/IMG_'+str(time.strftime("%Y-%b-%d at %H.%M.%S %p"))+'.png'
        self.count = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)

    def blur(self, frame):
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

    def display_video_stream(self):
        """Read frame from camera and repaint QLabel widget.
        """
        _, frame = self.capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # frame = cv2.flip(frame, 0)
        # frame =  cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # self.rotate_both_axis(frame)
        # frame = cv2.GaussianBlur(frame, (11, 11), 0)
        # self.blur(frame)
        # self.mono(frame)
        # self.hue(frame)
        # self.invert(frame)
        # self.rotate_x_axis(frame)
        # self.rotate_y_axis(frame)
        # self.rotate_both_axis(frame)

        # image = QImage(frame, frame.shape[1], frame.shape[0],
        #                frame.strides[0], QImage.Format_RGB888)
        # self.image_label.setPixmap(QPixmap.fromImage(image))
        image = QImage(frame.data, frame.shape[1], frame.shape[0],
                       frame.strides[0], QImage.Format_RGB888)
        image = QPixmap.fromImage(image)
        pixmap = QPixmap(image)
        resizeImage = pixmap.scaled(640, 480, Qt.KeepAspectRatio)
        QApplication.processEvents()
        self.image_label.setPixmap(resizeImage)
        self.temp = frame

    def saveVideo(self):
        # cv2.imwrite(self.filename.format(self.count), frame)
        # print("Photo is saved")
        """ This function will save the image"""
        self.temp = cv2.cvtColor(self.temp, cv2.COLOR_RGBA2BGRA)
        cv2.imwrite(self.filename, self.temp)
        print('Image saved as:', self.filename)
        os.chmod(self.filename , 0o777)
        # os.chmod(self.filename , 0777)

    def stop_preview(self):
        self.timer.stop()
        self.capture.release()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainApp()
    win.show()
    sys.exit(app.exec_())
