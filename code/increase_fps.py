#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Head       : Scan QR Code and Decode QR

Description:

Author     : Co Bao Hieu
Id         : M3718007
"""

################## Import Modules ##################
from __future__ import print_function
import sys
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import datetime
import time
import numpy as np
import usb
import usb.core
import usb.util
import usb.backend.libusb1
import ctypes
import cv2
import pyzbar.pyzbar as pyzbar
# import pyzar
import argparse
import imutils
import PyQt5
import logging
import xml.etree.ElementTree as ET
import colorsys

# import PyQt5.Qt as Qt
import PyQt5.QtCore as QtCore
import PyQt5.QtDBus as QtDBus
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtXml as QtXml
# import PyQt5.QtMultimedia as QtMultimedia
# import PyQt5.QtNetwork as QtNetwork
# import PyQt5.QtXmlPatterns as QtXmlPatterns


################## Modules path ##################
sys.path.append(os.path.join(os.path.dirname(__file__), "./"))
sys.path.append(os.path.join(os.path.dirname(__file__), "./get_blocks"))
sys.path.append(os.path.join(os.path.dirname(__file__), "./pantilt"))
sys.path.append(os.path.join(os.path.dirname(__file__), "./YOLOv3-CSGO-detection"))
sys.path.append(os.path.join(os.path.dirname(__file__), "./YOLOv3-custom-training"))

import about_ui
import config_ui
import usb_detect
import main_ui
import process_images
import process_xml

################## Import sub modules ##################
from threading import Thread
from time import gmtime, strftime
from PIL import Image
from imutils.video import FPS
from imutils.video import VideoStream
from imutils.video import WebcamVideoStream
from pyzbar import pyzbar
# from pyzbar.pyzbar import decode
from collections import OrderedDict

from PyQt5.QtCore import (Qt, QSysInfo, QUrl, QMetaType, QSettings, QObject, QDir, QVariant, QIODevice, QThread, QMutex, QWaitCondition, QMutexLocker, QTime, QTimer, QFile, QAbstractItemModel, QModelIndex, QDataStream, QTextStream, pyqtSlot, QSize)

from PyQt5.QtGui import (QIcon, QFont, QImage, QPixmap, QDesktopServices, QColor, QPen, QPainter, QMouseEvent, QKeyEvent, QTextCursor, QTextBlock, QTransform, QPalette, QBrush, QTextFormat, QCloseEvent)

# from PyQt5.QtMultimedia import QVideoFrame, QVideoEncoderSettings, QVideoSurfaceFormat, QMediaContent, QMediaPlayer
# from PyQt5.QtMultimediaWidgets import QVideoWidget

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QFileDialog, QInputDialog, QGraphicsRectItem, QGraphicsScene, QMessageBox, QMainWindow, QToolTip, QPushButton, QLineEdit, QDialog, QHBoxLayout, QSlider, QAbstractButton, QCheckBox, QTableWidget, QButtonGroup, QDialogButtonBox, QSpacerItem, QGridLayout, QAction, QHeaderView, QVBoxLayout, QTextBrowser, QSizePolicy, QStyle, QPlainTextEdit, QScrollBar, QTreeView,QAbstractItemDelegate, QAbstractItemView, QHeaderView, QStyleOptionFocusRect, QStyleOption, QStyleOptionFrame, QStyleOptionTabWidgetFrame, QStyleOptionTabBarBase, QStyleOptionHeader, QStyleOptionButton, QStyleOptionProgressBar, QStyleOptionToolBar, QStyleOptionViewItem, QStyleOptionComplex, QStyleOptionSlider, QStyleOptionGraphicsItem, QStyleOptionDockWidget, QStyleOptionSpinBox, QAbstractScrollArea, QStyleOptionGroupBox, QStyleOptionSizeGrip, QStyleOptionComboBox, QStyleOptionTitleBar, QDesktopWidget)

from PyQt5.QtXml import (QDomDocument, QDomElement)

from PyQt5.uic import loadUi

# from get_blocks import Blocks

# from pan_tilt import Blocks, Gimbal

# ap = argparse.ArgumentParser()
# ap.add_argument("-n", "--num-frames", type=int, default=100,
# 	help="# of frames to loop over for FPS test")
# ap.add_argument("-d", "--display", type=int, default=-1,
# 	help="Whether or not frames should be displayed")
# args = vars(ap.parse_args())

# def frame_from_webcame():
# 	# grab a pointer to the video stream and initialize the FPS counter
# 	print("[INFO] sampling frames from webcam...")
# 	stream = cv2.VideoCapture(0)
# 	fps = FPS().start()
# 	# loop over some frames
# 	while fps._numFrames < args["num_frames"]:
# 		# grab the frame from the stream and resize it to have a maximum
# 		# width of 400 pixels
# 		(grabbed, frame) = stream.read()
# 		frame = imutils.resize(frame, width=400)
# 		# check to see if the frame should be displayed to our screen
# 		if args["display"] > 0:
# 			cv2.imshow("Frame", frame)
# 			key = cv2.waitKey(1) & 0xFF
# 		# update the FPS counter
# 		fps.update()
# 	# stop the timer and display FPS information
# 	fps.stop()
# 	print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
# 	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
# 	# do a bit of cleanup
# 	stream.release()
# 	cv2.destroyAllWindows()

# def frame_video_stream():
# 	# created a *threaded* video stream, allow the camera sensor to warmup,
# 	# and start the FPS counter
# 	print("[INFO] sampling THREADED frames from webcam...")
# 	vs = WebcamVideoStream(src=0).start()
# 	fps = FPS().start()
# 	# loop over some frames...this time using the threaded stream
# 	while fps._numFrames < args["num_frames"]:
# 		# grab the frame from the threaded video stream and resize it
# 		# to have a maximum width of 400 pixels
# 		frame = vs.read()
# 		frame = imutils.resize(frame, width=400)
# 		# check to see if the frame should be displayed to our screen
# 		if args["display"] > 0:
# 			cv2.imshow("Frame", frame)
# 			key = cv2.waitKey(1) & 0xFF
# 		# update the FPS counter
# 		fps.update()
# 	# stop the timer and display FPS information
# 	fps.stop()
# 	print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
# 	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
# 	# do a bit of cleanup
# 	cv2.destroyAllWindows()
# 	vs.stop()

# class FPS:
# 	def __init__(self):
# 		# store the start time, end time, and total number of frames
# 		# that were examined between the start and end intervals
# 		self._start = None
# 		self._end = None
# 		self._numFrames = 0

# 	def start(self):
# 		# start the timer
# 		self._start = datetime.datetime.now()
# 		return self

# 	def stop(self):
# 		# stop the timer
# 		self._end = datetime.datetime.now()

# 	def update(self):
# 		# increment the total number of frames examined during the
# 		# start and end intervals
# 		self._numFrames += 1

# 	def elapsed(self):
# 		# return the total number of seconds between the start and
# 		# end interval
# 		return (self._end - self._start).total_seconds()

# 	def fps(self):
# 		# compute the (approximate) frames per second
# 		return self._numFrames / self.elapsed()

# class WebcamVideoStream:
# 	def __init__(self, src=0):
# 		# initialize the video camera stream and read the first frame
# 		# from the stream
# 		self.stream = cv2.VideoCapture(src)
# 		(self.grabbed, self.frame) = self.stream.read()
# 		# initialize the variable used to indicate if the thread should
# 		# be stopped
# 		self.stopped = False

# 	def start(self):
# 		# start the thread to read frames from the video stream
# 		Thread(target=self.update, args=()).start()
# 		return self

# 	def update(self):
# 		# keep looping infinitely until the thread is stopped
# 		while True:
# 			# if the thread indicator variable is set, stop the thread
# 			if self.stopped:
# 				return
# 			# otherwise, read the next frame from the stream
# 			(self.grabbed, self.frame) = self.stream.read()

# 	def read(self):
# 		# return the frame most recently read
# 		return self.frame

# 	def stop(self):
# 		# indicate that the thread should be stopped
# 		self.stopped = True


if __name__ == '__main__' :

    # Start default camera
    video = cv2.VideoCapture(0);

    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    # With webcam get(CV_CAP_PROP_FPS) does not work.
    # Let's see for ourselves.

    if int(major_ver)  < 3 :
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
    else :
        fps = video.get(cv2.CAP_PROP_FPS)
        print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

    # Number of frames to capture
    num_frames = 60;

    print("Capturing {0} frames".format(num_frames))

    # Start time
    start = time.time()

    # Grab a few frames
    for i in range(0, num_frames) :
        ret, frame = video.read()

    # End time
    end = time.time()

    # Time elapsed
    seconds = end - start
    print ("Time taken : {0} seconds".format(seconds))

    # Calculate frames per second
    fps  = num_frames / seconds
    print("Estimated frames per second : {0}".format(fps))

    # Release video
    video.release()