import cv2



def process_frame_rotate_x_axis(frame):
    # some intensive computation...
    frame = cv2.flip(frame, 0)
    return frame


def process_frame_y_axis(frame):
    # some intensive computation...
    frame = cv2.flip(frame, 1)
    return frame


def process_frame__both_axis(frame):
    # some intensive computation...
    frame = cv2.flip(frame, -1)
    return frame


def rotate_x_axis():
    stream = cv2.VideoCapture(0)
    while True:

        (ret, frame) = stream.read()
        frame = cv2.flip(frame, 0)

        cv2.imshow("Video record", frame)

        ch = cv2.waitKey(1)
        if ch == 27 or ch == ord('q') or ch == ord('Q'):
            break
    stream.release()
    cv2.destroyAllWindows()

def rotate_y_axis():
    stream = cv2.VideoCapture(0)
    while True:

        (ret, frame) = stream.read()
        frame = cv2.flip(frame, 1)

        cv2.imshow("Video record", frame)

        ch = cv2.waitKey(1)
        if ch == 27 or ch == ord('q') or ch == ord('Q'):
            break
    stream.release()
    cv2.destroyAllWindows()

def rotate_both_axis():
    stream = cv2.VideoCapture(0)
    while True:

        (ret, frame) = stream.read()
        frame = cv2.flip(frame, -1)

        cv2.imshow("Video record", frame)

        ch = cv2.waitKey(1)
        if ch == 27 or ch == ord('q') or ch == ord('Q'):
            break
    stream.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    rotate_both_axis()