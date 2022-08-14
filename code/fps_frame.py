# import the necessary packages
from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2

class CvFpsCalc(object):
    def __init__(self, buffer_len=1):
        self._start_tick = cv.getTickCount()
        self._freq = 1000.0 / cv.getTickFrequency()
        self._difftimes = deque(maxlen=buffer_len)

    def get(self):
        current_tick = cv.getTickCount()
        different_time = (current_tick - self._start_tick) * self._freq
        self._start_tick = current_tick

        self._difftimes.append(different_time)

        fps = 1000.0 / (sum(self._difftimes) / len(self._difftimes))
        fps_rounded = round(fps, 3)

        return fps_rounded

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=120,
        help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
        help="Whether or not frames should be displayed")
args = vars(ap.parse_args())

# grab a pointer to the video stream and initialize the FPS counter
print("[INFO] sampling frames from webcam...")
stream = cv2.VideoCapture(0)
# new_frame_time = time.time()
# fps will be number of frame processed in given time frame
# since their will be most of time error of 0.001 second
# we will be subtracting it to get more accurate result
# display_fps = 1/(new_frame_time-prev_frame_time)
# prev_frame_time = new_frame_time

fps = FPS().start()
# display_fps = fps.fps()
# cvFpsCalc = CvFpsCalc(buffer_len=50)
# loop over some frames
while fps._numFrames < args["num_frames"]:
    # display_fps = cvFpsCalc.get()
    # grab the frame from the stream and resize it to have a maximum
    # width of 400 pixels
    (grabbed, frame) = stream.read()
    frame = imutils.resize(frame, width=400)

    # check to see if the frame should be displayed to our screen
    if args["display"] > 0:
            cv2.putText(frame, "FPS:" + str(FPS()), (5, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

    # update the FPS counter
    fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
stream.release()
cv2.destroyAllWindows()

# created a *threaded* video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED frames from webcam...")
vs = WebcamVideoStream(src=0).start()
# new_frame_time = time.time()
# fps will be number of frame processed in given time frame
# since their will be most of time error of 0.001 second
# we will be subtracting it to get more accurate result
# display_fps = 1/(new_frame_time-prev_frame_time)
# prev_frame_time = new_frame_time
fps = FPS().start()
display_fps = fps.fps()
# cvFpsCalc = CvFpsCalc(buffer_len=50)

# loop over some frames...this time using the threaded stream
while fps._numFrames < args["num_frames"]:
    # display_fps = cvFpsCalc.get()
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    # check to see if the frame should be displayed to our screen
    if args["display"] > 0:
            cv2.imshow("Frame", frame)
            cv2.putText(frame, "FPS:" + str(FPS()), (5, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

    # update the FPS counter
    fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()