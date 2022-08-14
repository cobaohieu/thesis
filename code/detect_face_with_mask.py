#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Head       :Camera Application V2020

Description:

Author     : Co Bao Hieu
Id         : M3718007
"""

################## Import Modules ##################
# import OpenGL.GL
import numpy as np
import numpy.linalg
import sys
import os
import cv2
import datetime
import time
import copy
import PIL
import argparse
import imutils
import logging
import tkinter as tk
import mss
import tensorflow.keras.backend as K
import multiprocessing
import colorsys
import random

################## Import sub modules ##################
from time import gmtime, strftime
from datetime import datetime
from math import radians, degrees, cos, sin, tan
from PIL import Image
from imutils.video import VideoStream
from screeninfo import get_monitors

# from OpenGL.GL import *
# from OpenGL.GLU import *
# from OpenGL.GLUT import *

from collections import OrderedDict
from collections import deque

from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from tensorflow.python.keras.backend import get_session
from tensorflow.keras.layers import Input
# from keras import backend as K
# from keras.models import load_model
# from keras.layers import Input

from collect_XLM_images import *

global stream

width = 640
height = 480

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

def detect_and_predict_mask(frame, faceNet, maskNet):
    # grab the dimensions of the frame and then construct a blob
    # from it
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
        (104.0, 177.0, 123.0))

    # pass the blob through the network and obtain the face detections
    faceNet.setInput(blob)
    detections = faceNet.forward()
    print(detections.shape)

    # initialize our list of faces, their corresponding locations,
    # and the list of predictions from our face mask network
    faces = []
    locs = []
    preds = []

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the detection
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the confidence is
        # greater than the minimum confidence
        if confidence > 0.5:
            # compute the (x, y)-coordinates of the bounding box for
            # the object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # ensure the bounding boxes fall within the dimensions of
            # the frame
            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

            # extract the face ROI, convert it from BGR to RGB channel
            # ordering, resize it to 224x224, and preprocess it
            face = frame[startY:endY, startX:endX]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)

            # add the face and bounding boxes to their respective
            # lists
            faces.append(face)
            locs.append((startX, startY, endX, endY))

    # only make a predictions if at least one face was detected
    if len(faces) > 0:
        # for faster inference we'll make batch predictions on *all*
        # faces at the same time rather than one-by-one predictions
        # in the above `for` loop
        faces = np.array(faces, dtype="float32")
        preds = maskNet.predict(faces, batch_size=32)

    # return a 2-tuple of the face locations and their corresponding
    # locations
    return (locs, preds)

def detect_face_with_mask_v2():
    # load our serialized face detector model from disk
    prototxtPath = r"./face_detector/deploy.prototxt"
    weightsPath = r"./face_detector/res10_300x300_ssd_iter_140000.caffemodel"
    faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

    # load the face mask detector model from disk
    maskNet = load_model("mask_detector.model")

    # initialize the video stream
    # self.plainTextEdit.setPlainText("[INFO] starting video stream...")
    print("[INFO] starting video stream...")
    stream = VideoStream(src=0).start()

    # loop over the frames from the video stream
    while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        frame = stream.read()
        frame = imutils.resize(frame, width=400)
        # frame = imutils.resize(frame, width=640, height=480)

        # detect faces in the frame and determine if they are wearing a
        # face mask or not
        (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

        # loop over the detected face locations and their corresponding
        # locations
        for (box, pred) in zip(locs, preds):
            # unpack the bounding box and predictions
            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred

            # determine the class label and color we'll use to draw
            # the bounding box and text
            label = "Mask" if mask > withoutMask else "No Mask"
            color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

            # include the probability in the label
            label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

            # display the label and bounding box rectangle on the output
            # frame
            cv2.putText(frame, label, (startX, startY - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

        # show the output frame
        # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        # pixmap = QPixmap.fromImage(image)
        # self.imgLabel.setPixmap(pixmap)
        # self.imgLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        cv2.imshow("Frame", frame)

        # if the `ESC` key was pressed, break from the loop
        key = cv2.waitKey(1)
        if key == 27:
            break

    # do a bit of cleanup
    cv2.destroyAllWindows()
    stream.stop()

def detect_face_with_mask(stream):
    # load our serialized face detector model from disk
    prototxtPath = r"./face_detector/deploy.prototxt"
    weightsPath = r"./face_detector/res10_300x300_ssd_iter_140000.caffemodel"
    faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

    # load the face mask detector model from disk
    maskNet = load_model("mask_detector.model")

    # initialize the video stream
    # self.plainTextEdit.setPlainText("[INFO] starting video stream...")
    print("[INFO] starting video stream...")

    # font which we will be using to display FPS
    font = cv2.FONT_HERSHEY_SIMPLEX
    FpsCalc = FpsCalculator(buffer_len = 50)


    # loop over the frames from the video stream
    while True:
        display_fps = round(FpsCalc.get(), 3)
        print("Camera FPS       : ", display_fps)

        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        frame = stream.read()
        # frame = cv2.resize(frame, 640)
        frame = cv2.flip(frame,1)

        frame = imutils.resize(frame, width=640)
        # frame = imutils.resize(frame, width=640, height=480)

        # detect faces in the frame and determine if they are wearing a
        # face mask or not
        (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)
        # loop over the detected face locations and their corresponding
        # locations
        for (box, pred) in zip(locs, preds):

            glutInit(sys.argv)
            glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
            # unpack the bounding box and predictions
            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred

            # determine the class label and color we'll use to draw
            # the bounding box and text
            label = "Mask" if mask > withoutMask else "No Mask"
            color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

            # include the probability in the label
            label = "{}: {:.2f}%".format(label,
                                        max(mask, withoutMask) * 100)

            # display the label and bounding box rectangle on the output
            # frame
            cv2.putText(frame, label, (startX, startY - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX, startY),
                        (endX, endY), color, 2)

        # puting the FPS count on the frame
        cv2.putText(frame, "FPS:" + str(display_fps), ((width-150), 30),
                    font, 1.0, (0, 255, 0), 2, cv2.LINE_AA)

        # show the output frame
        cv2.imshow('Detect Face with mask mode', frame)

        # if the `ESC` key was pressed, break from the loop
        key = cv2.waitKey(1)
        if key == 27:
            break

    # Release everything if job or clean is finished
    cv2.destroyAllWindows()
    stream.stop()


if __name__ == "__main__":
    detect_face_with_mask(stream = VideoStream(src=1).start())