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

# from CountsPerSec import CountsPerSec
# from VideoGet import VideoGet
# from VideoShow import VideoShow
from time import gmtime, strftime
from datetime import datetime
from math import radians, degrees, cos, sin, tan
from collections import OrderedDict, deque
from PIL import Image
from imutils.video import VideoStream

from collections import OrderedDict, deque
from threading import Thread


width = 640
class CountsPerSec:
    """
    Class that tracks the number of occurrences ("counts") of an
    arbitrary event and returns the frequency in occurrences
    (counts) per second. The caller must increment the count.
    """

    def __init__(self):
        self._start_time = None
        self._num_occurrences = 0

    def start(self):
        self._start_time = datetime.now()
        return self

    def increment(self):
        self._num_occurrences += 1

    def countsPerSec(self):
        elapsed_time = (datetime.now() - self._start_time).total_seconds()
        return self._num_occurrences / elapsed_time if elapsed_time > 0 else 0


class FpsCalculator:
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
        fps_rounded = round(fps, 2)

        return fps_rounded

class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(3, 1280)
        self.stream.set(4, 720)
        width = int(self.stream.get(cv2.CAP_PROP_FRAME_WIDTH))
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):    
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def stop(self):
        self.stopped = True

class VideoShow:
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self, frame=None):
        self.frame = frame
        self.stopped = False

    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):
        while not self.stopped:
            cv2.imshow("Face recognition Mode", self.frame)
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        self.stopped = True

def putIterationsPerSec(frame, iterations_per_sec):
    """
    Add iterations per second text to lower-left corner of a frame.
    """

    # cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec),
    #     (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
    return frame

def noThreading(source=0):
    """Grab and show video frames without multithreading."""

    stream = cv2.VideoCapture(source)
    font = cv2.FONT_HERSHEY_SIMPLEX
    FpsCalc = FpsCalculator(buffer_len = 60)
    cps = CountsPerSec().start()

    while True:
        display_fps = round(FpsCalc.get(), 0)
        grabbed, frame = stream.read()
        if not grabbed or cv2.waitKey(1) == ord("q"):
            break

        frame = putIterationsPerSec(frame, cps.countsPerSec())
        cv2.imshow("Face recognition Mode", frame)
        cps.increment()

def threadVideoGet(source=0):
    """
    Dedicated thread for grabbing video frames with VideoGet object.
    Main thread shows video frames.
    """

    video_getter = VideoGet(source).start()
    cps = CountsPerSec().start()

    while True:
        if (cv2.waitKey(1) == ord("q")) or video_getter.stopped:
            video_getter.stop()
            break

        frame = video_getter.frame
        frame = putIterationsPerSec(frame, cps.countsPerSec())

        # Display the resulting image
        cv2.imshow('Face recognition Mode', frame)
        cps.increment()

def threadVideoShow(source=0):
    """
    Dedicated thread for showing video frames with VideoShow object.
    Main thread grabs video frames.
    """

    stream = cv2.VideoCapture(source)
    stream.set(3, 1280)
    stream.set(4, 720)
    width = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))
    (grabbed, frame) = stream.read()
    video_shower = VideoShow(frame).start()
    cps = CountsPerSec().start()

    # font = cv2.FONT_HERSHEY_SIMPLEX
    # font = cv2.FONT_HERSHEY_DUPLEX

    # Map fps display FPS
    # FpsCalc = FpsCalculator(buffer_len = 50)
    
    # Get date and time
    # today = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    while True:
        # display_fps = round(FpsCalc.get(), 0)
        (grabbed, frame) = stream.read()
        if not grabbed or video_shower.stopped:
            video_shower.stop()
            break

        frame = putIterationsPerSec(frame, cps.countsPerSec())
        video_shower.frame = frame
        cps.increment()

def threadBoth(source=0):
    """
    Dedicated thread for grabbing video frames with VideoGet object.
    Dedicated thread for showing video frames with VideoShow object.
    Main thread serves only to pass frames between VideoGet and
    VideoShow objects/threads.
    """

    video_getter = VideoGet(source).start()
    video_shower = VideoShow(video_getter.frame).start()
    cps = CountsPerSec().start()

    font = cv2.FONT_HERSHEY_SIMPLEX
    # font = cv2.FONT_HERSHEY_DUPLEX

    # Map fps display FPS
    FpsCalc = FpsCalculator(buffer_len = 50)
    
    # Get date and time
    today = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # # The training data would be all the face encodings from all the known images and the labels are their names
    # known_face_encodings = []
    # known_face_names = []

    # with open('face_recognition_hog.pkl', 'rb') as f:
    #     known_face_names = pickle.load(f)
    #     known_face_encodings = pickle.load(f)

    # tolerance=0.6

    while True:
        display_fps = round(FpsCalc.get(), 0)

        if video_getter.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter.stop()
            break

        frame = video_getter.frame
        frame = putIterationsPerSec(frame, cps.countsPerSec())

        # # Resize frame of video to 1/4 size for faster face recognition processing
        # small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        # rgb_small_frame = small_frame[:, :, ::-1]

        # # Only process every other frame of video to save time
        # # if process_this_frame:
        # # Find all the faces and face encodings in the current frame of video
        # face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")

        # # Given an image, return the 128-dimension face encoding for each face in the image
        # face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        # face_names = []

        # for face_encoding in face_encodings:
        #     # See if the face is a match for the known face(s)
        #     matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        #     # matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.45)

        #     name = "Unknown"

        #     # Or instead, use the known face with the smallest distance to the new face
        #     face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        #     best_match_index = np.argmin(face_distances)

        #     if matches[best_match_index]:
        #         name = known_face_names[best_match_index]

        #     face_names.append(name)

        # # Display the results
        # for (top, right, bottom, left), name in zip(face_locations, face_names):
        #     # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        #     top *= 4
        #     right *= 4
        #     bottom *= 4
        #     left *= 4

        #     # Draw a box around the face
        #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        #     # Draw a label with a name below the face
        #     cv2.rectangle(frame, (left, top + 35), (right, top), (0, 0, 255), cv2.FILLED)
        #     cv2.putText(frame, name, (left + 6, top + 27), font, 0.7, (255, 255, 255), 2)

        cv2.rectangle(frame, (0, 2), (81, 21), (0, 0, 0), -1)        
        cv2.rectangle(frame, (0, 35), (149, 18), (0, 0, 0), -1)
        cv2.putText(frame, "FPS: " + str(display_fps), ((0), 15), font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, str(today), ((0), 30), font, 0.4, (0, 0, 0), 1, cv2.LINE_AA)
        video_shower.frame = frame
        cps.increment()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", "-s", default=0,
        help="Path to video file or integer representing webcam index"
            + " (default 0).")
    ap.add_argument("--thread", "-t", default="both",
        help="Threading mode: get (video read in its own thread),"
            + " show (video show in its own thread),"
            + " both (video read and video show in their own threads),"
            + " none (default--no multithreading)")
    args = vars(ap.parse_args())

    # If source is a string consisting only of integers, check that it doesn't
    # refer to a file. If it doesn't, assume it's an integer camera ID and
    # convert to int.
    if (
        isinstance(args["source"], str)
        and args["source"].isdigit()
        and not os.path.isfile(args["source"])
    ):
        args["source"] = int(args["source"])

    if args["thread"] == "both":
        threadBoth(args["source"])
    elif args["thread"] == "get":
        threadVideoGet(args["source"])
    elif args["thread"] == "show":
        threadVideoShow(args["source"])
    else:
        noThreading(args["source"])

if __name__ == "__main__":
    main()
    # threadBoth(0)