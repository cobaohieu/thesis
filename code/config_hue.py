import cv2



def process_frame_hue(frame):
    # some intensive computation...
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
    return frame

def hue():
    stream = cv2.VideoCapture(0)
    while True:

        (ret, frame) = stream.read()
        frame =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)

        cv2.imshow("Video record", frame)

        ch = cv2.waitKey(1)
        if ch == 27 or ch == ord('q') or ch == ord('Q'):
            break

    stream.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    hue()