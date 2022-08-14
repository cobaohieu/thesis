#!/usr/bin/env python3
# Train multiple images per person
# Find and recognize faces in an image using a SVC with scikit-learn

"""
Structure:
        <test_image>.jpg
        <train>/
            <person_1>/
                <person_1_face-1>.jpg
                <person_1_face-2>.jpg
                .
                .
                <person_1_face-n>.jpg
           <person_2>/
                <person_2_face-1>.jpg
                <person_2_face-2>.jpg
                .
                .
                <person_2_face-n>.jpg
            .
            .
            <person_n>/
                <person_n_face-1>.jpg
                <person_n_face-2>.jpg
                .
                .
                <person_n_face-n>.jpg
"""

import face_recognition
import cv2
import pickle
import os
import datetime
import time
import math
import numpy as np
import numpy.linalg
# import matplotlib

from numpy import argmin
from time import gmtime, strftime
from datetime import datetime
from math import radians, degrees, cos, sin, tan
from collections import OrderedDict, deque
# from sklearn import svm
# from sklearn.metrics import confusion_matrix, accuracy_score

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

global stream
date_and_time = datetime.now()
width = 960
height = 549
# Try resolution (320, 240)
# Try resolution (640, 360)


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

################## Calculating Accuracy as a Percentage and draw maplot w/ threshold of 0.6
# import math

# def face_distance_to_conf(face_distance, face_match_threshold=0.6):
#     if face_distance > face_match_threshold:
#         range = (1.0 - face_match_threshold)
#         linear_val = (1.0 - face_distance) / (range * 2.0)
#         return linear_val
#     else:
#         range = face_match_threshold
#         linear_val = 1.0 - (face_distance / (range * 2.0))
#         return linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))

# def change_res(stream, width, height):
#     stream.set(3, width)
#     stream.set(4, height)

def main(stream):
    # Get a reference to webcam #0 (the default one)
    # stream = cv2.VideoCapture(0)
    stream.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
    stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    # stream.set(3, 320)
    # stream.set(4, 240)
    stream.set(cv2.CAP_PROP_AUTOFOCUS, 0)

    font = cv2.FONT_HERSHEY_SIMPLEX
    # font = cv2.FONT_HERSHEY_DUPLEX

    # Map fps display FPS
    FpsCalc = FpsCalculator(buffer_len = 50)
    
    # Get date and time
    today = str(date_and_time.strftime("%Y-%m-%d %H:%M:%S"))

    # The training data would be all the face encodings from all the known images and the labels are their names
    known_face_encodings = []
    known_face_names = []
    #count = 0

    with open('face_recognition_hog.pkl', 'rb') as f:
        known_face_names = pickle.load(f)
        known_face_encodings = pickle.load(f)

    tolerance=0.6

    while True:
        # Grab a single frame of video
        ret, frame = stream.read()
        width = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))

        display_fps = round(FpsCalc.get(), 3)

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
            cv2.putText(frame, name, (int(left *1.5), int(top*0.5) + 27), font, 0.7, (255, 255, 255), 2)

            # cv2.rectangle(frame, (left, top + 35), (right, top), (0, 0, 255), cv2.FILLED)
            # cv2.rectangle(frame, (left, top - 35), (right, top), (0, 0, 255), cv2.FILLED)
            # cv2.putText(frame, name, (left + 6, top + 27), font, 0.7, (255, 255, 255), 2)
            # cv2.putText(frame, name, (left + 6, top - 6), font, 0.7, (255, 255, 255), 2)
            # cv2.putText(frame, acc, (left + 6, top + 27), font, 0.7, (255, 255, 255), 2)
            # Counting people frame
            # cv2.putText(frame, "Counting people:" + str(count), (5,15), font, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
        
        # puting the FPS count on the frame and display date and time
        cv2.rectangle(frame, (0, 0), (81, 25), (0, 0, 0), -1)
        # cv2.rectangle(frame, (0, 2), (81, 21), (0, 0, 0), -1)        
        cv2.rectangle(frame, (0, 35), (149, 18), (0, 0, 0), -1)

        print("FPS: " + str(display_fps))
        cv2.putText(frame, "FPS: " + str(display_fps), ((0), 15), font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, str(today), ((0), 30), font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        # Display the resulting image
        cv2.imshow('Face recognition Mode', frame)

        # Hit 'q' or `ESC` on the keyboard to quit!
        key = cv2.waitKey(1) & 0xFF
        # Pause the camera
        if key == 32:
            cv2.waitKey()
        # Stop the camera
        elif key == 27:
            break


    # Release handle to the webcam
    f.close()
    stream.release()
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    main(cv2.VideoCapture(0, cv2.CAP_V4L2))
