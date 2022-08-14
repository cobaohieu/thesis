import cv2




def process_frame_mono(frame):
    # some intensive computation...
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return frame



def mono():
    stream = cv2.VideoCapture(0)
    while True:

        (ret, frame) = stream.read()
        frame =  cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow("Video record", frame)

        ch = cv2.waitKey(1)
        if ch == 27 or ch == ord('q') or ch == ord('Q'):
            break

    stream.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    mono()