import cv2


def process_frame_mirror(frame):
    # some intensive computation...
    frame = cv2.flip(frame, 1)
    return frame

def mirror():
    stream = cv2.VideoCapture(0)
    while True:

        (ret, frame) = stream.read()
        # frame = cv2.flip(frame, 0)
        frame = cv2.flip(frame,1)
        # frame = cv2.flip(frame,-1)

        cv2.imshow("Video record", frame)

        ch = cv2.waitKey(1)
        if ch == 27 or ch == ord('q') or ch == ord('Q'):
            break
    stream.release()
    cv2.destroyAllWindows()

mirror()