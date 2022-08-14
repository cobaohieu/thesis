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
width = 640
height = 360
# #
# width = 640
# height = 480
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

################## FPS Calculator
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

class MainApp(QTabWidget):

    def __init__(self):
        QTabWidget.__init__(self)
        self.acquisition_tab = QWidget()
        # self.tab2 = QWidget()
        # self.tab3 = QWidget()
        # self.video_size = QSize(640, 480)
        self.video_size = QSize(1280, 720)
        # self.video_size = QSize(1920, 1200)
        self.addTab(self.acquisition_tab,"Photo/Video Settings")
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
        self.today = None

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

    def show_fps(self, frame, fps):
        """Draw fps number at top-left corner of the image."""
        font = cv2.FONT_HERSHEY_PLAIN
        line = cv2.LINE_AA
        fps_text = 'FPS: {:.2f}'.format(fps)
        cv2.putText(frame, fps_text, (11, 20), font, 1.0, (32, 32, 32), 4, line)
        cv2.putText(frame, fps_text, (10, 20), font, 1.0, (240, 240, 240), 1, line)
        return frame

    def setup_camera(self):
        """Initialize camera.
        """
        self.capture = (cv2.VideoCapture(0, cv2.CAP_V4L2))
        self.capture.set(cv2.CAP_PROP_SETTINGS, 0)
        self.capture.set(3,width)
        self.capture.set(4,height)
        # self.capture.set(3, self.video_size.width())
        # self.capture.set(4, self.video_size.height())
        self.font = cv2.FONT_HERSHEY_SIMPLEX

        # Map fps display FPS
        self.FpsCalc = FpsCalculator(buffer_len = 50)
        

        # The training data would be all the face encodings from all the known images and the labels are their names
        self.known_face_encodings = []
        self.known_face_names = []
        #count = 0

        with open('face_recognition_hog.pkl', 'rb') as f:
            self.known_face_names = pickle.load(f)
            self.known_face_encodings = pickle.load(f)

        self.tolerance=0.6

        self.fps = 0.0
        self.tic = time.time()
        self.filename = '/home/'+username+'/Pictures/C922/IMG_'+str(time.strftime("%Y-%b-%d at %H.%M.%S %p"))+'.png'
        self.count = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)

    def display_video_stream(self):
        """Read frame from camera and repaint QLabel widget.
        """
        # Get date and time
        # self.today = str(datetime.now())
        self.today = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.count = self.count + 1
        _, frame = self.capture.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        display_fps = round(self.FpsCalc.get(), 3)

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        # if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        # Default for model is HOG and execute with CPU -> fast
        # face_locations = face_recognition.face_locations(rgb_small_frame)
        face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")

        # For model is CNN and execute with GPU NVIDIA CUDA -> slow
        # face_locations = face_recognition.face_locations(rgb_small_frame, model="cnn")

        # Given an image, return the 128-dimension face encoding for each face in the image
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []

        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            # matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.45)

            name = "Unknown"

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]


            face_names.append(name)

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            # top *= 4
            # right *= 4
            # bottom *= 4
            # left *= 4

            top *= 2
            right *= 3
            bottom *= 9
            left *= 3

            # Draw a box around the face
            cv2.rectangle(frame, (left, int(top*0.5)), (int(right*1.5), int(bottom*0.5)), (130, 252, 94), 2)
            # cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, int(top*0.5) + 35), (int(right*1.5), int(top*0.5)), (130, 252, 94), cv2.FILLED)
            cv2.putText(frame, name, (int(left *1.5), int(top*0.5) + 27), self.font, 0.7, (255, 255, 255), 2)
        
        # puting the FPS count on the frame and display date and time
        cv2.rectangle(frame, (0, 0), (81, 25), (0, 0, 0), -1)   
        cv2.rectangle(frame, (0, 35), (149, 18), (0, 0, 0), -1)
        # frame = self.show_fps(frame, self.fps)

        print("FPS: " + str(display_fps))
        # print("Now is: " + self.today)
        cv2.putText(frame, "FPS: " + str(display_fps), ((1), 15), self.font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, str(self.today), ((0), 30), self.font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        image = QImage(frame.data, frame.shape[1], frame.shape[0],
                       frame.strides[0], QImage.Format_RGB888)
        # self.image_label.setPixmap(QPixmap.fromImage(image))
        image = QPixmap.fromImage(image)
        pixmap = QPixmap(image)
        resizeImage = pixmap.scaled(640, 480, Qt.KeepAspectRatio)
        QApplication.processEvents()
        self.image_label.setPixmap(resizeImage)
        self.temp = frame

        # toc = time.time()
        # curr_fps = 1.0 / (toc - self.tic)
        # # calculate an exponentially decaying average of fps number
        # self.fps = curr_fps if self.fps == 0.0 else (self.fps*0.95 + curr_fps*0.05)
        # self.tic = toc

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
