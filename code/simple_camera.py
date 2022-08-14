# MIT License
# Copyright (c) 2019-2022 JetsonHacks

# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

import cv2
import face_recognition
import argparse
import os
import cv2
import pickle
import datetime
import time
import math
import imutils
import numpy as np
import numpy.linalg

from time import gmtime, strftime
from datetime import datetime
from math import radians, degrees, cos, sin, tan
from collections import OrderedDict, deque
from PIL import Image
from imutils.video import VideoStream

from collections import OrderedDict, deque
from threading import Thread

""" 
gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
Flip the image by setting the flip_method (most common values: 0 and 2)
display_width and display_height determine the size of each camera pane in the window on the screen
Default 1920x1080 displayd in a 1/4 size window
"""
def show_fps(frame, fps):
    """Draw fps number at top-left corner of the image."""
    font = cv2.FONT_HERSHEY_PLAIN
    line = cv2.LINE_AA
    fps_text = 'FPS: {:.2f}'.format(fps)
    cv2.putText(frame, fps_text, (11, 20), font, 1.0, (32, 32, 32), 4, line)
    cv2.putText(frame, fps_text, (10, 20), font, 1.0, (240, 240, 240), 1, line)
    return frame


def set_display(window_name, full_scrn):
    """Set disply window to either full screen or normal."""
    if full_scrn:
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                              cv2.WINDOW_FULLSCREEN)
    else:
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                              cv2.WINDOW_NORMAL)


class FpsCalculator():
    """Helper class for calculating frames-per-second (FPS)."""

    def __init__(self, decay_factor=0.95):
        self.fps = 0.0
        self.tic = time.time()
        self.decay_factor = decay_factor

    def update(self):
        toc = time.time()
        curr_fps = 1.0 / (toc - self.tic)
        self.fps = curr_fps if self.fps == 0.0 else self.fps
        self.fps = self.fps * self.decay_factor + \
                   curr_fps * (1 - self.decay_factor)
        self.tic = toc
        return self.fps

    def reset(self):
        self.fps = 0.0

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=960,
    capture_height=540,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
    # flip-method         : video flip methods
    # flags: readable, writable, controllable
    # Enum "GstNvVideoFlipMethod" Default: 0, "none"
    # (0): none             - Identity (no rotation)
    # (1): counterclockwise - Rotate counter-clockwise 90 degrees
    # (2): rotate-180       - Rotate 180 degrees
    # (3): clockwise        - Rotate clockwise 90 degrees
    # (4): horizontal-flip  - Flip horizontally
    # (5): upper-right-diagonal - Flip across upper right/lower left diagonal
    # (6): vertical-flip    - Flip vertically
    # (7): upper-left-diagonal - Flip across upper left/low

):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def main():
    window_title = "Face recognition Mode"

    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(gstreamer_pipeline(flip_method=0))
    stream = cv2.VideoCapture(gstreamer_pipeline(flip_method=4), cv2.CAP_GSTREAMER)

    fps = 0.0
    tic = time.time()

    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # Get date and time
    today = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # The training data would be all the face encodings from all the known images and the labels are their names
    known_face_encodings = []
    known_face_names = []
    #count = 0

    with open('face_recognition_hog.pkl', 'rb') as f:
        known_face_names = pickle.load(f)
        known_face_encodings = pickle.load(f)

    tolerance=0.6
    if stream.isOpened():
        try:
            window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
            while True:
                ret_val, frame = stream.read()

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
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    # matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.45)

                    name = "Unknown"

                    # If a match was found in known_face_encodings, just use the first one.
                    # if True in matches:
                    #     first_match_index = matches.index(True)
                    #     name = names[first_match_index]

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)

                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                    # cf = confusion_matrix(known_face_encodings[best_match_index], face_encoding)
                    # print("[DEBUG  ] cf: ", cf)
                    # acc = accuracy_score(known_face_encodings[best_match_index], face_encoding)
                    # print("[DEBUG  ] acc: ", acc)


                    face_names.append(name)
                    #count += 1

                # process_this_frame = not process_this_frame

                # Display the results
                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                # Check to see if the user closed the window
                # Under GTK+ (Jetson Default), WND_PROP_VISIBLE does not work correctly. Under Qt it does
                # GTK - Substitute WND_PROP_AUTOSIZE to detect if window has been closed by user
                if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                    frame = show_fps(frame, fps)
                    cv2.rectangle(frame, (0, 35), (149, 18), (0, 0, 0), -1)
                    cv2.putText(frame, str(today), ((0), 30), font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
                    cv2.imshow(window_title, frame)
                    toc = time.time()
                    curr_fps = 1.0 / (toc - tic)
                    # calculate an exponentially decaying average of fps number
                    fps = curr_fps if fps == 0.0 else (fps*0.95 + curr_fps*0.05)
                    tic = toc
                else:
                    break 
                keyCode = cv2.waitKey(10) & 0xFF
                # Stop the program on the ESC key or 'q'
                if keyCode == 27 or keyCode == ord('q'):
                    break
        finally:
            f.close()
            stream.release()
            cv2.destroyAllWindows()
    else:
        print("Error: Unable to open camera")


if __name__ == "__main__":
    main()
