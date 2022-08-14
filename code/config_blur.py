import cv2
import numpy as np


def process_frame_blur(frame):
    # some intensive computation...
    frame = cv2.GaussianBlur(frame, (11, 11), 0)
    return frame


def blur():
    stream = cv2.VideoCapture(0)

    if (stream.isOpened() == False):
        print('Error while trying to open camera. Plese check again...')

    # get the frame width and height
    frame_width = int(stream.get(3))
    frame_height = int(stream.get(4))

    # define codec and create VideoWriter object
    out = cv2.VideoWriter('out_videos/cam_blur.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))

    # read until end of video
    # while(stream.isOpened()):
    while True:
        # capture each frame of the video
        ret, frame = stream.read()
        if ret == True:
            # add gaussian blurring to frame
            frame = cv2.GaussianBlur(frame, (11, 11), 0)

            # save video frame
            out.write(frame)
            # display frame
            cv2.imshow('Video', frame)

            # press `q` to exit
            ch = cv2.waitKey(1)
            if ch == 27 or ch == ord('q') or ch == ord('Q'):
                break

    # release VideoCapture()
    stream.release()

    # close all frames and video windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    blur()